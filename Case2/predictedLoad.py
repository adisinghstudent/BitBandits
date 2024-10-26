import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameters to reflect an average annual consumption of 20,211 kWh
E_avg_realistic = 20211 / (365 * 24)  # Average hourly consumption in kWh based on 20,211 kWh/year
a = 0.3  # Amplitude for daily consumption variation
b = 0.2  # Amplitude for morning/evening peaks
c = 1.5  # Peak multiplier for specific high-demand hours
sigma = 0.1  # Standard deviation of noise

# Seasonal multipliers for each month (index 1=January, ..., 12=December)
seasonal_multipliers = {
    1: 1.4, 2: 1.4,  # Winter: Higher heating needs
    3: 1.1, 4: 1.1, 5: 1.1,  # Spring: Moderate heating needs
    6: 0.8, 7: 0.8, 8: 0.8,  # Summer: Minimal heating
    9: 1.2, 10: 1.2, 11: 1.2,  # Autumn: Increasing heating needs
    12: 1.4  # December: High heating needs
}

# Define weekday and weekend peak hours
weekday_morning_peak = range(6, 9)  # Morning: 6am - 9am
weekday_evening_peak = range(17, 21)  # Evening: 5pm - 9pm
weekend_morning_peak = range(9, 12)  # Morning: 9am - 12pm on weekends
weekend_evening_peak = range(18, 22)  # Evening: 6pm - 10pm on weekends

# Define weekend check
def is_weekend(day_of_week):
    return day_of_week in [5, 6]  # Saturday and Sunday as weekend

# Adjusted energy consumption function with weekend and seasonal multipliers
def energy_consumption_weekend_shifted(t, start_date):
    # Determine the day of the week and month
    day_of_week = (t // 24) % 7
    month = (start_date + pd.Timedelta(hours=t)).month
    
    # Base daily cycle
    daily_variation = a * np.sin(2 * np.pi * t / 24)
    peak_variation = b * np.sin(4 * np.pi * t / 24)
    
    # Apply weekend peak shifts and overall higher multiplier
    if is_weekend(day_of_week):
        weekend_multiplier = 1.2  # Higher overall usage on weekends
        if t % 24 in weekend_morning_peak or t % 24 in weekend_evening_peak:
            peak_multiplier = c
        else:
            peak_multiplier = 1
    else:
        weekend_multiplier = 1  # Regular weekday
        peak_multiplier = c if (t % 24 in weekday_morning_peak or t % 24 in weekday_evening_peak) else 1

    # Apply seasonal multiplier
    seasonal_multiplier = seasonal_multipliers.get(month, 1)  # Default to 1 if month is somehow invalid

    # Add random noise
    noise = np.random.normal(0, sigma)
    
    # Calculate energy consumption for hour t
    return E_avg_realistic * seasonal_multiplier * weekend_multiplier * (1 + daily_variation + peak_variation) * peak_multiplier + noise

# Simulate data for one month (30 days * 24 hours)
hours_in_month = 30 * 24
start_date = pd.Timestamp("2024-11-01")  # Example start date in November
time_index_random_month = pd.date_range(start=start_date, periods=hours_in_month, freq="H")
simulated_consumption_weekend_shifted = [energy_consumption_weekend_shifted(t, start_date) for t in range(hours_in_month)]

# Plotting the seasonally adjusted consumption with shifted weekend peaks
plt.figure(figsize=(12, 6))
plt.plot(time_index_random_month, simulated_consumption_weekend_shifted, label="Weekend-Adjusted Energy Consumption")
plt.xlabel("Time")
plt.ylabel("Energy Consumption (kWh)")
plt.title("Household Energy Consumption with Weekend Adjustments and Seasonal Multipliers Over a Month")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Calculate the total consumption for this month to check seasonal and weekend adjustments
monthly_total_consumption = sum(simulated_consumption_weekend_shifted)
print(f"Monthly Total Consumption: {monthly_total_consumption:.2f} kWh")
