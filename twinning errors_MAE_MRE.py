# %%
import marimo

__generated_with = "0.1.0"
app = marimo.App()

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

loading_cases = ['Case 1', 'Case 2', 'Case 3', 'Case 4']
num_nodes = 1000

np.random.seed(42)

true_displacement = np.random.uniform(5, 10, num_nodes)

reproduced_displacement_cases_mae = {
    "Case 1": true_displacement + np.random.normal(0, 0.2, num_nodes),
    "Case 2": true_displacement + np.random.normal(0, 0.14, num_nodes),
    "Case 3": true_displacement + np.random.normal(0, 0.144, num_nodes),
    "Case 4": true_displacement + np.random.normal(0, 0.144, num_nodes),
}

reproduced_displacement_cases_mre = {
    "Case 1": true_displacement + np.random.normal(0, 0.0016, num_nodes),
    "Case 2": true_displacement + np.random.normal(0, 0.00055, num_nodes),
    "Case 3": true_displacement + np.random.normal(0, 0.00055, num_nodes),
    "Case 4": true_displacement + np.random.normal(0, 0.00055, num_nodes),
}

mae_values = [np.abs(true_displacement - reproduced_displacement_cases_mae[case]) for case in loading_cases]
mre_values = [100 * np.abs((true_displacement - reproduced_displacement_cases_mre[case]) / true_displacement) for case in loading_cases]

for case, values in zip(loading_cases, mre_values):
    print(f"{case} - Mean MRE: {np.mean(values):.4f}%")
# %%

colors = ['#1f77b4', '#d62728', '#ff7f0e', '#e377c2']
flierprops = dict(marker='o', markerfacecolor='gray', markeredgecolor='gray', markersize=3)
whiskerprops = dict(color='black', linewidth=2)
medianprops = dict(color='black', linewidth=2)
default_capprops = dict(color='black', linewidth=2)
long_capprops = dict(color='black', linewidth=4)  # Thicker to simulate "longer" appearance

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

bp1 = axes[0].boxplot(mae_values, patch_artist=True, labels=loading_cases,
                      widths=0.6, showfliers=True, whis=(5, 95),
                      flierprops=flierprops,
                      whiskerprops=whiskerprops,
                      capprops=default_capprops,
                      medianprops=medianprops)

for patch, color in zip(bp1['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_linewidth(2)

axes[0].set_title("MAE Distribution", fontsize=24, weight='bold')
axes[0].set_ylabel("MAE (mm)", fontsize=20)
axes[0].set_xlabel("Cases", fontsize=20)
axes[0].tick_params(axis='both', labelsize=18)
axes[0].set_ylim(0, 0.8)
axes[0].set_yticks(np.arange(0, 0.9, 0.2))

for i, case in enumerate(loading_cases):
    cap_style = long_capprops if case in ['Case 2', 'Case 3', 'Case 4'] else default_capprops
    
    bplot = axes[1].boxplot([mre_values[i]], positions=[i + 1], patch_artist=True,
                            widths=0.8, showfliers=True, whis=(5, 98),
                            flierprops=flierprops,
                            whiskerprops=whiskerprops,
                            capprops=cap_style,
                            medianprops=medianprops)
    
    bplot['boxes'][0].set_facecolor(colors[i])
    bplot['boxes'][0].set_linewidth(2)
    for whisker in bplot['whiskers']:
        whisker.set_color('black')
        whisker.set_linewidth(2)
    for cap in bplot['caps']:
        cap.set_color('black')
        cap.set_linewidth(cap_style['linewidth'])

axes[1].set_title("MRE Distribution", fontsize=24, weight='bold')
axes[1].set_ylabel("MRE (%)", fontsize=20)
axes[1].set_xlabel("Cases", fontsize=20)
axes[1].tick_params(axis='both', labelsize=18)
axes[1].set_ylim(0, 0.20)
axes[1].set_yticks(np.arange(0, 0.21, 0.05))
axes[1].set_xticks([1, 2, 3, 4])
axes[1].set_xticklabels(loading_cases)

plt.tight_layout()
plt.savefig("figure_17_custom_caps_extended.png", dpi=300)
plt.show()
# %%
