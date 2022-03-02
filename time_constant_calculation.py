import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.integrate import odeint

from plots import plot_delta_fraction, plot_deltas, plot_temperatures
from splines import kdir

# CARNOT parameters
area = 1        # collector surface  (m2)
F_ta = 0.507    # F'(tau alfa)
c1 = 0.7153     # heat loss coefficient at (Tm-Ta)=0  [W/(m2*K)]
c2 = 0.00339    # temperature dependent heat loss coefficient [W/(m*K)²]
c5 = 675        # effective thermal capacity [J/(m²K)]

# my parameters
mdot = 80 / 3600    # mass flow rate (L/h to kg/s for water density=1000 kg/m3)
t_amb = 300         # ambient temperature (K)
t_in = 290          # water inlet temperature (K)
cp = 4200           # water heat capacity (J/kg*K)
idir_0 = 800        # initial solar radiation intensity (W/m2)
trigger_time = 40   # time to trigger step down function (s)
final_time = 60     # final simulation time (s)


def step_down(t, trigger_time):
    return 1 * (t < trigger_time)


def Idir(t):
    return step_down(t, trigger_time)*idir_0


def iso_equation(Tm, t):
    dTmdt = (F_ta*kdir(0, 0)*Idir(t) - c1 * (Tm - t_amb) -
             c2 * (Tm - t_amb)**2 - 2 * mdot*cp*(Tm - t_in)/area)/c5
    return dTmdt


def iso_equation_modified(Tout, t):
    dToutdt = (F_ta*kdir(0, 0)*Idir(t) - c1 * (Tout + t_in-2*t_amb) -
               c2 * (Tout + t_in - 2*t_amb)**2 - 2 * mdot*cp*(Tout - t_in)/area)*2/c5
    return dToutdt


def calc_time_constant(df):
    """ Time (s) to decrease Tout-Tin to 1/e of its initial value """
    time_constant = df[df['delta_t_frac'].lt(1/np.exp(1))].index[0]
    value = df["delta_t_frac"].iloc[time_constant]
    return time_constant, value


def calc_delta(df):
    df["delta_t"] = df["t_out"] - df["t_in"]


def calc_delta_frac(df):
    df["delta_t_frac"] = df["delta_t"] / df["delta_t"][0]


t = np.arange(0, final_time)

tm = odeint(iso_equation, t_in, t)
t_out = 2*tm - t_in

t_out_mod = odeint(iso_equation_modified, t_in, t)


iso = pd.DataFrame(data={"time": t, "irr": Idir(t), "t_in": t_in,
                         "t_amb": t_amb, "t_out": t_out.flatten()})

iso_mod = iso.copy()
iso_mod["t_out"] = t_out_mod

calc_delta(iso)
calc_delta(iso_mod)

plot_temperatures(iso, iso_mod)
plot_deltas(iso, iso_mod)


iso_dec = iso.iloc[trigger_time:].reset_index(drop=True)
iso_mod_dec = iso_mod.iloc[trigger_time:].reset_index(drop=True)

calc_delta_frac(iso_dec)
calc_delta_frac(iso_mod_dec)

tc_iso, val_iso = calc_time_constant(iso_dec)
tc_iso_mod, val_iso_mod = calc_time_constant(iso_mod_dec)

print(f"time constant ISO: \t\t {tc_iso} s")
print(f"time constant ISO mod: \t {tc_iso_mod} s")

plot_delta_fraction(iso_dec, iso_mod_dec, tc_iso,
                    val_iso, tc_iso_mod, val_iso_mod)
