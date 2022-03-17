import pandas as pd
import numpy as np


df = pd.read_csv('Solar_Irradiances_QC_1min_2016.csv',
                 index_col='timestamp', parse_dates=True)

diffuse_fraction = df['DHI'] / df['GHI']
df = df[(df['DNI'] > 790) & (diffuse_fraction.between(0, 0.2))]

# TODO use irradiance on collector instead of DNI
df['rolling_range'] = df['DNI'].rolling('10min').agg(np.ptp)
df = df[df['rolling_range'] <= 64]
df['rolling_nan3h'] = df['DNI'].rolling('3H').count()  # non NaN observarions

df['suitable'] = df['rolling_nan3h'] == 180
suitable_test_days = (df['suitable'].resample('D').count() > 1).sum()

print("Suitable test days:", suitable_test_days)
