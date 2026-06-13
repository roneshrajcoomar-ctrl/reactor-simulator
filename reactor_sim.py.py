import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Educational Reactor Simulator", layout="wide")

st.title("Educational Reactor Simulator")
st.write("This is a simplified educational simulation and is not a real reactor model.")

rod = st.sidebar.slider("Control Rod Insertion", 0.0, 1.0, 0.45, 0.01)
cooling = st.sidebar.slider("Cooling Strength", 0.005, 0.08, 0.02, 0.001)
start_power = st.sidebar.slider("Starting Power", 0.1, 5.0, 1.0, 0.1)
shutdown_temp = st.sidebar.slider("Emergency Shutdown Temperature", 400, 1200, 800, 10)

dt = 0.02
total_time = 80
steps = int(total_time / dt)

power = start_power
temperature = 300

times = []
powers = []
temps = []
rod_positions = []

for i in range(steps):
    t = i * dt
    current_rod = rod

    if temperature > shutdown_temp:
        current_rod = 1.0

    reactivity = 0.08 - 0.15 * current_rod

    power += reactivity * power * dt
    power = max(power, 0)

    heat_generated = 20 * power
    heat_removed = cooling * (temperature - 300)

    temperature += (heat_generated - heat_removed) * dt

    times.append(t)
    powers.append(power)
    temps.append(temperature)
    rod_positions.append(current_rod)

col1, col2, col3 = st.columns(3)

col1.metric("Power", f"{powers[-1]:.2f}")
col2.metric("Temperature", f"{temps[-1]:.0f} K")
col3.metric("Rod Position", f"{rod_positions[-1]*100:.0f}%")

if temps[-1] < 600:
    st.success("Status: Stable")
elif temps[-1] < shutdown_temp:
    st.warning("Status: Heating Up")
else:
    st.error("Status: Emergency Shutdown Triggered")

fig1, ax1 = plt.subplots()
ax1.plot(times, powers)
ax1.set_title("Reactor Power")
ax1.set_xlabel("Time")
ax1.set_ylabel("Power")
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.plot(times, temps)
ax2.axhline(shutdown_temp, linestyle="--")
ax2.set_title("Temperature")
ax2.set_xlabel("Time")
ax2.set_ylabel("Temperature (K)")
st.pyplot(fig2)

fig3, ax3 = plt.subplots()
ax3.plot(times, rod_positions)
ax3.set_title("Control Rod Position")
ax3.set_xlabel("Time")
ax3.set_ylabel("Insertion")
st.pyplot(fig3)
