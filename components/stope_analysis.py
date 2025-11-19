import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.calculations import calculate_stope_statistics

def create_stope_analysis(stope_data):
    """Create stope width analysis dashboard"""
    
    st.header("📊 Stope Width Analysis")
    
    # Key metrics
    stats = calculate_stope_statistics(stope_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Width", f"{stats['mean_width']:.2f}m")
    with col2:
        st.metric("Width Variation", f"{stats['width_variation']:.1f}%")
    with col3:
        st.metric("Min Width", f"{stats['min_width']:.2f}m")
    with col4:
        st.metric("Max Width", f"{stats['max_width']:.2f}m")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Time series of stope widths
        fig = px.line(stope_data, x='date', y='stope_width', color='stope_id',
                     title='Stope Width Over Time',
                     labels={'stope_width': 'Width (m)', 'date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribution of stope widths
        fig = px.histogram(stope_data, x='stope_width', 
                          title='Distribution of Stope Widths',
                          labels={'stope_width': 'Width (m)'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Zone analysis
    st.subheader("Zone-wise Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        zone_avg = stope_data.groupby('zone')['stope_width'].mean().reset_index()
        fig = px.bar(zone_avg, x='zone', y='stope_width',
                    title='Average Stope Width by Zone',
                    labels={'stope_width': 'Average Width (m)', 'zone': 'Zone'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(stope_data, x='zone', y='stope_width',
                    title='Stope Width Distribution by Zone',
                    labels={'stope_width': 'Width (m)', 'zone': 'Zone'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("Raw Data")
    st.dataframe(stope_data, use_container_width=True)
