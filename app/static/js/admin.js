// ==================== ADMIN UTILITIES ====================

/**
 * Confirm delete action
 */
function confirmDelete(itemName = 'this item') {
    return confirm(`Are you sure you want to delete ${itemName}? This action cannot be undone.`);
}

/**
 * Show notification
 */
function showAdminNotification(message, type = 'success', duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        ${message}
        <button class="alert-close" onclick="this.parentElement.style.display='none';">&times;</button>
    `;
    
    const adminContent = document.querySelector('.admin-content');
    if (adminContent) {
        adminContent.insertBefore(alertDiv, adminContent.firstChild);
        
        if (duration > 0) {
            setTimeout(() => {
                alertDiv.style.display = 'none';
            }, duration);
        }
    }
}

// ==================== TABLE INTERACTIONS ====================

document.addEventListener('DOMContentLoaded', function() {
    // Add row hover effects
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f9f9f9';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
    
    // Initialize delete buttons
    const deleteButtons = document.querySelectorAll('form[action*="delete"] button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirmDelete()) {
                e.preventDefault();
            }
        });
    });
});

// ==================== FORM HANDLING ====================

/**
 * Handle product form submission
 */
function handleProductFormSubmit(e) {
    const form = e.target;
    const name = form.querySelector('#name').value.trim();
    const price = parseFloat(form.querySelector('#price').value);
    const stock = parseInt(form.querySelector('#stock').value);
    
    if (!name) {
        e.preventDefault();
        showAdminNotification('Product name is required', 'error');
        return false;
    }
    
    if (isNaN(price) || price < 0) {
        e.preventDefault();
        showAdminNotification('Please enter a valid price', 'error');
        return false;
    }
    
    if (isNaN(stock) || stock < 0) {
        e.preventDefault();
        showAdminNotification('Please enter a valid stock quantity', 'error');
        return false;
    }
    
    return true;
}

// ==================== FILE UPLOAD PREVIEW ====================

function previewImage(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('image-preview');
    
    if (!preview) return;
    
    if (file) {
        // Check file size (16MB max)
        if (file.size > 16 * 1024 * 1024) {
            showAdminNotification('File size exceeds 16MB limit', 'error');
            event.target.value = '';
            preview.innerHTML = '';
            return;
        }
        
        // Check file type
        const validTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/webp'];
        if (!validTypes.includes(file.type)) {
            showAdminNotification('Please upload a valid image file (PNG, JPG, GIF, WebP)', 'error');
            event.target.value = '';
            preview.innerHTML = '';
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = '';
    }
}

// ==================== SEARCH & FILTER ====================

/**
 * Filter table rows by search query
 */
function filterTable(searchQuery, tableSelector = 'table') {
    const table = document.querySelector(tableSelector);
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    const query = searchQuery.toLowerCase();
    
    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
    });
}

/**
 * Debounce search
 */
function debounceSearch(func, wait) {
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

// ==================== EXPORT FUNCTIONALITY ====================

/**
 * Export table to CSV
 */
function exportTableToCSV(filename = 'export.csv') {
    const table = document.querySelector('table');
    if (!table) {
        showAdminNotification('No table found to export', 'error');
        return;
    }
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        cols.forEach(col => {
            // Skip action buttons
            if (!col.querySelector('form, .btn')) {
                csvRow.push('"' + col.innerText.replace(/"/g, '""') + '"');
            }
        });
        if (csvRow.length > 0) {
            csv.push(csvRow.join(','));
        }
    });
    
    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV file
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(csvFile);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ==================== PRINT FUNCTIONALITY ====================

/**
 * Print table
 */
function printTable() {
    window.print();
}

// ==================== BULK ACTIONS ====================

/**
 * Select/Deselect all checkboxes
 */
function toggleSelectAll(selectAllCheckbox) {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="item-select"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
}

/**
 * Get selected items
 */
function getSelectedItems() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][name="item-select"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

// ==================== SIDEBAR NAVIGATION ====================

document.addEventListener('DOMContentLoaded', function() {
    // Highlight active nav link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.href === window.location.href || 
            currentPath.includes(link.getAttribute('href'))) {
            link.classList.add('active');
        }
    });
});

// ==================== RESPONSIVE SIDEBAR ====================

function toggleSidebar() {
    const sidebar = document.querySelector('.admin-sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }
}

// ==================== KEYBOARD SHORTCUTS ====================

document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + S to save
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        const form = document.querySelector('form');
        if (form) {
            form.submit();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modal = document.querySelector('.modal.active');
        if (modal) {
            modal.classList.remove('active');
        }
    }
});

// ==================== STATS ANIMATION ====================

function animateStats() {
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        if (isNaN(finalValue)) return;
        
        let currentValue = 0;
        const increment = Math.ceil(finalValue / 30);
        const interval = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                stat.textContent = finalValue;
                clearInterval(interval);
            } else {
                stat.textContent = currentValue;
            }
        }, 30);
    });
}

// ==================== INITIALIZE ====================

document.addEventListener('DOMContentLoaded', function() {
    // Animate stats on dashboard
    if (document.querySelector('.dashboard-stats')) {
        animateStats();
    }
    
    // Initialize product form
    const productForm = document.querySelector('.product-form');
    if (productForm) {
        productForm.addEventListener('submit', handleProductFormSubmit);
    }
    
    // Add smooth transitions
    document.body.style.transition = 'all 0.3s ease';
});
