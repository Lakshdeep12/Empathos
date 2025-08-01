// Empathos - Main JavaScript File

// Utility Functions
const Empathos = {
    // Show notification/toast message
    showNotification: function(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        `;
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after duration
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    },

    // Format date
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Validate email
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Smooth scroll to element
    scrollToElement: function(elementId, offset = 0) {
        const element = document.getElementById(elementId);
        if (element) {
            const elementPosition = element.offsetTop - offset;
            window.scrollTo({
                top: elementPosition,
                behavior: 'smooth'
            });
        }
    },

    // Copy text to clipboard
    copyToClipboard: function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success', 2000);
            }).catch(() => {
                this.fallbackCopyToClipboard(text);
            });
        } else {
            this.fallbackCopyToClipboard(text);
        }
    },

    // Fallback copy method
    fallbackCopyToClipboard: function(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            this.showNotification('Copied to clipboard!', 'success', 2000);
        } catch (err) {
            this.showNotification('Failed to copy text', 'error', 3000);
        }
        
        document.body.removeChild(textArea);
    },

    // Loading state management
    setLoading: function(element, isLoading = true) {
        if (isLoading) {
            element.disabled = true;
            element.innerHTML = '<span class="loading"></span> Loading...';
        } else {
            element.disabled = false;
            element.innerHTML = element.getAttribute('data-original-text') || 'Submit';
        }
    },

    // Form validation
    validateForm: function(formElement) {
        const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.showFieldError(input, 'This field is required');
                isValid = false;
            } else {
                this.clearFieldError(input);
            }
        });
        
        return isValid;
    },

    // Show field error
    showFieldError: function(field, message) {
        field.classList.add('is-invalid');
        
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            field.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    },

    // Clear field error
    clearFieldError: function(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    },

    // Animate element on scroll
    animateOnScroll: function() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        });

        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
    },

    // Theme management
    setTheme: function(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('empathos-theme', theme);
    },

    // Get current theme
    getTheme: function() {
        return localStorage.getItem('empathos-theme') || 'light';
    },

    // Initialize theme
    initTheme: function() {
        const theme = this.getTheme();
        this.setTheme(theme);
        
        // Add theme toggle functionality
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const currentTheme = this.getTheme();
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                this.setTheme(newTheme);
            });
        }
    }
};

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme
    Empathos.initTheme();
    
    // Initialize animations
    Empathos.animateOnScroll();
    
    // Form validation
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!Empathos.validateForm(this)) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-save form data
    const autoSaveForms = document.querySelectorAll('form[data-autosave]');
    autoSaveForms.forEach(form => {
        const formId = form.getAttribute('data-autosave');
        
        // Load saved data
        const savedData = localStorage.getItem(`form-${formId}`);
        if (savedData) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const field = form.querySelector(`[name="${key}"]`);
                if (field) {
                    field.value = data[key];
                }
            });
        }
        
        // Save data on input
        const saveFormData = Empathos.debounce(() => {
            const formData = new FormData(form);
            const data = {};
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            localStorage.setItem(`form-${formId}`, JSON.stringify(data));
        }, 1000);
        
        form.addEventListener('input', saveFormData);
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            Empathos.scrollToElement(targetId, 80);
        });
    });
    
    // Loading states for buttons
    document.querySelectorAll('button[data-loading]').forEach(button => {
        button.setAttribute('data-original-text', button.innerHTML);
        
        button.addEventListener('click', function() {
            Empathos.setLoading(this, true);
            
            // Simulate loading (remove in production)
            setTimeout(() => {
                Empathos.setLoading(this, false);
            }, 2000);
        });
    });
    
    // Copy buttons
    document.querySelectorAll('[data-copy]').forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            Empathos.copyToClipboard(textToCopy);
        });
    });
    
    // Alert auto-dismiss
    document.querySelectorAll('.alert-auto-dismiss').forEach(alert => {
        const duration = alert.getAttribute('data-duration') || 5000;
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, parseInt(duration));
    });
    
    // Table row selection
    document.querySelectorAll('.table-selectable tbody tr').forEach(row => {
        row.addEventListener('click', function() {
            this.classList.toggle('selected');
        });
    });
    
    // Modal enhancements
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const firstInput = this.querySelector('input, select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });
    
    // Tooltip initialization
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Popover initialization
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    Empathos.showNotification('An error occurred. Please try again.', 'error');
});

// Network status monitoring
window.addEventListener('online', function() {
    Empathos.showNotification('Connection restored!', 'success', 3000);
});

window.addEventListener('offline', function() {
    Empathos.showNotification('You are offline. Some features may not work.', 'warning', 5000);
});

// Service Worker registration (for PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('SW registered: ', registration);
            })
            .catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Export for use in other scripts
window.Empathos = Empathos; 