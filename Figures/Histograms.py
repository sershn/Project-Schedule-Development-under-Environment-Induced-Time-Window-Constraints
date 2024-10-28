import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Assuming data_clean contains your data with 'tw0' and 'total_$' columns
data_clean = pd.read_csv('../gpt data 10m runs.csv')
time_window = 'total_t'
# Function to plot a histogram with larger font sizes
def plot_histogram_with_large_font(ax, cutoff, data, x_limit_min, x_limit_max, y_limit):
    filtered_data_exact = data[data[time_window] == cutoff]
    num_bins = int(1+np.log2(len(filtered_data_exact)))
    ax.hist(filtered_data_exact['total_$'], color='yellow', bins=16, edgecolor='black', alpha=0.7)
    ax.set_xlim(x_limit_min, x_limit_max)
    ax.set_ylim(0, y_limit)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))
    ax.set_xlabel('Total Project Cost, $', fontsize=22)
    ax.set_ylabel('Frequency', fontsize=22)
    ax.tick_params(axis='both', which='major', labelsize=22)
    ax.grid(True)
# Set font sizes for title, labels, and ticks
title_fontsize = 22
label_fontsize = 22
tick_fontsize = 22

# Min and max total cost and frequency limits for uniformity
min_total_cost_27m = 26000000
max_total_cost_32_5m = 34500000
max_frequency_exact = 200

# Create the figure with 4 histograms side by side
fig, axes = plt.subplots(1, 5, figsize=(20, 6))

# Plot histograms for tw_0 = 60, 80, 100, and 120 days
plot_histogram_with_large_font(axes[0], 600, data_clean, min_total_cost_27m, max_total_cost_32_5m, max_frequency_exact)
plot_histogram_with_large_font(axes[1], 620, data_clean, min_total_cost_27m, max_total_cost_32_5m, max_frequency_exact)
plot_histogram_with_large_font(axes[2], 640, data_clean, min_total_cost_27m, max_total_cost_32_5m, max_frequency_exact)
plot_histogram_with_large_font(axes[3], 660, data_clean, min_total_cost_27m, max_total_cost_32_5m, max_frequency_exact)
plot_histogram_with_large_font(axes[4], 680, data_clean, min_total_cost_27m, max_total_cost_32_5m, max_frequency_exact)

# Set titles for each histogram
axes[0].set_title('dur. = 600 days', fontsize=22)
axes[1].set_title('dur. = 620 days', fontsize=22)
axes[2].set_title('dur. = 640 days', fontsize=22)
axes[3].set_title('dur. = 660 days', fontsize=22)
axes[4].set_title('dur. = 680 days', fontsize=22)

plt.tight_layout()
plt.show()