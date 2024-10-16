import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Load your dataset (replace with your own data)
data = pd.read_csv('../gpt data 10m runs.csv')
time_window = 'tw4'
# Perform kernel density estimation for the scatter plot (heatmap)
total_cost_clean = data['total_$']
xy = np.vstack([data[time_window], total_cost_clean])
z = gaussian_kde(xy)(xy)

# Create the scatter plot with density (heatmap overlay)
plt.figure(figsize=(7, 5))
plt.scatter(data[time_window], total_cost_clean, c=z, s=20, cmap='viridis', alpha=0.7, marker='x')
#cmap='viridis'
#cmap='plasma'
# Set titles and labels
plt.title(time_window+' (thawing 2024)', fontsize=16)
plt.xlabel('Duration, days', fontsize=16)
plt.ylabel('Total project cost, $', fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Adjust the y-axis to display values in millions
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))

# Add a colorbar for density
cbar = plt.colorbar()
cbar.set_label('Density', fontsize=16)
cbar.ax.tick_params(labelsize=16)

# Display the grid and show the plot
plt.grid(True)

plt.show()