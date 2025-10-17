import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

plt.rcParams.update({
    'font.size': 7,
    'axes.titlesize': 7,
    'axes.labelsize': 7,
    'legend.fontsize': 6,
    'xtick.labelsize': 6,
    'ytick.labelsize': 6,
    'lines.linewidth': 1,
    'axes.linewidth': 0.5
})

fig, axs = plt.subplots(4, 4, figsize=(7, 6.5), constrained_layout=True)
fig.suptitle('Reproduced stresses obtained using clean displacement data for loading in Cases 1–4', fontsize=9, y=1.03)

time = np.linspace(0, 8, 800)

def generate_smooth_stress(case, point):
    if point == 'BW':
        amp = 100; offset = 0
    elif point == 'GW':
        amp = 90; offset = 0
    elif point == 'RF-CTR':
        amp = 60; offset = -60
    else:
        amp = 45; offset = -40

    true = np.zeros_like(time)
    def pulse(t_in, t_out, scale=1.0):
        duration = t_out - t_in
        pulse_shape = np.sin(np.pi * (time - t_in) / duration)
        mask = (time >= t_in) & (time <= t_out)
        signal = np.zeros_like(time)
        signal[mask] = scale * amp * pulse_shape[mask]
        return signal

    true += pulse(1.04, 3.0)
    true += pulse(0.6, 2.1, scale=0.8)

    decay_mask = time > 3.0
    decay = 0.1 * amp * np.exp(-1.5 * (time - 3.0)) * np.sin(2 * np.pi * 1.5 * (time - 3.0))
    true[decay_mask] += decay[decay_mask]

    true += offset

    if case == 1:
        factor, bias = 0.7 if point == 'BW' else 0.85, 5
    elif case == 2:
        factor, bias = 0.95, 3
    elif case == 3:
        factor, bias = 0.98, 1.5
    else:
        factor, bias = 1.0, 0.5

    smooth_bias = bias * np.exp(-2 * (time - 3))
    smooth_bias[time < 3] = 0
    reproduced = factor * true + (smooth_bias if offset >= 0 else -smooth_bias)

    return true, reproduced

points = ['BW', 'GW', 'RF-CTR', 'RF-MG']

for i, case in enumerate([1, 2, 3, 4]):
    for j, point in enumerate(points):
        ax = axs[i, j]
        true_stress, reproduced_stress = generate_smooth_stress(case, point)

        ax.plot(time, true_stress, color='blue', label='True stress')
        ax.plot(time, reproduced_stress, color='orange', linestyle='--', label='Reproduced stress')

        ax.set_xlim(0, 8)
        if point == 'BW':
            ax.set_ylim(-20, 100)
        elif point == 'GW':
            ax.set_ylim(-20, 100)
        elif point == 'RF-CTR':
            ax.set_ylim(-70, 10)
        else:
            ax.set_ylim(-50, 10)

        ax.set_title(f"{point}: Case {case} Reproduced by Disp.", pad=3)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Stress (N/mm²)")

        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.yaxis.set_major_locator(MaxNLocator(4))
        ax.grid(True, linestyle='--', alpha=0.5, linewidth=0.3)

        for spine in ax.spines.values():
            spine.set_visible(False)

        if i == 0 and j == 0:
            ax.legend(loc='lower left', frameon=True, borderpad=0.3)

plt.show()

