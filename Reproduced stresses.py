# %%
import marimo

__generated_with = "0.1.0"
app = marimo.App()

import matplotlib.pyplot as plt
import numpy as np

time = np.linspace(0, 8, 800)

def create_stress_pattern(base_amp, pattern_type='bw', phase_shift=0):
    stress = np.zeros_like(time)
    forced_idx = time <= 3
    free_idx = time > 3
    decay_rate = 0.4
    
    if pattern_type == 'bw':
        stress[forced_idx] = base_amp * (0.8 + 0.5 * np.sin(2 * np.pi * time[forced_idx] / 1.2 + phase_shift) + 0.3 * np.sin(4 * np.pi * time[forced_idx] / 1.5))
        stress[free_idx] = base_amp * 0.7 * np.sin(2 * np.pi * (time[free_idx] - 3) / 2) * np.exp(-decay_rate * (time[free_idx] - 3))
    elif pattern_type == 'gw':
        stress[forced_idx] = base_amp * (0.6 + 0.7 * np.sin(2 * np.pi * time[forced_idx] / 1.5 + phase_shift) + 0.2 * np.sin(3 * np.pi * time[forced_idx] / 0.8))
        stress[free_idx] = base_amp * 0.5 * np.sin(2 * np.pi * (time[free_idx] - 3) / 2.2) * np.exp(-decay_rate * (time[free_idx] - 3))
    elif pattern_type == 'rf_ctr':
        stress[forced_idx] = base_amp * (0.4 + 0.6 * np.sin(2 * np.pi * time[forced_idx] / 1.0 + phase_shift) + 0.25 * np.sin(5 * np.pi * time[forced_idx] / 1.2))
        stress[free_idx] = base_amp * 0.4 * np.sin(2 * np.pi * (time[free_idx] - 3) / 2.1) * np.exp(-decay_rate * (time[free_idx] - 3))
    elif pattern_type == 'rf_mg':
        stress[forced_idx] = base_amp * (0.3 + 0.4 * np.sin(2 * np.pi * time[forced_idx] / 0.9 + phase_shift) + 0.15 * np.sin(6 * np.pi * time[forced_idx] / 1.8))
        stress[free_idx] = base_amp * 0.3 * np.sin(2 * np.pi * (time[free_idx] - 3) / 1.9) * np.exp(-decay_rate * (time[free_idx] - 3))
    
    return stress

def create_reproduced_stress(true_stress, case_num, pattern_type):
    accuracy_factor = {1: 0.7, 2: 0.85, 3: 0.92, 4: 0.98}[case_num]
    noise_factor = {1: 0.3, 2: 0.15, 3: 0.08, 4: 0.02}[case_num]
    
    if case_num == 1 and pattern_type == 'bw':
        accuracy_factor = 0.5
        noise_factor = 0.5

    if pattern_type == 'bw':
        noise = np.sin(3 * np.pi * time / 1.2) + 0.5 * np.sin(5 * np.pi * time / 0.8)
    elif pattern_type == 'gw':
        noise = np.sin(2.5 * np.pi * time / 1.4) + 0.4 * np.sin(4 * np.pi * time / 1.1)
    elif pattern_type == 'rf_ctr':
        noise = np.sin(2.2 * np.pi * time / 1.3) + 0.3 * np.sin(4.5 * np.pi * time / 0.9)
    else:
        noise = np.sin(2.8 * np.pi * time / 1.5) + 0.2 * np.sin(3.5 * np.pi * time / 1.2)

    noise_applied = np.zeros_like(time)
    noise_applied[time <= 3] = noise_factor * noise[time <= 3] * np.max(np.abs(true_stress))
    noise_applied[time > 3] = noise_factor * noise[time > 3] * np.max(np.abs(true_stress)) * 0.5

    reproduced = accuracy_factor * true_stress + noise_applied

    if case_num == 1:
        free_idx = time > 3
        reproduced[free_idx] = 0.9 * true_stress[free_idx] + noise_factor * 0.2 * noise[free_idx] * np.max(np.abs(true_stress))
    
    return reproduced

true_stress_bw = create_stress_pattern(100, 'bw')
true_stress_gw = create_stress_pattern(80, 'gw', np.pi/6)
true_stress_rf_ctr = create_stress_pattern(60, 'rf_ctr', np.pi/4)
true_stress_rf_mg = create_stress_pattern(40, 'rf_mg', np.pi/3)

patterns = ['bw', 'gw', 'rf_ctr', 'rf_mg']
true_stress_all = [true_stress_bw, true_stress_gw, true_stress_rf_ctr, true_stress_rf_mg]

fig, axs = plt.subplots(4, 4, figsize=(20, 15))
for i, (pattern, true_stress) in enumerate(zip(patterns, true_stress_all)):
    for j in range(1, 5):
        row, col = i, j - 1
        reproduced = create_reproduced_stress(true_stress, j, pattern)
        axs[row, col].plot(time, true_stress, label='True Stress', color='blue', linewidth=2)
        axs[row, col].plot(time, reproduced, label=f'Case {j}', linestyle='--', color='orange', linewidth=2)
        axs[row, col].set_title(f'{pattern.upper()} - Case {j}')
        axs[row, col].set_xlabel('Time (s)')
        axs[row, col].set_ylabel('Stress (MPa)')
        axs[row, col].legend()
        axs[row, col].grid(True)

fig.tight_layout()
plt.show()# %%
