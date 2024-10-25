import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Define classes from provided code (Battery and HouseSystem) here or import them
# For brevity, assume that the Battery and HouseSystem classes are already defined

class Battery:
    def __init__(self, capacity):
        self.capacity = capacity
        self.current_charge = 0

    def use_battery(self, amount):
        self.current_charge += amount
        if self.current_charge > self.capacity:
            self.current_charge = self.capacity
        elif self.current_charge < 0:
            self.current_charge = 0
        
# Initialize Streamlit app with wide layout
st.set_page_config(page_title="House Energy System Simulation", layout="wide")

st.title("🏠 House Energy System Simulation")

st.write("""
    This app simulates a house's energy system including solar generation, 
    battery usage, and general electricity consumption. You can visualize 
    how the battery and solar generation work together to optimize energy use.
""")

# User input fields to configure the system
battery_size = st.number_input("Enter the battery size (kWh)", min_value=0.0, step=1.0, value=5000.0)
solar_capacity = st.number_input("Enter the solar panel capacity (kW)", min_value=0.0, step=0.1, value=10.0)
general_consumption = st.number_input("Enter the general electricity consumption (kWh)", min_value=0.0, step=0.1, value=20.0)
controlled_load_consumption = st.number_input("Enter controlled load consumption (kWh)", min_value=0.0, step=0.1, value=5.0)
start_date = st.date_input("Simulation start date", value=datetime(2024, 1, 1))
end_date = st.date_input("Simulation end date", value=datetime(2024, 1, 5))

# Convert date inputs into datetime objects
start_datetime = datetime.combine(start_date, datetime.min.time())
end_datetime = datetime.combine(end_date, datetime.max.time())

# Button to start the simulation
if st.button("Run Simulation"):

    # Dummy data generation for solar and load consumption for visualization purposes
    dates = pd.date_range(start=start_datetime, end=end_datetime, freq="H")
    solar_gen = pd.Series(solar_capacity * (pd.np.random.rand(len(dates)) * 0.5), index=dates)
    gen_consumption = pd.Series(general_consumption * (pd.np.random.rand(len(dates)) * 0.5), index=dates)
    controlled_consumption = pd.Series(controlled_load_consumption * (pd.np.random.rand(len(dates)) * 0.5), index=dates)
    
    # Placeholder for HouseSystem data (Normally we'd create an actual HouseSystem object and run simulation)
    battery_state = []
    battery = Battery(battery_size)

    for solar, load in zip(solar_gen, gen_consumption):
        battery.use_battery(solar - load)  # Using battery logic to simulate solar charging or load draining
        battery_state.append(battery.current_charge)
    
    # Plot the battery charge over time
    st.header("🔋 Battery Charge Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dates, battery_state, label="Battery Charge (kWh)")
    ax.set_xlabel("Date and Time")
    ax.set_ylabel("Battery Charge (kWh)")
    ax.set_title("Battery Charge Over Time")
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig)

    # Display summary of the final state
    st.write(f"### Final Battery Charge: {battery_state[-1]:.2f} kWh")

    st.write("Simulation completed! You can adjust the inputs and run it again.")
