import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Nuclear Reactor Safety Simulator", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #111111; color: white; }
h1, h2, h3, p, label { color: white; }
[data-testid="stMetricValue"] { color: white; }
.reactor-box {
    border: 3px solid white;
    border-radius: 20px;
    padding: 25px;
    background-color: #1b1b1b;
}
.core {
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
.rod {
    background: #3333ff;
    width: 35px;
    display: inline-block;
    margin: 10px;
    border: 2px solid white;
}
.statusbox {
    padding: 20px;
    border-radius: 10px;
    background-color: #222222;
    border: 2px solid #444444;
}
</style>
""", unsafe_allow_html=True)

st.title("Nuclear Reactor Safety Simulator")
st.write("Simplified educational model — not a real reactor simulation.")

rod = st.sidebar.slider("Control Rod Insertion (%)", 0, 100, 45)
cooling = st.sidebar.slider("Coolant Flow (%)", 0, 100, 50)
start_power = st.sidebar.slider("Starting Power (%)", 10, 100, 45)
shutdown = st.sidebar.button("Emergency Shutdown")

rod_fraction = rod / 100
cooling_fraction = cooling / 100
power = start_power / 100
temperature = 250

if shutdown:
    rod_fraction = 1.0
    rod = 100

times = []
powers = []
temps = []

dt = 0.05
steps = 500

for i in range(steps):
    t = i * dt

    reactivity = 0.06 - 0.12 * rod_fraction
    power += reactivity * power * dt
    power = max(0, min(power, 2.0))

    heat_generated = 18 * power
    heat_removed = cooling_fraction * 8 * ((temperature - 250) / 100)

    temperature += (heat_generated - heat_removed) * dt
    temperature = max(250, temperature)

    if temperature > 850:
        rod_fraction = 1.0
        rod = 100

    times.append(t)
    powers.append(power * 100)
    temps.append(temperature)

final_power = powers[-1]
final_temp = temps[-1]

if final_temp < 500:
    status = "Stable"
    status_colour = "lime"
elif final_temp < 850:
    status = "Warning"
    status_colour = "orange"
else:
    status = "Emergency Shutdown"
    status_colour = "red"

left, right = st.columns([2, 1])

with left:
    st.markdown("<div class='reactor-box'>", unsafe_allow_html=True)
    st.subheader("Simplified Nuclear Reactor Model")

    rod_height = int(40 + rod * 2)

    st.markdown(f"""
    <div style="text-align:center;">
        <p><b>Control Rods</b></p>
        <div class="rod" style="height:{rod_height}px;"></div>
        <div class="rod" style="height:{rod_height}px;"></div>
        <div class="rod" style="height:{rod_height}px;"></div>
        <div class="rod" style="height:{rod_height}px;"></div>
        <br><br>
        <div class="core">CORE</div>
        <br>
        <p style="color:cyan;">Coolant In → Reactor Core → Coolant Out</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress(min(int(final_power), 100), text=f"Power Output: {final_power:.0f}%")
    st.progress(min(int((final_temp - 250) / 8), 100), text=f"Core Temperature: {final_temp:.0f} °C")

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='statusbox'>", unsafe_allow_html=True)
    st.header("Control Panel")
    st.markdown(f"<h2 style='color:{status_colour};'>Status: {status}</h2>", unsafe_allow_html=True)
    st.metric("Core Temperature", f"{final_temp:.0f} °C")
    st.metric("Power Output", f"{final_power:.0f}%")
    st.metric("Control Rod Insertion", f"{rod}%")
    st.metric("Coolant Flow", f"{cooling}%")
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
ax2.set_title("Core Temperature Over Time")
ax2.set_xlabel("Time")
ax2.set_ylabel("Temperature (°C)")
st.pyplot(fig2)
