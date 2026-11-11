import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="HVAC Energy Optimization",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS - PROFESSIONAL UI
# =========================================================

st.markdown("""
<style>

    .main {
        background-color: #f5f7fa;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .dashboard-title {
        font-size: 38px;
        font-weight: 700;
        color: #172B4D;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        font-size: 17px;
        color: #6B778C;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 650;
        color: #172B4D;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .status-card {
        padding: 18px;
        border-radius: 12px;
        background-color: white;
        border: 1px solid #DFE1E6;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }

    .footer {
        text-align: center;
        color: #7A869A;
        font-size: 13px;
        padding: 25px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# GENERATE SYNTHETIC HVAC DATA
# =========================================================

np.random.seed(42)

time = pd.date_range(
    start="2026-09-01",
    periods=168,
    freq="h"
)

hours = np.arange(168)


# Temperature
temperature = (
    24
    + 4 * np.sin(hours * 2 * np.pi / 24)
    + np.random.normal(0, 0.8, 168)
)


# Humidity
humidity = (
    55
    + 10 * np.sin(hours * 2 * np.pi / 24 + 1)
    + np.random.normal(0, 2, 168)
)


# Occupancy
occupancy = np.random.randint(5, 50, 168)


# HVAC Power
hvac_power = (
    2.5
    + 0.25 * np.maximum(temperature - 23, 0)
    + 0.03 * occupancy
    + np.random.normal(0, 0.2, 168)
)

hvac_power = np.maximum(hvac_power, 0.5)


# =========================================================
# CREATE DATAFRAME
# =========================================================

df = pd.DataFrame({
    "Time": time,
    "Temperature": temperature,
    "Humidity": humidity,
    "Occupancy": occupancy,
    "HVAC Power": hvac_power
})

# 1-hour interval
df["Energy"] = df["HVAC Power"]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/air-conditioner.png",
        width=70
    )

    st.title("HVAC Control")

    st.markdown("---")

    st.subheader("Dashboard Filters")

    selected_day = st.selectbox(
        "Select Day",
        ["All Days"] +
        sorted(df["Time"].dt.strftime("%Y-%m-%d").unique().tolist())
    )

    st.markdown("---")

    st.subheader("System Information")

    st.write("**Data Source:** Synthetic IoT Data")
    st.write("**Sampling:** 1 hour")
    st.write("**Monitoring:** HVAC System")
    st.write("**Mode:** Analytics")


# =========================================================
# APPLY FILTER
# =========================================================

filtered_df = df.copy()

if selected_day != "All Days":

    filtered_df = df[
        df["Time"].dt.strftime("%Y-%m-%d") == selected_day
    ]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="dashboard-title">❄️ HVAC Energy Optimization</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'IoT-Based HVAC Monitoring & Energy Analytics Dashboard'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# CALCULATIONS
# =========================================================

latest = filtered_df.iloc[-1]

avg_temperature = filtered_df["Temperature"].mean()

avg_humidity = filtered_df["Humidity"].mean()

total_energy = filtered_df["Energy"].sum()

avg_occupancy = filtered_df["Occupancy"].mean()

peak_energy = filtered_df["Energy"].max()

peak_temperature = filtered_df["Temperature"].max()


# Estimated electricity cost
electricity_rate = 8

estimated_cost = total_energy * electricity_rate


# Estimated baseline consumption
baseline_energy = total_energy * 1.18

potential_saving = baseline_energy - total_energy

saving_percentage = (
    potential_saving / baseline_energy
) * 100


# =========================================================
# KPI CARDS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Live System Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "🌡️ Temperature",
    f"{latest['Temperature']:.1f} °C"
)

col2.metric(
    "💧 Humidity",
    f"{latest['Humidity']:.1f} %"
)

col3.metric(
    "⚡ Energy",
    f"{total_energy:.1f} kWh"
)

col4.metric(
    "👥 Occupancy",
    f"{latest['Occupancy']}"
)

col5.metric(
    "💰 Est. Cost",
    f"₹{estimated_cost:.0f}"
)


st.markdown("---")


# =========================================================
# HVAC STATUS
# =========================================================

st.markdown(
    '<div class="section-title">🌀 HVAC System Status</div>',
    unsafe_allow_html=True
)

status_col1, status_col2, status_col3 = st.columns(3)


with status_col1:

    if latest["Energy"] > 1:

        st.success("🟢 HVAC SYSTEM: ON")

    else:

        st.warning("🔴 HVAC SYSTEM: OFF")


with status_col2:

    st.info(
        f"⚡ Current Power: "
        f"{latest['HVAC Power']:.2f} kW"
    )


with status_col3:

    st.info(
        f"🔥 Peak Energy: "
        f"{peak_energy:.2f} kWh"
    )


# =========================================================
# TEMPERATURE + HUMIDITY
# =========================================================

st.markdown(
    '<div class="section-title">🌡️ Environmental Monitoring</div>',
    unsafe_allow_html=True
)

chart1, chart2 = st.columns(2)


with chart1:

    fig_temp = px.line(
        filtered_df,
        x="Time",
        y="Temperature",
        title="Temperature Trend",
        markers=True
    )

    fig_temp.update_layout(
        template="plotly_white",
        height=380,
        xaxis_title="Time",
        yaxis_title="Temperature (°C)"
    )

    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )


with chart2:

    fig_humidity = px.line(
        filtered_df,
        x="Time",
        y="Humidity",
        title="Humidity Trend",
        markers=True
    )

    fig_humidity.update_layout(
        template="plotly_white",
        height=380,
        xaxis_title="Time",
        yaxis_title="Humidity (%)"
    )

    st.plotly_chart(
        fig_humidity,
        use_container_width=True
    )


# =========================================================
# ENERGY ANALYTICS
# =========================================================

st.markdown(
    '<div class="section-title">⚡ Energy Analytics</div>',
    unsafe_allow_html=True
)


fig_energy = px.area(
    filtered_df,
    x="Time",
    y="Energy",
    title="HVAC Energy Consumption"
)

fig_energy.update_layout(
    template="plotly_white",
    height=420,
    xaxis_title="Time",
    yaxis_title="Energy (kWh)"
)

st.plotly_chart(
    fig_energy,
    use_container_width=True
)


# =========================================================
# OCCUPANCY VS ENERGY
# =========================================================

chart3, chart4 = st.columns(2)


with chart3:

    fig_occ = px.scatter(
        filtered_df,
        x="Occupancy",
        y="Energy",
        title="Occupancy vs HVAC Energy",
        size="HVAC Power",
        hover_data=[
            "Temperature",
            "Humidity"
        ]
    )

    fig_occ.update_layout(
        template="plotly_white",
        height=400
    )

    st.plotly_chart(
        fig_occ,
        use_container_width=True
    )


with chart4:

    fig_power = px.line(
        filtered_df,
        x="Time",
        y="HVAC Power",
        title="HVAC Power Consumption"
    )

    fig_power.update_layout(
        template="plotly_white",
        height=400,
        xaxis_title="Time",
        yaxis_title="Power (kW)"
    )

    st.plotly_chart(
        fig_power,
        use_container_width=True
    )


# =========================================================
# ENERGY PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">📈 Energy Performance</div>',
    unsafe_allow_html=True
)

perf1, perf2, perf3, perf4 = st.columns(4)


perf1.metric(
    "Average Temperature",
    f"{avg_temperature:.1f} °C"
)

perf2.metric(
    "Average Humidity",
    f"{avg_humidity:.1f} %"
)

perf3.metric(
    "Peak Energy",
    f"{peak_energy:.2f} kWh"
)

perf4.metric(
    "Potential Saving",
    f"{saving_percentage:.1f}%"
)


# =========================================================
# OPTIMIZATION RECOMMENDATION
# =========================================================

st.markdown(
    '<div class="section-title">🧠 Smart Optimization</div>',
    unsafe_allow_html=True
)


if latest["Occupancy"] < 15 and latest["Energy"] > 3:

    st.warning(
        "⚠️ High HVAC energy consumption detected "
        "during low occupancy. Consider reducing "
        "cooling output when the space is lightly occupied."
    )

elif latest["Temperature"] > 27:

    st.warning(
        "🔥 Temperature is above the preferred monitoring "
        "range. Cooling demand may be elevated."
    )

elif latest["Humidity"] > 70:

    st.warning(
        "💧 Humidity is relatively high. "
        "Consider checking HVAC dehumidification performance."
    )

else:

    st.success(
        "✅ HVAC operation is currently within the "
        "expected monitoring conditions."
    )


# =========================================================
# ALERTS
# =========================================================

st.markdown(
    '<div class="section-title"90>🚨 System Alerts</div>',
    unsafe_allow_html=True
)

alert_col1, alert_col2 = st.columns(2)


with alert_col1:

    if peak_temperature > 28:

        st.error(
            f"🌡️ High temperature detected: "
            f"{peak_temperature:.1f} °C"
        )

    else:

        st.success(
            "🌡️ Temperature levels are stable."
        )


with alert_col2:

    if peak_energy > 5:

        st.error(
            f"⚡ High energy consumption detected: "
            f"{peak_energy:.2f} kWh"
        )

    else:

        st.success(
            "⚡ Energy consumption is within monitored range."
        )


# =========================================================
# RAW SENSOR DATA
# =========================================================

st.markdown(
    '<div class="section-title">📋 IoT Sensor Data</div>',
    unsafe_allow_html=True
)

with st.expander("View Raw Sensor Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="footer">'
    'HVAC Energy Optimization | IoT Analytics | '
    'Python + Streamlit | Synthetic Sensor Data'
    '</div>',
    unsafe_allow_html=True
)