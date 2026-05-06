import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def predict_demand(zone_data):
    """
    Simulates a Demand Prediction (replacing a heavy GNN/Transformer for prototype).
    Predicts kW load based on historical trends + 20% random growth.
    """
    base_load = zone_data['historical_avg']
    time_factor = np.sin(np.linspace(0, 2 * np.pi, 24)) # Mocking diurnal cycle
    prediction = base_load * (1 + 0.2 * time_factor)
    return prediction

def get_optimal_schedule(arrival_time, energy_needed, grid_headroom):
    """
    Logic: If arrival is during Peak (6PM-10PM), delay to 11PM (Off-Peak).
    Includes Anti-Herding: Adds a random jitter of 0-30 mins so not everyone starts at once.
    """
    peak_start, peak_end = 18, 22
    arrival_hour = arrival_time.hour
    
    if peak_start <= arrival_hour <= peak_end:
        # Shift to Off-Peak
        optimized_start = datetime.combine(arrival_time.date(), datetime.min.time()) + timedelta(hours=23)
        jitter = timedelta(minutes=np.random.randint(0, 31))
        return optimized_start + jitter, "Delayed to Off-Peak (Grid Save)"
    
    return arrival_time, "Immediate Charging (Off-Peak)"