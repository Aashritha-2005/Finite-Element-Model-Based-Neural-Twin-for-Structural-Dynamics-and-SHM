# %%
import marimo

__generated_with = "0.1.0"
app = marimo.App()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

fig, axs = plt.subplots(4, 4, figsize=(16, 12))
fig.suptitle('Reproduced stresses obtained using clean displacement data for loading in Cases 1-4', y=1.02)

time = np.linspace(0, 8, 800)

def generate_stress_data(case, point):
    if point == 'BW':
        amplitude = 100  # Reduced from 150 to match PDF scale
        phase = 0
        invert = 1
    elif point == 'GW':
        amplitude = 80   # Reduced from 90
        phase = np.pi/8
        invert = 1
    elif point == 'RF-CTR':
        amplitude = 60   
        phase = np.pi/4
        invert = -1     # Inverted signal
    else:  # RF-MG
        amplitude = 45   # Increased from 40
        phase = np.pi/3
        invert = -1     # Inverted signal
    
    true_stress = np.zeros_like(time)
    
    v1_in, v1_out = 1.04, 3.0
    v2_in, v2_out = 0.6, 2.1
    
    mask_v1 = (time >= v1_in) & (time <= v1_out)
    mask_v2 = (time >= v2_in) & (time <= v2_out)
    
    true_stress[mask_v1] += amplitude * np.sin(np.pi*(time[mask_v1]-v1_in)/(v1_out-v1_in) + phase) * invert
    true_stress[mask_v2] += 0.7*amplitude * np.sin(np.pi*(time[mask_v2]-v2_in)/(v2_out-v2_in) + phase) * invert  # Changed from 0.8
    
    free_vib = 0.25*amplitude * np.exp(-0.7*(time-3.0)) * np.sin(1.8*np.pi*(time-3.0) + phase) * invert  # Changed frequency and damping
    free_vib[time < 3.0] = 0
    true_stress += free_vib
    
    if case == 1:
        if point == 'BW':
            reproduced = true_stress * 0.72 + np.random.normal(0, 6, len(time))  # Adjusted parameters
        else:
            reproduced = true_stress * 0.82 + np.random.normal(0, 4, len(time))
    elif case == 2:
        reproduced = true_stress * 0.92 + np.random.normal(0, 2, len(time))  # Adjusted parameters
    elif case == 3:
        reproduced = true_stress * 0.98 + np.random.normal(0, 1, len(time))
    else:  # case == 4
        reproduced = true_stress + np.random.normal(0, 0.3, len(time))
    
    return true_stress, reproduced

points = ['BW', 'GW', 'RF-CTR', 'RF-MG']

for i, case in enumerate([1, 2, 3, 4]):
    for j, point in enumerate(points):
        ax = axs[i, j]
        
        true_stress, reproduced_stress = generate_stress_data(case, point)
        
        ax.plot(time, true_stress, 'b-', linewidth=1.3, label='True stress')  # Slightly thicker line
        ax.plot(time, reproduced_stress, 'r--', linewidth=1.3, label='Reproduced stress')
        
        if i == 0:
            ax.set_title(point, pad=10)
        if j == 0:
            ax.set_ylabel(f'Case {case}\nStress (N/mm²)', rotation=0, ha='right', va='center')
        if i == 3:
            ax.set_xlabel('Time (s)')
        
        if point == 'BW':
            ax.set_ylim(-10, 110)  # Changed from (-20, 140)
        elif point == 'GW':
            ax.set_ylim(-10, 90)   # Changed from (-15, 110)
        elif point == 'RF-CTR':
            ax.set_ylim(-60, 10)   # Changed from (-70, 10)
        else:  # RF-MG
            ax.set_ylim(-45, 10)   # Changed from (-50, 10)
        
        ax.grid(True, linestyle=':', alpha=0.4)  # Changed to dotted
        
        if i == 0 and j == 0:
            ax.legend(loc='upper right', framealpha=1)
        
        ax.xaxis.set_major_locator(MaxNLocator(4))  # Reduced from 5
        ax.yaxis.set_major_locator(MaxNLocator(4))

plt.tight_layout()
plt.subplots_adjust(hspace=0.35, wspace=0.3)  # Adjusted spacing
plt.show()
# %%
