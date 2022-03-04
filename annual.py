from lookup.iam import kdir
from tqdm import tqdm
import numpy as np
from scipy.integrate import odeint
import pandas as pd
import sys
from plots import plot_temps, plot_power_eff

sys.path.append('../')

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
final_time = 20     # final simulation time (s)


def iso_equation_modified(Tout, t):
    dToutdt = (F_ta*kdir(transv, long)*dni - c1 * (Tout + t_in-2*t_amb) -
               c2 * (Tout + t_in - 2*t_amb)**2 - mdot*cp*(Tout - t_in)/area)*2/c5
    return dToutdt


def calc_qdot(df):
    df['qdot'] = mdot * cp * (df['t_out'] - df['t_in']) / area


def calc_eff(df):
    df['eff'] = df['qdot'] / df['dni']


def calc_delta(df):
    df['delta_t'] = df['t_out'] - df['t_in']


df = pd.read_csv("weather-data/2016_weather_upat.dat", sep="\t",
                 usecols=["az", "zen", "T", "dni"])
df = df.loc[(df['zen'] < 90) & (df["T"] > -10)]

# df.reset_index(drop=True, inplace=True)
df = df.rename(columns={"az": "transv", "zen": "long", "T": "t_amb"})
df['transv'] = abs(df['transv'])
df['transv'] = df['transv'].apply(lambda x: x if x < 90 else 180 - x)
df['t_amb'] = df['t_amb'] + 273
df['t_in'] = t_in

t = np.arange(0, final_time)

t_out_list = []
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    long, transv, dni, t_amb, t_in = row.tolist()
    t_out = odeint(iso_equation_modified, t_in, t)
    t_out_list.append(t_out[-1][0])
df["t_out"] = t_out_list

calc_qdot(df)
calc_delta(df)
calc_eff(df)
plot_temps(df)
plot_power_eff(df)

# CHECK this: kwh = df['qdot']/60000
