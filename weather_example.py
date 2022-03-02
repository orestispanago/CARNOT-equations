import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import odeint

from splines import kdir

# CARNOT parameters
area = 1        # collector surface  (m2)
F_ta = 0.507    # F'(tau alfa)
c1 = 0.7153     # heat loss coefficient at (Tm-Ta)=0  [W/(m2*K)]
c2 = 0.00339    # temperature dependent heat loss coefficient [W/(m*K)²]
c5 = 675        # effective thermal capacity [J/(m²K)]

# my parameters
mdot = 80 / 3600    # mass flow rate (L/h to kg/s for water density=1000 kg/m3)
t_in = 280          # water inlet temperature (K)
cp = 4200           # water heat capacity (J/kg*K)
final_time = 60     # final simulation time (s)


def iso_equation(Tm, t):
    dTmdt = (F_ta*kdir(az, zen)*dni - c1 * (Tm - t_amb) -
             c2 * (Tm - t_amb)**2 - 2 * mdot*cp*(Tm - t_in)/area)/c5
    return dTmdt


def iso_equation_modified(Tout, t):
    dToutdt = (F_ta*kdir(az, zen)*dni - c1 * (Tout + t_in-2*t_amb) -
               c2 * (Tout + t_in - 2*t_amb)**2 -  mdot*cp*(Tout - t_in)/area)*2/c5
    return dToutdt


def plot_temps():
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    df_all_iso['t_out'].plot(label='ISO')
    df_all_iso_mod['t_out'].plot(label='ISO mod')
    plt.legend()
    plt.title('$T_{out}$')
    plt.ylabel("$(K)$")
    plt.xlabel("time (s)")

    plt.subplot(1, 3, 2)
    df_all_iso['t_in'].plot(label="t_in")
    df_all_iso['t_amb'].plot(label="t_amb")
    plt.legend()
    plt.ylabel("$(K)$")
    plt.xlabel("time (s)")

    plt.subplot(1, 3, 3)
    df_all_iso['delta_t'].plot(label='ISO')
    df_all_iso_mod['delta_t'].plot(label='ISO mod')
    plt.legend()
    plt.title('$T_{out} - T_{in}$')
    plt.ylabel("$(K)$")
    plt.xlabel("time (s)")

    plt.tight_layout()
    plt.show()


def plot_power_eff():
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    df_all_iso['irr'].plot(label='ISO')
    plt.title("DNI")
    plt.ylabel("$(W \cdot m^{-2})$")
    plt.xlabel("time (s)")

    plt.subplot(1, 3, 2)
    df_all_iso['qdot'].plot(label='ISO')
    df_all_iso_mod['qdot'].plot(label='ISO mod')
    plt.legend()
    plt.title("$\dot Q$")
    plt.ylabel("$(W)$")
    plt.xlabel("time (s)")

    plt.subplot(1, 3, 3)
    df_all_iso['eff'].plot(label='ISO')
    df_all_iso_mod['eff'].plot(label='ISO mod')
    plt.legend()
    plt.title("Efficiency")

    plt.xlabel("time (s)")
    plt.tight_layout()
    plt.show()


def calc_qdot(df):
    df['qdot'] = mdot * cp * (df['t_out'] - df['t_in']) / area


def calc_eff(df):
    df['eff'] = df['qdot'] / df['irr']


def calc_delta(df):
    df['delta_t'] = df['t_out'] / df['t_in']


df = pd.read_csv("weather-data/2016_weather_upat.dat", sep="\t",
                 usecols=["az", "zen", "T", "dni"], nrows=560)
df = df.loc[(df['zen'] < 90) & (df["T"] > -10)]
df['az'] = abs(df['az'])
df['T'] = df['T'] + 273
df.reset_index(drop=True, inplace=True)

df = df[150:155]  # select rows with DNI about 800 W

iso_list = []
iso_mod_list = []
for index, row in df.iterrows():
    zen, az, dni, t_amb = row.tolist()
    t = np.arange(0, final_time)
    tm = odeint(iso_equation, t_in, t)
    t_out = 2*tm - t_in
    t_out_mod = odeint(iso_equation_modified, t_in, t)
    iso = pd.DataFrame(data={"time": t, "irr": dni, "t_in": t_in,
                             "t_amb": t_amb, "t_out": t_out.flatten()})
    iso_mod = iso.copy()
    iso_mod["t_out"] = t_out_mod
    iso_list.append(iso)
    iso_mod_list.append(iso_mod)

df_all_iso = pd.concat(iso_list, ignore_index=True)
df_all_iso_mod = pd.concat(iso_mod_list, ignore_index=True)

calc_qdot(df_all_iso)
calc_eff(df_all_iso)
calc_delta(df_all_iso)

calc_qdot(df_all_iso_mod)
calc_eff(df_all_iso_mod)
calc_delta(df_all_iso_mod)


plot_temps()
plot_power_eff()
