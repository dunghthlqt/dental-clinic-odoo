/** @odoo-module **/

// Hide unallocated credit banner in account.move form view
// This banner is created dynamically by Odoo, so we need to use JavaScript to hide it

(function() {
    'use strict';
    
    // Function to hide unallocated credit banner
    function hideUnallocatedCreditBanner() {
        const alerts = document.querySelectorAll('.o_form_view .alert, .o_form_view [role="alert"]');
        alerts.forEach(function(alert) {
            const text = alert.textContent || alert.innerText || '';
            if (text.includes('dư có chưa phân bổ') || 
                text.includes('unallocated credit') || 
                text.includes('phân bổ')) {
                alert.style.display = 'none';
            }
        });
    }
    
    // Hide banner when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', hideUnallocatedCreditBanner);
    } else {
        hideUnallocatedCreditBanner();
    }
    
    // Also hide banner when content changes (for dynamic content)
    const observer = new MutationObserver(function(mutations) {
        hideUnallocatedCreditBanner();
    });
    
    // Start observing when body is available
    if (document.body) {
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        });
    }
})();

