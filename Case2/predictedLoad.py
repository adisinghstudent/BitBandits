import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameters for realistic household energy consumption
E_avg = 20211 / (365 * 24)  # Average hourly consumption based on 20,211 kWh/year
a = 0.1  # Lower daily cycle amplitude to balance the weekend baseline
sigma = 0.1  # Standard deviation of random noise

# Seasonal multipliers by month (index 1=January, ..., 12=December)
seasonal_multipliers = {
    1: 1.4, 2: 1.4,  # Winter months with higher consumption
    3: 1.2, 4: 1.1, 5: 1.0,  # Spring with moderate consumption
    6: 0.8, 7: 0.75, 8: 0.8,  # Summer with lower consumption
    9: 1.1, 10: 1.2, 11: 1.3,  # Autumn with increasing consumption
    12: 1.4  # December with higher consumption
}

# Define Gaussian peak functions
def gaussian_peak(t, center, width=2, amplitude=1):
    return amplitude * np.exp(-0.5 * ((t % 24 - center) / width) ** 2)

# Seasonal multiplier function based on month
def seasonal_multiplier(t, start_date):
    month = (start_date + pd.Timedelta(hours=t)).month
    return seasonal_multipliers.get(month, 1)

# Function to check if it's a weekend
def is_weekend(day_of_week):
    return day_of_week in [5, 6]  # Saturday and Sunday

# Energy consumption function with day and season adjustments
def energy_consumption_simulation(start_day, num_days):
    hours_in_simulation = num_days * 24
    start_date = pd.Timestamp("2024-11-01") + pd.Timedelta(days=start_day)  # Adjust for start day of the week
    simulated_consumption = []
    
    for t in range(hours_in_simulation):
        day_of_week = (start_day + (t // 24)) % 7  # Determine the day of the week
        
        # Determine if it’s a weekend and set peaks accordingly
        if is_weekend(day_of_week):
            # Weekend: Lower peak intensities, but higher baseline throughout the day
            morning_peak = gaussian_peak(t, center=9, width=4, amplitude=0.8)  # Lower amplitude
            evening_peak = gaussian_peak(t, center=20, width=3, amplitude=0.8)  # Lower amplitude
            baseline_multiplier = 1.2  # Higher baseline consumption for weekends
        else:
            # Weekday: Higher peak intensities for morning and evening
            morning_peak = gaussian_peak(t, center=7, width=2, amplitude=1.2)  # Higher amplitude
            evening_peak = gaussian_peak(t, center=18, width=3, amplitude=1.2)  # Higher amplitude
            baseline_multiplier = 1  # Regular baseline for weekdays

        # Base daily cycle with seasonal multiplier and random noise
        daily_cycle = a * np.sin(2 * np.pi * t / 24)  # Day/night cycle
        seasonal_mult = seasonal_multiplier(t, start_date)
        noise = np.random.normal(0, sigma)  # Random noise

        # Final energy consumption calculation
        energy_use = E_avg * (1 + daily_cycle + morning_peak + evening_peak) * seasonal_mult * baseline_multiplier + noise
        simulated_consumption.append(energy_use)
    
    # Create a time index for the simulation
    time_index = pd.date_range(start=start_date, periods=hours_in_simulation, freq="H")
    return pd.DataFrame({"Timestamp": time_index, "Energy_Consumption_kWh": simulated_consumption})

# Example usage
start_day = 0  # E.g., start on a Wednesday
num_days = 7  # Simulate one week
energy_data = energy_consumption_simulation(start_day, num_days)

# Plotting the simulated consumption
plt.figure(figsize=(14, 6))
plt.plot(energy_data["Timestamp"], energy_data["Energy_Consumption_kWh"], label="Simulated Energy Consumption")
plt.xlabel("Time")
plt.ylabel("Energy Consumption (kWh)")
plt.title("Simulated Household Energy Consumption with Lower Weekend Peaks and Higher Baseline")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Calculate total consumption for the simulation period
total_consumption = energy_data["Energy_Consumption_kWh"].sum()
print(f"Total Consumption for {num_days} Days: {total_consumption:.2f} kWh")
