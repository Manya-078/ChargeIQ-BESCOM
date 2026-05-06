import numpy as np

def mask_sensitive_data(df, columns):
    """
    Ensures PII is removed or obfuscated before processing.
    """
    masked_df = df.copy()
    for col in columns:
        if col in masked_df.columns:
            masked_df[col] = masked_df[col].apply(lambda x: f"MASKED_{hash(str(x)) % 10000}")
    return masked_df

def calculate_grid_headroom(capacity, current_load):
    """
    Returns percentage of available power.
    """
    if capacity == 0: return 0
    return ((capacity - current_load) / capacity) * 100