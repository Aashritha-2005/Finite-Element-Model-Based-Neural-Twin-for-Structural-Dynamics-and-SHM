# %%
import marimo

__generated_with = "0.1.0"
app = marimo.App()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def create_mass_stiffness_matrices(m1, m2, k1, k2):
    M = np.array([[m1, 0], [0, m2]])
    K = np.array([[k1 + k2, -k2], [-k2, k2]])
    return M, K

def calculate_eigenfrequencies(M, K):
    """ eigenfrequencies of system"""
    A = np.linalg.inv(M) @ K
    eigvals = np.linalg.eigvals(A)
    return np.sqrt(np.real(eigvals))

def generate_samples(n_samples, uncertainty_stiff, uncertainty_mass, uncertainty_freq):
    k1_nom, k2_nom = 100.0, 100.0
    m1_nom, m2_nom = 1.0, 1.0

    freq1_healthy = np.zeros(n_samples)
    freq2_healthy = np.zeros(n_samples)
    freq1_damaged = np.zeros(n_samples)
    freq2_damaged = np.zeros(n_samples)

    for i in range(n_samples):
        k1 = np.random.uniform(k1_nom * (1 - uncertainty_stiff), k1_nom * (1 + uncertainty_stiff))
        k2 = np.random.uniform(k2_nom * (1 - uncertainty_stiff), k2_nom * (1 + uncertainty_stiff))
        m1 = np.random.uniform(m1_nom * (1 - uncertainty_mass), m1_nom * (1 + uncertainty_mass))
        m2 = np.random.uniform(m2_nom * (1 - uncertainty_mass), m2_nom * (1 + uncertainty_mass))

        M, K = create_mass_stiffness_matrices(m1, m2, k1, k2)
        freqs_healthy = calculate_eigenfrequencies(M, K)

        freq1_healthy[i] = np.random.uniform(freqs_healthy[0] * (1 - uncertainty_freq),
                                             freqs_healthy[0] * (1 + uncertainty_freq))
        freq2_healthy[i] = np.random.uniform(freqs_healthy[1] * (1 - uncertainty_freq),
                                             freqs_healthy[1] * (1 + uncertainty_freq))

        M_damaged, K = create_mass_stiffness_matrices(m1, m2 * 1.1, k1, k2)
        freqs_damaged = calculate_eigenfrequencies(M_damaged, K)

        freq1_damaged[i] = np.random.uniform(freqs_damaged[0] * (1 - uncertainty_freq),
                                             freqs_damaged[0] * (1 + uncertainty_freq))
        freq2_damaged[i] = np.random.uniform(freqs_damaged[1] * (1 - uncertainty_freq),
                                             freqs_damaged[1] * (1 + uncertainty_freq))

    return freq1_healthy, freq2_healthy, freq1_damaged, freq2_damaged


def plot_eigenfrequencies_separately(uncertainty_levels):
    n_samples = 400

    titles = ['(A) 1% Uncertainty', '(B) 1% Uncertainty',
              '(C) 2% Uncertainty', '(D) 3% Uncertainty']

    for idx, (title, uncertainty) in enumerate(zip(titles, uncertainty_levels)):
        freq1_h, freq2_h, freq1_d, freq2_d = generate_samples(
            n_samples, uncertainty_stiff=uncertainty, uncertainty_mass=uncertainty, uncertainty_freq=0.01
        )

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(freq1_h, freq2_h, edgecolor='#FF8C00',facecolor='None', alpha=0.9, s=40, label='Healthy') 
        ax.scatter(freq1_d, freq2_d, edgecolor='green',facecolor='None', alpha=0.9, s=40, label='Damaged')

        M, K = create_mass_stiffness_matrices(1.0, 1.0, 100.0, 100.0)
        freqs_healthy = calculate_eigenfrequencies(M, K)
        M_damaged, K = create_mass_stiffness_matrices(1.0, 1.1, 100.0, 100.0)
        freqs_damaged = calculate_eigenfrequencies(M_damaged, K)

        ax.scatter(freqs_healthy[0], freqs_healthy[1], c='#FF8C00', s=100, marker='s') 
        ax.scatter(freqs_damaged[0], freqs_damaged[1], c='green', s=100, marker='s')
        

        ax.set_title(title, fontsize=24, fontweight='bold', fontname='Times New Roman')
    
        ax.set_xlabel('Frequency 1', fontsize=22, fontweight='bold', fontname='Times New Roman')
        ax.set_ylabel('Frequency 2', fontsize=22, fontweight='bold', fontname='Times New Roman')

        
        ax.legend(loc='lower right', frameon=True, prop={'family': 'Times New Roman', 'weight': 'bold', 'size': 18})

        ax.tick_params(axis='x', labelsize=16, labelrotation=0)
        ax.tick_params(axis='y', labelsize=16, labelrotation=0)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontname('Times New Roman')
            label.set_fontweight('bold')
        

        plt.tight_layout()
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.show()
# %%


uncertainty_levels = [0.01, 0.01, 0.02, 0.03]
plot_eigenfrequencies_separately(uncertainty_levels)




