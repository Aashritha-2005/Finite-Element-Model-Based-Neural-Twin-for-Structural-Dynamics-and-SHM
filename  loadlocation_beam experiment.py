import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 16
plt.rcParams['font.style'] = 'normal'
plt.rcParams['font.weight'] = 'bold'

L = 20  
EI = 1e9  

P1 = 120e3  
P2 = 120e3  
a1 = 1.0  
a2 = 7.0  

x = np.linspace(0, L, 1000)

def deflection(x, a, P, L, EI):
    b = L - a
    w = np.zeros_like(x)
    
    mask_left = x <= a
    w[mask_left] = (P * b * x[mask_left]) / (6 * EI * L) * (L**2 - x[mask_left]**2 - b**2)
    
    mask_right = x > a
    w[mask_right] = (P * b) / (6 * EI * L) * (
        (L / b) * (x[mask_right] - a)**3 + (L**2 - b**2) * x[mask_right] - x[mask_right]**3
    )
    
    return w

w1 = deflection(x, a1, P1, L, EI)
w2 = deflection(x, a2, P2, L, EI)
w_total = -(w1 + w2)

max_def_idx = np.argmin(w_total)
max_def = w_total[max_def_idx]
max_def_loc = x[max_def_idx]

plt.figure(figsize=(8, 4))

plt.plot([0, L], [0, 0], color='gray', linewidth=2.5, linestyle='--')


plt.arrow(a1, 0.008, 0, -0.006, head_width=0.4, head_length=0.002, fc='blue', ec='blue', linewidth=2, alpha=0.7)
plt.arrow(a2, 0.008, 0, -0.006, head_width=0.4, head_length=0.002, fc='blue', ec='blue', linewidth=2, alpha=0.7)

plt.scatter([a1, a2], [0, 0], color='black', zorder=5)

intersect_1_idx = np.argmin(np.abs(x - a1))
intersect_2_idx = np.argmin(np.abs(x - a2))
intersect_1 = w_total[intersect_1_idx]
intersect_2 = w_total[intersect_2_idx]

plt.plot([a1, a1], [0, intersect_1], 'k--', alpha=0.8, linewidth=2)
plt.plot([a2, a2], [0, intersect_2], 'k--', alpha=0.8, linewidth=2)

plt.scatter([a1, a2], [intersect_1, intersect_2], color='black', zorder=5)

plt.plot(x, w_total, color='dimgray', linewidth=2.5, label='Deformation Curve',)
plt.rcParams.update({'font.size': 16, 'font.weight': 'bold'})

plt.text(a1 + 0.3, 0.005, 'P1', ha='left', fontsize=14.5, color='black')
plt.text(a2 + 0.3, 0.005, 'P2', ha='left', fontsize=14.5, color='black')

plt.scatter(max_def_loc, max_def, color='red', zorder=5)
plt.annotate(f'({max_def_loc:.2f} m, {max_def:.3f} m)', 
             xy=(max_def_loc, max_def), 
             xytext=(max_def_loc - 1.5, max_def - 0.003),
             fontsize=16)

plt.ylim(-0.03, 0.01)  
plt.xlim(-1, L + 1)

plt.xlabel('Location (m)', fontsize=24, fontweight='bold')
plt.ylabel('Deformation (m)', fontsize=24, fontweight='bold')



ax = plt.gca()
ax.tick_params(axis='both', which='major', width=2.5, length=7, labelsize=18)
for spine in ax.spines.values():
    spine.set_linewidth(2.5)

plt.tight_layout()
plt.legend()
plt.show()
