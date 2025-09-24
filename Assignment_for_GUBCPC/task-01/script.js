// Dark Mode Toggle Functionality
class ThemeManager {
    constructor() {
        this.themeToggle = document.getElementById('themeToggle');
        this.toggleIcon = document.querySelector('.toggle-icon');
        this.currentTheme = localStorage.getItem('theme') || 'light';
        
        this.init();
    }
    
    init() {
        // Set initial theme
        this.setTheme(this.currentTheme);
        
        // Add event listener for theme toggle
        this.themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });
        
        // Add keyboard support for accessibility
        this.themeToggle.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.toggleTheme();
            }
        });
        
        // Add smooth animation on page load
        this.addLoadAnimation();
    }
    
    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
        
        // Update toggle icon
        this.toggleIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
        
        // Update button aria-label for accessibility
        this.themeToggle.setAttribute('aria-label', 
            theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
        );
    }
    
    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
        
        // Add a subtle animation to the toggle button
        this.animateToggle();
    }
    
    animateToggle() {
        this.themeToggle.style.transform = 'scale(0.9)';
        setTimeout(() => {
            this.themeToggle.style.transform = 'scale(1)';
        }, 150);
    }
    
    addLoadAnimation() {
        // Add entrance animation to the card
        const card = document.querySelector('.card');
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100);
    }
}

// Card Interaction Enhancements
class CardEnhancements {
    constructor() {
        this.card = document.querySelector('.card');
        this.infoItems = document.querySelectorAll('.info-item');
        this.socialIcons = document.querySelectorAll('.social-icon');
        
        this.init();
    }
    
    init() {
        this.addCardTiltEffect();
        this.addInfoItemAnimations();
        this.addSocialIconEffects();
        this.addKeyboardNavigation();
    }
    
    addCardTiltEffect() {
        this.card.addEventListener('mousemove', (e) => {
            const rect = this.card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            this.card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
        });
        
        this.card.addEventListener('mouseleave', () => {
            this.card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    }
    
    addInfoItemAnimations() {
        this.infoItems.forEach((item, index) => {
            // Stagger the initial animation
            item.style.opacity = '0';
            item.style.transform = 'translateX(-20px)';
            
            setTimeout(() => {
                item.style.transition = 'all 0.4s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, 200 + (index * 100));
            
            // Add click effect
            item.addEventListener('click', () => {
                item.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    item.style.transform = 'scale(1)';
                }, 100);
            });
        });
    }
    
    addSocialIconEffects() {
        this.socialIcons.forEach((icon, index) => {
            // Add bounce effect on hover
            icon.addEventListener('mouseenter', () => {
                icon.style.animation = 'bounce 0.6s ease';
            });
            
            icon.addEventListener('animationend', () => {
                icon.style.animation = '';
            });
            
            // Add click effect
            icon.addEventListener('click', () => {
                this.createRippleEffect(icon);
            });
        });
    }
    
    createRippleEffect(element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = '50%';
        ripple.style.top = '50%';
        ripple.style.transform = 'translate(-50%, -50%)';
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(255, 255, 255, 0.6)';
        ripple.style.animation = 'ripple 0.6s linear';
        ripple.style.pointerEvents = 'none';
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
    
    addKeyboardNavigation() {
        // Make info items focusable for keyboard navigation
        this.infoItems.forEach(item => {
            item.setAttribute('tabindex', '0');
            item.addEventListener('focus', () => {
                item.style.outline = '2px solid var(--accent-color)';
                item.style.outlineOffset = '2px';
            });
            item.addEventListener('blur', () => {
                item.style.outline = 'none';
            });
        });
    }
}

// Add CSS animations dynamically
function addDynamicStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes bounce {
            0%, 20%, 60%, 100% { transform: translateY(0) scale(1); }
            40% { transform: translateY(-10px) scale(1.1); }
            80% { transform: translateY(-5px) scale(1.05); }
        }
        
        @keyframes ripple {
            to {
                transform: translate(-50%, -50%) scale(4);
                opacity: 0;
            }
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(74, 144, 226, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(74, 144, 226, 0); }
            100% { box-shadow: 0 0 0 0 rgba(74, 144, 226, 0); }
        }
    `;
    document.head.appendChild(style);
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    addDynamicStyles();
    new ThemeManager();
    new CardEnhancements();
    
    // Add a subtle pulse effect to the avatar periodically
    const avatar = document.querySelector('.avatar');
    setInterval(() => {
        avatar.style.animation = 'pulse 2s';
        setTimeout(() => {
            avatar.style.animation = '';
        }, 2000);
    }, 10000);
});

// Handle system theme preference changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
        const themeManager = new ThemeManager();
        themeManager.setTheme(e.matches ? 'dark' : 'light');
    }
});
