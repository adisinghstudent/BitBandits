// Import necessary modules
const fetch = require('node-fetch'); // For Node.js environment

// Function to get solar radiation data from Open-Meteo API
async function getOpenMeteoSolarData(lat, lon) {
    // Fetch solar radiation data
    const url = 'https://api.open-meteo.com/v1/forecast';
    const params = new URLSearchParams({
        latitude: lat,
        longitude: lon,
        hourly: 'shortwave_radiation',
        timezone: 'Europe/Oslo'
    });

    const response = await fetch(`${url}?${params.toString()}`);
    const data = await response.json();

    // Extract hourly solar radiation for the next 24 hours
    const solarRadiation = data.hourly && data.hourly.shortwave_radiation
        ? data.hourly.shortwave_radiation.slice(0, 24)
        : Array(24).fill(0);

    return solarRadiation;
}

// Function to get cloud cover data from MET Norway API
async function getMetWeatherForecast(lat, lon) {
    // MET Norway API request for cloud cover data
    const url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact';
    const params = new URLSearchParams({
        lat: lat,  
        lon: lon   
    });

    const headers = {
        'User-Agent': 'BitBandits' 
    };

    const response = await fetch(`${url}?${params.toString()}`, { headers });
    const data = await response.json();

    // Extract hourly cloud cover for the next 24 hours
    const cloudCover = data.properties.timeseries.slice(0, 24).map(timeStep => {
        return timeStep.data.instant.details.cloud_area_fraction;
    });

    return cloudCover;
}

// Function to predict PV production based on solar radiation and cloud cover
function predictPvProduction(solarRadiation, cloudCover) {
    const maxRadiation = 1000; // Peak solar radiation for max PV output (W/m²)
    const production = solarRadiation.map((radiation, index) => {
        const cover = cloudCover[index] || 0;
        return Math.max(0, (radiation / maxRadiation) * (1 - cover / 100));
    });
    return production;
}

// Main function to execute the script
async function test() {
    // Coordinates for Trondheim
    const lat = 63.4305;
    const lon = 10.3951;

    // Get weather data
    const [cloudCover, solarRadiation] = await Promise.all([
        getMetWeatherForecast(lat, lon),
        getOpenMeteoSolarData(lat, lon)
    ]);

    // Display results
    console.log("Hourly Cloud Cover (%) and Estimated Solar Radiation (W/m²):");
    for (let hour = 0; hour < 24; hour++) {
        const cc = cloudCover[hour] || 0;
        const rad = solarRadiation[hour] || 0;
        console.log(`Hour ${hour}: Cloud Cover = ${cc}%, Estimated Solar Radiation = ${rad.toFixed(2)} W/m²`);
    }

    // Predict PV production based on solar radiation and cloud cover
    const predictedPvProduction = predictPvProduction(solarRadiation, cloudCover);

    // Display the results
    console.log("Predicted PV Production:", predictedPvProduction);
}

// Execute the main function
test().catch(error => console.error('Error:', error));
//test
