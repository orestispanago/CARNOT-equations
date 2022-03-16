import pandas as pd
from annual import calc_tout, calc_qdot, calc_eff
import matplotlib.pyplot as plt
from scipy import stats

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



plt.plot(df['qdot'], solstice['qdot'], ',')
plt.xlabel('CARNOT')
plt.ylabel('Solstice')
plt.title('qdot (W)')
plt.show()

df['solstice_carnot'] = solstice['qdot'] -  df['qdot']

df['solstice_carnot'].resample("D").mean().plot()
plt.title("solstice - carnot")
plt.show()


df['zen'].resample("D").mean().plot()
plt.title('longitudinal incidence angle')
plt.show()


df['qdot'].resample("D").mean().plot()
solstice['qdot'].resample("D").mean().plot(label="solstice")
plt.legend()
plt.show()