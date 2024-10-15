import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Load your dataset (replace with your own data)
data_clean = pd.read_csv('../gpt data 10m runs.csv')

# Perform kernel density estimation for the scatter plot (heatmap)
total_cost_clean = data_clean['total_$']
xy_tw3 = np.vstack([data_clean['tw3'], total_cost_clean])
z_tw3 = gaussian_kde(xy_tw3)(xy_tw3)

# Create the scatter plot with density (heatmap overlay)
plt.figure(figsize=(10, 6))
plt.scatter(data_clean['tw3'], total_cost_clean, c=z_tw3, s=20, cmap='viridis', alpha=0.7)

# Set titles and labels
plt.title('tw_3 (winter road 2024)', fontsize=16)
plt.xlabel('Duration, days', fontsize=14)
plt.ylabel('Total project cost, m$', fontsize=14)

# Adjust the y-axis to display values in millions
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/1e6:.0f}m'))

# Add a colorbar for density
cbar = plt.colorbar()
cbar.set_label('Density', fontsize=14)

# Display the grid and show the plot
plt.grid(True)
plt.show()