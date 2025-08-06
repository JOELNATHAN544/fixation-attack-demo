// Professional JavaScript for Session Fixation Lab

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to containers
    const containers = document.querySelectorAll('.container, .dashboard');
    containers.forEach(container => {
        container.classList.add('fade-in');
    });

    // Form validation and enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[type="text"], input[type="password"]');
        
        inputs.forEach(input => {
            // Add focus effects
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('focused');
            });
            
            // Add loading state to submit button
            form.addEventListener('submit', function(e) {
                const submitBtn = form.querySelector('input[type="submit"], button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="spinner"></span>Logging in...';
                }
            });
        });
    });

    // Session ID display enhancement
    const sessionDisplays = document.querySelectorAll('.session-id');
    sessionDisplays.forEach(display => {
        if (display.textContent) {
            display.style.fontFamily = 'Courier New, monospace';
            display.style.backgroundColor = '#ecf0f1';
            display.style.padding = '5px 10px';
            display.style.borderRadius = '4px';
            display.style.fontSize = '0.9em';
        }
    });

    // Copy session ID functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sessionId = this.getAttribute('data-session-id');
            if (sessionId) {
                navigator.clipboard.writeText(sessionId).then(() => {
                    this.textContent = 'Copied!';
                    setTimeout(() => {
                        this.textContent = 'Copy';
                    }, 2000);
                });
            }
        });
    });

    // Alert auto-dismiss
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Session fixation demonstration helper
    const demoButtons = document.querySelectorAll('.demo-btn');
    demoButtons.forEach(button => {
        button.addEventListener('click', function() {
            const demoType = this.getAttribute('data-demo');
            if (demoType === 'vulnerable') {
                showDemoInfo('This app is vulnerable to session fixation attacks. Session IDs remain the same after login.');
            } else if (demoType === 'secure') {
                showDemoInfo('This app prevents session fixation by regenerating session IDs after login.');
            }
        });
    });
});

// Helper function to show demo information
function showDemoInfo(message) {
    const infoDiv = document.createElement('div');
    infoDiv.className = 'alert alert-info fade-in';
    infoDiv.innerHTML = `
        <strong>Demo Info:</strong> ${message}
        <button type="button" class="close-btn" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    const container = document.querySelector('.container, .dashboard');
    if (container) {
        container.insertBefore(infoDiv, container.firstChild);
    }
}

// Utility function to format session data
function formatSessionData(data) {
    if (typeof data === 'string') {
        try {
            data = JSON.parse(data);
        } catch (e) {
            return data;
        }
    }
    
    return JSON.stringify(data, null, 2);
}

// Add session data formatting to page load
window.addEventListener('load', function() {
    const sessionDataElements = document.querySelectorAll('.session-data');
    sessionDataElements.forEach(element => {
        if (element.textContent) {
            element.textContent = formatSessionData(element.textContent);
        }
    });
}); 