import pandas as pd
import numpy as np
import datetime
from lookup.iam import kdir

tilt = 38

df = pd.read_csv("input/2016_weather_upat.dat", sep="\t",
                 usecols=["az", "zen", "T", "dni"])
df['time'] = datetime.datetime(2016, 1, 1) + \
    pd.TimedeltaIndex(df.index, unit='m')
df.set_index('time', inplace=True)
df = df.tz_localize('UTC')
df = df.between_time("07:00", "14:00")

df = df.replace(-9999.9, np.NaN)
df['T'] = df['T'].interpolate(method='nearest')

df['zen'] = abs(df['zen'] - tilt	)
# df = df.loc[(df['az'] < 90) & (df['az'] > -90)] # use this to select valid az
df['az'] = abs(df['az'])
df['t_amb'] = df['T'] + 273
df['kdir_idir'] = kdir(transv=df['az'], long=df['zen'])*df['dni']


df.to_csv("input/preproc_tilt38_kdir_idir_07_14.csv", index_label='time')
