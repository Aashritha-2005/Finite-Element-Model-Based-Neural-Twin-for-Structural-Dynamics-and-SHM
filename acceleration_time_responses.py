import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Sensor Data Visualization", layout="wide")

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    selected_sensor = st.selectbox("Select Sensor", ["A1", "A2"])
    start_step = st.slider("Start Time Step", 0, 1000, 0)
    end_step = st.slider("End Time Step", 0, 1000, 500)

# Main content area
st.title("Sensor Data Visualization Dashboard")

if uploaded_file is not None:
    try:
        # Load data
        data = pd.read_csv(uploaded_file)
        
        # Data processing
        time_columns = [col for col in data.columns if col.startswith('Timestep_')]
        time_steps = np.arange(len(time_columns))[start_step:end_step]

        def get_sensor_data(sensor):
            return {
                'experimental': data[(data['Sensor'] == sensor) & 
                                   (data['Model_Type'] == 'experimental')][time_columns].iloc[0].values[start_step:end_step],
                'optimal': data[(data['Sensor'] == sensor) & 
                              (data['Model_Type'] == 'optimal')][time_columns].iloc[0].values[start_step:end_step],
                'nominal': data[(data['Sensor'] == sensor) & 
                              (data['Model_Type'] == 'nominal')][time_columns].iloc[0].values[start_step:end_step]
            }

        sensor_data = get_sensor_data(selected_sensor)

        # Create plot
        plt.rcParams.update({
            'font.family': 'Times New Roman',
            'font.size': 20,
            'font.weight': 'bold',
            'figure.figsize': (11, 8)
        })

        fig, ax = plt.subplots()
        ax.plot(time_steps, sensor_data['experimental'], 
                label='Experimental (Healthy)', color='black', linewidth=1)
        ax.plot(time_steps, sensor_data['optimal'], 
                label='Optimal Numerical', linestyle='--', color='green')
        ax.plot(time_steps, sensor_data['nominal'], 
                label='Nominal Numerical', linestyle='--', color='orange')
        
        ax.set_title(f'Time Responses: Sensor {selected_sensor}', 
                    fontsize=40, fontweight='bold')
        ax.set_xlabel('Time Steps (s)', fontsize=36, fontweight='bold')
        ax.set_ylabel('Acceleration (m/s²)', fontsize=36, fontweight='bold')
        ax.legend(loc='lower right', fontsize=28, frameon=True)
        ax.grid()
        ax.spines['bottom'].set_linewidth(4)
        ax.spines['left'].set_linewidth(4)
        
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
else:
    st.info("Please upload a CSV file to begin visualization")

