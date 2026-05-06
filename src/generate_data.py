import pandas as pd
import numpy as np

def create_synthetic_data():
    # 1. Create Transformer Grid Data (The "Where")
    # Coordinates roughly around Indiranagar, Koramangala, Whitefield
    transformers = {
        'id': [f'TX_{i}' for i in range(1, 6)],
        'lat': [12.9784, 12.9345, 12.9698, 12.9279, 12.9958],
        'lon': [77.6408, 77.6101, 77.7500, 77.6833, 77.6964],
        'capacity_kw': [500, 800, 1000, 400, 750],
        'current_load': [420, 310, 890, 150, 600], # Some are stressed (near capacity)
        'ev_growth_rate': [0.15, 0.30, 0.50, 0.10, 0.25]
    }
    df_grid = pd.DataFrame(transformers)
    df_grid.to_csv('data/grid_status.csv', index=False)

    # 2. Create Demand Pattern (The "When")
    # 24 hours of load data
    hours = list(range(24))
    unmanaged_load = [20, 15, 10, 10, 15, 30, 50, 70, 80, 75, 70, 65, 60, 65, 70, 85, 110, 150, 190, 200, 180, 140, 80, 40]
    
    # AI Optimized load shifts the 18:00-22:00 peak to 23:00-04:00
    managed_load = [40, 45, 45, 40, 35, 30, 50, 70, 80, 75, 70, 65, 60, 65, 70, 80, 85, 90, 95, 100, 100, 100, 80, 60]
    
    df_demand = pd.DataFrame({
        'hour': hours,
        'unmanaged': unmanaged_load,
        'chargeiq_managed': managed_load
    })
    df_demand.to_csv('data/demand_trends.csv', index=False)
    print("✅ Synthetic BESCOM data generated in /data folder!")

if __name__ == "__main__":
    import os
    if not os.path.exists('data'): os.makedirs('data')
    create_synthetic_data()