import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(
    page_title="Fugacity Calculator — Material Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Custom CSS (Material-ish)
# -------------------------
st.markdown(
    """
    <style>
    /* Page background */
    .stApp {
        background: linear-gradient(180deg, #f6fbff 0%, #ffffff 100%);
        color: #0d1b2a;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    /* Card */
    .card {
        background: white;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(16,24,40,0.06);
        border: 1px solid rgba(16,24,40,0.04);
    }
    .sidebar .stButton>button {
        border-radius: 8px;
    }
    /* Header */
    .big-title {
        color: #0d47a1;
        font-weight: 700;
        font-size: 26px;
        margin-bottom: 6px;
    }
    .subtitle {
        color: #243b55;
        margin-top: -6px;
        margin-bottom: 14px;
    }
    /* Table header */
    .stDataFrame thead th {
        background-color: #1e88e5 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Gas database
# -------------------------
GAS_DB = {
    "Carbon Dioxide (CO2)": {"Tc": 304.2, "Pc": 73.8, "omega": 0.225},
    "Methane (CH4)": {"Tc": 190.6, "Pc": 45.99, "omega": 0.011},
    "Nitrogen (N2)": {"Tc": 126.2, "Pc": 33.5, "omega": 0.037},
    "Oxygen (O2)": {"Tc": 154.6, "Pc": 50.4, "omega": 0.022},
    "Hydrogen (H2)": {"Tc": 33.2, "Pc": 12.8, "omega": -0.22},
    "Ammonia (NH3)": {"Tc": 405.5, "Pc": 113.5, "omega": 0.256},
    "Custom": {"Tc": 300.0, "Pc": 50.0, "omega": 0.1},
}

# -------------------------
# Sidebar: inputs
# -------------------------
with st.sidebar:
    st.markdown("<div style='text-align:center'><img src='https://img.icons8.com/ios-filled/80/1e88e5/thermometer.png'/></div>", unsafe_allow_html=True)
    st.header("Inputs — Material Dashboard")
    selected_gas = st.selectbox("Select gas", list(GAS_DB.keys()))

    Tc = st.number_input("Critical Temp Tc [K]", value=GAS_DB[selected_gas]["Tc"], format="%.3f")
    Pc = st.number_input("Critical Pressure Pc [bar]", value=GAS_DB[selected_gas]["Pc"], format="%.3f")
    omega = st.number_input("Acentric factor ω", value=GAS_DB[selected_gas]["omega"], format="%.4f")

    st.markdown("---")
    st.subheader("Operating conditions")
    T = st.number_input("Temperature T [K]", value=300.0, format="%.3f")
    P = st.number_input("Pressure P [bar]", value=10.0, format="%.3f")

    y = st.slider("Mole fraction / concentration (y)", min_value=0.0, max_value=1.0, value=1.0, step=0.01)

    calc_button = st.button("Calculate — Run Analysis")

    st.markdown("\n---\nMade for engineering workflows.\n")

# -------------------------
# Pitzer correlation
# -------------------------
R = 0.08314  # L·bar/(mol·K)


def pitzer_fugacity(T, P, Tc, Pc, omega):
    """Return dictionary of intermediate and final results using the simple Pitzer form used previously."""
    Tr = T / Tc
    Pr = P / Pc

    # B0 and B1 correlations (simple forms) — keep same as original
    B0 = 0.083 - (0.422 / (Tr ** 1.6))
    B1 = 0.139 - (0.172 / (Tr ** 4.2))

    ln_phi = (Pr / Tr) * (B0 + omega * B1)
    phi = np.exp(ln_phi)
    fugacity = phi * P

    return {
        "Tr": Tr,
        "Pr": Pr,
        "B0": B0,
        "B1": B1,
        "ln_phi": ln_phi,
        "phi": phi,
        "fugacity": fugacity,
    }

# -------------------------
# Main layout
# -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div style='display:flex; align-items:center; justify-content:space-between'>", unsafe_allow_html=True)
st.markdown("<div style='padding-right:16px'><h1 class='big-title'>Fugacity & Fugacity Coefficient Calculator</h1><div class='subtitle'>Material-style engineering dashboard for Pitzer correlation</div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div><br/>", unsafe_allow_html=True)

# Tabs for organization
tab_calc, tab_results, tab_theory = st.tabs(["Calculator", "Results & Plots", "Theory & References"])

with tab_calc:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Calculation Controls")
    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        st.metric(label="Selected gas", value=selected_gas)
        st.write("Tc (K):", f"{Tc:.3f}")
        st.write("Pc (bar):", f"{Pc:.3f}")

    with c2:
        st.metric(label="Operating T [K]", value=f"{T:.2f}")
        st.metric(label="Operating P [bar]", value=f"{P:.2f}")

    with c3:
        st.metric(label="Mole fraction y", value=f"{y:.2f}")
        if st.button("Reset to defaults"):
            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with tab_results:
    if calc_button:
        results = pitzer_fugacity(T, P, Tc, Pc, omega)
        fug_adj = results["fugacity"] * y

        # Top-level KPIs
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        k1.metric(label="Fugacity coefficient φ", value=f"{results['phi']:.5f}")
        k2.metric(label="Fugacity f [bar]", value=f"{fug_adj:.5f}")
        k3.metric(label="ln φ", value=f"{results['ln_phi']:.5f}")
        st.markdown("</div>", unsafe_allow_html=True)

        # Detailed results table
        st.markdown("<div class='card' style='margin-top:12px'>", unsafe_allow_html=True)
        st.subheader("Detailed Results")
        df = pd.DataFrame({
            "Parameter": [
                "Selected Gas", "Reduced Temp (Tr)", "Reduced Pressure (Pr)",
                "B0", "B1", "ln φ", "φ", "Fugacity (f, bar)"
            ],
            "Value": [
                selected_gas, f"{results['Tr']:.5f}", f"{results['Pr']:.5f}",
                f"{results['B0']:.6f}", f"{results['B1']:.6f}", f"{results['ln_phi']:.6f}",
                f"{results['phi']:.6f}", f"{fug_adj:.6f}"
            ]
        })
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


        # Small explanation and save option
        with st.expander("Save results / export"):
            st.write("You can download a CSV of the detailed results.")
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name='fugacity_results.csv', mime='text/csv')

        # celebration
        st.balloons()

    else:
        st.info("Press \"Calculate — Run Analysis\" on the sidebar to run the Pitzer calculation and view results.")

with tab_theory:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Theory & References")
    st.markdown(
        """
        **Pitzer correlation (simple implementation)** — The app uses empirically-derived B⁰ and B¹ temperature correlations
        together with the acentric factor ω to estimate the fugacity coefficient φ via a truncated virial/Pitzer form:

        \[ \ln \phi = \frac{P/P_c}{T/T_c} \left( B^0(T_r) + \omega B^1(T_r) \right) \]

        This formulation is appropriate for moderate pressures and provides quick engineering estimates. For high-pressure
        or very non-ideal systems, use a more rigorous EOS (e.g., Peng–Robinson, Soave–Redlich–Kwong) or direct
        experimental data.

        **References**
        - Pitzer, K.S. & Curl, R.F. Jr. (1957).
        - Smith, J.M., Van Ness, H.C., & Abbott, M.M., *Introduction to Chemical Engineering Thermodynamics*.
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

