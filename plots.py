import matplotlib.pyplot as plt


def plot_temperatures(iso, iso_mod):
    iso["t_out"].plot()
    iso_mod["t_out"].plot(label="t_out mod")
    iso["t_in"].plot(style="--")
    iso["t_amb"].plot(style="--")
    plt.legend()
    plt.ylabel("$Temperature \ (K)$")
    plt.xlabel("time (s)")
    plt.show()


def plot_deltas(iso, iso_mod):
    iso["delta_t"].plot(label="ISO")
    iso_mod["delta_t"].plot(label="ISO mod")
    plt.legend()
    plt.xlabel("time (s)")
    plt.ylabel("(K)")
    plt.title("$T_{out} - T_{in}$")
    plt.show()


def plot_delta_fraction(iso_dec, iso_mod_dec, tc_iso, val_iso, tc_iso_mod, val_iso_mod):
    iso_dec["delta_t_frac"].plot(label="ISO")
    iso_mod_dec["delta_t_frac"].plot(label="ISO mod")
    plt.plot(tc_iso, val_iso, "o")
    plt.plot(tc_iso_mod, val_iso_mod, "o")
    plt.xlabel("time (s)")
    plt.title("$\Delta T / \Delta T_0$")
    plt.legend()
    plt.show()
