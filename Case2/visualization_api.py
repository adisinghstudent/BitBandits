import matplotlib.pyplot as plt
from datetime import datetime
from apis.api import get_open_meteo_solar_data, get_met_weather_forecast, predict_pv_production
from optimize_battery_schedule import optimize_battery_schedule

# Constants for the simulation
LATITUDE = 63.4305
LONGITUDE = 10.3951
HOURS_SIMULATE = 24 

# Function to visualize all data
def visualize_simulation():
    # Step 1: Get solar radiation and cloud cover data
    solar_radiation = get_open_meteo_solar_data(LATITUDE, LONGITUDE)
    cloud_cover = get_met_weather_forecast(LATITUDE, LONGITUDE)
    
    # Step 2: Predict PV production based on solar radiation and cloud cover
    predicted_pv_production = predict_pv_production(solar_radiation, cloud_cover)
    print(predict_pv_production)
    
    # Example data for the battery optimization
    battery_capacity = 13.5  # kWh
    charge_rate = 2.0  # kW
    initial_soc = 50  # Starting at 50% state of charge
    spot_prices = generate_example_spot_prices(HOURS_SIMULATE)
    predicted_load = generate_example_load_profile(HOURS_SIMULATE)
    
    # Step 3: Run optimization for battery scheduling
    soc, grid_power = optimize_battery_schedule(
        battery_capacity,
        charge_rate,
        spot_prices,
        predicted_load,
        predicted_pv_production,
        initial_soc
    )
    
    # Step 4: Plot data
    plot_results(spot_prices, predicted_load, predicted_pv_production, grid_power, soc)

# Generate example spot prices (can replace with actual spot price data)
def generate_example_spot_prices(hours):
    # Placeholder for spot price data
    return [
        0.10, 0.09, 0.08, 0.08, 0.09, 0.15, 
        0.20, 0.25, 0.22, 0.18, 0.15, 0.12,
        0.11, 0.10, 0.12, 0.14, 0.18, 0.25,
        0.28, 0.22, 0.18, 0.15, 0.12, 0.11
    ] * (hours // 24)

# Generate example load profile (can replace with actual load data)
def generate_example_load_profile(hours):
    return [
        0.8, 0.6, 0.5, 0.4, 0.4, 0.6,
        1.2, 2.0, 2.5, 2.0, 1.8, 1.5,
        1.3, 1.2, 1.4, 1.6, 2.0, 2.8,
        3.0, 2.5, 2.0, 1.5, 1.2, 1.0
    ] * (hours // 24)

# Plot the results
def plot_results(spot_prices, load, pv_production, grid_power, soc):
    hours = list(range(HOURS_SIMULATE))

    fig, axs = plt.subplots(3, 1, figsize=(15, 10), sharex=True)

    # Plot spot prices
    axs[0].plot(hours, spot_prices, 'r-', label='Spot Price ($/kWh)')
    axs[0].set_ylabel('Spot Price ($/kWh)')
    axs[0].legend()
    axs[0].grid(True)

    # Plot load, PV production, and grid power
    axs[1].plot(hours, load, 'b-', label='Load (kW)')
    axs[1].plot(hours, pv_production, 'g-', label='PV Production (kW)')
    axs[1].plot(hours, grid_power, 'r-', label='Grid Power (kW)')
    axs[1].set_ylabel('Power (kW)')
    axs[1].legend()
    axs[1].grid(True)

    # Plot battery state of charge (SOC)
    axs[2].plot(hours, soc, 'b-', label='Battery State of Charge (%)')
    axs[2].set_xlabel('Hour')
    axs[2].set_ylabel('SOC (%)')
    axs[2].set_ylim(0, 100)
    axs[2].legend()
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()

# Run the visualization
if __name__ == "__main__":
    visualize_simulation()
