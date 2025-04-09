import streamlit as st
import math

st.set_page_config(page_title="Dump Truck Hauling Bid Calculator", layout="centered")

st.title("🚛 Dump Truck Hauling Bid Calculator")

st.sidebar.header("🔧 Inputs")

# Inputs
total_material = st.sidebar.number_input("Total Material to Haul (CY)", value=3000.0)
truck_capacity = st.sidebar.number_input("Truck Capacity (CY)", value=10.0)
round_trip_time = st.sidebar.number_input("Round Trip Time per Load (hrs)", value=1.25)
work_hours_per_day = st.sidebar.number_input("Work Hours per Day", value=9.0)
days_to_complete = st.sidebar.number_input("Days to Complete", value=5)
one_way_distance = st.sidebar.number_input("One-Way Distance to Dump (miles)", value=12.0)
mpg = st.sidebar.number_input("Truck MPG", value=6.0)
fuel_cost_per_gallon = st.sidebar.number_input("Fuel Cost per Gallon ($)", value=4.5)
driver_hourly_rate = st.sidebar.number_input("Driver Hourly Rate ($/hr)", value=32.0)
truck_lease = st.sidebar.number_input("Truck Lease per Day ($)", value=250.0)
insurance = st.sidebar.number_input("Insurance per Day ($)", value=50.0)
permits = st.sidebar.number_input("Permit Cost per Day ($)", value=10.0)
maintenance_per_mile = st.sidebar.number_input("Maintenance Cost per Mile ($)", value=0.25)
overhead_pct = st.sidebar.number_input("Overhead %", value=10.0) / 100
profit_margin_pct = st.sidebar.number_input("Profit Margin %", value=20.0) / 100

# Calculations
round_trip_miles = one_way_distance * 2
total_loads = total_material / truck_capacity
loads_per_truck_per_day = work_hours_per_day / round_trip_time
total_loads_per_truck = loads_per_truck_per_day * days_to_complete
trucks_needed = math.ceil(total_loads / total_loads_per_truck)
total_miles = total_loads * round_trip_miles
gallons_used = total_miles / mpg
fuel_cost = gallons_used * fuel_cost_per_gallon
driver_hours = total_loads * round_trip_time
driver_cost = driver_hours * driver_hourly_rate
maintenance_cost = total_miles * maintenance_per_mile
daily_ops_cost = (truck_lease + insurance + permits) * trucks_needed * days_to_complete
total_cost = fuel_cost + driver_cost + maintenance_cost + daily_ops_cost
overhead = total_cost * overhead_pct
profit = (total_cost + overhead) * profit_margin_pct
total_bid = total_cost + overhead + profit
cost_per_load = total_cost / total_loads
price_per_load = total_bid / total_loads
profit_per_load = price_per_load - cost_per_load
break_even_hourly = total_cost / (trucks_needed * work_hours_per_day * days_to_complete)

# Output
st.subheader("📊 Summary")
st.metric("Trucks Needed", trucks_needed)
st.metric("Total Loads", f"{total_loads:.2f}")
st.metric("Total Miles", f"{total_miles:.0f} mi")
st.metric("Fuel Cost", f"${fuel_cost:,.2f}")
st.metric("Driver Cost", f"${driver_cost:,.2f}")
st.metric("Maintenance Cost", f"${maintenance_cost:,.2f}")
st.metric("Daily Ops Cost", f"${daily_ops_cost:,.2f}")
st.metric("Total Cost", f"${total_cost:,.2f}")
st.metric("Overhead", f"${overhead:,.2f}")
st.metric("Profit", f"${profit:,.2f}")
st.metric("Total Bid", f"${total_bid:,.2f}")
st.metric("Cost per Load", f"${cost_per_load:,.2f}")
st.metric("Price per Load", f"${price_per_load:,.2f}")
st.metric("Profit per Load", f"${profit_per_load:,.2f}")
st.metric("Break-Even Hourly Rate", f"${break_even_hourly:,.2f}")
