import pandas as pd
import numpy as np

def calculate_stope_statistics(df):
    """Calculate comprehensive stope statistics"""
    stats = {
        'mean_width': df['stope_width'].mean(),
        'std_width': df['stope_width'].std(),
        'min_width': df['stope_width'].min(),
        'max_width': df['stope_width'].max(),
        'width_variation': df['stope_width'].std() / df['stope_width'].mean() * 100
    }
    return stats

def calculate_equipment_efficiency(df):
    """Calculate equipment efficiency metrics"""
    efficiency_metrics = {
        'avg_utilization': df['utilization_rate'].mean(),
        'avg_downtime': df['downtime_hours'].mean(),
        'avg_maintenance': df['maintenance_hours'].mean(),
        'total_operating_hours': df['hours_operated'].sum()
    }
    return efficiency_metrics

def calculate_blast_efficiency(df):
    """Calculate blast efficiency metrics"""
    efficiency_metrics = {
        'avg_fragmentation': df['fragmentation_size'].mean(),
        'avg_explosives': df['explosives_used'].mean(),
        'avg_vibration': df['vibration_level'].mean(),
        'blast_frequency': len(df) / (df['date'].max() - df['date'].min()).days
    }
    return efficiency_metrics
