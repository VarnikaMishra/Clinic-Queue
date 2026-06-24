# Clinic Queue (Queue Cure '26) 🩺

An instant-sync, zero-hardware digital queue management assistant engineered to eliminate paper token slips, shouting, and informational asymmetry across local medical clinics. Built entirely using Python and Streamlit, this dual-screen dashboard leverages an adaptive, time-series telemetry machine to compute precise, data-driven patient wait times automatically.

## 🚀 Core Architectural Features

### 📋 Screen 1: Receptionist Control Panel
- **Instant Triage Input:** Administrative check-in workflow that validates patient data and increments sequential tokens in under 2 seconds.
- **Underflow Safeguards:** Structural UI constraints completely disable queue advancement actions if the line is empty, preventing backend runtime `IndexError` exceptions.
- **Hybrid Configuration Engine:** Intelligently handles early morning data scarcity before seamlessly handing off orchestration to autonomous monitoring metrics.
- **Atomic Structural Purge:** End-of-day state clearance valves that clean temporary operational records and reset token variables cleanly.

### 📺 Screen 2: Patient Waiting Room Display
- **High-Visibility Status Board:** Replaces ambient waiting room shouting with a centralized panel displaying the active token currently with the physician.
- **Reactive Fragment Polling:** Re-renders line status dynamically via localized backend loops running on a 1,000ms heartbeat, bypassing full-browser refreshes entirely.
- **Predictive Timeline Matrix:** Organizes upcoming tokens into intuitive layout columns showing the absolute positional queue index and remaining time forecasts.

---

## 🛠️ Local Installation & Setup

1. **Clone the project repository:**
   ```bash
   git clone [https://github.com/yourusername/clinic-queue.git](https://github.com/yourusername/clinic-queue.git)
   cd clinic-queue
   ```
   
2. **Configure your Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt --prefer-binary
   ```
   
2. **Boot up the Application:**
   ```bash
   streamlit run app.py
   ```

## 📐 The Math Behind the Telemetry Engine
To prevent operational distrust and client confusion, upcoming position cards do not output stagnant, hardcoded timeline assumptions. The system maps expectations using a time-series rolling vector:
  ```bash
  Estimated Wait Time = (Patients Ahead + 1) × Average Consultation Time
  ```
By appending a +1 factor to the position loop index, the algorithm systematically builds in a realistic session buffer, recognizing that upcoming entries must wait for the active consultation inside the checkup room to conclude.

## 🌅 Resolving the Cold-Start Problem (The Hybrid Lifecycle)
**Tokens 0–3 (Initial Seed Phase):** The system relies on a manual receptionist-controlled input baseline to initialize early morning operations based on initial patient density.

**Token 4+ (Autonomous Telemetry Phase):** The exact moment the receptionist calls the 4th patient, the system calculates the exact difference in timestamps between the completion of preceding visits. It locks human entry inputs and dynamically delegates forecasting metrics to a 3-point rolling moving average engine.

## 🗺️ System Synchronization Flow
[ SCREEN 1: RECEPTIONIST VIEW ]
               │
               ▼ (Action: Adds Patient / Clicks "Call Next")
    ┌─────────────────────────┐
    │  Streamlit App Engine   │
    └─────────────────────────┘
               │
               ▼ (Atomic OS-Level Overwrite)
    ┌─────────────────────────┐
    │    queue_data.json      │ ◀─── Single Source of Truth
    └─────────────────────────┘
               │
               ▲ (Isolated Event Re-rendering)
               │
    ┌─────────────────────────┐
    │ @st.fragment Loop (1s)  │
    └─────────────────────────┘
               │
               ▼
  [ SCREEN 2: PATIENT VIEW ] ──▶ (UI Updates Live Without Full Page Refresh)

  Thank you !
  If you want to know more and want to understand the project by a demo video then do check this out:
  https://youtu.be/thHSbHRe-Kk?si=IlnlHv5kGnBSUpXK
