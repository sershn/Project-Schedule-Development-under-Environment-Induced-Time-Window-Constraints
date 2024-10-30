import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Load your dataset (replace with your own data)
#data = pd.read_csv('../gpt data 10m runs.csv')
data = pd.read_csv('../data.csv')
#data = data.sample(frac=0.01, random_state=42)
time_window = 'tw4_st'
# Perform kernel density estimation for the scatter plot (heatmap)
total_cost_clean = data['total_$']
xy = np.vstack([data[time_window], total_cost_clean])
z = gaussian_kde(xy)(xy)
font = 16
# Create the scatter plot with density (heatmap overlay)
plt.figure(figsize=(7, 5))
plt.scatter(data[time_window], total_cost_clean, c=z, s=20, cmap='plasma', alpha=0.7, marker='x')
# x1 = [96,104]
# y1 = [28499000,28499000]
# x2 = [100,100]
# y2 = [28100000,28900000]
# plt.plot(x1,y1, c='lime', label='Deterministic TW')
# plt.plot(x2,y2, c='lime')
# plt.legend(loc='upper right', fontsize=font)
#cmap='viridis'
#cmap='plasma'
#cmap='hot'
# Set titles and labels
plt.title('Project Duration vs Cost', fontsize=16)
plt.xlabel('Duration, days', fontsize=font)
plt.ylabel('Total project cost, $', fontsize=font)
plt.xticks(fontsize=font)
plt.yticks(fontsize=font)

# Adjust the y-axis to display values in millions
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))

# Add a colorbar for density
cbar = plt.colorbar()
cbar.set_label('Density', fontsize=font)
cbar.ax.tick_params(labelsize=font)

# Display the grid and show the plot
#plt.grid(True)

plt.show()