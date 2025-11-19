import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.calculations import calculate_blast_efficiency

def create_blast_sequencing(blast_data):
    """Create blast sequencing analysis dashboard"""
    
    st.header("💥 Blast Sequencing Analysis")
    
    # Key metrics
    efficiency = calculate_blast_efficiency(blast_data)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Fragmentation", f"{efficiency['avg_fragmentation']:.2f}m")
    with col2:
        st.metric("Avg Explosives Used", f"{efficiency['avg_explosives']:.0f}kg")
    with col3:
        st.metric("Avg Vibration", f"{efficiency['avg_vibration']:.1f}mm/s")
    with col4:
        st.metric("Blast Frequency", f"{efficiency['blast_frequency']:.1f}/day")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Explosives usage over time
        fig = px.line(blast_data, x='date', y='explosives_used', color='blast_id',
                     title='Explosives Usage Over Time',
                     labels={'explosives_used': 'Explosives (kg)', 'date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Fragmentation vs Explosives
        fig = px.scatter(blast_data, x='explosives_used', y='fragmentation_size',
                        color='blast_id', size='vibration_level',
                        title='Fragmentation vs Explosives Used',
                        labels={'explosives_used': 'Explosives (kg)', 
                               'fragmentation_size': 'Fragmentation Size (m)'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Sequence analysis
    st.subheader("Blast Sequence Analysis")
    
    sequence_analysis = blast_data.groupby('sequence_number').agg({
        'fragmentation_size': 'mean',
        'explosives_used': 'mean',
        'vibration_level': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sequence_analysis['sequence_number'], 
                            y=sequence_analysis['fragmentation_size'],
                            name='Fragmentation Size',
                            yaxis='y1'))
    fig.add_trace(go.Scatter(x=sequence_analysis['sequence_number'], 
                            y=sequence_analysis['explosives_used'],
                            name='Explosives Used',
                            yaxis='y2'))
    
    fig.update_layout(
        title='Blast Sequence Performance',
        xaxis_title='Sequence Number',
        yaxis=dict(title='Fragmentation Size (m)', side='left'),
        yaxis2=dict(title='Explosives (kg)', side='right', overlaying='y')
    )
    
    st.plotly_chart(fig, use_container_width=True)
