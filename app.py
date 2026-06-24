import streamlit as st
import json
import os
import time

DB_FILE = "queue_data.json"

# Initialize file state with adaptive threshold tracking
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({
            "current_token": 0, 
            "average_time": 10.0,      
            "patients": [], 
            "last_call_time": None, 
            "history": [],
            "is_automated": False     
        }, f)

def load_data():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

st.set_page_config(page_title="Clinic Queue", layout="wide")

# Sidebar navigation
st.sidebar.title("🎮 Navigation")
screen = st.sidebar.radio("Go to Screen:", ["Screen 1: Receptionist Control", "Screen 2: Patient Waiting Room"])

# SCREEN 1: RECEPTIONIST
if screen == "Screen 1: Receptionist Control":
    st.title("📋 Receptionist Control Panel")
    data = load_data()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Add New Patient")
        patient_name = st.text_input("Patient Name", key="name_input").strip()
        
        if st.button("Add to Queue", use_container_width=True, disabled=not patient_name):
            next_token = data["patients"][-1]["token"] + 1 if data["patients"] else data["current_token"] + 1
            data["patients"].append({"token": next_token, "name": patient_name})
            save_data(data)
            st.toast(f"Added {patient_name} (Token #{next_token})", icon="✅")
            st.rerun()
                
        st.write("---")
        st.subheader("Timing Configuration")
        
        if not data["is_automated"]:
            avg_time = st.number_input("Set Initial Consultation Time (mins)", min_value=1, max_value=60, value=int(data["average_time"]))
            if avg_time != data["average_time"]:
                data["average_time"] = float(avg_time)
                save_data(data)
                st.rerun()
            st.info("ℹ️ Manual Mode: Adjusting estimates based on morning crowd density.")
        else:
            st.metric(label="📊 Live Automated Average", value=f"{round(data['average_time'], 1)} mins")
            st.success("⚡ Telemetry Active: Tracking real-time rolling patient averages.")

        st.write("---")
        st.subheader("Danger Zone")
        if st.button("🚨 Clear All & Reset Tokens", type="secondary", use_container_width=True):
            save_data({"current_token": 0, "average_time": 10.0, "patients": [], "last_call_time": None, "history": [], "is_automated": False})
            st.toast("Queue cleared and history reset!", icon="🔄")
            st.rerun()

    with col2:
        st.subheader("Queue Controls")
        queue_is_empty = len(data["patients"]) == 0
        
        if st.button("🔔 CALL NEXT PATIENT", type="primary", use_container_width=True, disabled=queue_is_empty):
            current_timestamp = time.time()
            
            if data["last_call_time"] is not None:
                duration_seconds = current_timestamp - data["last_call_time"]
                duration_minutes = duration_seconds / 60
                
                # Simulation fallback for video recording (seconds count as minutes)
                if duration_minutes < 1:
                    duration_minutes = duration_seconds

                data["history"].append(duration_minutes)
                
                if len(data["history"]) > 3:
                    data["history"].pop(0)
                
                if len(data["history"]) >= 3:
                    data["average_time"] = sum(data["history"]) / len(data["history"])
                    data["is_automated"] = True

            next_patient = data["patients"].pop(0)
            data["current_token"] = next_patient["token"]
            data["last_call_time"] = current_timestamp
            
            save_data(data)
            st.balloons()
            st.rerun()
            
        if queue_is_empty:
            st.caption("⚠️ No patients currently waiting in line.")
                
        st.markdown(f"### Inside with Doctor: <span style='color:#F38BA8; font-size:24px;'><b>Token #{data['current_token']}</b></span>", unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("Active Lineup")
        if data["patients"]:
            for p in data["patients"]:
                st.write(f"• **Token #{p['token']}** — {p['name']}")
        else:
            st.write("_No upcoming appointments_")

# SCREEN 2: PATIENT WAITING ROOM 
else:
    st.title("📺 Patient Waiting Room Display")
    
    @st.fragment(run_every="1s")
    def render_waiting_room():
        data = load_data()
        
        st.markdown(
            f"""
            <div style="background-color:#1E1E2E; padding:30px; border-radius:15px; text-align:center; border: 2px solid #2A2A3E; margin-bottom: 25px;">
                <h2 style="color:#A6ADC8; margin:0; font-family:sans-serif;">NOW SERVING</h2>
                <h1 style="color:#F38BA8; font-size: 75px; margin:10px 0; font-family:sans-serif;">TOKEN #{data['current_token']}</h1>
                <p style="color:#A6ADC8; margin:0; font-family:sans-serif;">{"✨ Dynamic tracking enabled" if data['is_automated'] else "📋 Using scheduled baseline estimates"}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.write("## ⏳ Upcoming Tokens & Dynamic Wait Times")
        if data["patients"]:
            cols = st.columns(3)
            for idx, p in enumerate(data["patients"]):
                col_to_use = cols[idx % 3]
                computed_wait = (idx + 1) * data["average_time"]
                
                with col_to_use:
                    st.markdown(
                        f"""
                        <div style="background-color:#313244; padding:15px; border-radius:10px; margin-bottom:15px; border-left: 5px solid #89B4FA;">
                            <h3 style="color:#89B4FA; margin:0; font-family:sans-serif;">Token #{p['token']}</h3>
                            <p style="color:#CDD6F4; margin:5px 0 0 0; font-family:sans-serif;">Est. Wait: <b>~{round(computed_wait, 1)} mins</b></p>
                            <small style="color:#A6ADC8; font-family:sans-serif;">{idx} people ahead</small>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
        else:
            st.info("The waiting room line is clear!")

    render_waiting_room()