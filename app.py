import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_real_data, get_mine_context
from components.stope_analysis import create_stope_analysis
from components.blast_sequencing import create_blast_sequencing
from components.equipment_utilization import create_equipment_utilization

# Page configuration
st.set_page_config(
    page_title="Mining Data Dashboard",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">⛏️ Mining Data Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    stope_data, blast_data, equipment_data = load_real_data()
    
    # Sidebar
    st.sidebar.title("Navigation")
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Stope Width Analysis", "Blast Sequencing", "Equipment Utilization"]
    )
    
    # Date range filter
    st.sidebar.subheader("Date Range Filter")
    if not stope_data.empty:
        min_date = stope_data['date'].min()
        max_date = stope_data['date'].max()
        start_date, end_date = st.sidebar.date_input(
            "Select date range",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
    
    # Main content based on selection
    if analysis_type == "Stope Width Analysis":
        create_stope_analysis(stope_data)
    elif analysis_type == "Blast Sequencing":
        create_blast_sequencing(blast_data)
    elif analysis_type == "Equipment Utilization":
        create_equipment_utilization(equipment_data)
    
    # Key Metrics Overview
    st.sidebar.markdown("---")
    st.sidebar.subheader("Key Metrics")
    
    if not stope_data.empty:
        avg_width = stope_data['stope_width'].mean()
        st.sidebar.metric("Average Stope Width", f"{avg_width:.2f}m")
    
    if not equipment_data.empty:
        avg_utilization = equipment_data['utilization_rate'].mean()
        st.sidebar.metric("Avg Equipment Utilization", f"{avg_utilization:.1f}%")

    # Mine Context Information
    st.sidebar.markdown("---")
    st.sidebar.subheader("Mine Context")
    mine_info = get_mine_context()
    st.sidebar.write(f"**Method:** {mine_info['likely_method']}")
    st.sidebar.write(f"**Commodity:** {mine_info['likely_commodity']}")
    st.sidebar.write(f"**Depth:** {mine_info['depth_category']}")
    st.sidebar.write(f"**Examples:** {', '.join(mine_info['typical_operations'])}")

if __name__ == "__main__":
    main()
