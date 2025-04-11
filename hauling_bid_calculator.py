import streamlit as st
import math
import streamlit.components.v1 as components

st.set_page_config(page_title="Dump Truck Hauling Bid Calculator", layout="centered")
st.title("🚛 Dump Truck Hauling Bid Calculator")

# --- Material Density Data ---
material_densities = {
    "Dirt (dry)": 1.1,
    "Dirt (wet)": 1.3,
    "Sand": 1.4,
    "Gravel": 1.5,
    "Crushed Stone": 1.6,
    "Topsoil": 1.2,
    "Asphalt": 1.45,
    "Clay (wet)": 1.7,
    "Clay (dry)": 1.3,
    "Recycled Concrete": 1.4,
    "Limestone": 1.55,
}

# --- Job Type Selector ---
job_type = st.selectbox("What type of job are you bidding?", ["By the Load", "Hourly"])

# === LOAD-BASED CALCULATOR ===
if job_type == "By the Load":
    st.sidebar.header("🔧 Inputs for Load-Based Job")

    material_type = st.sidebar.selectbox("Material Type", list(material_densities.keys()))
    material_density = material_densities[material_type]

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

    round_trip_miles = one_way_distance * 2
    total_loads = total_material / truck_capacity
    loads_per_truck_per_day = work_hours_per_day / round_trip_time
    total_loads_per_truck = loads_per_truck_per_day * days_to_complete
    trucks_needed = math.ceil(total_loads / total_loads_per_truck)
    total_miles = total_loads * round_trip_miles
    gallons_used = total_miles / mpg
    fuel_cost = gallons_used * fuel_cost_per_gallon
    driver_hours = work_hours_per_day * days_to_complete * trucks_needed
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
    total_tons = total_material * material_density

    st.subheader("📊 Bid Summary (Per Load)")
    st.metric("Material", material_type)
    st.metric("Material Density", f"{material_density} T/CY")
    st.metric("Total Tons", f"{total_tons:.0f} tons")
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

# === HOURLY CALCULATOR ===
elif job_type == "Hourly":
    st.sidebar.header("🔧 Inputs for Hourly Job")

    hourly_trucks = st.sidebar.number_input("Number of Trucks", value=3)
    hourly_hours_per_day = st.sidebar.number_input("Hours per Day", value=8)
    hourly_days = st.sidebar.number_input("Number of Days", value=5)
    hourly_driver_hourly_rate = st.sidebar.number_input("Driver Hourly Rate ($/hr)", value=32.0)
    truck_hourly_cost = st.sidebar.number_input("Truck Operating Cost per Hour ($)", value=60.0)
    fuel_cost_per_hour = st.sidebar.number_input("Fuel Cost per Hour ($)", value=15.0)
    hourly_overhead_pct = st.sidebar.number_input("Overhead %", value=10.0) / 100
    hourly_profit_margin_pct = st.sidebar.number_input("Profit Margin %", value=20.0) / 100

    total_hours = hourly_trucks * hourly_hours_per_day * hourly_days
    driver_cost = total_hours * hourly_driver_hourly_rate
    truck_cost = total_hours * truck_hourly_cost
    fuel_cost = total_hours * fuel_cost_per_hour
    base_cost = driver_cost + truck_cost + fuel_cost
    overhead = base_cost * hourly_overhead_pct
    profit = (base_cost + overhead) * hourly_profit_margin_pct
    total_bid = base_cost + overhead + profit
    final_hourly_rate = total_bid / total_hours

    st.subheader("📊 Hourly Job Bid Summary")
    st.metric("Total Hours", total_hours)
    st.metric("Driver Cost", f"${driver_cost:,.2f}")
    st.metric("Truck Cost", f"${truck_cost:,.2f}")
    st.metric("Fuel Cost", f"${fuel_cost:,.2f}")
    st.metric("Total Cost", f"${base_cost:,.2f}")
    st.metric("Overhead", f"${overhead:,.2f}")
    st.metric("Profit", f"${profit:,.2f}")
    st.metric("Total Bid", f"${total_bid:,.2f}")
    st.metric("Bid Hourly Rate", f"${final_hourly_rate:,.2f}/hr")

# === PRINT TO PDF BUTTON ===
st.markdown("---")
st.subheader("🖨️ Export or Print")

components.html(
    """
    <script>
    function printPDF() {
        window.print();
    }
    </script>
    <button onclick="printPDF()" style="
        background-color:#4CAF50;
        color:white;
        padding:10px 20px;
        border:none;
        border-radius:5px;
        font-size:16px;
        cursor:pointer;
        margin-top:10px;
    ">🖨️ Print or Save as PDF</button>
    """,
    height=100,
)
