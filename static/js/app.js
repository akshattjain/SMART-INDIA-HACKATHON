// Basic linking of the API:
// Replace 'YOUR_PUBLIC_ACCESS_TOKEN' with your actual Mapbox public access token
mapboxgl.accessToken = 'pk.eyJ1Ijoic3JpcmFtY2hpbm1heSIsImEiOiJjbG11ZWVhajYwaDN0MmtvY3phNThhcmFkIn0.qMUf1E7BZKxYHmZ14yoMNA';
var map = new mapboxgl.Map({
    container: 'map', // Specify the container ID
    style: 'mapbox://styles/mapbox/streets-v11', // Use a Mapbox style
    center: [76.796929, 10.199910], // Set the initial center coordinates for India (longitude, latitude)
    zoom: 8 // Set the initial zoom level
});


// Displaying the Longitude and Latitude of the marker
// Initialize variables to store latitude and longitude
var latitudeElement = document.getElementById('latitude');
var longitudeElement = document.getElementById('longitude');
var locationElement = document.getElementById('location'); //  At the Location adding step



// Displaying the marker
// Initialize a marker variable
var marker = new mapboxgl.Marker();

// Add a click event listener to the map
map.on('click', function (e) {
    // Get the clicked coordinates
    var latitude = e.lngLat.lat;
    var longitude = e.lngLat.lng;

    // Update the HTML elements with the clicked coordinates
    latitudeElement.textContent = latitude.toFixed(6);
    longitudeElement.textContent = longitude.toFixed(6);


    // At the moment we added the Location 
    // Perform reverse geocoding to get the location name
    fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${longitude},${latitude}.json?access_token=${mapboxgl.accessToken}`)
    .then(response => response.json())
    .then(data => {
        // Get the place name from the response
        var placeName = data.features[0].place_name;
        // Update the HTML element with the location name
        locationElement.textContent = placeName;
    });

    // Set the marker's location to the clicked coordinates
    marker.setLngLat([longitude, latitude])
        .addTo(map);
});

// Add zoom controls to the map
map.addControl(new mapboxgl.NavigationControl());

var searchInput = document.getElementById('search-input');
        var searchResults = document.getElementById('search-results');

        // Add an event listener to the search input for typing
        searchInput.addEventListener('input', function (e) {
            var query = e.target.value;

            // Clear previous search results
            searchResults.innerHTML = '';

            // Perform a search with Mapbox Geocoding API
            fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${query}.json?access_token=${mapboxgl.accessToken}`)
                .then(response => response.json())
                .then(data => {
                    // Display search results as dropdown items
                    data.features.forEach(function (feature) {
                        var searchItem = document.createElement('div');
                        searchItem.className = 'search-item';
                        searchItem.textContent = feature.place_name;
                        searchItem.addEventListener('click', function () {
                            // Set the map's center to the selected location
                            map.setCenter(feature.center);
                            map.setZoom(10); // You can adjust the zoom level as needed

                            // Update latitude and longitude
                            var latitude = feature.center[1];
                            var longitude = feature.center[0];
                            latitudeElement.textContent = latitude.toFixed(6);
                            longitudeElement.textContent = longitude.toFixed(6);

                            // Update location
                            locationElement.textContent = feature.place_name;

                            // Set the marker's location
                            marker.setLngLat([longitude, latitude])
                                .addTo(map);

                            searchInput.value = ''; // Clear the search input
                            searchResults.style.display = 'none'; // Hide the results
                        });
                        searchResults.appendChild(searchItem);
                    });

                    // Show the results dropdown
                    searchResults.style.display = 'block';
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });

        // Close the results dropdown when clicking outside of it
        document.addEventListener('click', function (e) {
            if (e.target !== searchInput && e.target !== searchResults) {
                searchResults.style.display = 'none';
            }
        });