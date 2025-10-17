import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sampling_freq = 2048
excitation_time = 8
num_timesteps = min(1000, int(sampling_freq * excitation_time))
t = np.linspace(0, excitation_time, num_timesteps)

np.random.seed(42)
random_excitation = np.random.normal(0, 1, len(t))
print("Random excitation generated.")

def simulate_response(time, base_excitation, model_type):
    """Simulate response for different models."""
    if model_type == 'experimental':
        freq_factor = 1.0
        damping_factor = 1.0
        noise_level = 0.05
    elif model_type == 'optimal':
        freq_factor = 0.998
        damping_factor = 0.995
        noise_level = 0.02
    else:  # nominal
        freq_factor = 0.95
        damping_factor = 0.9
        noise_level = 0.01

    frequencies = np.array([8.97, 15.31, 63.42, 187.24]) * freq_factor
    response_A1 = np.zeros_like(time)
    response_A2 = np.zeros_like(time)

    for i, freq in enumerate(frequencies):
        zeta = 0.02 * damping_factor
        mode_response = base_excitation * np.sin(2 * np.pi * freq * time) * np.exp(-zeta * time)
        if i == 0:
            response_A1 += mode_response * 1.2
            response_A2 += mode_response * 1.5
        elif i == 1:
            response_A1 += mode_response * 0.9
            response_A2 += mode_response * 1.4
        elif i == 2:
            response_A1 += mode_response * 0.7
            response_A2 += mode_response * 1.6
        else:
            response_A1 += mode_response * 1.0
            response_A2 += mode_response * 1.3

    response_A1 += np.random.normal(0, noise_level, len(time))
    response_A2 += np.random.normal(0, noise_level, len(time))

    return response_A1, response_A2

samples = 2000
data = []
models = ['experimental', 'optimal', 'nominal']
health_statuses = ['Healthy', 'Damaged']

for sample_id in range(samples):
    sensor = np.random.choice(["A1", "A2"])
    model_type = np.random.choice(models)

    if model_type == 'experimental':
        health_status = np.random.choice(health_statuses, p=[0.7, 0.3])  # 70% Healthy, 30% Damaged
    elif model_type == 'optimal':
        health_status = 'Healthy'  # Optimal models are always Healthy
    else:  # nominal
        health_status = 'Damaged'  # Nominal models are always Damaged

    response_A1, response_A2 = simulate_response(t, random_excitation, model_type)

    if sensor == "A1":
        data.append({
            'Sample_Id': sample_id,
            'Sensor': sensor,
            'Model_Type': model_type,
            'Health_Status': health_status,  # Ensure Health_Status is included
            **{f'Timestep_{i}': response_A1[i] for i in range(num_timesteps)}
        })
    else:
        data.append({
            'Sample_Id': sample_id,
            'Sensor': sensor,
            'Model_Type': model_type,
            'Health_Status': health_status,  # Ensure Health_Status is included
            **{f'Timestep_{i}': response_A2[i] for i in range(num_timesteps)}
        })

data_df = pd.DataFrame(data)
print("DataFrame with structural responses created.")

data_df.to_csv('SHM_dataset_03.csv', index=False)
print("Data saved to 'SHM_dataset_03.csv'.")


