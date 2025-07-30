// Navigation and Hamburger Menu JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Hamburger menu functionality
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const mobileNav = document.querySelector('.mobile-nav');
    const mobileNavClose = document.querySelector('.mobile-nav-close');
    
    if (hamburgerMenu) {
        hamburgerMenu.addEventListener('click', function() {
            hamburgerMenu.classList.toggle('active');
            mobileNav.classList.toggle('active');
            document.body.style.overflow = mobileNav.classList.contains('active') ? 'hidden' : '';
        });
    }
    
    if (mobileNavClose) {
        mobileNavClose.addEventListener('click', function() {
            hamburgerMenu.classList.remove('active');
            mobileNav.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    
    // Close mobile nav when clicking outside
    if (mobileNav) {
        mobileNav.addEventListener('click', function(e) {
            if (e.target === mobileNav) {
                hamburgerMenu.classList.remove('active');
                mobileNav.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }
    
    // Close mobile nav with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileNav && mobileNav.classList.contains('active')) {
            hamburgerMenu.classList.remove('active');
            mobileNav.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
    
    // User profile icon click handler
    const userProfileIcon = document.querySelector('.user-profile-icon');
    if (userProfileIcon) {
        userProfileIcon.addEventListener('click', function() {
            window.location.href = '/profile';
        });
    }
    
    // Auto-remove flash messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
}); 