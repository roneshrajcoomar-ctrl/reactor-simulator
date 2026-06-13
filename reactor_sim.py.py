import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Nuclear Reactor Safety Simulator", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #0f0f0f;
    color: white;
}
section[data-testid="stSidebar"] {
    background-color: #1f1f1f;
}
section[data-testid="stSidebar"] * {
    color: white !important;
    font-size: 16px !important;
}
h1, h2, h3, p, label {
    color: white !important;
}
[data-testid="stMetricValue"] {
    color: white !important;
}
.reactor-box {
    border: 3px solid white;
    padding: 25px;
    background-color: #111111;
}
.control-box {
    border: 2px solid #444;
    padding: 25px;
    background-color: #1b1b1b;
}
.core-normal {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: orange;
    margin: auto;
    text-align: center;
    line-height: 180px;
    font-size: 32px;
    font-weight: bold;
    color: black;
}
.core-meltdown {
    width: 220px;
    height: 220px;
    border-radius: 50%;
    background: red;
    margin: auto;
    text-align: center;
    line-height: 220px;
    font-size: 34px;
    font-weight: bold;
    color: yellow;
    animation: pulse 0.8s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 10px red; }
    50% { box-shadow: 0 0 60px orange; }
    100% { box-shadow: 0 0 10px red; }
}
.rod {
    background: #3333ff;
    width: 35px;
    display: inline-block;
    margin: 8px;
    border: 2px solid white;
}
.warning-text {
    color: red;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    animation: blink 0.8s infinite;
}
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0.2; }
    100% { opacity: 1; }
}
.particle {
    display: inline-block;
    width: 22px;
    height: 22px;
    margin: 6px;
    border-radius: 50%;
    background: yellow;
    animation: shake 0.4s infinite;
}
.hot-particle {
    display: inline-block;
    width: 26px;
    height: 26px;
    margin: 6px;
    border-radius: 50%;
    background: red;
    animation: shake 0.2s infinite;
}
@keyframes shake {
    0% { transform: translate(0px, 0px); }
    25% { transform: translate(4px, -3px); }
    50% { transform: translate(-3px, 4px); }
    75% { transform: translate(3px, 3px); }
    100% { transform: translate(0px, 0px); }
}
</style>
""", unsafe_allow_html=True)

st.title("Nuclear Reactor Safety Simulator")
st.write("Simplified educational model — not a real reactor simulation.")

rod = st.sidebar.slider("Control Rod Insertion (%)", 0, 100, 20)
cooling = st.sidebar.slider("Coolant Flow (%)", 0, 100, 50)
start_power = st.sidebar.slider("Starting Power (%)", 10, 150, 80)
meltdown_limit = st.sidebar.slider("Meltdown Temperature (°C)", 600, 1200, 900)

shutdown = st.sidebar.button("Emergency Shutdown")
reset = st.sidebar.button("Reset Simulation")

if shutdown:
    rod = 100
    cooling = 100

rod_fraction = rod / 100
cooling_fraction = cooling / 100
power = start_power / 100
temperature = 250

times = []
powers = []
temps = []

dt = 0.05
steps = 600

meltdown = False

for i in range(steps):
    t = i * dt

    reactivity = 0.09 - 0.16 * rod_fraction
    power += reactivity * power * dt
    power = max(0, min(power, 2.5))

    heat_generated = 22 * power
    heat_removed = cooling_fraction * 10 * ((temperature - 250) / 100)

    temperature += (heat_generated - heat_removed) * dt
    temperature = max(250, temperature)

    if temperature >= meltdown_limit:
        meltdown = True
        power = max(power, 1.0)

    times.append(t)
    powers.append(power * 100)
    temps.append(temperature)

final_power = powers[-1]
final_temp = temps[-1]

if meltdown:
    status = "MELTDOWN CONDITION REACHED"
    status_colour = "red"
elif final_temp > meltdown_limit * 0.75:
    status = "Warning"
    status_colour = "orange"
else:
    status = "Stable"
    status_colour = "lime"

left, right = st.columns([2, 1])

with left:
    st.markdown("<div class='reactor-box'>", unsafe_allow_html=True)
    st.subheader("Simplified Nuclear Reactor Model")

    if meltdown:
        st.markdown("<div class='warning-text'>⚠ MELTDOWN CONDITION REACHED ⚠</div>", unsafe_allow_html=True)

    rod_height = int(60 + rod * 2)

    st.markdown("<div style='text-align:center;'><b>Control Rods</b><br>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="rod" style="height:{rod_height}px;"></div>
        <div class="rod" style="height:{rod_height}px;"></div>
        <div class="rod" style="height:{rod_height}px;"></div>
        <div class="rod" style="height:{rod_height}px;"></div>
    """, unsafe_allow_html=True)

    if meltdown:
        st.markdown("<br><div class='core-meltdown'>CORE</div>", unsafe_allow_html=True)
        particles = ""
        for n in range(30):
            if n % 2 == 0:
                particles += "<span class='hot-particle'></span>"
            else:
                particles += "<span class='particle'></span>"
        st.markdown(f"<div style='text-align:center; margin-top:20px;'>{particles}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<br><div class='core-normal'>CORE</div>", unsafe_allow_html=True)

    st.markdown("<p style='color:cyan; text-align:center;'>Coolant In → Reactor Core → Coolant Out</p>", unsafe_allow_html=True)

    st.progress(min(int(final_power), 100), text=f"Power Output: {final_power:.0f}%")
    st.progress(min(int((final_temp - 250) / 8), 100), text=f"Core Temperature: {final_temp:.0f} °C")

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='control-box'>", unsafe_allow_html=True)
    st.header("Control Panel")
    st.markdown(f"<h2 style='color:{status_colour};'>Status: {status}</h2>", unsafe_allow_html=True)
    st.metric("Core Temperature", f"{final_temp:.0f} °C")
    st.metric("Power Output", f"{final_power:.0f}%")
    st.metric("Control Rod Insertion", f"{rod}%")
    st.metric("Coolant Flow", f"{cooling}%")

    st.write("Teaching model:")
    st.write("- Fewer rods = higher reaction rate")
    st.write("- More coolant = more heat removed")
    st.write("- Excess heat can trigger meltdown condition")
    st.write("- Emergency shutdown inserts rods and increases coolant")

    st.markdown("</div>", unsafe_allow_html=True)

st.subheader("Simulation Graphs")

fig1, ax1 = plt.subplots()
ax1.plot(times, powers)
ax1.set_title("Power Output Over Time")
ax1.set_xlabel("Time")
ax1.set_ylabel("Power (%)")
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.plot(times, temps)
ax2.axhline(meltdown_limit, linestyle="--")
ax2.set_title("Core Temperature Over Time")
ax2.set_xlabel("Time")
ax2.set_ylabel("Temperature (°C)")
st.pyplot(fig2)
