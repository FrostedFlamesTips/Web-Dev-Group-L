// form-validation.js - Client-side form validation for data entry forms
// This file provides reusable validation functions for various forms in the application

document.addEventListener('DOMContentLoaded', function() {
    console.log("Initializing form validation");

    // Find all forms with the data-validate attribute
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Prevent default form submission
            event.preventDefault();
            
            // Get the form type from the data-form-type attribute
            const formType = form.getAttribute('data-form-type');
            
            // Validate the form based on its type
            let isValid = true;
            let errorMessage = '';
            
            switch(formType) {
                case 'login':
                    isValid = validateLoginForm(form);
                    break;
                case 'add-machine':
                    isValid = validateMachineForm(form);
                    break;
                case 'fault-report':
                    isValid = validateFaultForm(form);
                    break;
                case 'user-profile':
                    isValid = validateUserProfileForm(form);
                    break;
                case 'add-warning':
                    isValid = validateWarningForm(form);
                    break;
                default:
                    // For forms without specific validation, do basic required field check
                    isValid = validateRequiredFields(form);
            }
            
            // If the form is valid, submit it
            if (isValid) {
                // For demo/static pages, this will simulate form submission
                // In the real application, this would submit to the server
                handleFormSubmission(form, formType);
            }
        });
    });
    
    // Form field real-time validation
    document.querySelectorAll('input[data-validate], select[data-validate], textarea[data-validate]')
        .forEach(field => {
            field.addEventListener('blur', function() {
                validateField(field);
            });
        });
});

// Validate login form
function validateLoginForm(form) {
    const username = form.querySelector('#username');
    const password = form.querySelector('#password');
    let isValid = true;
    
    // Basic username validation
    if (!username.value.trim()) {
        showError(username, 'Username is required');
        isValid = false;
    } else {
        clearError(username);
    }
    
    // Basic password validation
    if (!password.value) {
        showError(password, 'Password is required');
        isValid = false;
    } else if (password.value.length < 6) {
        showError(password, 'Password must be at least 6 characters');
        isValid = false;
    } else {
        clearError(password);
    }
    
    return isValid;
}

// Validate machinery form
function validateMachineForm(form) {
    const fields = [
        {field: form.querySelector('#machine-id'), message: 'Machine ID is required', pattern: /^[A-Z0-9]{3,10}$/},
        {field: form.querySelector('#machine-name'), message: 'Machine name is required'},
        {field: form.querySelector('#machine-model'), message: 'Model is required'},
        {field: form.querySelector('#machine-location'), message: 'Location is required'}
    ];
    
    return validateFields(fields);
}

// Validate fault reporting form
function validateFaultForm(form) {
    const fields = [
        {field: form.querySelector('#fault-title'), message: 'Fault title is required'},
        {field: form.querySelector('#fault-category'), message: 'Please select a fault category'},
        {field: form.querySelector('#fault-description'), message: 'Detailed description is required', minLength: 20},
        {field: form.querySelector('#fault-priority'), message: 'Please select a priority level'}
    ];
    
    return validateFields(fields);
}

// Validate user profile form
function validateUserProfileForm(form) {
    const fields = [
        {field: form.querySelector('#user-name'), message: 'Full name is required'},
        {field: form.querySelector('#user-email'), message: 'Email is required', pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/},
        {field: form.querySelector('#user-role'), message: 'Please select a role'}
    ];
    
    const password = form.querySelector('#user-password');
    const confirmPassword = form.querySelector('#confirm-password');
    
    let isValid = validateFields(fields);
    
    // Only validate passwords if they are being changed (not empty)
    if (password && confirmPassword && password.value) {
        if (password.value.length < 8) {
            showError(password, 'Password must be at least 8 characters');
            isValid = false;
        } else if (password.value !== confirmPassword.value) {
            showError(confirmPassword, 'Passwords do not match');
            isValid = false;
        } else {
            clearError(password);
            clearError(confirmPassword);
        }
    }
    
    return isValid;
}

// Validate warning form
function validateWarningForm(form) {
    const fields = [
        {field: form.querySelector('#warning-text'), message: 'Warning message is required'}
    ];
    
    return validateFields(fields);
}

// Generic validation for all required fields in a form
function validateRequiredFields(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showError(field, `This field is required`);
            isValid = false;
        } else {
            clearError(field);
        }
    });
    
    return isValid;
}

// Validate a list of fields
function validateFields(fields) {
    let isValid = true;
    
    fields.forEach(({field, message, pattern, minLength}) => {
        if (!field) return; // Skip if field doesn't exist
        
        const value = field.value.trim();
        
        if (!value) {
            showError(field, message);
            isValid = false;
        } else if (pattern && !pattern.test(value)) {
            showError(field, `Invalid format`);
            isValid = false;
        } else if (minLength && value.length < minLength) {
            showError(field, `Minimum ${minLength} characters required`);
            isValid = false;
        } else {
            clearError(field);
        }
    });
    
    return isValid;
}

// Validate a single field
function validateField(field) {
    const value = field.value.trim();
    const isRequired = field.hasAttribute('required');
    const minLength = field.getAttribute('minlength');
    const pattern = field.getAttribute('pattern');
    
    if (isRequired && !value) {
        showError(field, 'This field is required');
        return false;
    }
    
    if (minLength && value.length < parseInt(minLength)) {
        showError(field, `Minimum ${minLength} characters required`);
        return false;
    }
    
    if (pattern && value) {
        const regex = new RegExp(pattern);
        if (!regex.test(value)) {
            showError(field, 'Invalid format');
            return false;
        }
    }
    
    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showError(field, 'Invalid email format');
            return false;
        }
    }
    
    clearError(field);
    return true;
}

// Show validation error
function showError(field, message) {
    // Remove any existing error
    clearError(field);
    
    // Add error class to the field
    field.classList.add('error');
    
    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.color = '#EF4444';
    errorDiv.style.fontSize = '0.85rem';
    errorDiv.style.marginTop = '0.25rem';
    
    // Insert error message after the field
    field.parentNode.appendChild(errorDiv);
}

// Clear validation error
function clearError(field) {
    field.classList.remove('error');
    
    // Remove any existing error message
    const errorMessage = field.parentNode.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

// Handle form submission (simulation for static pages)
function handleFormSubmission(form, formType) {
    console.log(`Submitting ${formType} form`);
    
    // For demonstration purposes, simulate different form submissions
    switch(formType) {
        case 'login':
            // Simulate login
            const username = form.querySelector('#username').value;
            const password = form.querySelector('#password').value;
            
            // For demo, we'll use hardcoded credentials
            let isAuthenticated = false;
            let role = '';
            let fullName = '';
            
            if (username === 'manager' && password === 'manager123') {
                isAuthenticated = true;
                role = 'manager';
                fullName = 'John Doe';
            } else if (username === 'tech' && password === 'tech123') {
                isAuthenticated = true;
                role = 'technician';
                fullName = 'Jane Smith';
            } else if (username === 'repair' && password === 'repair123') {
                isAuthenticated = true;
                role = 'repair';
                fullName = 'Bob Johnson';
            }
            
            if (isAuthenticated) {
                // Store authentication info in session storage
                sessionStorage.setItem('userLoggedIn', 'true');
                sessionStorage.setItem('userName', fullName);
                sessionStorage.setItem('userRole', role);
                
                // Redirect to dashboard
                window.location.href = 'index.html';
            } else {
                // Show login error
                const errorContainer = form.querySelector('.form-error');
                if (errorContainer) {
                    errorContainer.textContent = 'Invalid username or password';
                    errorContainer.style.display = 'block';
                }
            }
            break;
            
        case 'fault-report':
            // Simulate fault report submission
            alert('Fault report submitted successfully! A case ID will be assigned and you will be redirected to the case details.');
            window.location.href = 'fault-details.html?id=NEW-CASE';
            break;
            
        case 'add-machine':
            // Simulate adding a machine
            alert('Machine added successfully!');
            window.location.href = 'machinery.html';
            break;
            
        case 'add-warning':
            // Simulate adding a warning
            alert('Warning added successfully!');
            location.reload();
            break;
            
        default:
            // For other forms, just show a success message
            alert('Form submitted successfully!');
            // Optional: redirect back to related page
            // window.location.href = document.referrer || 'index.html';
    }
}