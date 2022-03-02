## CARNOT-equations

Solve CARNOT Simulink toolbox equations in python.

**Test case:** mirror array concentrating solar collector

CARNOT provides two options to model a flat plate solar collector. SI units are used for both cases.

### 1. ISO 9806 equation
$$
\begin{equation}
    \begin{split}
        \dot m C_p \frac{(T_{out} - T_{in})}{A} & = F'\tau \alpha K_{dir} I_{dir} + F'\tau \alpha K_{dfu} I_{dfu} - c_1 (T_m - T_{amb}) \\
        & - c_2 (T_m - T_{amb})^2 - c_3 v_w (T_m - T_{amb}) - c_6 v_w I_{glb} \\
        & + c_4 (\epsilon_{longwave} - \sigma_{SB} T_{amb}^4) - c_5 \frac{dT_m}{dt}
    \end{split}
\end{equation}
$$


For our test case, $I_{dfu} = c_3 = c_4 = c_6 = 0$:

$$
\begin{equation}
    \dot m C_p \frac{(T_{out} - T_{in})}{A}  = F'\tau \alpha K_{dir} I_{dir} - c_1 (T_m - T_{amb}) - c_2 (T_m - T_{amb})^2 - c_5 \frac{dT_m}{dt}
\end{equation}
$$

Substituting $T_{out} = 2T_m -Tin$ and solving for $\frac{dT_m}{dt}$ we get:


$$
\begin{equation}
    \begin{split}
         \frac{dT_m}{dt} & = \frac{1}{c_5} [F'\tau \alpha K_{dir} I_{dir} - c_1 (T_m - T_{amb}) - c_2 (T_m - T_{amb})^2 -2 \frac{\dot m C_p}{A} (T_{m} - T_{in})]
    \end{split}
\end{equation}
$$

where $K_{dir} = K_b(\theta_{lon}) \cdot K_b(\theta_{transv})$

### 2. Modified ISO equation
$$
\begin{equation}
    \begin{split}
        \dot m C_p \frac{(T_{out} - T_{in})}{A} & = F'\tau \alpha K_{dir} I_{dir} + F'\tau \alpha K_{dfu} I_{dfu} - c_1 (T_m - T_{amb}) \\
        & - c_2 (T_m - T_{amb})^2 - c_3 v_w (T_m - T_{amb}) - c_6 v_w I_{glb} \\
        & + c_4 (\epsilon_{longwave} - \sigma_{SB} T_{amb}^4) - \frac{c_5}{2} \frac{dT_{out}}{dt}
    \end{split}
\end{equation}
$$

Removing zero terms and solving for $\frac{dT_{out}}{dt}$ we get:

$$
\begin{equation}
    \begin{split}
         \frac{dT_{out}}{dt} & = \frac{2}{c_5} [F'\tau \alpha K_{dir} I_{dir} - c_1 (T_{out} +T_{in} - 2T_{amb}) \\ 
         & - c_2 (T_{out} +T_{in} - 2T_{amb})^2 - \frac{\dot m C_p}{A} (T_{out} - T_{in})]
    \end{split}
\end{equation}
$$