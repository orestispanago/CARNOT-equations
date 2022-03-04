import matplotlib.pyplot as plt


def plot_temps(df):
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
