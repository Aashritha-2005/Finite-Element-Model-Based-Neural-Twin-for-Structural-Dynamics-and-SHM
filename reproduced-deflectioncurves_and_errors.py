#Reproduced deflection curves of the beam and corresponding errors in the four cases with different numbers of loading points. 
import numpy as np
import matplotlib.pyplot as plt

L = 20  
EI = 1e9  
P1, P2 = 120e3, 120e3  
a1, a2 = 1.0, 7.0  

x = np.linspace(0, L, 1000)

def deflection(x, a, P, L, EI):
    b = L - a
    w = np.zeros_like(x)
    mask_left = x <= a
    mask_right = x > a
    
    w[mask_left] = -(P * b * x[mask_left]) / (6 * EI * L) * (L**2 - x[mask_left]**2 - b**2)
    w[mask_right] = -(P * b) / (6 * EI * L) * (
        (L / b) * (x[mask_right] - a)**3 + (L**2 - b**2) * x[mask_right] - x[mask_right]**3
    )
    return w

w1 = deflection(x, a1, P1, L, EI)
w2 = deflection(x, a2, P2, L, EI)
w_true = w1 + w2

cases = [1, 3, 7, 15]  

for case_index, case in enumerate(cases):
    sample_points = np.linspace(0, L, case + 2)[1:-1] 
    sampled_deflection = np.interp(sample_points, x, w_true)
    
    A = np.zeros((case, case))
    for i in range(case):
        for j in range(case):
            a_i = sample_points[i]
            P_j = 1.0  # Unit force
            A[i, j] = deflection(np.array([a_i]), sample_points[j], P_j, L, EI)[0]
    
    F_eq = np.linalg.solve(A, sampled_deflection)
    
    w_reproduced = np.zeros_like(x)
    for i in range(case):
        w_reproduced += deflection(x, sample_points[i], F_eq[i], L, EI)
    
    error = -(w_true - w_reproduced)
    
    rel_error = np.abs(error / np.where(np.abs(w_true) > 1e-10, w_true, 1e-10))
    
    plt.style.use('default')
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 16
    plt.rcParams['font.style'] = 'normal'
    plt.rcParams['font.weight'] = 'bold'
   


    fig1 = plt.figure(figsize=(10, 6.5))
    plt.plot([0, L], [0, 0], color='gray', linewidth=2.5, linestyle='--', alpha=1.0) 
    plt.plot(x, w_true, label='True Deformation', color='grey', linewidth=3, alpha=1.0)
    plt.plot(x, w_reproduced, label='Reproduced Deformation', color='green', linewidth=3)
    plt.scatter(sample_points, sampled_deflection, color='red', s=40, zorder=3)
    
    for sp, sd in zip(sample_points, sampled_deflection):
        plt.plot([sp, sp], [sd, 0], color='red', linestyle='--', linewidth=2.2)
        plt.scatter(sp, 0, color='red', s=50, zorder=5)  # Intersection points on the beam line
        plt.scatter(sp, sd, color='red', s=50, zorder=5)  # Intersection points on the deformation curve
    
    plt.xlabel('Location (m)', fontsize=24, fontweight='bold', fontname='Times New Roman')
    plt.ylabel('Deformation (m)', fontsize=24, fontweight='bold', fontname='Times New Roman')
    plt.legend(loc='lower right', frameon=False, prop={'weight': 'bold'})
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.tight_layout()
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', width=2.5, length=7, labelsize=18)
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)

    plt.savefig(f'case_{case_index + 1}_deformation.png')
    plt.show()
    plt.close(fig1)

    fig2 = plt.figure(figsize=(6, 5))
    plt.plot(x, error, label='Error', color='orange', linewidth=3, alpha=1.0)
    plt.scatter(sample_points, np.interp(sample_points, x, error), color='red', s=40, zorder=3)
    plt.xlabel('Location (m)', fontsize=24, fontweight='bold', fontname='Times New Roman')
    plt.ylabel('Error (m)', fontsize=24, fontweight='bold', fontname='Times New Roman')
    plt.legend(loc='best', frameon=False, prop={'weight': 'bold'})
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.tight_layout()
    ax = plt.gca()
    ax.tick_params(axis='both', which='major', width=2.5, length=7, labelsize=18)
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)
    plt.savefig(f'case_{case_index + 1}_error.png')
    plt.show()
    plt.close(fig2)

    fig3 = plt.figure(figsize=(6, 5))
    plt.plot(x, rel_error, label='Relative Error', color='orange', linewidth=3, alpha=1.0)
    plt.scatter(sample_points, np.interp(sample_points, x, rel_error), color='red', s=40, zorder=3)
    plt.xlabel('Location (m)', fontsize=24, fontweight='bold', fontname='Times New Roman')
    plt.ylabel('Relative Error', fontsize=24, fontweight='bold', fontname='Times New Roman')
    plt.legend(loc='best', frameon=False, prop={'weight': 'bold'})
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.tight_layout()

    ax = plt.gca()
    ax.tick_params(axis='both', which='major', width=2.5, length=7, labelsize=18)
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)
    plt.savefig(f'case_{case_index + 1}_relative_error.png')
    plt.show()
    plt.close(fig3)
