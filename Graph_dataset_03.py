import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_path = '/Users/aashrithalakshmi/Downloads/sopp/Newww/projects/SHM_dataset_03.csv'
data = pd.read_csv(file_path)
print("Data loaded successfully!")

time_columns = [col for col in data.columns if col.startswith('Timestep_')]
num_timesteps = len(time_columns)
time_steps = np.arange(num_timesteps)

experimental_a1 = data[(data['Sensor'] == 'A1') & (data['Model_Type'] == 'experimental')][time_columns].iloc[0].values
optimal_a1 = data[(data['Sensor'] == 'A1') & (data['Model_Type'] == 'optimal')][time_columns].iloc[0].values
nominal_a1 = data[(data['Sensor'] == 'A1') & (data['Model_Type'] == 'nominal')][time_columns].iloc[0].values

experimental_a2 = data[(data['Sensor'] == 'A2') & (data['Model_Type'] == 'experimental')][time_columns].iloc[0].values
optimal_a2 = data[(data['Sensor'] == 'A2') & (data['Model_Type'] == 'optimal')][time_columns].iloc[0].values
nominal_a2 = data[(data['Sensor'] == 'A2') & (data['Model_Type'] == 'nominal')][time_columns].iloc[0].values

start, end = 0, 500
time_steps = time_steps[start:end]
experimental_a1 = experimental_a1[start:end]
optimal_a1 = optimal_a1[start:end]
nominal_a1 = nominal_a1[start:end]
experimental_a2 = experimental_a2[start:end]
optimal_a2 = optimal_a2[start:end]
nominal_a2 = nominal_a2[start:end]

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 20
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['figure.figsize'] = (11, 8)  

plt.figure()
plt.plot(time_steps, experimental_a1, label='Experimental (Healthy)', color='black', linewidth=1)
plt.plot(time_steps, optimal_a1, label='Optimal Numerical', linestyle='--', color='green')
plt.plot(time_steps, nominal_a1, label='Nominal Numerical', linestyle='--', color='orange')
plt.title('Time Responses: Sensor A1', fontsize=40, fontweight='bold')
plt.xlabel('Time Steps (s)', fontsize=36, fontweight='bold')  
plt.ylabel('Acceleration (m/s²)', fontsize=36, fontweight='bold')  
plt.legend(loc='lower right', fontsize=28, frameon=True)
plt.grid()
plt.tight_layout()
plt.gca().spines['bottom'].set_linewidth(4)  
plt.gca().spines['left'].set_linewidth(4)
plt.show()

plt.figure()
plt.plot(time_steps, experimental_a2, label='Experimental (Healthy)', color='black', linewidth=1)
plt.plot(time_steps, optimal_a2, label='Optimal Numerical', linestyle='--', color='green')
plt.plot(time_steps, nominal_a2, label='Nominal Numerical', linestyle='--', color='orange')
plt.title('Time Responses: Sensor A2', fontsize=40, fontweight='bold')
plt.xlabel('Time Steps (s)', fontsize=36, fontweight='bold') 
plt.ylabel('Acceleration (m/s²)', fontsize=36, fontweight='bold') 
plt.legend(loc='lower right', fontsize=28, frameon=True)
plt.grid()
plt.tight_layout()
plt.gca().spines['bottom'].set_linewidth(4)  
plt.gca().spines['left'].set_linewidth(4)    
plt.show()
