import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


SMALL_SIZE = 8
MEDIUM_SIZE = 14
BIGGER_SIZE = 42


def plot_temps(df):
    plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    df['t_out'].plot()
    plt.title('$T_{out}$')
    plt.ylabel("$(K)$")
    plt.xlabel("time (s)")

    plt.subplot(1, 3, 2)
    df['t_in'].plot(label="$T_{in}$")
    df['t_amb'].plot(label="$T_{amb}$")
    plt.legend()
    plt.ylabel("$(K)$")
    plt.xlabel("time (s)")

    plt.subplot(1, 3, 3)
    df['delta_t'].plot()
    plt.title('$T_{out} - T_{in}$')
    plt.ylabel("$(K)$")
    plt.xlabel("time (s)")

    plt.tight_layout()
    plt.show()


def plot_power_eff(df):
    plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    df['dni'].plot()
    plt.title("DNI")
    plt.ylabel("$(W \cdot m^{-2})$")
    plt.xlabel("time (s)")

    plt.subplot(1, 3, 2)
    df['qdot'].plot()
    plt.title("$\dot Q$")
    plt.ylabel("$(W)$")
    plt.xlabel("time (s)")

    plt.subplot(1, 3, 3)
    df['eff'].plot(label='ISO')
    plt.title("Efficiency")

    plt.xlabel("time (s)")
    plt.tight_layout()
    plt.show()


def plot_kwh_timeseries(dfin, col='qdot', interval="D", ylabel="kWh", folder=None):
    plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
    dfout = dfin.resample(interval).sum() / 60000
    fig, ax = plt.subplots(figsize=(36, 7))
    ax.set_title("Energy yield")
    ax.bar(dfout.index, dfout[col])
    ax.set_xlim(dfout.index[0], dfout.index[-1])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.set_xlabel("2016")
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='y', which='major', pad=30)
    plt.show()


def plot_calendar_heatmap(dfin, col, freq="1min", cbar_title="cbar_title", units="",
                          title="Title",
                          folder="calendar-heatmaps"):
    plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
    df = dfin.resample(freq).mean().dropna()
    df["Time, UTC"] = df.index.time
    df["Date"] = df.index.date
    df.reset_index(inplace=True)
    df = df.pivot("Time, UTC", "Date", col)
    fig, ax = plt.subplots(figsize=(30, 8))
    ax.set_title(title)

    ax = sns.heatmap(df, cmap="jet",  xticklabels=31, yticklabels=120)
    cbar = ax.collections[0].colorbar
    # cbar.set_label(cbar_label, labelpad=30)
    cbar.ax.set_title(cbar_title)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    """ Y tick labels format HH:MM """
    yticklabels = ax.get_yticklabels()
    for lab in yticklabels:
        lab.set_text(lab.get_text()[:-3])
    ax.set_yticklabels(yticklabels)

    ax.set_xlabel("2016")
    ax.invert_yaxis()
    ax.tick_params(axis='y', which='major', pad=30)
    plt.xticks(rotation=0)
    # plt.tight_layout()
    # plt.savefig(f"{folder}/{col}.png")
    plt.show()
