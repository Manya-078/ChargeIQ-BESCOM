ChargeIQ: AI-Powered EV Grid Management
A Decision-Support Layer for BESCOM (Theme 9)

🔍 Project Overview
ChargeIQ is a dual-AI system designed to optimize Electric Vehicle (EV) charging infrastructure and grid load management for Bengaluru. It operates as a non-intrusive decision-support layer, requiring zero modifications to existing distribution systems.

🚀 Key Features
Part A: Demand Prediction & Smart Scheduling

Predicts EV charging demand using spatiotemporal modeling.

Implements Anti-Herding logic to distribute charging sessions.

Reduces peak load stress by shifting charging to off-peak windows via Time-of-Use (ToU) recommendations.

Part B: Infrastructure Planning

Identifies high-priority zones for new charging stations.

Uses Explainable AI (XAI) to provide "Evidence Cards" for grid planners.

Ranks locations based on grid headroom, EV density, and accessibility.

🛠️ Tech Stack
Frontend: Streamlit (Custom Dark Theme)

Analytics: Python, Pandas, NumPy

Visualization: Pydeck (Geospatial Heatmaps), Plotly (Load Profiles)

Data Strategy: Masked/Synthetic BESCOM grid data for privacy compliance.

**📦 Installation**
git clone https://github.com/Manya-078/ChargeIQ-BESCOM.git

pip install -r requirements.txt

python src/generate_data.py

streamlit run app.py
