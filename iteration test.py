import itertools
import pandas as pd
alt_3 = [0,1]
alt_2 = [0,1]
combinations = list(itertools.product(alt_3,alt_3,alt_3,alt_3,alt_3,alt_2,alt_3,alt_3,alt_3,alt_3,alt_3,alt_3,alt_3,alt_2))
df = pd.DataFrame(combinations)
print(df)
df.drop_duplicates()
print(df.nunique())
