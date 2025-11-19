import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_stope_data():
    """Generate sample stope width data"""
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
    
    data = []
    for date in dates:
        for stope_id in range(1, 6):
            data.append({
                'date': date,
                'stope_id': f'STOPE_{stope_id:02d}',
                'stope_width': np.random.normal(15, 3),
                'rock_density': np.random.normal(2.8, 0.2),
                'depth': np.random.normal(500, 100),
                'zone': np.random.choice(['North', 'South', 'East', 'West'])
            })
    
    return pd.DataFrame(data)

def generate_sample_blast_data():
    """Generate sample blast sequencing data"""
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-06-01', freq='D')
    
    data = []
    for date in dates:
        for blast_id in range(1, 4):
            data.append({
                'date': date,
                'blast_id': f'BLAST_{blast_id:02d}',
                'explosives_used': np.random.normal(500, 100),
                'fragmentation_size': np.random.normal(0.5, 0.1),
                'vibration_level': np.random.normal(8, 2),
                'sequence_number': np.random.randint(1, 10)
            })
    
    return pd.DataFrame(data)

def generate_sample_equipment_data():
    """Generate sample equipment utilization data"""
    np.random.seed(42)
    equipment_types = ['Drill Rig', 'LHD', 'Truck', 'Excavator']
    
    data = []
    for day in range(180):  # 6 months
        date = datetime(2024, 1, 1) + timedelta(days=day)
        for eq_type in equipment_types:
            for eq_id in range(1, 4):
                data.append({
                    'date': date,
                    'equipment_id': f'{eq_type}_{eq_id:02d}',
                    'equipment_type': eq_type,
                    'hours_operated': np.random.normal(16, 4),
                    'maintenance_hours': np.random.normal(2, 0.5),
                    'downtime_hours': np.random.normal(1, 0.3),
                    'fuel_consumption': np.random.normal(50, 10)
                })
    
    df = pd.DataFrame(data)
    df['utilization_rate'] = (df['hours_operated'] / 24) * 100
    return df

def load_sample_data():
    """Load all sample datasets"""
    stope_data = generate_sample_stope_data()
    blast_data = generate_sample_blast_data()
    equipment_data = generate_sample_equipment_data()
    
    return stope_data, blast_data, equipment_data

def get_mine_context():
    return {
        'likely_method': 'Sublevel Open Stoping',
        'likely_commodity': 'Copper', 
        'depth_category': 'Medium-depth Underground',
        'typical_operations': ['El Teniente (Chile)', 'Kidd Creek (Canada)']
    }

def load_real_data():
    """Load data from CSV files if available, otherwise use sample data"""
    import os
    import glob
    
    # Check for CSV files
    csv_files = glob.glob('data/*.csv')
    print(f"Found CSV files: {csv_files}")
    
    stope_data = None
    blast_data = None
    equipment_data = None
    
    # Load stope data
    for csv_file in csv_files:
        try:
            if 'stope' in csv_file.lower():
                print(f"Loading stope data: {csv_file}")
                stope_data = pd.read_csv(csv_file)
                print(f"Successfully loaded stope data with shape: {stope_data.shape}")
                
                # Clean up the data
                if 'Unnamed: 0' in stope_data.columns:
                    stope_data = stope_data.drop(columns=['Unnamed: 0'])
                    print("Removed index column 'Unnamed: 0' from stope data")
                
                if 'date' in stope_data.columns:
                    stope_data['date'] = pd.to_datetime(stope_data['date'])
                    print("Converted stope date column to datetime")
                
                print(f"Cleaned stope data shape: {stope_data.shape}")
                break
                    
        except Exception as e:
            print(f"Error loading stope data {csv_file}: {e}")
    
    # Load equipment data
    for csv_file in csv_files:
        try:
            if 'equipment' in csv_file.lower():
                print(f"Loading equipment data: {csv_file}")
                equipment_data = pd.read_csv(csv_file)
                print(f"Successfully loaded equipment data with shape: {equipment_data.shape}")
                
                # Clean up the data
                if 'Unnamed: 0' in equipment_data.columns:
                    equipment_data = equipment_data.drop(columns=['Unnamed: 0'])
                    print("Removed index column 'Unnamed: 0' from equipment data")
                
                # If no date column exists (summary data), create a dummy date for compatibility
                if 'date' not in equipment_data.columns:
                    equipment_data['date'] = pd.to_datetime('2024-01-01')  # Use a fixed date
                    print("Added dummy date column for equipment summary data")
                else:
                    equipment_data['date'] = pd.to_datetime(equipment_data['date'])
                    
                # Ensure utilization_rate exists, calculate if needed
                if 'utilization_rate' not in equipment_data.columns and 'hours_operated' in equipment_data.columns:
                    equipment_data['utilization_rate'] = (equipment_data['hours_operated'] / 24) * 100
                    print("Calculated utilization_rate from hours_operated")
                    
                print(f"Cleaned equipment data shape: {equipment_data.shape}")
                break
                
        except Exception as e:
            print(f"Error loading equipment data {csv_file}: {e}")
    
    # Load blast data (use sample if no CSV)
    blast_data_loaded = False
    for csv_file in csv_files:
        try:
            if 'blast' in csv_file.lower():
                print(f"Loading blast data: {csv_file}")
                blast_data = pd.read_csv(csv_file)
                print(f"Successfully loaded blast data with shape: {blast_data.shape}")
                
                if 'date' in blast_data.columns:
                    blast_data['date'] = pd.to_datetime(blast_data['date'])
                    print("Converted blast date column to datetime")
                
                blast_data_loaded = True
                break
        except Exception as e:
            print(f"Error loading blast data {csv_file}: {e}")
    
    # Fill in missing data with sample data
    if stope_data is None:
        print("No stope data CSV found, using sample data")
        stope_data = generate_sample_stope_data()
    else:
        print(f"Using real stope data with {len(stope_data)} rows")
    
    if blast_data is None or not blast_data_loaded:
        print("No blast data CSV found, using sample data")
        blast_data = generate_sample_blast_data()
    else:
        print(f"Using real blast data with {len(blast_data)} rows")
    
    if equipment_data is None:
        print("No equipment data CSV found, using sample data")
        equipment_data = generate_sample_equipment_data()
    else:
        print(f"Using real equipment data with {len(equipment_data)} rows")
    
    return stope_data, blast_data, equipment_data
