// Hotel Billing System - Client-side JavaScript

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
});

// Slide out animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateY(0);
            opacity: 1;
        }
        to {
            transform: translateY(-20px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = 'var(--danger-color)';
            isValid = false;
        } else {
            field.style.borderColor = 'var(--border-color)';
        }
    });
    
    return isValid;
}

// Phone number validation
function validatePhone(input) {
    const phoneRegex = /^[0-9]{10}$/;
    if (!phoneRegex.test(input.value.replace(/\D/g, ''))) {
        input.setCustomValidity('Please enter a valid 10-digit phone number');
    } else {
        input.setCustomValidity('');
    }
}

// Email validation
function validateEmail(input) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (input.value && !emailRegex.test(input.value)) {
        input.setCustomValidity('Please enter a valid email address');
    } else {
        input.setCustomValidity('');
    }
}

// Format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// Calculate number of days between dates
function calculateDays(startDate, endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? diffDays : 1;
}

// Confirm before submission
function confirmAction(message) {
    return confirm(message);
}

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Add event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Phone validation
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validatePhone(this);
        });
    });
    
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEmail(this);
        });
    });
    
    // Set minimum date for check-in to today
    const checkInInputs = document.querySelectorAll('input[name="check_in_date"]');
    checkInInputs.forEach(input => {
        const today = new Date().toISOString().split('T')[0];
        input.setAttribute('min', today);
    });
    
    // Set minimum date for check-out based on check-in
    const checkInDate = document.querySelector('input[name="check_in_date"]');
    const checkOutDate = document.querySelector('input[name="check_out_date"]');
    
    if (checkInDate && checkOutDate) {
        checkInDate.addEventListener('change', function() {
            checkOutDate.setAttribute('min', this.value);
            if (checkOutDate.value && checkOutDate.value < this.value) {
                checkOutDate.value = this.value;
            }
        });
    }
    
    // Highlight navigation menu item for current page
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = 'var(--primary-color)';
            link.style.fontWeight = '700';
        }
    });
});

// Print functionality
function printInvoice() {
    window.print();
}

// Export to PDF (requires additional library in production)
function exportToPDF() {
    // This is a placeholder - in production, you would use a library like jsPDF
    alert('PDF export functionality would be implemented here with jsPDF library');
}

// Search/Filter functionality for tables
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    const filter = input.value.toUpperCase();
    const tr = table.getElementsByTagName('tr');
    
    for (let i = 1; i < tr.length; i++) {
        let found = false;
        const td = tr[i].getElementsByTagName('td');
        
        for (let j = 0; j < td.length; j++) {
            if (td[j]) {
                const txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        tr[i].style.display = found ? '' : 'none';
    }
}

// Local storage functions for draft forms
function saveDraft(formId) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    localStorage.setItem(formId + '_draft', JSON.stringify(data));
    alert('Draft saved!');
}

function loadDraft(formId) {
    const draft = localStorage.getItem(formId + '_draft');
    if (!draft) return;
    
    const data = JSON.parse(draft);
    const form = document.getElementById(formId);
    
    if (!form) return;
    
    for (let key in data) {
        const input = form.elements[key];
        if (input) {
            input.value = data[key];
        }
    }
    
    alert('Draft loaded!');
}

function clearDraft(formId) {
    localStorage.removeItem(formId + '_draft');
}

// Utility function to show/hide elements
function toggleElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = element.style.display === 'none' ? 'block' : 'none';
    }
}

// Debounce function for search inputs
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

// Console log for debugging (can be removed in production)
console.log('Hotel Billing System - JavaScript loaded successfully');
