import requests
from datetime import datetime

def get_open_meteo_solar_data(lat, lon):
    # Fetch solar radiation data from Open-Meteo API
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "shortwave_radiation",
        "timezone": "Europe/Oslo"
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract hourly solar radiation for the next 24 hours
    solar_radiation = data.get("hourly", {}).get("shortwave_radiation", [0] * 24)
    return solar_radiation

def get_met_weather_forecast():
    # MET Norway API request for cloud cover data only
    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
    params = {
        "lat": 63.4305,      # Trondheim latitude
        "lon": 10.3951       # Trondheim longitude
    }
    headers = {
        "User-Agent": "Your-Application-Name"
    }
    
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    
    # Extract hourly cloud cover for the next 24 hours
    cloud_cover = [
        time_step["data"]["instant"]["details"]["cloud_area_fraction"]
        for time_step in data["properties"]["timeseries"][:24]
    ]
    
    return cloud_cover

def predict_pv_production(solar_radiation, cloud_cover):
    max_radiation = 1000  # Peak solar radiation for max PV output (W/m²)
    production = [
        max(0, (radiation / max_radiation) * (1 - cover / 100))
        for radiation, cover in zip(solar_radiation, cloud_cover)
    ]
    return production

def main():
    # Coordinates for Trondheim
    lat, lon = 63.4305, 10.3951
    
    # Get weather data
    cloud_cover = get_met_weather_forecast()
    solar_radiation = get_open_meteo_solar_data(lat, lon)


    # Display results
    print("Hourly Cloud Cover (%) and Estimated Solar Radiation (W/m²):")
    for hour, (cc, rad) in enumerate(zip(cloud_cover, solar_radiation)):
        print(f"Hour {hour}: Cloud Cover = {cc}%, Estimated Solar Radiation = {rad:.2f} W/m²")

    
    # Predict PV production based on solar radiation and cloud cover
    predicted_pv_production = predict_pv_production(solar_radiation, cloud_cover)
    
    # Display the results
    print("Predicted PV Production:", predicted_pv_production)

if __name__ == "__main__":
    main()
