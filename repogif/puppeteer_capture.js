#!/usr/bin/env node

/**
 * RepoGif - Puppeteer script for capturing GitHub repository header animation
 * 
 * This script captures a series of screenshots from the animation of a GitHub
 * repository header, including cursor movement and star button interaction.
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

// Parse command line arguments
const argv = yargs(hideBin(process.argv))
  .option('repo', {
    alias: 'r',
    description: 'Repository name',
    type: 'string',
    default: 'RepoGif'
  })
  .option('stars', {
    alias: 's',
    description: 'Star count',
    type: 'string',
    default: '5.8k'
  })
  .option('forks', {
    alias: 'f',
    description: 'Fork count',
    type: 'string',
    default: '397'
  })
  .option('output', {
    alias: 'o',
    description: 'Output directory for screenshots',
    type: 'string',
    default: './output'
  })
  .option('frames', {
    description: 'Number of frames to capture',
    type: 'number',
    default: 46  // Truncate at frame_045 (46 frames total including frame_000)
  })
  .option('interval', {
    alias: 'i',
    description: 'Interval between frames (ms)',
    type: 'number',
    default: 60
  })
  .option('show-forks', {
    description: 'Whether to display the fork section',
    type: 'boolean',
    default: true
  })
  .help()
  .alias('help', 'h')
  .argv;

// Ensure output directory exists
const ensureDirectoryExists = (dirPath) => {
  if (!fs.existsSync(dirPath)) {
    try {
      fs.mkdirSync(dirPath, { recursive: true });
      console.log(`Created directory: ${dirPath}`);
    } catch (err) {
      console.error(`Error creating directory ${dirPath}:`, err);
      process.exit(1);
    }
  }
};

// Function to pad number with leading zeros
const padNumber = (num, size) => {
  let s = num + "";
  while (s.length < size) s = "0" + s;
  return s;
};

// Main function to capture screenshots
async function captureAnimation() {
  // Ensure output directory exists
  ensureDirectoryExists(argv.output);

  console.log('Starting browser...');
  const browser = await puppeteer.launch({
    headless: "new", // Use the new headless mode
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    
    // Set viewport size
    await page.setViewport({
      width: 1100,
      height: 140,
      deviceScaleFactor: 1,
    });

    // Get the absolute path to the HTML file
    const htmlPath = path.resolve(`${__dirname}/web_template/index.html`);
    const htmlUrl = `file://${htmlPath}`;
    
    console.log(`Opening file: ${htmlUrl}`);
    await page.goto(htmlUrl, { waitUntil: 'networkidle0' });
    
    // Customize the repository display based on CLI arguments
    await page.evaluate((repoName, stars, forks, showForks) => {
      // Update repository name
      document.querySelector('.repo-name').textContent = repoName;
      
      // Update star count
      document.querySelector('#star-button .count').textContent = stars;
      
      // Update fork count
      document.querySelector('.fork-button .count').textContent = forks;
      
      // Show/hide fork section based on showForks parameter
      if (!showForks) {
        document.querySelector('.fork-button').style.display = 'none';
      }
      
      // Set initial animation state to unstarred
      const starButton = document.getElementById('star-button');
      starButton.classList.remove('starred');
      starButton.querySelector('.star-label').textContent = 'Star';
      
    }, argv.repo, argv.stars, argv.forks, argv['show-forks']);

    // Wait for animation elements to be ready
    await page.waitForSelector('#cursor', { visible: false });
    
    // Pause animation auto-start and ensure unstarred state
    await page.evaluate(() => {
      // Prevent animation from auto-starting by overriding the initialDelay
      // We'll start it manually after capture setup is complete
      window.originalStartAnimation = window.startAnimation;
      window.startAnimation = () => {
        console.log('Animation start prevented - will start manually');
      };
      
      // Ensure star button is in unstarred state
      const starButton = document.getElementById('star-button');
      starButton.classList.remove('starred');
      starButton.querySelector('.star-label').textContent = 'Star';
    });
    
    // Add a small delay to ensure the page is fully rendered
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Capture pre-animation screenshot
    await page.screenshot({
      path: path.join(argv.output, `frame_000.png`),
      fullPage: false
    });
    console.log('Captured initial state');
    
    // Now manually start the animation with controlled timing
    await page.evaluate(() => {
      // Restore the original startAnimation function
      if (window.originalStartAnimation) {
        window.startAnimation = window.originalStartAnimation;
      }
      
      // Start with minimal delay
      const animationSettings = document.animationSettings || {};
      animationSettings.initialDelay = 100; // Override the 55000ms delay
      
      // Start the animation
      startAnimation();
    });

    // Phase 1: Capture cursor moving to star button
    console.log('Capturing cursor movement...');
    // Allocate 60% of frames for cursor movement to star button for smoother motion
    const movementFrames = Math.floor(argv.frames * 0.6);
    for (let i = 1; i <= movementFrames; i++) {
      // Using setTimeout wrapped in a promise instead of waitForTimeout
      await new Promise(resolve => setTimeout(resolve, argv.interval));
      await page.screenshot({
        path: path.join(argv.output, `frame_${padNumber(i, 3)}.png`),
        fullPage: false
      });
    }

    // Phase 2: Wait for cursor to reach star button
    await page.waitForFunction(() => {
      const cursor = document.getElementById('cursor');
      const starButton = document.getElementById('star-button');
      const cursorRect = cursor.getBoundingClientRect();
      const buttonRect = starButton.getBoundingClientRect();
      
      // Check if cursor is near the star button
      return Math.abs(cursorRect.left + cursorRect.width/2 - (buttonRect.left + buttonRect.width/2)) < 10 &&
             Math.abs(cursorRect.top + cursorRect.height/2 - (buttonRect.top + buttonRect.height/2)) < 10;
    }, { timeout: 8000 }).catch(() => {
      console.log('Timeout waiting for cursor to reach button - continuing anyway');
    });
    
    // Capture hover state
    await page.screenshot({
      path: path.join(argv.output, `frame_${padNumber(movementFrames + 1, 3)}.png`),
      fullPage: false
    });
    console.log('Captured hover state');
    
    // Add pre-click anticipation (slight pause before clicking)
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Capture pre-click state
    await page.screenshot({
      path: path.join(argv.output, `frame_${padNumber(movementFrames + 2, 3)}.png`),
      fullPage: false
    });
    
    // Verify the button is initially in the unstarred state before clicking
    const initialStarState = await page.evaluate(() => {
      const starButton = document.getElementById('star-button');
      return {
        hasStarredClass: starButton.classList.contains('starred'),
        labelText: starButton.querySelector('.star-label').textContent
      };
    });
    console.log(`Initial star button state: ${JSON.stringify(initialStarState)}`);
    
    // Wait for click animation
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Trigger the click event explicitly to ensure it happens
    await page.evaluate(() => {
      const starButton = document.getElementById('star-button');
      const cursor = document.getElementById('cursor');
      
      // Trigger click event programmatically
      const clickEvent = new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window
      });
      starButton.dispatchEvent(clickEvent);
      
      // Implement simulateClick functionality directly
      // (Based on the simulateClick function from animation.js)
      cursor.classList.add('clicking');
      starButton.classList.add('starred');
      starButton.querySelector('.star-label').textContent = 'Starred';
      
      // Remove clicking class after animation
      setTimeout(() => {
        cursor.classList.remove('clicking');
      }, 200);
    });
    
    // Capture the click moment
    await page.screenshot({
      path: path.join(argv.output, `frame_${padNumber(movementFrames + 3, 3)}.png`),
      fullPage: false
    });
    console.log('Captured click moment');
    
    // Capture click transition frames (4 frames for smoother click animation)
    for (let i = 1; i <= 4; i++) {
      await new Promise(resolve => setTimeout(resolve, 80));
      await page.screenshot({
        path: path.join(argv.output, `frame_${padNumber(movementFrames + 3 + i, 3)}.png`),
        fullPage: false
      });
    }
    
    // Wait a moment for star button transition to complete
    await new Promise(resolve => setTimeout(resolve, 120));
    
    // Capture after click (starred state)
    await page.screenshot({
      path: path.join(argv.output, `frame_${padNumber(movementFrames + 8, 3)}.png`),
      fullPage: false
    });
    console.log('Captured starred state');
    
    // Verify the button is in the starred state
    const isStarred = await page.evaluate(() => {
      const starButton = document.getElementById('star-button');
      return {
        hasStarredClass: starButton.classList.contains('starred'),
        labelText: starButton.querySelector('.star-label').textContent
      };
    });
    
    console.log(`Star button state: ${JSON.stringify(isStarred)}`);
    if (!isStarred.hasStarredClass || isStarred.labelText !== 'Starred') {
      console.warn('Warning: Star button may not be in the correct starred state!');
    }
    
    // Phase 3: Capture cursor moving away
    console.log('Capturing cursor exit...');
    // Calculate remaining frames for exit animation
    const interactionFrames = 9; // hover + pre-click + click + 4 transition frames + after-click
    const exitFrames = Math.max(1, argv.frames - movementFrames - interactionFrames);
    
    console.log(`Total frames: ${argv.frames}, Movement frames: ${movementFrames}, Interaction frames: ${interactionFrames}, Exit frames: ${exitFrames}`);
    
    // Brief pause before cursor starts moving away
    await new Promise(resolve => setTimeout(resolve, 150));
    
    // Ensure we don't exceed frame_045 by checking total frame count before each capture
    for (let i = 1; i <= exitFrames && (movementFrames + interactionFrames + i) <= 45; i++) {
      await new Promise(resolve => setTimeout(resolve, argv.interval));
      await page.screenshot({
        path: path.join(argv.output, `frame_${padNumber(movementFrames + interactionFrames + i, 3)}.png`),
        fullPage: false
      });
    }
    
    // Calculate actual total frames captured
    const totalFramesCaptured = Math.min(movementFrames + interactionFrames + exitFrames, 46) + 1;
    
    console.log('Animation capture complete!');
    console.log(`Saved ${totalFramesCaptured} frames to ${argv.output} (frame_000 to frame_${padNumber(totalFramesCaptured - 1, 3)})`);
    
  } catch (error) {
    console.error('Error during animation capture:', error);
  } finally {
    await browser.close();
  }
}

// Run the capture function
captureAnimation().catch(console.error);