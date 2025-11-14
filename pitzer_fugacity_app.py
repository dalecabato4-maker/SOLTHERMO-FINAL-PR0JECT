# pitzer_fugacity_app.py
import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------------
# Page configuration (must be first call)
# -----------------------------------------
st.set_page_config(
    page_title="Fugacity Calculator (Pitzer)",
    page_icon="⚗️",
    layout="wide",
)

# -----------------------------------------
# Session state: intro toggle
# -----------------------------------------
if "show_intro" not in st.session_state:
    st.session_state.show_intro = True 

# -----------------------------------------
# INTRO SCREEN (animated + styled)
# -----------------------------------------
if st.session_state.show_intro:
    st.markdown(
        """
<style>
html, body, [class*="css"] { margin:0; padding:0; }
.fullscreen-wrapper {
    position: fixed;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #0b0f17, #0f1720, #0d1b2a);
    background-size: 300% 300%;
    animation: gradientShift 12s ease infinite;
    z-index: 9999;
}
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.intro-box {
    width: 86%;
    max-width: 900px;
    padding: 38px;
    border-radius: 16px;
    background: rgba(12, 18, 28, 0.72);
    color: #eaf2ff;
    text-align: center;
    backdrop-filter: blur(8px);
}

.intro-title { font-size: 46px; font-weight: 800; margin-bottom: 6px; }
.intro-text { font-size: 17px; line-height: 1.6; margin-bottom: 14px; }
.team-title { margin-top: 15px; font-weight: 700; color:#7fe3ff; }
.team-names { margin-top: 8px; font-size: 15px;}

.enter-btn {
    padding: 10px 26px;
    border-radius: 28px;
    background: linear-gradient(90deg,#00c2ff,#0066ff);
    color: #fff;
    font-weight: 700;
    text-decoration: none;
}
</style>

<div class="fullscreen-wrapper">
    <div class="intro-box">

        <div class="intro-title">Calculator Suite</div>

        <div class="intro-text">
            A fully interactive tool for predicting real-gas behavior using the
            <b>Pitzer virial method</b>.
        </div>

        <div class="intro-text">
            Computes <b>fugacity (f)</b>, <b>fugacity coefficient (φ)</b>,
            reduced properties, and Pitzer second virial coefficients.
        </div>

        <div class="team-title">Developed By</div>
        <div class="team-names">
            Dale Clarenz Cabato · Francisco Andrei Joseph Laudez · Aliona Tejada ·
            Rafaela Villas · Archie Plata · Andrea Hernandez · Armela Martin · Dimple Padilla
        </div>

        <br/>
        <a class="enter-btn" href="#">Enter Calculator</a>

    </div>
</div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🚀 Enter Fugacity Calculator", key="enter_calc"):
        st.session_state.show_intro = False
        st.experimental_rerun()

    st.stop()

# -----------------------------------------
# MAIN APP (runs only after intro closed)
# -----------------------------------------

background_image_url = "https://png.pngtree.com/thumb_back/fh260/background/20210728/pngtree-hexagon-light-effect-molecular-structure-chemical-engineering-geometric-texture-colorful-background-image_752109.jpg"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="background: rgba(0,0,0,0.55); padding:18px 22px; border-radius:10px; max-width:1100px;">
      <h1 style="color:#eaf6ff; margin:0 0 4px 0;">🌡️ Fugacity & Fugacity Coefficient Calculator (Pitzer)</h1>
      <p style="color:#d8ecff; margin:6px 0 0 0;">
        Compute fugacity and fugacity coefficient for gases using the Pitzer correlation.
        Enter conditions and critical constants in the sidebar, then click <b>Calculate</b>.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

gases = {
    "Carbon Dioxide (CO₂)": {"Tc": 304.2, "Pc": 73.8, "omega": 0.225},
    "Methane (CH₄)": {"Tc": 190.6, "Pc": 45.99, "omega": 0.011},
    "Nitrogen (N₂)": {"Tc": 126.2, "Pc": 33.5, "omega": 0.037},
    "Oxygen (O₂)": {"Tc": 154.6, "Pc": 50.4, "omega": 0.022},
    "Hydrogen (H₂)": {"Tc": 33.2, "Pc": 12.8, "omega": -0.22},
    "Ammonia (NH₃)": {"Tc": 405.5, "Pc": 113.5, "omega": 0.256},
    "Custom": {"Tc": 300.0, "Pc": 50.0, "omega": 0.1},
}

st.sidebar.header("⚙️ Gas Selection & Critical Data")
selected_gas = st.sidebar.selectbox("Select gas", list(gases.keys()))

Tc = st.sidebar.number_input("Critical Temperature Tc (K)", value=gases[selected_gas]["Tc"], step=0.1)
Pc = st.sidebar.number_input("Critical Pressure Pc (bar)", value=gases[selected_gas]["Pc"], step=0.1)
omega = st.sidebar.number_input("Acentric factor ω", value=gases[selected_gas]["omega"], step=0.001, format="%.3f")

st.sidebar.markdown("---")
st.sidebar.write("Input operating conditions:")
T = st.sidebar.number_input("Temperature (K)", value=300.0, step=0.1)
P = st.sidebar.number_input("Pressure (bar)", value=10.0, step=0.1)
y = st.sidebar.number_input("Mole fraction (y)", value=1.0, min_value=0.0, max_value=1.0, step=0.01)

calc_pressed = st.sidebar.button("🧮 Calculate Fugacity")

def pitzer_fugacity(T, P, Tc, Pc, omega):
    Tr = T / Tc
    Pr = P / Pc
    B0 = 0.083 - (0.422 / (Tr ** 1.6))
    B1 = 0.139 - (0.172 / (Tr ** 4.2))
    ln_phi = (Pr / Tr) * (B0 + omega * B1)
    phi = float(np.exp(ln_phi))
    f = phi * P
    return {"Tr": Tr, "Pr": Pr, "B0": B0, "B1": B1, "phi": phi, "f": f}

if calc_pressed:
    if Tc <= 0 or Pc <= 0:
        st.error("Critical properties must be positive numbers.")
    else:
        res = pitzer_fugacity(T, P, Tc, Pc, omega)
        f_corrected = res["f"] * y

        df = pd.DataFrame({
            "Parameter": [
                "Selected gas",
                "Temperature (K)",
                "Pressure (bar)",
                "Reduced temperature (Tr)",
                "Reduced pressure (Pr)",
                "B⁰ (Pitzer)",
                "B¹ (Pitzer)",
                "Fugacity coefficient (φ)",
                "Fugacity (bar) — corrected (φ·P·y)"
            ],
            "Value": [
                selected_gas,
                f"{T:.3f}",
                f"{P:.3f}",
                f"{res['Tr']:.5f}",
                f"{res['Pr']:.5f}",
                f"{res['B0']:.6f}",
                f"{res['B1']:.6f}",
                f"{res['phi']:.6f}",
                f"{f_corrected:.6f}"
            ]
        })

        st.success("✅ Calculation completed")
        st.write("")


        # Display styled table via Styler (Streamlit supports Styler objects)
        styled = df.style.set_table_styles([
            {"selector": "thead th", "props": [("background-color", "#0b2138"), ("color", "white"), ("font-weight", "600")]},
            {"selector": "tbody td", "props": [("background-color", "#f6fbff"), ("color", "#0b2138"), ("padding", "6px 10px")]},
            {"selector": "tbody tr:nth-child(even) td", "props": [("background-color", "#eef6ff")]},
        ]).hide(axis="index")
        st.write(styled, unsafe_allow_html=True)

        # also provide CSV download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download results (CSV)", data=csv, file_name="pitzer_fugacity_results.csv", mime="text/csv")

        st.caption("Model: Pitzer correlation. Valid for many nonpolar gases at moderate pressures. Reference: Pitzer & Curl (1957).")

# Footer / references
st.markdown("---")
st.markdown(
    """
    **References**  
    - Pitzer, K.S. & Curl, R.F. Jr. (1957). J. Am. Chem. Soc., 79, 2369.  
    - Smith, Van Ness & Abbott — Introduction to Chemical Engineering Thermodynamics.
    """,
    unsafe_allow_html=True,
)



