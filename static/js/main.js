// EV Spot - Main JavaScript

// Global variables
let currentUser = null;
let activeSession = null;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkAuthenticationStatus();
});

// Initialize the application
function initializeApp() {
    // Add fade-in animation to elements
    const elements = document.querySelectorAll('.card, .feature-icon, .stat-item');
    elements.forEach((element, index) => {
        element.style.animationDelay = `${index * 0.1}s`;
        element.classList.add('fade-in-up');
    });
}

// Setup event listeners
function setupEventListeners() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }

    // Logout button
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // Search radius slider
    const searchRadius = document.getElementById('searchRadius');
    if (searchRadius) {
        searchRadius.addEventListener('input', updateRadiusDisplay);
    }

    // Station cards click events
    document.addEventListener('click', function(e) {
        if (e.target.closest('.station-card')) {
            const stationCard = e.target.closest('.station-card');
            handleStationCardClick(stationCard);
        }
    });
}

// Check authentication status
function checkAuthenticationStatus() {
    // Check if user is logged in (you can implement session checking here)
    const token = localStorage.getItem('authToken');
    if (token) {
        // Verify token with backend
        verifyToken(token);
    } else {
        updateUIForGuest();
    }
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    if (!username || !password) {
        showAlert('Please fill in all fields', 'danger');
        return;
    }
    
    try {
        const csrfToken = getCookie('csrftoken');
        if (!csrfToken) {
            showAlert('CSRF token not found. Please refresh the page.', 'danger');
            return;
        }
        
        const response = await fetch('/api/users/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store user data
            localStorage.setItem('authToken', data.token || 'dummy-token');
            localStorage.setItem('userData', JSON.stringify(data.user));
            
            currentUser = data.user;
            updateUIForUser();
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
            modal.hide();
            
            showAlert('Login successful!', 'success');
        } else {
            showAlert(data.error || 'Login failed', 'danger');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('An error occurred during login', 'danger');
    }
}

// Handle register
async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const password2 = document.getElementById('registerPassword2').value;
    
    if (!username || !email || !password || !password2) {
        showAlert('Please fill in all fields', 'danger');
        return;
    }
    
    if (password !== password2) {
        showAlert('Passwords do not match', 'danger');
        return;
    }
    
    if (password.length < 8) {
        showAlert('Password must be at least 8 characters long', 'danger');
        return;
    }
    
    try {
        const csrfToken = getCookie('csrftoken');
        if (!csrfToken) {
            showAlert('CSRF token not found. Please refresh the page.', 'danger');
            return;
        }
        
        const response = await fetch('/api/users/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                password2: password2
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
            modal.hide();
            
            showAlert('Registration successful! Please log in.', 'success');
        } else {
            const errorMessage = data.error || Object.values(data).flat().join(', ');
            showAlert(errorMessage, 'danger');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showAlert('An error occurred during registration', 'danger');
    }
}

// Handle logout
async function handleLogout() {
    try {
        const csrfToken = getCookie('csrftoken');
        const response = await fetch('/api/users/logout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        });
        
        // Clear local storage
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
        
        currentUser = null;
        updateUIForGuest();
        
        showAlert('Logout successful!', 'success');
    } catch (error) {
        console.error('Logout error:', error);
        // Still clear local storage even if API call fails
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
        currentUser = null;
        updateUIForGuest();
    }
}

// Verify token
async function verifyToken(token) {
    try {
        const response = await fetch('/api/users/profile/', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            const userData = await response.json();
            currentUser = userData;
            updateUIForUser();
        } else {
            // Token is invalid
            localStorage.removeItem('authToken');
            localStorage.removeItem('userData');
            updateUIForGuest();
        }
    } catch (error) {
        console.error('Token verification error:', error);
        updateUIForGuest();
    }
}

// Update UI for authenticated user
function updateUIForUser() {
    const userDropdown = document.querySelector('.navbar-nav .dropdown-toggle');
    if (userDropdown && currentUser) {
        userDropdown.innerHTML = `<i class="fas fa-user me-1"></i>${currentUser.username}`;
    }
    
    // Show user-specific features
    const userFeatures = document.querySelectorAll('.user-only');
    userFeatures.forEach(feature => {
        feature.style.display = 'block';
    });
}

// Update UI for guest user
function updateUIForGuest() {
    const userFeatures = document.querySelectorAll('.user-only');
    userFeatures.forEach(feature => {
        feature.style.display = 'none';
    });
}

// Handle station card click
function handleStationCardClick(stationCard) {
    const stationName = stationCard.querySelector('h6').textContent;
    const stationAddress = stationCard.querySelector('p').textContent;
    
    // Show station details modal
    showStationDetails(stationName, stationAddress);
}

// Show station details
function showStationDetails(name, address) {
    const modal = new bootstrap.Modal(document.getElementById('stationDetailsModal'));
    
    // Update modal content
    document.getElementById('stationName').textContent = name;
    document.getElementById('stationAddress').textContent = address;
    
    modal.show();
}

// Update radius display
function updateRadiusDisplay() {
    const radius = document.getElementById('searchRadius').value;
    const radiusValue = document.getElementById('radiusValue');
    if (radiusValue) {
        radiusValue.textContent = radius + 'km';
    }
}

// Show alert message
function showAlert(message, type) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// API helper functions
const API = {
    // Get nearby stations
    async getNearbyStations(lat, lng, radius) {
        try {
            const csrfToken = getCookie('csrftoken');
            if (!csrfToken) {
                throw new Error('CSRF token not found');
            }
            
            const response = await fetch('/api/stations/nearby/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    latitude: lat,
                    longitude: lng,
                    radius: radius
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch stations');
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // Start charging session
    async startCharging(stationId) {
        try {
            const response = await fetch(`/api/stations/${stationId}/start_charging/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to start charging');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Start charging error:', error);
            throw error;
        }
    },
    
    // Stop charging session
    async stopCharging(stationId) {
        try {
            const response = await fetch(`/api/stations/${stationId}/stop_charging/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to stop charging');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Stop charging error:', error);
            throw error;
        }
    },
    
    // Add to favorites
    async addToFavorites(stationId) {
        try {
            const response = await fetch('/api/favorites/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    station: stationId
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to add to favorites');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Add to favorites error:', error);
            throw error;
        }
    },
    
    // Get user sessions
    async getUserSessions() {
        try {
            const response = await fetch('/api/sessions/', {
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch sessions');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Get sessions error:', error);
            throw error;
        }
    }
};

// Utility functions
const Utils = {
    // Format currency
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },
    
    // Format distance
    formatDistance(distance) {
        if (distance < 1) {
            return `${Math.round(distance * 1000)}m`;
        }
        return `${distance.toFixed(1)}km`;
    },
    
    // Format time
    formatTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    },
    
    // Debounce function
    debounce(func, wait) {
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
};

// Export for use in other scripts
window.EVSpot = {
    API,
    Utils,
    currentUser,
    showAlert
}; 