import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

fig, axs = plt.subplots(4, 4, figsize=(16, 12))
fig.suptitle('Reproduced stresses obtained using clean displacement data for loading in Cases 1-4', y=1.02)

time = np.linspace(0, 8, 800)

def generate_stress_data(case, point):
    if point == 'BW':
        amplitude = 150  # Butt weld has highest stress
        phase = 0
        invert = 1
    elif point == 'GW':
        amplitude = 90   # Gusset weld
        phase = np.pi/8
        invert = 1
    elif point == 'RF-CTR':
        amplitude = 60   # Reinforcement center
        phase = np.pi/4
        invert = -1     # Inverted signal
    else:  # RF-MG
        amplitude = 40   # Reinforcement main girder
        phase = np.pi/3
        invert = -1     # Inverted signal
    
    true_stress = np.zeros_like(time)
    
    v1_in, v1_out = 1.04, 3.0
    v2_in, v2_out = 0.6, 2.1
    
    mask_v1 = (time >= v1_in) & (time <= v1_out)
    mask_v2 = (time >= v2_in) & (time <= v2_out)
    
    true_stress[mask_v1] += amplitude * np.sin(np.pi*(time[mask_v1]-v1_in)/(v1_out-v1_in) + phase) * invert
    true_stress[mask_v2] += 0.8*amplitude * np.sin(np.pi*(time[mask_v2]-v2_in)/(v2_out-v2_in) + phase) * invert
    
    free_vib = 0.3*amplitude * np.exp(-0.5*(time-3.0)) * np.sin(2*np.pi*2*(time-3.0) + phase) * invert
    free_vib[time < 3.0] = 0
    true_stress += free_vib
    
    if case == 1:
        if point == 'BW':
            reproduced = true_stress * 0.7 + np.random.normal(0, 8, len(time))
        else:
            reproduced = true_stress * 0.85 + np.random.normal(0, 5, len(time))
    elif case == 2:
        reproduced = true_stress * 0.95 + np.random.normal(0, 3, len(time))
    elif case == 3:
        reproduced = true_stress * 0.98 + np.random.normal(0, 1.5, len(time))
    else:  # case == 4
        reproduced = true_stress + np.random.normal(0, 0.5, len(time))
    
    return true_stress, reproduced

points = ['BW', 'GW', 'RF-CTR', 'RF-MG']

for i, case in enumerate([1, 2, 3, 4]):
    for j, point in enumerate(points):
        ax = axs[i, j]
        
        true_stress, reproduced_stress = generate_stress_data(case, point)
        
        ax.plot(time, true_stress, 'b-', linewidth=1.2, label='True stress')
        ax.plot(time, reproduced_stress, 'r--', linewidth=1.2, label='Reproduced stress')
        
        if i == 0:
            ax.set_title(point, pad=10)
        if j == 0:
            ax.set_ylabel(f'Case {case}\nStress (N/mm²)', rotation=0, ha='right', va='center')
        if i == 3:
            ax.set_xlabel('Time (s)')
        
        if point == 'BW':
            ax.set_ylim(-20, 140)
        elif point == 'GW':
            ax.set_ylim(-15, 110)
        elif point == 'RF-CTR':
            ax.set_ylim(-70, 10)  # Inverted range
        else:  # RF-MG
            ax.set_ylim(-50, 10)  # Inverted range
        
        ax.grid(True, linestyle='--', alpha=0.3)
        
        if i == 0 and j == 0:
            ax.legend(loc='upper right', framealpha=1)
        
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(5))

plt.tight_layout()
plt.subplots_adjust(hspace=0.3, wspace=0.3)
plt.show()
