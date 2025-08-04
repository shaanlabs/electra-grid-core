// script.js

// Initialize the map
function initMap() {
    const map = L.map('map-container').setView([37.7749, -122.4194], 13); // Example coordinates (San Francisco)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Add a marker for a charging station
    const marker = L.marker([37.7749, -122.4194]).addTo(map)
        .bindPopup('EV Charging Station')
        .openPopup();
}

// Call the initMap function when the page loads
document.addEventListener('DOMContentLoaded', initMap);

// Function to alert the user when the button is clicked
document.getElementById('find-stations').addEventListener('click', function() {
    alert('Finding nearby charging stations...');
});