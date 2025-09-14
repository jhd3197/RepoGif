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
    default: 20
  })
  .option('interval', {
    alias: 'i',
    description: 'Interval between frames (ms)',
    type: 'number',
    default: 100
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
      width: 1200,
      height: 450,
      deviceScaleFactor: 1,
    });

    // Get the absolute path to the HTML file
    const htmlPath = path.resolve(`${__dirname}/web_template/index.html`);
    const htmlUrl = `file://${htmlPath}`;
    
    console.log(`Opening file: ${htmlUrl}`);
    await page.goto(htmlUrl, { waitUntil: 'networkidle0' });
    
    // Customize the repository display based on CLI arguments
    await page.evaluate((repoName, stars, forks) => {
      // Update repository name
      document.querySelector('.repo-name').textContent = repoName;
      
      // Update star count
      document.querySelector('#star-button .count').textContent = stars;
      
      // Update fork count
      document.querySelector('.fork-button .count').textContent = forks;
      
      // Reset animation state
      const starButton = document.getElementById('star-button');
      starButton.classList.add('starred');
      starButton.querySelector('.star-label').textContent = 'Starred';
      
    }, argv.repo, argv.stars, argv.forks);

    // Wait for animation to be ready
    await page.waitForSelector('#cursor', { visible: true });
    
    // Capture pre-animation screenshot
    await page.screenshot({
      path: path.join(argv.output, `frame_000_initial.png`),
      fullPage: false
    });
    console.log('Captured initial state');

    // Phase 1: Capture cursor moving to star button
    console.log('Capturing cursor movement...');
    for (let i = 1; i <= Math.floor(argv.frames / 2); i++) {
      // Using setTimeout wrapped in a promise instead of waitForTimeout
      await new Promise(resolve => setTimeout(resolve, argv.interval));
      await page.screenshot({
        path: path.join(argv.output, `frame_${padNumber(i, 3)}_moving.png`),
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
    }, { timeout: 5000 }).catch(() => {
      console.log('Timeout waiting for cursor to reach button - continuing anyway');
    });
    
    // Capture hover state
    await page.screenshot({
      path: path.join(argv.output, `frame_${padNumber(Math.floor(argv.frames / 2) + 1, 3)}_hover.png`),
      fullPage: false
    });
    console.log('Captured hover state');
    
    // Wait for click animation
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Capture the click moment
    await page.screenshot({
      path: path.join(argv.output, `frame_${padNumber(Math.floor(argv.frames / 2) + 2, 3)}_click.png`),
      fullPage: false
    });
    console.log('Captured click moment');
    
    // Wait for post-click state
    await new Promise(resolve => setTimeout(resolve, 200));
    
    // Capture after click (unstarred state)
    await page.screenshot({
      path: path.join(argv.output, `frame_${padNumber(Math.floor(argv.frames / 2) + 3, 3)}_after_click.png`),
      fullPage: false
    });
    console.log('Captured after-click state');
    
    // Phase 3: Capture cursor moving away
    console.log('Capturing cursor exit...');
    const remainingFrames = argv.frames - Math.floor(argv.frames / 2) - 3;
    for (let i = 1; i <= remainingFrames; i++) {
      await new Promise(resolve => setTimeout(resolve, argv.interval));
      await page.screenshot({
        path: path.join(argv.output, `frame_${padNumber(Math.floor(argv.frames / 2) + 3 + i, 3)}_exit.png`),
        fullPage: false
      });
    }
    
    console.log('Animation capture complete!');
    console.log(`Saved ${argv.frames + 1} frames to ${argv.output}`);
    
  } catch (error) {
    console.error('Error during animation capture:', error);
  } finally {
    await browser.close();
  }
}

// Run the capture function
captureAnimation().catch(console.error);