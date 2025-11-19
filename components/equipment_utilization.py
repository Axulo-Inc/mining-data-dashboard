import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.calculations import calculate_equipment_efficiency

def create_equipment_utilization(equipment_data):
    """Create equipment utilization dashboard"""
    
    st.header("🏗️ Equipment Utilization Analysis")
    
    # Key metrics
    efficiency = calculate_equipment_efficiency(equipment_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Utilization", f"{efficiency['avg_utilization']:.1f}%")
    with col2:
        st.metric("Avg Downtime", f"{efficiency['avg_downtime']:.1f}hrs/day")
    with col3:
        st.metric("Avg Maintenance", f"{efficiency['avg_maintenance']:.1f}hrs/day")
    with col4:
        st.metric("Total Operating Hours", f"{efficiency['total_operating_hours']:.0f}hrs")
    
    # Utilization by equipment type
    st.subheader("Utilization by Equipment Type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        type_utilization = equipment_data.groupby('equipment_type')['utilization_rate'].mean().reset_index()
        fig = px.bar(type_utilization, x='equipment_type', y='utilization_rate',
                    title='Average Utilization by Equipment Type',
                    labels={'utilization_rate': 'Utilization Rate (%)', 
                           'equipment_type': 'Equipment Type'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Time series of utilization
        daily_utilization = equipment_data.groupby(['date', 'equipment_type'])['utilization_rate'].mean().reset_index()
        fig = px.line(daily_utilization, x='date', y='utilization_rate', color='equipment_type',
                     title='Utilization Rate Over Time',
                     labels={'utilization_rate': 'Utilization Rate (%)', 'date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Maintenance and downtime analysis
    st.subheader("Maintenance & Downtime Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        maintenance_data = equipment_data.groupby('equipment_type').agg({
            'maintenance_hours': 'mean',
            'downtime_hours': 'mean'
        }).reset_index()
        
        fig = px.bar(maintenance_data, x='equipment_type', 
                    y=['maintenance_hours', 'downtime_hours'],
                    title='Average Maintenance & Downtime by Equipment Type',
                    labels={'value': 'Hours', 'equipment_type': 'Equipment Type'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Fuel consumption analysis - only if column exists
        if 'fuel_consumption' in equipment_data.columns:
            fuel_data = equipment_data.groupby('equipment_type')['fuel_consumption'].mean().reset_index()
            fig = px.pie(fuel_data, values='fuel_consumption', names='equipment_type',
                        title='Fuel Consumption Distribution by Equipment Type')
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Alternative: Show operating hours distribution instead
            hours_data = equipment_data.groupby('equipment_type')['hours_operated'].mean().reset_index()
            fig = px.pie(hours_data, values='hours_operated', names='equipment_type',
                        title='Operating Hours Distribution by Equipment Type')
            st.plotly_chart(fig, use_container_width=True)
