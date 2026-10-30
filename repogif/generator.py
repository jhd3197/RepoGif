"""
RepoGif - Generator for GitHub repository header GIFs.

This module provides the main functionality for generating GitHub repository
header GIFs using customizable templates.
"""

import base64
import mimetypes
import os
import re
import shutil
import tempfile
from urllib.parse import quote, urlencode

import numpy as np
from PIL import Image


_ACCENT_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
_GIF_BYTE_LIMIT = 15 * 1024 * 1024
_TEMPLATE10_FRAMES = 30
_TEMPLATE10_FPS = 20
_TEMPLATE10_SCALE = 2


def _normalize_accent(accent):
    """Return a 6-digit hex color, or None when no accent was requested."""
    if accent is None or str(accent).strip() == "":
        return None
    value = str(accent).strip()
    if not _ACCENT_RE.match(value):
        raise ValueError("accent must be a hex color like #f5c451")
    if len(value) == 4:
        value = "#" + "".join(ch * 2 for ch in value[1:])
    return value.lower()


def _normalize_topics(topics):
    """Return a comma-separated topic list, or None when there are no topics."""
    if topics is None:
        return None
    if isinstance(topics, str):
        items = [part.strip() for part in topics.split(",")]
    else:
        items = [str(part).strip() for part in topics]
    items = [item for item in items if item]
    if not items:
        return None
    return ",".join(items)


def _resolve_frames(template_name, frames):
    if frames is None:
        return _TEMPLATE10_FRAMES if template_name == "template10" else 2
    count = int(frames)
    if count < 1:
        raise ValueError("frames must be at least 1")
    return count


def _resolve_scale(template_name, scale):
    if scale is None:
        return _TEMPLATE10_SCALE if template_name == "template10" else 1
    value = int(scale)
    if value < 1:
        raise ValueError("scale must be at least 1")
    return value


def _frame_duration_ms(frame_count, fps):
    """Legacy two-frame GIFs keep a 1 second hold. Longer clips use fps."""
    if frame_count <= 2:
        return 1000
    rate = float(fps)
    if rate <= 0:
        raise ValueError("fps must be positive")
    return max(20, int(round(1000.0 / rate)))


def _mp4_target(out, mp4):
    if mp4 is None or mp4 is False:
        return None
    if mp4 is True:
        root, _ext = os.path.splitext(out)
        return root + ".mp4"
    return str(mp4)


def _hero_source(hero):
    """Return an http(s), data, or local-file data URL for the hero image."""
    if hero is None or str(hero).strip() == "":
        return None
    value = str(hero)
    if value.startswith(("http://", "https://", "data:")):
        return value
    path = os.path.abspath(value)
    if not os.path.isfile(path):
        raise ValueError(f"Hero image not found: {hero}")
    mime, _encoding = mimetypes.guess_type(path)
    if not mime:
        mime = "image/png"
    with open(path, "rb") as handle:
        encoded = base64.b64encode(handle.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _query(params):
    clean = {}
    for key, value in params.items():
        if value is None or value == "":
            continue
        clean[key] = value
    return urlencode(clean, quote_via=quote)


def _pad_even(image):
    """H.264 yuv420 needs even dimensions. Duplicate the last row or column."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    pad_w = width % 2
    pad_h = height % 2
    if not pad_w and not pad_h:
        return rgb
    padded = Image.new("RGB", (width + pad_w, height + pad_h))
    padded.paste(rgb, (0, 0))
    if pad_w:
        column = rgb.crop((width - 1, 0, width, height))
        padded.paste(column, (width, 0))
    if pad_h:
        row = padded.crop((0, height - 1, width + pad_w, height))
        padded.paste(row, (0, height))
    return padded


def _palette_from_frames(frames, colors):
    thumbs = []
    indexes = sorted({0, len(frames) // 2, len(frames) - 1})
    for index in indexes:
        thumb = frames[index].copy()
        thumb.thumbnail((420, 236))
        thumbs.append(thumb.convert("RGB"))
    mosaic = Image.new("RGB", (sum(thumb.width for thumb in thumbs), max(thumb.height for thumb in thumbs)))
    offset = 0
    for thumb in thumbs:
        mosaic.paste(thumb, (offset, 0))
        offset += thumb.width
    return mosaic.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)


def _palettize_frames(frames, colors):
    """
    Dither the first frame so photos stay rich, then reuse those pixels
    wherever later frames are unchanged. Animated regions take the nearest
    palette color, which keeps the GIF delta small.
    """
    palette_image = _palette_from_frames(frames, colors)
    base_rgb = np.asarray(frames[0].convert("RGB"))
    base_paletted = frames[0].convert("RGB").quantize(
        palette=palette_image,
        dither=Image.Dither.FLOYDSTEINBERG,
    )
    base_indexes = np.array(base_paletted)
    palette = base_paletted.getpalette()
    paletted = []
    for frame in frames:
        rgb = np.asarray(frame.convert("RGB"))
        nearest = np.array(
            frame.convert("RGB").quantize(palette=palette_image, dither=Image.Dither.NONE)
        )
        changed = np.any(rgb != base_rgb, axis=2)
        merged = base_indexes.copy()
        merged[changed] = nearest[changed]
        image = Image.fromarray(merged, mode="P")
        image.putpalette(palette)
        paletted.append(image)
    return paletted


def _write_gif(frames, path, duration_ms, colors, dither_first):
    if dither_first:
        paletted = _palettize_frames(frames, colors)
    else:
        palette_image = _palette_from_frames(frames, colors)
        paletted = [
            frame.convert("RGB").quantize(palette=palette_image, dither=Image.Dither.NONE)
            for frame in frames
        ]
    paletted[0].save(
        path,
        format="GIF",
        save_all=True,
        append_images=paletted[1:],
        duration=duration_ms,
        loop=0,
        optimize=True,
        disposal=1,
    )


def _save_animated_gif(frames, path, duration_ms):
    """Write a looping GIF, simplifying the palette if the file exceeds 15MB."""
    attempts = (
        (256, True),
        (128, False),
        (64, False),
    )
    last_error = None
    for colors, dither_first in attempts:
        try:
            _write_gif(frames, path, duration_ms, colors, dither_first)
        except Exception as exc:
            last_error = exc
            continue
        size = os.path.getsize(path)
        print(f"GIF size {size / (1024 * 1024):.2f}MB at {colors} colors")
        if size <= _GIF_BYTE_LIMIT:
            return size
    if last_error and not os.path.exists(path):
        raise RuntimeError(f"Failed to write GIF: {last_error}")
    size = os.path.getsize(path)
    raise RuntimeError(
        f"GIF is {size / (1024 * 1024):.1f}MB, above the 15MB limit"
    )


def _save_mp4(frames, path, fps):
    try:
        import imageio.v2 as imageio
    except ImportError as exc:
        raise RuntimeError(
            "MP4 output requires imageio and imageio-ffmpeg.\n"
            "pip install imageio imageio-ffmpeg"
        ) from exc

    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent)
    even_frames = [_pad_even(frame) for frame in frames]
    writer = imageio.get_writer(
        path,
        fps=fps,
        codec="libx264",
        quality=8,
        pixelformat="yuv420p",
        macro_block_size=1,
        output_params=["-movflags", "+faststart"],
    )
    try:
        for frame in even_frames:
            writer.append_data(np.asarray(frame))
    finally:
        writer.close()


def _use_legacy_capture(template_name, frames, scale, mp4, description, language,
                        topics, accent, hero, owner, hero_focus):
    """Templates 1-9 keep the original two-frame capture unless new options are set."""
    if template_name == "template10":
        return False
    if frames is not None or scale is not None or mp4:
        return False
    if any((description, language, topics, accent, hero, owner, hero_focus)):
        return False
    return True


class RepoGifGenerator:
    """
    Template-based GitHub repository header GIF generator.
    This class provides a framework for generating repository header GIFs
    using various templates.
    """

    def __init__(self):
        """Initialize the generator with available templates."""
        self.templates = {
            "template1": "repogif.templates.template1",
            "template2": "repogif.templates.template2",
            "template3": "repogif.templates.template3",
            "template4": "repogif.templates.template4",
            "template5": "repogif.templates.template5",
            "template6": "repogif.templates.template6",
            "template7": "repogif.templates.template7",
            "template8": "repogif.templates.template8",
            "template9": "repogif.templates.template9",
            "template10": "repogif.templates.template10"
        }
        self.default_template = "template1"

    def get_available_templates(self):
        """Returns a list of available template names."""
        return list(self.templates.keys())

    def generate_gif(self,
                     repo_name="repogif",
                     stars=123,
                     forks=45,
                     out="repo.gif",
                     debug_dir=None,
                     show_forks=True,
                     template=None,
                     width=580,
                     height=140,
                     contributors=None,
                     commits=None,
                     description=None,
                     language=None,
                     topics=None,
                     accent=None,
                     hero=None,
                     hero_focus=None,
                     owner=None,
                     frames=None,
                     fps=_TEMPLATE10_FPS,
                     scale=None,
                     mp4=None):
        """
        Generate a GitHub repository header GIF using the specified template.

        Args:
            repo_name (str): Name of the repository
            stars (int/str): Number of stars to display
            forks (int/str): Number of forks to display
            out (str): Output path for the GIF
            debug_dir (str/bool, optional): Directory to save frame images for debugging purposes.
                                         If None or False, frames are not saved.
                                         If True, frames are saved to a default directory in the package.
                                         If a string path, frames are saved to that directory.
            show_forks (bool, optional): Whether to display the fork section in the repository header.
            template (str, optional): The template to use for generating the GIF.
                                    If None, the default template will be used.
            width (int, optional): Width of the GIF in pixels. Default is 580.
            height (int, optional): Height of the GIF in pixels. Default is 140.
            contributors (str, optional): JSON-encoded string of contributors data for template9.
                                       Each contributor should have 'date', 'login', and 'avatar_url'.
            commits (str, optional): Comma-separated string of weekly commit counts for template8.
                                  Example: "10,25,15,30,20,35,40"
            description (str, optional): Repository description. Used by template10.
            language (str, optional): Primary language badge. Used by template10.
            topics (str/list, optional): Topic badges, as a list or comma-separated string.
            accent (str, optional): Hex accent color, for example #f5c451.
            hero (str, optional): Screenshot or marketing image, as a file path or URL.
            hero_focus (str, optional): CSS object-position for the hero image.
            owner (str, optional): Repository owner shown in the kicker.
            frames (int, optional): Number of animation frames. Template10 defaults to 30.
            fps (int, optional): Frames per second for multi-frame GIF and MP4 output.
            scale (int, optional): Supersampling factor. Template10 renders at 2x, then
                                downscales to width and height for crisp text.
            mp4 (str/bool, optional): Also write an H.264 MP4. True uses the GIF path
                                   with an .mp4 extension.

        Returns:
            None: The GIF is saved to the specified path

        Raises:
            ValueError: If the specified template is not available
            RuntimeError: If required dependencies are not available
        """
        template_name = template or self.default_template

        if template_name not in self.templates:
            available = ", ".join(self.get_available_templates())
            raise ValueError(f"Template '{template_name}' not found. Available templates: {available}")

        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise RuntimeError(
                "Required dependencies not found. Please install with:\n"
                "pip install playwright pillow\n"
                "Then run: playwright install"
            )

        width = int(width)
        height = int(height)
        if width < 1 or height < 1:
            raise ValueError("width and height must be positive")

        accent = _normalize_accent(accent)
        topics = _normalize_topics(topics)
        mp4_path = _mp4_target(out, mp4)
        legacy = _use_legacy_capture(
            template_name, frames, scale, mp4, description, language,
            topics, accent, hero, owner, hero_focus,
        )

        template_dir = os.path.join(os.path.dirname(__file__), "templates", template_name)
        template_path = os.path.join(template_dir, "template.html")
        template_url = f"file://{os.path.abspath(template_path)}"

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                if legacy:
                    self._capture_legacy(
                        sync_playwright, template_url, temp_dir, out, debug_dir,
                        repo_name, stars, forks, show_forks, width, height,
                        contributors, commits, template_name,
                    )
                    return

                frame_count = _resolve_frames(template_name, frames)
                device_scale = _resolve_scale(template_name, scale)
                duration_ms = _frame_duration_ms(frame_count, fps)
                hero_src = _hero_source(hero)
                images = self._capture_frames(
                    sync_playwright, template_url, temp_dir,
                    repo_name, stars, forks, show_forks, width, height,
                    contributors, commits, template_name,
                    description, language, topics, accent, hero_src, hero_focus, owner,
                    frame_count, device_scale,
                )
                print("Creating GIF from screenshots...")
                if frame_count <= 2 and device_scale == 1 and not mp4_path:
                    images[0].save(
                        out,
                        format="GIF",
                        append_images=images[1:],
                        save_all=True,
                        duration=duration_ms,
                        loop=0,
                    )
                    print(f"✅ Saved {out}")
                else:
                    _save_animated_gif(images, out, duration_ms)
                    print(f"✅ Saved {out}")

                if mp4_path:
                    print("Creating MP4...")
                    video_fps = 1000.0 / duration_ms
                    _save_mp4(images, mp4_path, video_fps)
                    print(f"✅ Saved {mp4_path}")

                self._write_debug_frames(debug_dir, images)
            except Exception as e:
                raise RuntimeError(f"Error generating GIF: {e}")

    def _capture_legacy(self, sync_playwright, template_url, temp_dir, out, debug_dir,
                        repo_name, stars, forks, show_forks, width, height,
                        contributors, commits, template_name):
        unstarred_path = os.path.join(temp_dir, "unstarred.png")
        starred_path = os.path.join(temp_dir, "starred.png")

        print("Capturing screenshots with Playwright...")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": width, "height": height})

            print("Capturing unstarred state...")
            params = {
                "repo_name": repo_name,
                "stars": stars,
                "forks": forks,
                "starred": "false",
                "show_forks": "true" if show_forks else "false",
                "width": width,
                "height": height
            }

            if commits and template_name == "template8":
                params["commits"] = commits

            if contributors and template_name == "template9":
                params["contributors"] = contributors
                params["animation_state"] = "initial"
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            page.goto(f"{template_url}?{query_string}")
            page.screenshot(path=unstarred_path)

            print("Capturing starred state...")
            params["starred"] = "true"

            if contributors and template_name == "template9":
                params["animation_state"] = "animated"

            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            page.goto(f"{template_url}?{query_string}")
            page.screenshot(path=starred_path)

            browser.close()

        print("Creating GIF from screenshots...")
        frames = [Image.open(unstarred_path), Image.open(starred_path)]
        frames[0].save(
            out,
            format='GIF',
            append_images=[frames[1]],
            save_all=True,
            duration=1000,
            loop=0
        )
        print(f"✅ Saved {out}")

        if debug_dir is not None and debug_dir is not False:
            if debug_dir is True:
                debug_dir = os.path.join(os.path.dirname(__file__), "debug_frames")
                print(f"Debug mode: using default debug directory: {debug_dir}")
            else:
                print(f"Debug mode: copying frames to {debug_dir}")

            try:
                if not os.path.exists(debug_dir):
                    os.makedirs(debug_dir)
                    print(f"Created debug directory: {debug_dir}")

                frame_files = [unstarred_path, starred_path]
                frame_names = ["unstarred.png", "starred.png"]

                for i, frame_file in enumerate(frame_files):
                    dest_path = os.path.join(debug_dir, frame_names[i])
                    shutil.copy2(frame_file, dest_path)

                print(f"✅ Copied frames to {debug_dir}")
            except PermissionError:
                print(f"⚠️ Warning: Permission denied when copying frames to {debug_dir}")
            except OSError as e:
                print(f"⚠️ Warning: Failed to copy frames to debug directory: {e}")

    def _capture_frames(self, sync_playwright, template_url, temp_dir,
                        repo_name, stars, forks, show_forks, width, height,
                        contributors, commits, template_name,
                        description, language, topics, accent, hero_src, hero_focus, owner,
                        frame_count, device_scale):
        images = []
        print(f"Capturing {frame_count} frames at {width}x{height} @{device_scale}x...")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=device_scale,
            )
            page = context.new_page()
            for index in range(frame_count):
                progress = 1.0 if frame_count == 1 else index / (frame_count - 1)
                params = {
                    "repo_name": repo_name,
                    "stars": stars,
                    "forks": forks,
                    "starred": "true" if progress >= 1 else "false",
                    "show_forks": "true" if show_forks else "false",
                    "width": width,
                    "height": height,
                    "progress": f"{progress:.6f}",
                }
                if description:
                    params["description"] = description
                if language:
                    params["language"] = language
                if topics:
                    params["topics"] = topics
                if accent:
                    params["accent"] = accent
                if hero_focus:
                    params["hero_focus"] = hero_focus
                if owner:
                    params["owner"] = owner
                if commits and template_name == "template8":
                    params["commits"] = commits
                if contributors and template_name == "template9":
                    params["contributors"] = contributors
                    params["animation_state"] = "animated" if progress >= 1 else "initial"

                page.goto(f"{template_url}?{_query(params)}")
                if hero_src:
                    page.evaluate(
                        """(src) => { if (window.setHero) window.setHero(src); }""",
                        hero_src,
                    )
                    page.wait_for_function(
                        """() => {
                            const img = document.querySelector('.hero-image');
                            if (!img) return true;
                            return img.complete && img.naturalWidth > 0;
                        }""",
                        timeout=15000,
                    )
                shot_path = os.path.join(temp_dir, f"frame_{index:03d}.png")
                page.screenshot(path=shot_path)
                image = Image.open(shot_path).convert("RGB")
                if image.size != (width, height):
                    image = image.resize((width, height), Image.Resampling.LANCZOS)
                images.append(image)
                print(f"  frame {index + 1}/{frame_count}")
            browser.close()
        return images

    def _write_debug_frames(self, debug_dir, images):
        if debug_dir is None or debug_dir is False:
            return
        if debug_dir is True:
            debug_dir = os.path.join(os.path.dirname(__file__), "debug_frames")
            print(f"Debug mode: using default debug directory: {debug_dir}")
        else:
            print(f"Debug mode: copying frames to {debug_dir}")
        try:
            if not os.path.exists(debug_dir):
                os.makedirs(debug_dir)
            for index, image in enumerate(images):
                image.save(os.path.join(debug_dir, f"frame_{index:03d}.png"))
            images[0].save(os.path.join(debug_dir, "unstarred.png"))
            images[-1].save(os.path.join(debug_dir, "starred.png"))
            print(f"✅ Copied frames to {debug_dir}")
        except PermissionError:
            print(f"⚠️ Warning: Permission denied when copying frames to {debug_dir}")
        except OSError as exc:
            print(f"⚠️ Warning: Failed to copy frames to debug directory: {exc}")


# Create a singleton instance of the generator
_generator = RepoGifGenerator()


def generate_repo_gif(repo_name="repogif", stars=123, forks=45, out="repo.gif",
                     debug_dir=None, show_forks=True, template=None,
                     width=580, height=140, contributors=None, commits=None,
                     description=None, language=None, topics=None, accent=None,
                     hero=None, hero_focus=None, owner=None, frames=None,
                     fps=_TEMPLATE10_FPS, scale=None, mp4=None):
    """
    Generate a GitHub repository header GIF using the specified template.

    Args:
        repo_name (str): Name of the repository
        stars (int/str): Number of stars to display
        forks (int/str): Number of forks to display
        out (str): Output path for the GIF
        debug_dir (str/bool, optional): Directory to save frame images for debugging purposes.
        show_forks (bool, optional): Whether to display the fork section in the repository header.
        template (str, optional): The template to use for generating the GIF.
                                If None, the default template will be used.
        width (int, optional): Width of the GIF in pixels. Default is 580.
        height (int, optional): Height of the GIF in pixels. Default is 140.
        contributors (str, optional): JSON-encoded string of contributors data for template9.
                                   Each contributor should have 'date', 'login', and 'avatar_url'.
        commits (str, optional): Comma-separated string of weekly commit counts for template8.
                              Example: "10,25,15,30,20,35,40"
        description (str, optional): Repository description. Used by template10.
        language (str, optional): Primary language badge. Used by template10.
        topics (str/list, optional): Topic badges, as a list or comma-separated string.
        accent (str, optional): Hex accent color, for example #f5c451.
        hero (str, optional): Screenshot or marketing image, as a file path or URL.
        hero_focus (str, optional): CSS object-position for the hero image.
        owner (str, optional): Repository owner shown in the kicker.
        frames (int, optional): Number of animation frames. Template10 defaults to 30.
        fps (int, optional): Frames per second for multi-frame GIF and MP4 output.
        scale (int, optional): Supersampling factor. Template10 renders at 2x.
        mp4 (str/bool, optional): Also write an H.264 MP4.

    Returns:
        None: The GIF is saved to the specified path
    """
    return _generator.generate_gif(
        repo_name=repo_name,
        stars=stars,
        forks=forks,
        out=out,
        debug_dir=debug_dir,
        show_forks=show_forks,
        template=template,
        width=width,
        height=height,
        contributors=contributors,
        commits=commits,
        description=description,
        language=language,
        topics=topics,
        accent=accent,
        hero=hero,
        hero_focus=hero_focus,
        owner=owner,
        frames=frames,
        fps=fps,
        scale=scale,
        mp4=mp4,
    )


def get_available_templates():
    """Returns a list of available template names."""
    return _generator.get_available_templates()


# Define the public API
__all__ = ['generate_repo_gif', 'get_available_templates']
