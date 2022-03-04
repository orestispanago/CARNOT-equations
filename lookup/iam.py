from scipy.interpolate import interp1d

angles = [0, 10, 20, 30, 40, 50, 60, 70, 90]  # (degrees)
kbL = [1, 1, 1, 0.99, 0.98, 0.96, 0.93, 0.87, 0]  # longitudinal IAM
kbT = [1, 1.01, 1.04, 1.07, 1.09, 1.14, 1.22, 1.24, 0]  # transversal IAM

kbT_spline = interp1d(angles, kbT, kind='cubic')
kbL_spline = interp1d(angles, kbL, kind='cubic')


def kbt(angle_transv):
    return kbT_spline(angle_transv)


def kbl(angle_long):
    return kbL_spline(angle_long)


def kdir(angle_long, angle_transv):
    return kbl(angle_long)*kbt(angle_transv)
