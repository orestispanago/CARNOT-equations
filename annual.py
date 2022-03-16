from lookup.iam import kdir
import numpy as np
from scipy.integrate import odeint
import pandas as pd
import sys
import matplotlib.pyplot as plt
from plots import plot_temps, plot_power_eff, plot_kwh_timeseries, plot_calendar_heatmap

sys.path.append('../')

# CARNOT parameters
area = 1        # collector surface  (m2)
F_ta = 0.507    # F'(tau alfa)
c1 = 0.7153     # heat loss coefficient at (Tm-Ta)=0  [W/(m2*K)]
c2 = 0.00339    # temperature dependent heat loss coefficient [W/(m*K)²]
c5 = 675        # effective thermal capacity [J/(m²K)]

# my parameters
mdot = 80 / 3600    # mass flow rate (L/h to kg/s for water density=1000 kg/m3)
t_in_0 = 280          # water inlet temperature (K)
cp = 4200           # water heat capacity (J/kg*K)
final_time = 20     # final simulation time (s)


def iso_equation(Tm, t, transv, long, dni, t_amb, t_in):
    dTmdt = (F_ta*kdir(transv, long)*dni - c1 * (Tm - t_amb) -
             c2 * (Tm - t_amb)**2 - 2 * mdot*cp*(Tm - t_in)/area)/c5
    return dTmdt


def iso_equation_modified(Tout, t, transv, long, dni, t_amb, t_in):
    dToutdt = (F_ta*kdir(long, transv)*dni - c1 * (Tout + t_in-2*t_amb) -
               c2 * (Tout + t_in - 2*t_amb)**2 - mdot*cp*(Tout - t_in)/area)*2/c5
    return dToutdt


def iso_eq_mod_no_lookup(Tout, t, kdir_idir, t_amb, t_in):
    dToutdt = (F_ta*kdir_idir - c1 * (Tout + t_in-2*t_amb) -
               c2 * (Tout + t_in - 2*t_amb)**2 - mdot*cp*(Tout - t_in)/area)*2/c5
    return dToutdt


def calc_qdot(df):
    df['delta_t'] = df['t_out'] - df['t_in']
    df['qdot'] = mdot*cp/area*np.where(df['delta_t'] <= 1, 0, df['delta_t'])


def calc_eff(df):
    df['eff'] = df['qdot'] / df['dni']


def calc_tout(df):
    """ Solves ODE for each row in weather data file """
    t = np.arange(0, final_time)
    df['t_in'] = t_in_0
    df_arr = df.to_numpy()
    t_amb = df_arr[:, 4]
    kdir_idir = df_arr[:, 5]
    t_in = df_arr[:,6]
    tout = odeint(iso_eq_mod_no_lookup, t_in, t, args=(kdir_idir, t_amb, t_in))
    t_out = tout[-1, :]
    df['t_out'] = t_out



# plot_temps(df)
# plot_power_eff(df)

# plot_kwh_timeseries(df)

# # plot_calendar_heatmap(df, 'az', title='Transversal incidence angle', cbar_title="$\\theta_T \ (\degree)$")
# # plot_calendar_heatmap(df, 'zen', title='Longitudinal incidence angle', cbar_title="$\\theta_L \ (\degree)$")

# plot_calendar_heatmap(df, 'dni', title='$DNI$', cbar_title="$W \cdot m^{-2}$")
# plot_calendar_heatmap(df, 'kdir_idir', title='$K_{dir} \cdot DNI$', cbar_title="$W \cdot m^{-2}$")
# plot_calendar_heatmap(df, 'qdot', title='$\dot Q$', cbar_title="$W$")
# plot_calendar_heatmap(df, 'eff', title='Efficiency', cbar_title=" ")

