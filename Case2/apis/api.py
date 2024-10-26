import requests
import matplotlib.pyplot as plt
from datetime import datetime

hours_simulate = 24

def get_open_meteo_solar_data(lat, lon):
    # Fetch solar radiation data from Open-Meteo API
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "shortwave_radiation",
        "hourly": "direct_radiation",
        "timezone": "Europe/Oslo"
    }
    response = requests.get(url, params=params)
    data = response.json()
    

    #solar_radiation = data.get("hourly", {}).get("shortwave_radiation", [0] * hours_simulate)
    solar_radiation = data.get("hourly", {}).get("direct_radiation", [0] * hours_simulate)
    return solar_radiation[:hours_simulate]

def get_met_weather_forecast(lat, lon):
    # MET Norway API request for cloud cover data only
    url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
    params = {
        "lat": lat,      
        "lon": lon       
    }
    headers = {
        "User-Agent": "Your-Application-Name"
    }
    
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    
    # Extract hourly cloud cover for the next 24 hours
    cloud_cover = [
        time_step["data"]["instant"]["details"]["cloud_area_fraction"]
        for time_step in data["properties"]["timeseries"][:hours_simulate]
    ]
    
    return cloud_cover[:hours_simulate]  # Slice to ensure only 24 hours

def predict_pv_production(solar_radiation, cloud_cover):
    max_radiation = 1000  # Peak solar radiation for max PV output (W/m²)
    production = [
        max(0, (radiation / max_radiation) * (1 - cover / 200))
        for radiation, cover in zip(solar_radiation, cloud_cover)
    ]
    print(production)
    return production

def visualize_daily_graph(lat, lon):
    # Fetch weather data
    solar_radiation = get_open_meteo_solar_data(lat, lon)
    cloud_cover = get_met_weather_forecast(lat, lon)
    predicted_pv_production = predict_pv_production(solar_radiation, cloud_cover)

    
    # Ensure data is limited to 24 hours for each variable
    hours = range(hours_simulate)
    print(len(cloud_cover))
    plt.figure(figsize=(12, 6))
    plt.plot(hours, solar_radiation, label="Solar Radiation (W/m²)", color="orange", marker="o")
    plt.plot(hours, cloud_cover, label="Cloud Cover (%)", color="blue", linestyle="--", marker="s")
    plt.plot(hours, predicted_pv_production, label="Predicted PV Production (normalized)", color="green", marker="^")

    # Configure plot aesthetics
    plt.title(f"Solar Radiation, Cloud Cover, and PV Production - {datetime.now().strftime('%Y-%m-%d')}")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    plt.xticks(hours)  # Show each hour on the x-axis
    plt.tight_layout()
    
    # Save the plot with date as part of the filename
    plt.savefig(f"pv_production_{datetime.now().strftime('%Y-%m-%d')}.png")
    plt.show()

def main():
    # Coordinates for Trondheim
    lat, lon = 63.4305, 10.3951
    #52.5200, 13.4050

    # Visualize and save the daily plot
    visualize_daily_graph(lat, lon)
    

main()
