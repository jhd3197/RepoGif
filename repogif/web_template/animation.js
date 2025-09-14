// GitHub Repository Header Animation Script

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const cursor = document.getElementById('cursor');
    const starButton = document.getElementById('star-button');
    
    // Get star button position for animation target
    const getStarButtonPosition = () => {
        const rect = starButton.getBoundingClientRect();
        return {
            x: rect.left + rect.width / 2 - cursor.offsetWidth / 2,
            y: rect.top + rect.height + 10 // Position cursor below the star button
        };
    };
    
    // Animation settings
    const animationSettings = {
        cursorSpeed: 10, // Higher values = faster animation
        initialDelay: 500, // Reduced delay before animation starts
        hoverDelay: 500, // Delay before clicking after hover
        resetDelay: 2000 // Reduced delay before animation repeats
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
        
        // Calculate direction vector
        const dx = targetX - currentX;
        const dy = targetY - currentY;
        
        // Calculate distance
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 1) {
            // Target reached
            cursor.style.left = targetX + 'px';
            cursor.style.top = targetY + 'px';
            if (onComplete) onComplete();
            return;
        }
        
        // Move toward target
        const moveX = dx / distance * animationSettings.cursorSpeed;
        const moveY = dy / distance * animationSettings.cursorSpeed;
        
        cursor.style.left = (currentX + moveX) + 'px';
        cursor.style.top = (currentY + moveY) + 'px';
        
        // Continue animation
        requestAnimationFrame(() => moveCursor(targetX, targetY, onComplete));
    };
    
    // Start the animation sequence
    const startAnimation = () => {
        // Initial position - off screen from bottom
        cursor.style.left = window.innerWidth / 2 + 'px';
        cursor.style.top = (window.innerHeight + 50) + 'px';
        
        // Show cursor
        showCursor();
        
        // Get star button position
        const starPos = getStarButtonPosition();
        
        // Move cursor to star button
        setTimeout(() => {
            moveCursor(starPos.x, starPos.y, () => {
                // Wait before clicking
                setTimeout(() => {
                    // Click animation
                    simulateClick();
                    
                    // Reset after delay
                    setTimeout(() => {
                        // Move cursor away downward
                        moveCursor(starPos.x, window.innerHeight + 50, () => {
                            hideCursor();
                            
                            // Restart animation
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