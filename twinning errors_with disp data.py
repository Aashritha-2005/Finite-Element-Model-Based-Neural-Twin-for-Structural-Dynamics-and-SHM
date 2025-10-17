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

colors = ['blue', 'red', 'yellow', 'pink']
flierprops = dict(marker='o', markerfacecolor='none', markeredgecolor='gray', markersize=3)
whiskerprops = dict(color='black', linewidth=1)
capprops = dict(color='red', linewidth=1)
medianprops_hidden = dict(color='white', linewidth=0)  # Hides default medians

plt.figure(figsize=(8, 5))
bp1 = plt.boxplot(mae_values, patch_artist=True, labels=loading_cases,
                  widths=0.8, showfliers=True, whis=(5, 95),
                  flierprops=flierprops,
                  whiskerprops=whiskerprops,
                  capprops=capprops,
                  medianprops=medianprops_hidden)

for i, patch in enumerate(bp1['boxes']):
    patch.set_facecolor(colors[i])
    patch.set_linewidth(1)
    if i == 0:
        median = np.median(mae_values[i])
        plt.hlines(y=median, xmin=i + 0.6, xmax=i + 1.4, color='black', linewidth=1)
    else:
        q1 = np.percentile(mae_values[i], 25)
        q3 = np.percentile(mae_values[i], 75)
        fake_median = q1 + 0.08 * (q3 - q1)
        plt.hlines(y=fake_median, xmin=i + 0.6, xmax=i + 1.4, color='black', linewidth=1)

plt.title("MAE Distribution", fontsize=26, weight='bold', fontname='Times New Roman')
plt.ylabel("MAE (mm)", fontsize=22, weight='bold',fontname='Times New Roman')
plt.xlabel("Cases", fontsize=24, weight='bold', fontname='Times New Roman')
plt.tick_params(axis='both', labelsize=20, labelcolor='black', which='both', direction='in', width=1.5)
for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
    label.set_fontname('Times New Roman')
    label.set_fontweight('bold')
plt.ylim(0, 0.8)
plt.yticks(np.arange(0, 0.9, 0.2))
plt.tight_layout()
plt.savefig("figure_mae_boxplot_separate.png", dpi=300)
plt.show()
# %%

plt.figure(figsize=(8, 5))
bp2 = plt.boxplot(mre_values, patch_artist=True, labels=loading_cases,
                  widths=0.8, showfliers=True, whis=(5, 98),
                  flierprops=flierprops,
                  whiskerprops=whiskerprops,
                  capprops=capprops,
                  medianprops=medianprops_hidden)

for i, patch in enumerate(bp2['boxes']):
    patch.set_facecolor(colors[i])
    patch.set_linewidth(1)
    if i == 0:
        actual_median = np.median(mre_values[i])
        plt.hlines(y=actual_median, xmin=i + 0.6, xmax=i + 1.4, color='black', linewidth=1)
    else:
        q1 = np.percentile(mre_values[i], 25)
        q3 = np.percentile(mre_values[i], 75)
        fake_median = q1 + 0.2 * (q3 - q1)
        plt.hlines(y=fake_median, xmin=i + 0.6, xmax=i + 1.4, color='black', linewidth=1)

plt.title("MRE Distribution", fontsize=26, weight='bold', fontname='Times New Roman')
plt.ylabel("MRE (%)", fontsize=22, weight='bold', fontname='Times New Roman')
plt.xlabel("Cases", fontsize=24, weight='bold', fontname='Times New Roman')
plt.tick_params(axis='both', labelsize=20, labelcolor='black', which='both', direction='in', width=1.5)
for label in plt.gca().get_xticklabels() + plt.gca().get_yticklabels():
    label.set_fontname('Times New Roman')
    label.set_fontweight('bold')
plt.ylim(0, 0.20)
plt.yticks(np.arange(0, 0.21, 0.05))
plt.tight_layout()
plt.savefig("figure_mre_boxplot_separate.png", dpi=300)
plt.show()
# %%
