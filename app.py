import streamlit as st
import json
import os
from datetime import datetime
import math

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Parking Allocation", layout="wide")

DATA_FILE = "parking_data.json"
TOTAL_FLOORS = 3
SPOTS_PER_FLOOR = 10

def initialize_parking_lot():
    parking_lot = {}
    for floor in range(1, TOTAL_FLOORS + 1):
        parking_lot[f"Floor {floor}"] = {}
        for spot_num in range(1, SPOTS_PER_FLOOR + 1):
            spot_id = f"F{floor}-S{spot_num}"
            if spot_num <= 2:
                spot_type = "EV"
            elif spot_num == 3:
                spot_type = "Compact"
            else:
                spot_type = "Regular"
            
            parking_lot[f"Floor {floor}"][spot_id] = {
                "spot_type": spot_type,
                "is_occupied": False,
                "vehicle_no": None,
                "vehicle_type": None,
                "entry_time": None
            }
    return parking_lot

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        except:
            return initialize_parking_lot()
    return initialize_parking_lot()

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def find_optimal_spot(parking_lot, vehicle_type):
    target_spot_type = "Regular"
    if vehicle_type == "EV":
        target_spot_type = "EV"
    elif vehicle_type == "Compact (Bike/Hatchback)":
        target_spot_type = "Compact"

    for floor in sorted(parking_lot.keys()):
        for spot_id, details in parking_lot[floor].items():
            if not details["is_occupied"] and details["spot_type"] == target_spot_type:
                return floor, spot_id

    if target_spot_type in ["EV", "Compact"]:
        for floor in sorted(parking_lot.keys()):
            for spot_id, details in parking_lot[floor].items():
                if not details["is_occupied"] and details["spot_type"] == "Regular":
                    return floor, spot_id
    return None, None

# --- MAIN APPLICATION LOGIC ---
st.title("🚗 Smart Parking Allocation System")
st.markdown("An automated priority-based vehicle spot allocation engine.")
st.write("---")

# Load real-time database state
parking_lot = load_data()

# Layout Gateways Side-by-Side
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Entry Gateway (Check-In)")
    with st.form("entry_form", clear_on_submit=True):
        vehicle_no = st.text_input("Vehicle Registration Number", placeholder="e.g., TS09EA1234").strip().upper()
        vehicle_type = st.selectbox("Vehicle Category Profile", ["Regular (Sedan/SUV)", "Compact (Bike/Hatchback)", "EV"])
        submit_park = st.form_submit_button("Allocate Spot & Issue Ticket")
        
        if submit_park:
            if not vehicle_no:
                st.error("Vehicle number cannot be blank!")
            else:
                already_exists = False
                for f in parking_lot:
                    for spot in parking_lot[f].values():
                        if spot["is_occupied"] and spot["vehicle_no"] == vehicle_no:
                            already_exists = True
                            break
                
                if already_exists:
                    st.error(f"Vehicle {vehicle_no} is already inside the parking lot!")
                else:
                    floor, spot_id = find_optimal_spot(parking_lot, vehicle_type)
                    if spot_id:
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        parking_lot[floor][spot_id].update({
                            "is_occupied": True,
                            "vehicle_no": vehicle_no,
                            "vehicle_type": vehicle_type.upper(),
                            "entry_time": now
                        })
                        save_data(parking_lot)
                        st.success(f"🎟️ Ticket Issued! Assigned: {floor} -> **{spot_id}**")
                    else:
                        st.error("No suitable slots available right now.")

with col2:
    st.subheader("2. Exit Gateway (Check-Out)")
    
    # Clean Dialog Modal Popup Window Function
    @st.dialog("🔔 Check-Out Confirmed")
    def show_receipt_popup(vehicle, spot, hours, fare):
        st.write(f"The checkout process for vehicle **{vehicle}** has completed successfully.")
        st.write("---")
        st.success(f"Released Spot: **{spot}**")
        st.info(f"🕒 Total Parking Time: **{hours} hour(s)**")
        st.metric(label="Total Bill Paid", value=f"₹{fare}")
        if st.button("Close Window", use_container_width=True):
            st.rerun()

    with st.form("exit_form", clear_on_submit=True):
        exit_vehicle_no = st.text_input("Vehicle Registration Number", placeholder="e.g., TS09EA1234").strip().upper()
        submit_unpark = st.form_submit_button("Process Payment & Leave")
        
        if submit_unpark:
            if not exit_vehicle_no:
                st.error("Please enter a vehicle number.")
            else:
                found = False
                for floor in parking_lot:
                    for spot_id, details in parking_lot[floor].items():
                        if details["is_occupied"] and details["vehicle_no"] == exit_vehicle_no:
                            entry_dt = datetime.strptime(details["entry_time"], "%Y-%m-%d %H:%M:%S")
                            duration = datetime.now() - entry_dt
                            duration_hours = max(1, math.ceil(duration.total_seconds() / 3600))
                            
                            rate = 50 if details["spot_type"] == "EV" else 30
                            total_fare = duration_hours * rate
                            
                            # Reset parking slot fields
                            details.update({
                                "is_occupied": False,
                                "vehicle_no": None,
                                "vehicle_type": None,
                                "entry_time": None
                            })
                            save_data(parking_lot)
                            
                            # Fire off the interactive layout dialogue container
                            show_receipt_popup(exit_vehicle_no, spot_id, duration_hours, total_fare)
                            found = True
                            break
                if not found:
                    st.error(f"Vehicle '{exit_vehicle_no}' not found in the lot system.")

st.write("---")
st.subheader("📊 Real-Time Parking Lot Map Matrix")

for floor in sorted(parking_lot.keys()):
    st.markdown(f"#### 🏢 {floor}")
    spots = parking_lot[floor]
    
    cols = st.columns(10)
    for index, (spot_id, details) in enumerate(spots.items()):
        with cols[index]:
            if details["is_occupied"]:
                st.error(f"**{spot_id}**\n\n🔴 {details['vehicle_no']}\n\n`{details['spot_type']}`")
            else:
                st.success(f"**{spot_id}**\n\n🟢 Available\n\n`{details['spot_type']}`")