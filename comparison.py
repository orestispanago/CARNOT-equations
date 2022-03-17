import pandas as pd
from annual import calc_tout, calc_qdot, calc_eff
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


def plot_scatter(x, y, xlabel="", ylabel="", title=""):
    mask = ~np.isnan(x) & ~np.isnan(y)
    regresults = stats.linregress(x[mask], y[mask])
    plt.plot(x, y, ',')
    plt.plot(x, regresults.slope*x + regresults.intercept, 'r',
             label=f'{regresults.slope:.2f}x + {regresults.intercept:.2f}')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()


df = pd.read_csv('input/preproc_tilt38_kdir_idir_07_14.csv', index_col='time',
                 parse_dates=True)
solstice = pd.read_csv('input/preproc_tilt38_solstice_07_14.csv', index_col='time',
                       parse_dates=True)
calc_tout(df)
calc_qdot(df)
calc_eff(df)

calc_tout(solstice)
calc_qdot(solstice)
calc_eff(solstice)

annual_energy_yield = df['qdot'].sum()/60000
print(f"Annual energy yield: {annual_energy_yield:.2f} kWh")

annual_energy_yield = solstice['qdot'].sum()/60000
print(f"Solstice Annual energy yield: {annual_energy_yield:.2f} kWh")


plot_scatter(df['qdot'], solstice['qdot'], xlabel='CARNOT',
             ylabel='Solstice', title='qdot (W)')

df['solstice_carnot'] = solstice['qdot'] - df['qdot']

df['solstice_carnot'].resample("D").mean().plot()
plt.title("solstice - carnot")
plt.show()


df['zen'].resample("D").mean().plot()
plt.title('longitudinal incidence angle')
plt.show()

(solstice['kdir_idir'] - df['dni']).resample('D').mean().plot()
plt.show()

plot_scatter(df['dni'], solstice['kdir_idir'])
