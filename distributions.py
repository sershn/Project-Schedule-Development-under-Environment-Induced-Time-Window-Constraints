import numpy as np
import pandas as pd
import seaborn as sns
from fitter import Fitter, get_common_distributions, get_distributions
import matplotlib.pyplot as plt

dataset = pd.read_csv("winter_road.csv")
print(dataset.head())

sns.set_style('white')
sns.set_context("paper", font_scale = 2)
sns.displot(data=dataset, x="date", kde=True, rug=False, bins=30)
plt.show()

height = dataset["date"].values
f = Fitter(height, distributions= get_common_distributions())
f.fit()
f.summary()
plt.show()
print(f.get_best(method = 'sumsquare_error'))