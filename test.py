import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv("output.csv", index_col='Unnamed: 0')


df['time'] = datetime.datetime(2016, 1, 1) + \
    pd.TimedeltaIndex(df.index, unit='m')
df.set_index('time', inplace=True)

df = df.fillna(0)

def plot_kwh_timeseries(dfin, col, interval="D", ylabel="", folder=None):
    dfout = dfin.resample(interval).sum() / 60000
    fig, ax = plt.subplots(figsize=(36, 7))
    ax.bar(dfout.index, dfout[col])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlabel("2016")
    ax.set_ylabel(ylabel)
    plt.show()

plot_kwh_timeseries(df, 'qdot')

print(df['qdot'].sum()/60000)
