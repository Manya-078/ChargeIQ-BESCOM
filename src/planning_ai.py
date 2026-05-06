import pandas as pd

def rank_candidate_locations(candidate_df):
    """
    Scores locations based on:
    1. EV Density (40%)
    2. Grid Headroom (30%)
    3. Distance to existing chargers (20%)
    4. Accessibility/POIs (10%)
    """
    # Normalize factors 0-1
    candidate_df['score'] = (
        candidate_df['ev_density'] * 0.4 +
        candidate_df['grid_headroom'] * 0.3 +
        (1 / candidate_df['dist_to_nearest']) * 0.2 +
        candidate_df['poi_count'] * 0.1
    )
    
    return candidate_df.sort_values(by='score', ascending=False)