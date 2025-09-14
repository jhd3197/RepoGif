// GitHub Repository Header Animation Script

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const cursor = document.getElementById('cursor');
    const starButton = document.getElementById('star-button');
    const forkButton = document.querySelector('.fork-button');
    
    // Check if fork button is visible (controlled by show_forks parameter)
    const isForkVisible = forkButton && forkButton.style.display !== 'none';
    
    // Get star button position for animation target
    const getStarButtonPosition = () => {
        const rect = starButton.getBoundingClientRect();
        const cursorRect = cursor.getBoundingClientRect();
        console.log('Star button rect:', rect);
        console.log('Cursor rect:', cursorRect);
        
        // Position cursor to click center of star button
        // Add offset to y position to account for cursor image click point
        const targetX = rect.left + (rect.width / 2) - (cursorRect.width / 2);
        const targetY = rect.top + (rect.height / 2) - 4; // Reduced offset for lower positioning
        
        console.log(`Calculated target position: (${targetX}, ${targetY})`);
        return {
            x: Math.round(targetX), // Round to prevent floating point issues
            y: Math.round(targetY)  // Round to prevent floating point issues
        };
    };
    
    // Animation settings
    const animationSettings = {
        cursorSpeed: 0.7, // Reduced for smoother animation and better frame capture
        initialDelay: 100, // Increased delay before animation starts for better visibility
        hoverDelay: 500, // Delay before clicking after hover
        resetDelay: 2000 // Delay before animation repeats
    };
    
    // Show cursor element
    const showCursor = () => {
        cursor.style.opacity = '1';
        cursor.classList.add('visible');
    };
    
    // Hide cursor element
    const hideCursor = () => {
        cursor.style.opacity = '0';
        cursor.classList.remove('visible');
    };
    
    // Simulate cursor click
    const simulateClick = () => {
        // Add clicking class for visual effect
        cursor.classList.add('clicking');
        
        // Always change to starred state (not toggling)
        starButton.classList.add('starred');
        starButton.querySelector('.star-label').textContent = 'Starred';
        
        // Remove clicking class after animation
        setTimeout(() => {
            cursor.classList.remove('clicking');
        }, 200);
    };
    
    // Move cursor to target position
    const moveCursor = (targetX, targetY, onComplete) => {
        // Get current position
        const currentX = parseFloat(cursor.style.left) || 0;
        const currentY = parseFloat(cursor.style.top) || 0;

        console.log(`Cursor position: (${currentX}, ${currentY}), Target: (${targetX}, ${targetY})`);
        console.log(`Cursor element dimensions: ${cursor.offsetWidth}x${cursor.offsetHeight}`);
        console.log(`Cursor dot dimensions: ${cursor.querySelector('.cursor-dot').offsetWidth}x${cursor.querySelector('.cursor-dot').offsetHeight}`);

        // Calculate direction vector
        const dx = targetX - currentX;
        const dy = targetY - currentY;

        // Calculate distance
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 5) {  // Increased threshold to prevent oscillation
            // Target reached - snap to exact position
            cursor.style.left = targetX + 'px';
            cursor.style.top = targetY + 'px';
            console.log(`Target reached at (${targetX}, ${targetY})`);
            if (onComplete) onComplete();
            return;
        }

        // Move toward target with adaptive speed
        const speed = Math.min(animationSettings.cursorSpeed, Math.max(2, distance / 3));
        const moveX = (dx / distance) * speed;
        const moveY = (dy / distance) * speed;

        cursor.style.left = (currentX + moveX) + 'px';
        cursor.style.top = (currentY + moveY) + 'px';

        // Continue animation
        requestAnimationFrame(() => moveCursor(targetX, targetY, onComplete));
    };
    
    // Start the animation sequence
    const startAnimation = () => {
        // Get star button position first
        const starPos = getStarButtonPosition();
        
        // Initial position - align with star button horizontally but place cursor further below screen
        // to ensure cursor movement is clearly visible
        cursor.style.left = starPos.x + 'px';
        cursor.style.top = (window.innerHeight + 100) + 'px';
        
        // Show cursor
        showCursor();
        
        // Move cursor up to star button
        setTimeout(() => {
            moveCursor(starPos.x, starPos.y, () => {
                // Wait before clicking
                setTimeout(() => {
                    // Click animation
                    simulateClick();
                    
                    // Reset after delay
                    setTimeout(() => {
                        // Move cursor straight down
                        moveCursor(starPos.x, window.innerHeight + 100, () => {
                            hideCursor();
                            
                            // Add a delay before restarting animation to ensure cursor fully disappears
                            // This prevents the cursor from "jumping" when the gif loops
                            setTimeout(startAnimation, 500);
                        });
                    }, animationSettings.resetDelay);
                }, animationSettings.hoverDelay);
            });
        }, animationSettings.initialDelay);
    };
    
    // Initialize - make sure the star button starts as unstarred
    starButton.classList.remove('starred');
    starButton.querySelector('.star-label').textContent = 'Star';
    
    // Start the animation sequence immediately
    startAnimation();
    
    // Add window resize listener to recalculate positions
    window.addEventListener('resize', () => {
        if (cursor.classList.contains('visible')) {
            const starPos = getStarButtonPosition();
            cursor.style.left = starPos.x + 'px';
            cursor.style.top = starPos.y + 'px';
        }
    });
});