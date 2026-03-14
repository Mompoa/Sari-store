// ==================== UTILITY FUNCTIONS ====================

/**
 * Close alert messages
 */
function closeAlert(element) {
    element.style.display = 'none';
}

/**
 * Format currency to PHP
 */
function formatCurrency(amount) {
    return '₱' + parseFloat(amount).toFixed(2);
}

/**
 * Debounce function for search
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==================== SEARCH FUNCTIONALITY ====================

const searchInput = document.querySelector('.search-input');
if (searchInput) {
    searchInput.addEventListener('input', debounce(function() {
        // Form submission handled by HTML form
    }, 300));
}

// ==================== PRODUCT CARD INTERACTIONS ====================

document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to product cards
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// ==================== QUANTITY INPUT ====================

function updateQuantityDisplay() {
    const quantityInput = document.getElementById('quantity');
    if (quantityInput) {
        const quantity = parseInt(quantityInput.value) || 1;
        const productPrice = parseFloat(document.querySelector('[data-price]')?.dataset.price || 0);
        
        if (productPrice > 0) {
            const total = productPrice * quantity;
            const totalElement = document.getElementById('total-price');
            if (totalElement) {
                totalElement.textContent = formatCurrency(total);
            }
        }
    }
}

// ==================== FORM VALIDATION ====================

function validateCheckoutForm() {
    const form = document.querySelector('.checkout-form');
    if (!form) return true;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#e74c3c';
            isValid = false;
        } else {
            field.style.borderColor = '';
        }
    });
    
    return isValid;
}

// ==================== SMOOTH SCROLL ====================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// ==================== IMAGE LAZY LOADING ====================

if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src || img.src;
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ==================== MOBILE MENU ====================

function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks) {
        navLinks.classList.toggle('active');
    }
}

// ==================== PRINT FUNCTIONALITY ====================

function printOrder() {
    window.print();
}

// ==================== EXPORT FUNCTIONALITY ====================

function exportToCSV(filename = 'export.csv') {
    const table = document.querySelector('table');
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        cols.forEach(col => {
            csvRow.push('"' + col.innerText.replace(/"/g, '""') + '"');
        });
        csv.push(csvRow.join(','));
    });
    
    downloadCSV(csv.join('\n'), filename);
}

function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// ==================== NOTIFICATION SYSTEM ====================

function showNotification(message, type = 'success', duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        ${message}
        <button class="alert-close" onclick="this.parentElement.style.display='none';">&times;</button>
    `;
    
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.insertBefore(alertDiv, mainContent.firstChild);
        
        if (duration > 0) {
            setTimeout(() => {
                alertDiv.style.display = 'none';
            }, duration);
        }
    }
}

// ==================== INITIALIZE ====================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if any
    initializeTooltips();
    
    // Initialize form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (this.classList.contains('checkout-form')) {
                if (!validateCheckoutForm()) {
                    e.preventDefault();
                    showNotification('Please fill in all required fields', 'error');
                }
            }
        });
    });
});

function initializeTooltips() {
    // Add tooltip functionality if needed
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            this.appendChild(tooltip);
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.tooltip');
            if (tooltip) tooltip.remove();
        });
    });
}
