import numpy as np
import pandas as pd
from scipy.integrate import odeint
import matplotlib.pyplot as plt

import sys
sys.path.append('../')
params = {
           'savefig.dpi': 150,
          }
plt.rcParams.update(params)

from lookup.iam import kdir

area = 1        # collector surface  (m2)
F_ta = 0.507    # F'(tau alfa)
c1 = 0.7153     # heat loss coefficient at (Tm-Ta)=0  [W/(m2*K)]
c2 = 0.00339    # temperature dependent heat loss coefficient [W/(m*K)²]
c5 = 675        # effective thermal capacity [J/(m²K)]

mdot = 80 / 3600    # mass flow rate (L/h to kg/s for water density=1000 kg/m3)
t_amb = 300         # ambient temperature (K)
t_in = 290          # water inlet temperature (K)
cp = 4200           # water heat capacity (J/kg*K)
idir_0 = 800        # initial solar radiation intensity (W/m2)
trigger_time = 40   # time to trigger step down function (s)
final_time = 60     # final simulation time (s)


def plot_temperatures(iso):
    iso["t_out"].plot(label="$T_{out}$")
    iso["t_in"].plot(style="--", label="$T_{in}$")
    iso["t_amb"].plot(style="--", label="$T_{amb}$")
    plt.title("Temperatures")
    plt.legend()
    plt.ylabel("$(K)$")
    plt.xlabel("time (s)")
    plt.grid()
    plt.savefig("temperatures.png")
    plt.show()
    
    
def plot_delta(iso):
    iso["delta_t"].plot()
    plt.xlabel("time (s)")
    plt.ylabel("(K)")
    plt.title("$T_{out} - T_{in}$")
    plt.grid()
    plt.savefig("delta_t.png")
    plt.show()



def plot_delta_fraction(iso_dec, tc, tc_dfrac, t95, t95_dfrac):
    iso_dec["delta_t_frac"].plot()
    plt.plot(tc, tc_dfrac, "o")
    plt.plot(t95, t95_dfrac, "o")
    plt.xlabel("time (s)")
    plt.title("$\Delta T / \Delta T_0$")
    plt.annotate(f"< 1/e ({tc}, {tc_dfrac:.3f})", (tc+1, tc_dfrac+0.1))
    plt.annotate(f"< 5% ({t95}, {t95_dfrac:.3f})", (t95+1, t95_dfrac+0.1))
    plt.grid()
    plt.savefig("delta_frac.png")
    plt.show()

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
               c2 * (Tout + t_in - 2*t_amb)**2 - mdot*cp*(Tout - t_in)/area)*2/c5
    return dToutdt


def calc_decrease_time(df, threshold=1/np.exp(1)):
    """ Time (s) to decrease Tout-Tin to 1/threshold of its initial value """
    dec_time = df[df['delta_t_frac'].lt(threshold)].index[0]
    delta_frac_value = df["delta_t_frac"].iloc[dec_time]
    return dec_time, delta_frac_value


def calc_delta(df):
    df["delta_t"] = df["t_out"] - df["t_in"]


def calc_delta_frac(df):
    df["delta_t_frac"] = df["delta_t"] / df["delta_t"][0]


t = np.arange(0, final_time)

tm = odeint(iso_equation, t_in, t)
t_out = 2*tm - t_in

iso = pd.DataFrame(data={"time": t, "irr": Idir(t), "t_in": t_in,
                         "t_amb": t_amb, "t_out": t_out.flatten()})

calc_delta(iso)

plot_temperatures(iso)
plot_delta(iso)
# plot_deltas(iso)

iso_dec = iso.iloc[trigger_time:].reset_index(drop=True)

calc_delta_frac(iso_dec)
tc, tc_dfrac = calc_decrease_time(iso_dec)
t95, t95_dfrac = calc_decrease_time(iso_dec, threshold=5/100)


print(f"Time constant : \t\t {tc} s")
print(f"Time @$\Delta T / \Delta T_0$ < 95% : \t\t {t95} s")

plot_delta_fraction(iso_dec, tc, tc_dfrac, t95, t95_dfrac)
