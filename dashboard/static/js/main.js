/**
 * Main JavaScript for ALC Competitive Intelligence Tracker
 */

// Set Chart.js default options for dark theme
Chart.defaults.color = '#999';
Chart.defaults.borderColor = '#444';
Chart.defaults.backgroundColor = 'rgba(0, 123, 255, 0.1)';

// Update last updated timestamp
document.addEventListener('DOMContentLoaded', function() {
    updateLastUpdated();
    setInterval(updateLastUpdated, 60000); // Update every minute
});

/**
 * Update the last updated timestamp in footer
 */
function updateLastUpdated() {
    const now = new Date();
    const timeString = now.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });

    const element = document.getElementById('last-updated');
    if (element) {
        element.textContent = timeString;
    }
}

/**
 * Format numbers with K/M suffixes
 */
function formatNumber(num) {
    if (!num) return '0';
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}

/**
 * Format percentage with 2 decimal places
 */
function formatPercent(num) {
    return (num * 100).toFixed(2) + '%';
}

/**
 * Format date string to human-readable format
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Get API data from endpoint
 */
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        return null;
    }
}

/**
 * Show loading spinner
 */
function showLoading(element) {
    element.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
}

/**
 * Get color based on performance
 */
function getPerformanceColor(value, benchmark = 0) {
    if (value > benchmark * 1.2) return '#28a745'; // Green - above average
    if (value > benchmark * 0.8) return '#ffc107'; // Yellow - near average
    return '#dc3545'; // Red - below average
}

/**
 * Initialize tooltips (Bootstrap)
 */
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

/**
 * Handle market selection change
 */
function changeMarket(market) {
    const params = new URLSearchParams(window.location.search);
    params.set('market', market);
    window.location.search = params.toString();
}

/**
 * Handle date range selection
 */
function changeDateRange(days) {
    const params = new URLSearchParams(window.location.search);
    params.set('range', days);
    window.location.search = params.toString();
}

// Export functions for use in templates
window.formatNumber = formatNumber;
window.formatPercent = formatPercent;
window.formatDate = formatDate;
window.fetchAPI = fetchAPI;
window.showLoading = showLoading;
window.getPerformanceColor = getPerformanceColor;
window.changeMarket = changeMarket;
window.changeDateRange = changeDateRange;
