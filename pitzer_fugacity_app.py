import streamlit as st
import numpy as np
import pandas as pd
import time

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(page_title="Fugacity Calculator (Pitzer Correlation)", layout="centered")

# ------------------------------------------------------------
# Custom CSS Styling (UPDATED)
# ------------------------------------------------------------
st.markdown("""
    <style>
    .poppins-italic {
        font-family: 'Poppins', sans-serif !important;
        font-style: italic !important;
    }
    .open-sans {
        font-family: 'Open Sans', sans-serif !important;
    }

    .open-sans-italic {
        font-family: 'Open Sans', sans-serif !important;
        font-style: italic !important;
    }
    .montserrat {
        font-family: 'Montserrat', sans-serif !important;
    }
    .montserrat-italic {
        font-family: 'Montserrat', sans-serif !important;
        font-style: italic !important;
    }
    .playfair {
            font-family: 'Playfair Display', serif !important;
    }
     .playfair-italic {
            font-family: 'Playfair Display', serif !important;
            font-style: italic !important;
     }


    :root{
      --bg:#ffffff;
      --card:#f7f8fb;
      --accent:#1e3a8a;
      --muted:#6b7280;
    }

    body{
      margin:0;
      font-family:Inter, Arial, sans-serif;
      background:var(--bg);
      color:#111827;
    }
    .app{
      max-width:980px;
      margin:24px auto;
      padding:20px;
    }
    header h1{
      font-size:20px;
      margin:0 0 18px 0;
      color:var(--accent);
    }
    .controls{
      background:var(--card);
      padding:16px;
      border-radius:10px;
      border:1px solid #e6edf6;
    }
    .controls label{
      display:block;margin:10px 0 6px 0;font-weight:600;
    }
    #numSpecies{
      width:120px;
      padding:8px;
      border-radius:6px;
      border:1px solid #d1d5db;
      background:#fff;
    }
    .species-box{
      background:#fff;
      border:1px solid #e6edf6;
      padding:12px;
      border-radius:8px;
      margin-top:14px;
    }
    .species-box h3{margin:0 0 8px 0}
    .species-row{
      display:flex;
      gap:12px;
      align-items:center;
      flex-wrap:wrap;
    }
    .species-row select, .species-row input[type="number"]{
      padding:8px;
      border-radius:6px;
      border:1px solid #d1d5db;
      min-width:200px;
    }
    .conditions{
      display:flex;
      gap:12px;
      margin-top:8px;
      align-items:center;
    }
    .conditions label{font-weight:500}
    .btn{
      margin-top:16px;
      background:linear-gradient(90deg,#2563eb,#1e40af);
      color:white;
      border:none;
      padding:10px 14px;
      border-radius:8px;
      cursor:pointer;
      font-weight:700;
    }
    .results{
      margin-top:18px;
    }
    .result-table{
      width:100%;
      border-collapse:collapse;
    }
    .result-table th, .result-table td{
      border:1px solid #e6edf6;
      padding:8px;
      text-align:left;
    }
    .note{color:var(--muted);font-size:13px;margin-top:8px}

    #loadingScreen {
      position: fixed;
      inset: 0;
      background: #0f172a;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 9999;
      color: white;
    }

    .loading-logo img {
      width: 160px;
      height: 160px;
      animation: logoPulse 2s infinite ease-in-out;
      background: transparent !important;
    }

    .load-labels {
      width: 320px;
      display: flex;
      justify-content: space-between;
      margin-top: 15px;
      margin-bottom: 6px;
    }

    .loading-left, .loading-right {
      font-size: 16px;
      color: #cbd5e1;
    }
    .loading-right { font-weight: 700; }

    .loading-bar-container {
      width: 320px;
      height: 10px;
      background: #1e293b;
      border-radius: 20px;
      overflow: hidden;
    }

    .loading-bar {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg,#3b82f6,#1d4ed8);
      transition: width 0.1s linear;
    }

    @keyframes logoPulse {
      0% { transform: scale(1); opacity: 0.7; }
      50% { transform: scale(1.18); opacity: 1; }
      100% { transform: scale(1); opacity: 0.7; }
    }

    /* INTRO SCREEN */
    .intro-screen {
      position: fixed;
      inset: 0;
      display: none;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      padding: 40px 20px;
      background: url("galaxy-bg.png") center/cover no-repeat;
      overflow-y: auto;
    }

    .intro-card {
      background: #ffffff;
      width: 90%;
      max-width: 900px;
      padding: 30px 35px;
      border-radius: 18px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.55);
      text-align: center;
    }

    .intro-top-card { margin-top: 60px; }
    .intro-bottom-card {
        margin-top: 300px;
        margin-bottom: 120px;
        width: 50%;
        max-width: 650px;
    }

    .intro-title { display:flex; align-items:center; justify-content:center; gap:15px; }
    .intro-title h1 {
      font-size:2.1rem;
      margin:0;
      color:#005f5f;
    }

    .intro-icon { width:50px; height:auto; }
    .intro-logo { width:160px; height:auto; }

    .intro-description {
      margin-top:15px;
      font-size:1.05rem;
      color:#003c3c;
      line-height:1.6;
    }

    .intro-developed {
      color: #005f5f;
      font-size: 1.3rem;
      margin-bottom: 10px;
    }

    .intro-names {
      font-size: 0.95rem;
      color: #003c3c;
      line-height: 1.5;
      margin-bottom: 22px;
    }

    .intro-button {
      background:#007bff;
      color:white;
      border:none;
      padding:12px 25px;
      font-size:1rem;
      border-radius:6px;
      cursor:pointer;
      transition:0.25s ease;
      box-shadow:0px 3px 6px rgba(0,0,0,0.15);
    }

    .intro-button:hover {
      background:#005fcc;
      transform:translateY(-6px);
      box-shadow:0px 6px 12px rgba(0,0,0,0.25);
    }

    button { transition:0.25s ease; }
    button:hover {
      transform:translateY(-6px);
      box-shadow:0px 9px 15px rgba(0,0,0,0.25);
    }

    /* Background image for whole app */
    .intro-screen, .app {
        background: url("https://i.pinimg.com/736x/ad/92/8a/ad928a7fbfbc8ead5321928115095ae4.jpg")
        center/cover no-repeat fixed;
    }

    body {
        background: url("https://i.pinimg.com/736x/ad/92/8a/ad928a7fbfbc8ead5321928115095ae4.jpg")
        no-repeat center center fixed;
        background-size: cover;
    }

    .app {
        background:#ffffff !important;
        padding:25px;
        border-radius:18px;
        box-shadow:0 10px 35px rgba(0,0,0,0.45);
        max-width:900px;
        margin:40px auto;
    }

    .calc-title { color:#005f5f !important; }

    input[type=number] {
      -webkit-appearance: textfield !important;
    }
    input[type=number]::-webkit-inner-spin-button,
    input[type=number]::-webkit-outer-spin-button {
      -webkit-appearance: inner-spin-button !important;
      opacity:1 !important;
      display:block !important;
      height:20px !important;
      width:20px !important;
      margin:0 !important;
    }

    #calculateBtn:disabled {
        cursor:not-allowed !important;
        opacity:0.6;
        transform:none !important;
        box-shadow:none !important;
    }

    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    st.image("https://o.quizlet.com/86QryQ7W36NpbLjAlS.iRg_b.png", width=200)
    st.markdown("### 📘 About This App")
    st.markdown("""
    <p class="playfair-italic">
            This calculator uses the Pitzer correlation to estimate fugacity and 
            fugacity coefficients for gases under ideal and non-ideal conditions.
        </p>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <p class="playfair">
            Made by Group 4 of ChE-3106
        </p>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------
# Session State: Homepage Toggle
# ------------------------------------------------------------
if "show_homepage" not in st.session_state:
    st.session_state.show_homepage = True
import time

# ------------------------------------------------------------
# Loading Screen with Logo (Auto-Disappear)
# ------------------------------------------------------------
if "loaded" not in st.session_state:
    loading_placeholder = st.empty()
    with loading_placeholder:
        st.markdown("""
            <div style="text-align:center; padding:60px;">
                <img src="https://github.com/dalecabato4-maker/SOLTHERMO-FINAL-PR0JECT/blob/main/Calculator%20(1).png?raw=true" width="400" style="margin-bottom:40px;" />
                <h2 style="color:#1E88E5;">🔄 Loading Fugacity Calculator...</h2>
                <p style="font-size:24px;">
                <p class="playfair">
                Initializing thermodynamic models and styling interface...
                </p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(3.5)  # Simulate loading delay
    loading_placeholder.empty()  # Clear the loading screen
    st.session_state.loaded = True
# ------------------------------------------------------------
# HOMEPAGE INTRO SCREEN
# ------------------------------------------------------------
if st.session_state.show_homepage:
    st.markdown("""
    <div style="text-align:center; padding:40px;">
        <h1 style="font-size:40px;">⚗️Fugacitor⚗️</h1>
        <p style="font-size:18px; max-width:700px; margin:auto;">
        <p class="playfair">
            Welcome to the Fugacity & Fugacity Coefficient Calculator using the <b>Pitzer correlation</b>.  
            Fugacity is a corrected pressure that accounts for non-ideal gas behavior — essential for accurate thermodynamic modeling.  
            This tool supports both pure gases and mixtures, and is based on the work of Pitzer & Curl.
        </p>
        <br/>
        <h3 style="color:#00aaff;">Developed By:</h3>
        <p style="font-size:16px;">
        <p class="playfair">
            Dale Clarenz J. Cabato · Andrea Mae A. Hernandez · Francisco Andrei Joseph Laudez ·  Armela Monique D. Martin ·  
            Dimple Jean E. Padilla · Archie P. Plata · Aliona Galle D. Tejada ·  Rafaella Anne D. Villas
        </p>
        <br/><br/>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Enter Calculator"):
        st.session_state.show_homepage = False

    st.stop()
# ------------------------------------------------------------
# Gas Database (Critical Constants)
# ------------------------------------------------------------
gases = {
        "Acetaldehyde": {"Tc": 466, "Pc": 55.7, "omega": 0.262493},
    "Acetamide": {"Tc": 761, "Pc": 66.0, "omega": 0.421044},
    "Acetic acid": {"Tc": 591.95, "Pc": 57.86, "omega": 0.466521},
    "Acetic anhydride": {"Tc": 606, "Pc": 40.0, "omega": 0.455328},
    "Acetone": {"Tc": 508.2, "Pc": 47.01, "omega": 0.306527},
    "Acetonitrile": {"Tc": 545.5, "Pc": 48.5, "omega": 0.341926},
    "Acetylene": {"Tc": 308.3, "Pc": 61.38, "omega": 0.191185},
    "Acrolein": {"Tc": 506, "Pc": 50.0, "omega": 0.319832},
    "Acrylic acid": {"Tc": 615, "Pc": 56.6, "omega": 0.538324},
    "Acrylonitrile": {"Tc": 540, "Pc": 46.6, "omega": 0.310664},
    "Air": {"Tc": 132.45, "Pc": 37.74, "omega": 0},
    "Ammonia": {"Tc": 405.65, "Pc": 112.8, "omega": 0.252608},
    "Anisole": {"Tc": 645.6, "Pc": 42.5, "omega": 0.350169},
    "Argon": {"Tc": 150.86, "Pc": 48.98, "omega": 0},
    "Benzamide": {"Tc": 824, "Pc": 50.5, "omega": 0.5585},
    "Benzene": {"Tc": 562.05, "Pc": 48.95, "omega": 0.2103},
    "Benzenethiol": {"Tc": 689, "Pc": 47.4, "omega": 0.262789},
    "Benzoic acid": {"Tc": 751, "Pc": 44.7, "omega": 0.602794},
    "Benzonitrile": {"Tc": 702.3, "Pc": 42.15, "omega": 0.343214},
    "Benzophenone": {"Tc": 830, "Pc": 33.52, "omega": 0.501941},
    "Benzyl alcohol": {"Tc": 720.15, "Pc": 43.74, "omega": 0.363116},
    "Benzyl ethyl ether": {"Tc": 662, "Pc": 31.1, "omega": 0.433236},
    "Benzyl mercaptan": {"Tc": 718, "Pc": 40.6, "omega": 0.312604},
    "Biphenyl": {"Tc": 773, "Pc": 33.8, "omega": 0.402873},
    "Bromine": {"Tc": 584.15, "Pc": 103.0, "omega": 0.128997},
    "Bromobenzene": {"Tc": 670.15, "Pc": 45.191, "omega": 0.250575},
    "Bromoethane": {"Tc": 503.8, "Pc": 55.65, "omega": 0.205275},
    "Bromomethane": {"Tc": 464, "Pc": 69.29, "omega": 0.153426},
    "1,2-Butadiene": {"Tc": 452, "Pc": 43.6, "omega": 0.165877},
    "1,3-Butadiene": {"Tc": 425, "Pc": 43.2, "omega": 0.195032},
    "Butane": {"Tc": 425.12, "Pc": 37.96, "omega": 0.200164},
    "1,2-Butanediol": {"Tc": 680, "Pc": 52.1, "omega": 0.630463},
    "1,3-Butanediol": {"Tc": 676, "Pc": 40.2, "omega": 0.704256},
    "1-Butanol": {"Tc": 563.1, "Pc": 44.14, "omega": 0.58828},
    "2-Butanol": {"Tc": 535.9, "Pc": 41.885, "omega": 0.580832},
    "1-Butene": {"Tc": 419.5, "Pc": 40.2, "omega": 0.184495},
    "cis-2-Butene": {"Tc": 435.5, "Pc": 42.1, "omega": 0.201877},
    "trans-2-Butene": {"Tc": 428.6, "Pc": 41.0, "omega": 0.217592},
    "Butyl acetate": {"Tc": 575.4, "Pc": 30.9, "omega": 0.439393},
    "Butylbenzene": {"Tc": 660.5, "Pc": 28.9, "omega": 0.394149},
    "Butyl mercaptan": {"Tc": 570.1, "Pc": 39.7, "omega": 0.271361},
    "sec-Butyl mercaptan": {"Tc": 554, "Pc": 40.6, "omega": 0.25059},
    "1-Butyne": {"Tc": 440, "Pc": 46.0, "omega": 0.246976},
    "Butyraldehyde": {"Tc": 537.2, "Pc": 44.1, "omega": 0.282553},
    "Butyric acid": {"Tc": 615.7, "Pc": 40.6, "omega": 0.675003},
    "Butyronitrile": {"Tc": 585.4, "Pc": 38.8, "omega": 0.3601},
    "Carbon dioxide": {"Tc": 304.21, "Pc": 73.83, "omega": 0.223621},
    "Carbon disulfide": {"Tc": 552, "Pc": 79.0, "omega": 0.110697},
    "Carbon monoxide": {"Tc": 132.92, "Pc": 34.99, "omega": 0.0481621},
    "Carbon tetrachloride": {"Tc": 556.35, "Pc": 45.6, "omega": 0.192552},
    "Carbon tetrafluoride": {"Tc": 227.51, "Pc": 37.45, "omega": 0.178981},
    "Chlorine": {"Tc": 417.15, "Pc": 77.1, "omega": 0.0688183},
    "Chlorobenzene": {"Tc": 632.35, "Pc": 45.191, "omega": 0.249857},
    "Chloroethane": {"Tc": 460.35, "Pc": 52.7, "omega": 0.188591},
    "Chloroform": {"Tc": 536.4, "Pc": 54.72, "omega": 0.221902},
    "Chloromethane": {"Tc": 416.25, "Pc": 66.8, "omega": 0.151},
    "1-Chloropropane": {"Tc": 503.15, "Pc": 44.25, "omega": 0.215047},
    "2-Chloropropane": {"Tc": 489, "Pc": 45.4, "omega": 0.198553},
    "m-Cresol": {"Tc": 705.85, "Pc": 45.6, "omega": 0.448034},
    "o-Cresol": {"Tc": 697.55, "Pc": 50.1, "omega": 0.43385},
    "p-Cresol": {"Tc": 704.65, "Pc": 51.5, "omega": 0.50721},
    "Cumene": {"Tc": 631, "Pc": 32.09, "omega": 0.327406},
    "Cyanogen": {"Tc": 400.15, "Pc": 59.24, "omega": 0.275605},
    "Cyclobutane": {"Tc": 459.93, "Pc": 49.8, "omega": 0.18474},
    "Cyclohexane": {"Tc": 553.8, "Pc": 40.8, "omega": 0.208054},
    "Cyclohexanol": {"Tc": 650.1, "Pc": 42.6, "omega": 0.369047},
    "Cyclohexanone": {"Tc": 653, "Pc": 40.0, "omega": 0.299006},
    "Cyclohexene": {"Tc": 560.4, "Pc": 43.5, "omega": 0.212302},
    "Cyclopentane": {"Tc": 511.7, "Pc": 45.1, "omega": 0.194874},
    "Cyclopentene": {"Tc": 507, "Pc": 48.0, "omega": 0.19611},
    "Cyclopropane": {"Tc": 398, "Pc": 55.4, "omega": 0.127829},
    "Cyclohexyl mercaptan": {"Tc": 664, "Pc": 39.7, "omega": 0.264134},
    "Decanal": {"Tc": 674, "Pc": 26.0, "omega": 0.520066},
    "Decane": {"Tc": 617.7, "Pc": 21.1, "omega": 0.492328},
    "Decanoic acid": {"Tc": 722.1, "Pc": 22.8, "omega": 0.813724},
    "1-Decanol": {"Tc": 688, "Pc": 23.08, "omega": 0.606986},
    "1-Decene": {"Tc": 616.6, "Pc": 22.23, "omega": 0.480456},
    "Decyl mercaptan": {"Tc": 696, "Pc": 21.3, "omega": 0.587421},
    "1-Decyne": {"Tc": 619.85, "Pc": 23.7, "omega": 0.51783},
    "Deuterium": {"Tc": 38.35, "Pc": 16.617, "omega": -0.14486},
    "1,1-Dibromoethane": {"Tc": 628, "Pc": 60.3, "omega": 0.125025},
    "1,2-Dibromoethane": {"Tc": 650.15, "Pc": 54.769, "omega": 0.206724},
    "Dibromomethane": {"Tc": 611, "Pc": 71.7, "omega": 0.20945},
    "Dibutyl ether": {"Tc": 584.1, "Pc": 24.6, "omega": 0.447646},
    "m-Dichlorobenzene": {"Tc": 683.95, "Pc": 40.7, "omega": 0.27898},
    "o-Dichlorobenzene": {"Tc": 705, "Pc": 40.7, "omega": 0.219189},
    "p-Dichlorobenzene": {"Tc": 684.75, "Pc": 40.7, "omega": 0.284638},
    "1,1-Dichloroethane": {"Tc": 523, "Pc": 50.7, "omega": 0.233943},
    "1,2-Dichloroethane": {"Tc": 561.6, "Pc": 53.7, "omega": 0.286595},
    "Dichloromethane": {"Tc": 510, "Pc": 60.8, "omega": 0.198622},
    "1,1-Dichloropropane": {"Tc": 560, "Pc": 42.4, "omega": 0.252928},
    "1,2-Dichloropropane": {"Tc": 572, "Pc": 42.4, "omega": 0.256391},
    "Diethanol amine": {"Tc": 736.6, "Pc": 42.7, "omega": 0.952882},
    "Diethyl amine": {"Tc": 496.6, "Pc": 37.1, "omega": 0.303856},
    "Diethyl ether": {"Tc": 466.7, "Pc": 36.4, "omega": 0.281065},
    "Diethyl sulfide": {"Tc": 557.15, "Pc": 39.6, "omega": 0.29002},
    "1,1-Difluoroethane": {"Tc": 386.44, "Pc": 45.198, "omega": 0.275052},
    "1,2-Difluoroethane": {"Tc": 445, "Pc": 43.4, "omega": 0.222428},
    "Difluoromethane": {"Tc": 351.255, "Pc": 57.84, "omega": 0.277138},
    "Di–isopropyl amine": {"Tc": 523.1, "Pc": 32.0, "omega": 0.388315},
    "Di–isopropyl ether": {"Tc": 500.05, "Pc": 28.8, "omega": 0.338683},
    "Di–isopropyl ketone": {"Tc": 576, "Pc": 30.2, "omega": 0.404427},
    "1,1-Dimethoxyethane": {"Tc": 507.8, "Pc": 37.73, "omega": 0.32768},
    "1,2-Dimethoxypropane": {"Tc": 543, "Pc": 34.46, "omega": 0.352222},
    "Dimethyl acetylene": {"Tc": 473.2, "Pc": 48.7, "omega": 0.238542},
    "Dimethyl amine": {"Tc": 437.2, "Pc": 53.4, "omega": 0.299885},
    "2,3-Dimethylbutane": {"Tc": 500, "Pc": 31.5, "omega": 0.249251},
    "1,1-Dimethylcyclohexane": {"Tc": 591.15, "Pc": 29.3843, "omega": 0.232569},
    "cis-1,2-Dimethylcyclohexane": {"Tc": 606.15, "Pc": 29.3843, "omega": 0.232443},
    "trans-1,2-Dimethylcyclohexane": {"Tc": 596.15, "Pc": 29.3843, "omega": 0.237864},
    "Dimethyl disulfide": {"Tc": 615, "Pc": 53.6, "omega": 0.205916},
    "Dimethyl ether": {"Tc": 400.1, "Pc": 53.7, "omega": 0.200221},
    "N,N-Dimethyl formamide": {"Tc": 649.6, "Pc": 44.2, "omega": 0.31771},
    "2,3-Dimethylpentane": {"Tc": 537.3, "Pc": 29.1, "omega": 0.296407},
    "Dimethyl phthalate": {"Tc": 766, "Pc": 27.8, "omega": 0.656848},
    "Dimethylsilane": {"Tc": 402, "Pc": 35.6, "omega": 0.129957},
    "Dimethyl sulfide": {"Tc": 503.04, "Pc": 55.3, "omega": 0.194256},
    "Dimethyl sulfoxide": {"Tc": 729, "Pc": 56.5, "omega": 0.280551},
    "Dimethyl terephthalate": {"Tc": 777.4, "Pc": 27.6, "omega": 0.580691},
    "1,4-Dioxane": {"Tc": 587, "Pc": 52.081, "omega": 0.279262},
    "Diphenyl ether": {"Tc": 766.8, "Pc": 30.8, "omega": 0.43889},
    "Dipropyl amine": {"Tc": 550, "Pc": 31.4, "omega": 0.449684},
    "Dodecane": {"Tc": 658, "Pc": 18.2, "omega": 0.576385},
    "Eicosane": {"Tc": 768, "Pc": 11.6, "omega": 0.906878},
    "Ethane": {"Tc": 305.32, "Pc": 48.72, "omega": 0.099493},
    "Ethanol": {"Tc": 514, "Pc": 61.37, "omega": 0.643558},
    "Ethyl acetate": {"Tc": 523.3, "Pc": 38.8, "omega": 0.366409},
    "Ethyl amine": {"Tc": 456.15, "Pc": 56.2, "omega": 0.284788},
    "Ethylbenzene": {"Tc": 617.15, "Pc": 36.09, "omega": 0.30347},
    "Ethyl benzoate": {"Tc": 698, "Pc": 31.8, "omega": 0.477055},
    "2-Ethyl butanoic acid": {"Tc": 655, "Pc": 34.1, "omega": 0.632579},
    "Ethyl butyrate": {"Tc": 571, "Pc": 29.5, "omega": 0.401075},
    "Ethylcyclohexane": {"Tc": 609.15, "Pc": 30.4, "omega": 0.245525},
    "Ethylcyclopentane": {"Tc": 569.5, "Pc": 34.0, "omega": 0.270095},
    "Ethylene": {"Tc": 282.34, "Pc": 50.41, "omega": 0.0862484},
    "Ethylenediamine": {"Tc": 593, "Pc": 62.9, "omega": 0.472367},
    "Ethylene glycol": {"Tc": 720, "Pc": 82.0, "omega": 0.506776},
    "Ethyleneimine": {"Tc": 537, "Pc": 68.5, "omega": 0.200735},
    "Ethylene oxide": {"Tc": 469.15, "Pc": 71.9, "omega": 0.197447},
    "Ethyl formate": {"Tc": 508.4, "Pc": 47.4, "omega": 0.284736},
    "2-Ethyl hexanoic acid": {"Tc": 674.6, "Pc": 27.78, "omega": 0.801289},
    "Ethylhexyl ether": {"Tc": 583, "Pc": 24.6, "omega": 0.494378},
    "Ethylisopropyl ether": {"Tc": 489, "Pc": 34.1, "omega": 0.305629},
    "Ethylisopropyl ketone": {"Tc": 567, "Pc": 33.2, "omega": 0.389061},
    "Ethyl mercaptan": {"Tc": 499.15, "Pc": 54.9, "omega": 0.187751},
    "Ethyl propionate": {"Tc": 546, "Pc": 33.62, "omega": 0.394373},
    "Ethylpropyl ether": {"Tc": 500.23, "Pc": 33.7007, "omega": 0.347328},
    "Ethyltrichlorosilane": {"Tc": 559.95, "Pc": 33.3, "omega": 0.269778},
    "Fluorine": {"Tc": 144.12, "Pc": 51.724, "omega": 0.0530336},
    "Fluorobenzene": {"Tc": 560.09, "Pc": 45.5051, "omega": 0.247183},
    "Fluoroethane": {"Tc": 375.31, "Pc": 50.28, "omega": 0.217903},
    "Fluoromethane": {"Tc": 317.42, "Pc": 58.7511, "omega": 0.194721},
    "Formaldehyde": {"Tc": 420, "Pc": 65.9, "omega": 0.167887},
    "Formamide": {"Tc": 771, "Pc": 78.0, "omega": 0.412381},
    "Formic acid": {"Tc": 588, "Pc": 58.1, "omega": 0.312521},
    "Furan": {"Tc": 490.15, "Pc": 55.0, "omega": 0.201538},
    "Helium-4": {"Tc": 5.2, "Pc": 2.275, "omega": -0.390032},
    "Heptadecane": {"Tc": 736, "Pc": 13.4, "omega": 0.769688},
    "Heptanal": {"Tc": 620, "Pc": 31.6, "omega": 0.405751},
    "Heptane": {"Tc": 540.2, "Pc": 27.4, "omega": 0.349469},
    "Heptanoic acid": {"Tc": 677.3, "Pc": 30.43, "omega": 0.759934},
    "1-Heptanol": {"Tc": 632.3, "Pc": 30.85, "omega": 0.562105},
    "2-Heptanol": {"Tc": 608.3, "Pc": 30.0, "omega": 0.567733},
    "3-Heptanone": {"Tc": 606.6, "Pc": 29.2, "omega": 0.407565},
    "2-Heptanone": {"Tc": 611.4, "Pc": 29.4, "omega": 0.418982},
    "1-Heptene": {"Tc": 537.4, "Pc": 29.2, "omega": 0.343194},
    "Heptyl mercaptan": {"Tc": 645, "Pc": 27.7, "omega": 0.422568},
    "1-Heptyne": {"Tc": 547, "Pc": 32.1, "omega": 0.377799},
    "Hexadecane": {"Tc": 723, "Pc": 14.0, "omega": 0.717404},
    "Hexanal": {"Tc": 594, "Pc": 34.6, "omega": 0.361818},
    "Hexane": {"Tc": 507.6, "Pc": 30.25, "omega": 0.301261},
    "Hexanoic acid": {"Tc": 660.2, "Pc": 33.08, "omega": 0.733019},
    "1-Hexanol": {"Tc": 611.3, "Pc": 34.46, "omega": 0.558598},
    "2-Hexanol": {"Tc": 585.3, "Pc": 33.11, "omega": 0.553},
    "2-Hexanone": {"Tc": 587.61, "Pc": 32.87, "omega": 0.384626},
    "3-Hexanone": {"Tc": 582.82, "Pc": 33.2, "omega": 0.380086},
    "1-Hexene": {"Tc": 504, "Pc": 32.1, "omega": 0.285121},
    "3-Hexyne": {"Tc": 544, "Pc": 35.3, "omega": 0.218301},
    "Hexyl mercaptan": {"Tc": 623, "Pc": 30.8, "omega": 0.368101},
    "1-Hexyne": {"Tc": 516.2, "Pc": 36.2, "omega": 0.332699},
    "2-Hexyne": {"Tc": 549, "Pc": 35.3, "omega": 0.221387},
    "Hydrazine": {"Tc": 653.15, "Pc": 147.0, "omega": 0.314282},
    "Hydrogen": {"Tc": 33.19, "Pc": 13.13, "omega": -0.215993},
    "Hydrogen bromide": {"Tc": 363.15, "Pc": 85.52, "omega": 0.073409},
    "Hydrogen chloride": {"Tc": 324.65, "Pc": 83.1, "omega": 0.131544},
    "Hydrogen cyanide": {"Tc": 456.65, "Pc": 53.9, "omega": 0.409913},
    "Hydrogen fluoride": {"Tc": 461.15, "Pc": 64.8, "omega": 0.382283},
    "Hydrogen sulfide": {"Tc": 373.53, "Pc": 89.6291, "omega": 0.0941677},
    "Isobutyric acid": {"Tc": 605, "Pc": 37.0, "omega": 0.61405},
    "Isopropyl amine": {"Tc": 471.85, "Pc": 45.4, "omega": 0.275913},
    "Malonic acid": {"Tc": 834, "Pc": 61.0, "omega": 0.738273},
    "Methacrylic acid": {"Tc": 662, "Pc": 47.9, "omega": 0.331817},
    "Methane": {"Tc": 190.564, "Pc": 45.99, "omega": 0.0115478},
    "Methanol": {"Tc": 512.5, "Pc": 80.84, "omega": 0.565831},
    "N-Methyl acetamide": {"Tc": 718, "Pc": 49.8, "omega": 0.435111},
    "Methyl acetate": {"Tc": 506.55, "Pc": 47.5, "omega": 0.331255},
    "Methyl acetylene": {"Tc": 402.4, "Pc": 56.3, "omega": 0.211537},
    "Methyl acrylate": {"Tc": 536, "Pc": 42.5, "omega": 0.342296},
    "Methyl amine": {"Tc": 430.05, "Pc": 74.6, "omega": 0.281417},
     "Methyl Benzoate (C8H8O2)": {"Tc": 693, "Pc": 3.59, "omega": 0.420541},
    "3-Methyl-1,2-butadiene (C5H6)": {"Tc": 490, "Pc": 3.83, "omega": 0.187439},
    "2-Methylbutane (C5H12)": {"Tc": 460.4, "Pc": 3.38, "omega": 0.227875},
    "2-Methylbutanoic Acid (C5H10O2)": {"Tc": 643, "Pc": 3.89, "omega": 0.589443},
    "3-Methyl-1-butanol (C5H12O)": {"Tc": 577.2, "Pc": 3.93, "omega": 0.59002},
    "2-Methyl-1-butene (C5H10)": {"Tc": 465, "Pc": 3.447, "omega": 0.234056},
    "2-Methyl-2-butene (C5H10)": {"Tc": 470, "Pc": 3.42, "omega": 0.28703},
    "2-Methyl-1-butene-3-yne (C5H6)": {"Tc": 492, "Pc": 4.38, "omega": 0.137046},
    "Methylbutyl Ether (C5H12O)": {"Tc": 512.74, "Pc": 3.371, "omega": 0.313008},
    "Methylbutyl Sulfide (C5H12S)": {"Tc": 593, "Pc": 3.47, "omega": 0.3229},
    "3-Methyl-1-butyne (C5H8)": {"Tc": 463.2, "Pc": 4.2, "omega": 0.308085},
    "Methyl Butyrate (C5H10O2)": {"Tc": 554.5, "Pc": 3.473, "omega": 0.377519},
    "Methylchlorosilane (CH3SiCl)": {"Tc": 442, "Pc": 4.17, "omega": 0.225204},
    "Methylcyclohexane (C7H14)": {"Tc": 572.1, "Pc": 3.48, "omega": 0.236055},
    "1-Methylcyclohexanol (C7H14O)": {"Tc": 686, "Pc": 4, "omega": 0.221299},
    "cis-2-Methylcyclohexanol (C7H14O)": {"Tc": 614, "Pc": 3.79, "omega": 0.68049},
    "trans-2-Methylcyclohexanol (C7H14O)": {"Tc": 617, "Pc": 3.79, "omega": 0.67904},
    "Methylcyclopentane (C6H12)": {"Tc": 532.7, "Pc": 3.79, "omega": 0.228759},
    "1-Methylcyclopentene (C6H10)": {"Tc": 542, "Pc": 4.13, "omega": 0.23179},
    "3-Methylcyclopentene (C6H10)": {"Tc": 526, "Pc": 4.13, "omega": 0.229606},
    "Methyldichlorosilane (CH3SiCl2)": {"Tc": 483, "Pc": 3.95, "omega": 0.275755},
    "Methylethyl Ether (C3H8O)": {"Tc": 437.8, "Pc": 4.4, "omega": 0.231374},
    "Methylethyl Ketone (C4H8O)": {"Tc": 535.5, "Pc": 4.15, "omega": 0.323369},
    "Methylethyl Sulfide (C3H8S)": {"Tc": 533, "Pc": 4.26, "omega": 0.209108},
    "Methyl Formate (C2H4O2)": {"Tc": 487.2, "Pc": 6, "omega": 0.255551},
    "Methylisobutyl Ether (C5H12O)": {"Tc": 497, "Pc": 3.41, "omega": 0.307786},
    "Methylisobutyl Ketone (C5H10O)": {"Tc": 574.6, "Pc": 3.27, "omega": 0.355671},
    "Methyl Isocyanate (C2H3NO)": {"Tc": 488, "Pc": 5.48, "omega": 0.300694},
    "Methylisopropyl Ether (C4H10O)": {"Tc": 464.48, "Pc": 3.762, "omega": 0.26555},
    "Methylisopropyl Ketone (C5H10O)": {"Tc": 553.4, "Pc": 3.8, "omega": 0.320845},
    "Methylisopropyl Sulfide (C4H10S)": {"Tc": 553.1, "Pc": 4.021, "omega": 0.24611},
    "Methyl Mercaptan (CH4S)": {"Tc": 469.95, "Pc": 7.23, "omega": 0.158174},
    "Methyl Methacrylate (C5H8O2)": {"Tc": 566, "Pc": 3.68, "omega": 0.280233},
    "2-Methyloctanoic Acid (C9H18O2)": {"Tc": 694, "Pc": 2.54, "omega": 0.791271},
    "2-Methylpentane (C6H14)": {"Tc": 497.7, "Pc": 3.04, "omega": 0.279149},
    "Methyl Pentyl Ether (C6H14O)": {"Tc": 546.49, "Pc": 3.042, "omega": 0.344201},
    "2-Methylpropane (C4H10)": {"Tc": 407.8, "Pc": 3.64, "omega": 0.183521},
    "2-Methyl-2-propanol (C4H10O)": {"Tc": 506.2, "Pc": 3.972, "omega": 0.615203},
    "2-Methyl Propene (C4H8)": {"Tc": 417.9, "Pc": 4, "omega": 0.19484},
    "Methyl Propionate (C4H8O2)": {"Tc": 530.6, "Pc": 4.004, "omega": 0.346586},
    "Methylpropyl Ether (C5H12O)": {"Tc": 476.25, "Pc": 3.801, "omega": 0.276999},
    "Methylpropyl Sulfide (C5H12S)": {"Tc": 565, "Pc": 3.97, "omega": 0.273669},
    "Methylsilane (CH4Si)": {"Tc": 352.5, "Pc": 4.7, "omega": 0.131449},
    "alpha-Methyl Styrene (C9H10)": {"Tc": 654, "Pc": 3.36, "omega": 0.32297},
    "Methyl tert-butyl Ether (C5H12O)": {"Tc": 497.1, "Pc": 3.286, "omega": 0.246542},
    "Methyl Vinyl Ether (C3H6O)": {"Tc": 437, "Pc": 4.67, "omega": 0.241564},
    "Naphthalene (C10H8)": {"Tc": 748.4, "Pc": 4.05, "omega": 0.302034},
    "Neon (Ne)": {"Tc": 44.4, "Pc": 2.653, "omega": -0.0395988},
    "Nitroethane (C2H5NO2)": {"Tc": 593, "Pc": 5.16, "omega": 0.380324},
    "Nitrogen (N2)": {"Tc": 126.2, "Pc": 3.4, "omega": 0.0377215},
    "Nitrogen Trifluoride (NF3)": {"Tc": 234, "Pc": 4.4607, "omega": 0.119984},
    "Nitromethane (CH3NO2)": {"Tc": 588.15, "Pc": 6.31, "omega": 0.348026},
    "Nitrous Oxide (N2O)": {"Tc": 309.57, "Pc": 7.245, "omega": 0.140894},
    "Nitric Oxide (NO)": {"Tc": 180.15, "Pc": 6.48, "omega": 0.582944},
    "Nonadecane (C19H40)": {"Tc": 758, "Pc": 1.21, "omega": 0.852231},
    "Nonanal (C9H18O)": {"Tc": 658.5, "Pc": 2.68, "omega": 0.473309},
    "Nonane (C9H20)": {"Tc": 594.6, "Pc": 2.29, "omega": 0.44346},
    "Nonanoic Acid (C9H18O2)": {"Tc": 710.7, "Pc": 2.514, "omega": 0.778706},
    "1-Nonanol (C9H20O)": {"Tc": 670.9, "Pc": 2.527, "omega": 0.584074},
    "2-Nonanol (C9H20O)": {"Tc": 649.5, "Pc": 2.5408, "omega": 0.6092},
    "1-Nonene (C9H18)": {"Tc": 593.1, "Pc": 2.428, "omega": 0.436736},
    "Nonyl Mercaptan (C9H20S)": {"Tc": 681, "Pc": 2.31, "omega": 0.52604},
    "1-Nonyne (C9H16)": {"Tc": 598.05, "Pc": 2.61, "omega": 0.470974},
    "Octadecane (C18H38)": {"Tc": 747, "Pc": 1.27, "omega": 0.811359},
    "Octanal (C8H16O)": {"Tc": 638.9, "Pc": 2.96, "omega": 0.441993},
    "Octane (C8H18)": {"Tc": 568.7, "Pc": 2.49, "omega": 0.399552},
    "Octanoic Acid (C8H16O2)": {"Tc": 694.26, "Pc": 2.779, "omega": 0.773427},
    "1-Octanol (C8H18O)": {"Tc": 652.3, "Pc": 2.783, "omega": 0.569694},
    "2-Octanol (C8H18O)": {"Tc": 629.8, "Pc": 2.749, "omega": 0.58814},
    "2-Octanone (C8H16O)": {"Tc": 632.7, "Pc": 2.64, "omega": 0.454874},
    "3-Octanone (C8H16O)": {"Tc": 627.7, "Pc": 2.704, "omega": 0.440561},
    "1-Octene (C8H16)": {"Tc": 566.9, "Pc": 2.663, "omega": 0.392149},
    "Octyl Mercaptan (C8H18S)": {"Tc": 667.3, "Pc": 2.52, "omega": 0.449744},
    "1-Octyne (C8H14)": {"Tc": 574, "Pc": 2.88, "omega": 0.42329},
    "Oxalic Acid (C2H2O4)": {"Tc": 828, "Pc": 8.2, "omega": 0.286278},
    "Oxygen (O2)": {"Tc": 154.58, "Pc": 5.043, "omega": 0.0221798},
    "Ozone (O3)": {"Tc": 261, "Pc": 5.57, "omega": 0.211896},
    "Pentadecane (C15H32)": {"Tc": 708, "Pc": 1.48, "omega": 0.68632},
    "Pentanal (C5H10O)": {"Tc": 566.1, "Pc": 3.845, "omega": 0.313152},
    "Pentane (C5H12)": {"Tc": 469.7, "Pc": 3.37, "omega": 0.251506},
    "Pentanoic Acid (C5H10O2)": {"Tc": 639.16, "Pc": 3.63, "omega": 0.706632},
    "1-Pentanol (C5H12O)": {"Tc": 588.1, "Pc": 3.897, "omega": 0.57483},
    "2-Pentanol (C5H12O)": {"Tc": 561, "Pc": 3.7, "omega": 0.554979},
    "2-Pentanone (C5H10O)": {"Tc": 561.08, "Pc": 3.694, "omega": 0.343288},
    "3-Pentanone (C5H10O)": {"Tc": 560.95, "Pc": 3.74, "omega": 0.344846},
    "1-Pentene (C5H10)": {"Tc": 464.8, "Pc": 3.56, "omega": 0.237218},
    "2-Pentyl Mercaptan (C5H12S)": {"Tc": 584.3, "Pc": 3.536, "omega": 0.26853},
    "Pentyl Mercaptan (C5H12S)": {"Tc": 598, "Pc": 3.47, "omega": 0.320705},
    "1-Pentyne (C5H8)": {"Tc": 481.2, "Pc": 4.17, "omega": 0.289925},
    "2-Pentyne (C5H8)": {"Tc": 519, "Pc": 4.03, "omega": 0.175199},
    "Phenanthrene (C14H10)": {"Tc": 869, "Pc": 2.9, "omega": 0.470716},
    "Phenol (C6H6O)": {"Tc": 694.25, "Pc": 6.13, "omega": 0.44346},
    "Phenyl Isocyanate (C7H5NO)": {"Tc": 653, "Pc": 4.06, "omega": 0.412323},
    "Phthalic Anhydride (C8H4O3)": {"Tc": 791, "Pc": 4.72, "omega": 0.702495},
    "Propadiene (C3H4)": {"Tc": 394, "Pc": 5.25, "omega": 0.104121},
    "Propane (C3H8)": {"Tc": 369.83, "Pc": 4.248, "omega": 0.152291},
    "1-Propanol (C3H8O)": {"Tc": 536.8, "Pc": 5.169, "omega": 0.6209},
    "2-Propanol (C3H8O)": {"Tc": 508.3, "Pc": 4.765, "omega": 0.663},
    "Propenylcyclohexene (C9H14)": {"Tc": 636, "Pc": 3.12, "omega": 0.341975},
    "Propionaldehyde (C3H6O)": {"Tc": 503.6, "Pc": 5.038, "omega": 0.281254},
    "Propionic Acid (C3H6O2)": {"Tc": 600.81, "Pc": 4.668, "omega": 0.579579},
    "Propionitrile (C3H5N)": {"Tc": 561.3, "Pc": 4.26, "omega": 0.350057},
    "Propyl Acetate (C5H10O2)": {"Tc": 549.73, "Pc": 3.36, "omega": 0.388902},
    "Propyl Amine (C3H9N)": {"Tc": 496.95, "Pc": 4.74, "omega": 0.279839},
    "Propylbenzene (C9H12)": {"Tc": 638.35, "Pc": 3.2, "omega": 0.344391},
    "Propylene (C3H6)": {"Tc": 364.85, "Pc": 4.6, "omega": 0.137588},
    "Propyl Formate (C4H8O2)": {"Tc": 538, "Pc": 4.02, "omega": 0.308779},
     "2-Propyl Mercaptan": {"Tc": 517, "Pc": 4.75, "omega": 0.21381},
    "Propyl Mercaptan": {"Tc": 536.6, "Pc": 4.63, "omega": 0.231789},
    "1,2-Propylene Glycol": {"Tc": 626, "Pc": 6.1, "omega": 0.231789},
    "Quinone": {"Tc": 683, "Pc": 5.96, "omega": 0.494515},
    "Silicon Tetrafluoride": {"Tc": 259, "Pc": 3.72, "omega": 0.38584},
    "Styrene": {"Tc": 636, "Pc": 3.84, "omega": 0.297097},
    "Succinic Acid": {"Tc": 838, "Pc": 5, "omega": 0.743044},
    "Sulfur Dioxide": {"Tc": 430.75, "Pc": 7.8841, "omega": 0.245381},
    "Sulfur Hexafluoride": {"Tc": 318.69, "Pc": 3.76, "omega": 0.215146},
    "Sulfur Trioxide": {"Tc": 490.85, "Pc": 8.21, "omega": 0.42396},
    "Terephthalic Acid": {"Tc": 883.6, "Pc": 3.486, "omega": 0.94695},
    "o-Terphenyl": {"Tc": 857, "Pc": 2.99, "omega": 0.551265},
    "Tetradecane": {"Tc": 693, "Pc": 1.57, "omega": 0.643017},
    "Tetrahydrofuran": {"Tc": 540.15, "Pc": 5.19, "omega": 0.225354},
    "1,2,3,4-Tetrahydronaphthalene": {"Tc": 720, "Pc": 3.65, "omega": 0.335255},
    "Tetrahydrothiophene": {"Tc": 631.95, "Pc": 5.16, "omega": 0.199551},
    "2,2,3,3-Tetramethylbutane": {"Tc": 568, "Pc": 2.87, "omega": 0.244953},
    "Thiophene": {"Tc": 579.35, "Pc": 5.69, "omega": 0.196972},
    "Toluene": {"Tc": 591.75, "Pc": 4.108, "omega": 0.264012},
    "1,1,2-Trichloroethane": {"Tc": 602, "Pc": 4.48, "omega": 0.259135},
    "Tridecane": {"Tc": 675, "Pc": 1.68, "omega": 0.617397},
    "Triethyl Amine": {"Tc": 535.15, "Pc": 3.04, "omega": 0.316193},
    "Trimethyl Amine": {"Tc": 433.25, "Pc": 4.07, "omega": 0.206243},
    "1,2,3-Trimethylbenzene": {"Tc": 664.5, "Pc": 3.454, "omega": 0.366553},
    "1,2,4-Trimethylbenzene": {"Tc": 649.1, "Pc": 3.232, "omega": 0.37871},
    "2,2,4-Trimethylpentane": {"Tc": 543.8, "Pc": 2.57, "omega": 0.303455},
    "2,3,3-Trimethylpentane": {"Tc": 573.5, "Pc": 2.82, "omega": 0.2903},
    "1,3,5-Trinitrobenzene": {"Tc": 846, "Pc": 3.39, "omega": 0.862257},
    "2,4,6-Trinitrotoluene": {"Tc": 828, "Pc": 3.04, "omega": 0.897249},
    "Undecane": {"Tc": 639, "Pc": 1.95, "omega": 0.530316},
    "1-Undecanol": {"Tc": 703.9, "Pc": 2.119, "omega": 0.623622},
    "Vinyl Acetate": {"Tc": 519.13, "Pc": 3.958, "omega": 0.351307},
    "Vinyl Acetylene": {"Tc": 454, "Pc": 4.86, "omega": 0.106852},
    "Vinyl Chloride": {"Tc": 432, "Pc": 5.67, "omega": 0.100107},
    "Vinyl Trichlorosilane": {"Tc": 543.15, "Pc": 3.06, "omega": 0.281543},
    "Water": {"Tc": 647.096, "Pc": 22.064, "omega": 0.344861},
    "m-Xylene": {"Tc": 617, "Pc": 3.541, "omega": 0.326485},
    "o-Xylene": {"Tc": 630.3, "Pc": 3.732, "omega": 0.31013},
    "p-Xylene": {"Tc": 616.2, "Pc": 3.511, "omega": 0.321839},
    "Custom": {"Tc": 300.0, "Pc": 50.0, "omega": 0.1}
}

# ------------------------------------------------------------
# Pitzer Correlation Function
# ------------------------------------------------------------
def pitzer_fugacity(T, P, Tc, Pc, omega):
    Tr = T / Tc
    Pr = P / Pc
    B0 = 0.083 - (0.422 / Tr**1.6)
    B1 = 0.139 - (0.172 / Tr**4.2)
    ln_phi = (Pr / Tr) * (B0 + omega * B1)
    phi = np.exp(ln_phi)
    f = phi * P
    return {
        "Tr": Tr,
        "Pr": Pr,
        "B0": B0,
        "B1": B1,
        "phi": phi,
        "fugacity": f
    }

# ------------------------------------------------------------
# Header Section
# ------------------------------------------------------------
st.markdown("""
    <h1 style="
        font-family: 'Montserrat', sans-serif; 
        font-size: 40px; 
        font-weight: 700;
    ">
    🌡️ Fugacity & Fugacity Coefficient Calculator (Pitzer Correlation)
    </h1>

    <p style="
        font-family: 'Poppins', sans-serif;
        font-size: 18px;
        line-height: 1.6;
    ">
    This interactive app estimates <i>fugacity</i> and <i>fugacity coefficient (φ)</i> for selected gases  
    using the <i>Pitzer correlation</i>. It supports both pure gases and mixtures (via mole fraction input).
    </p>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Multi-Species Input Section
# ------------------------------------------------------------
st.markdown("""<h2>🧪 Multi-Species Fugacity Calculation <span style="color:#1E88E5;">(Ideal Gas model)</span></h2>""",
            unsafe_allow_html=True)


num_species = st.selectbox("Number of species to calculate:", [1, 2, 3])

species_inputs = []
for i in range(num_species):
    st.subheader(f"Species {i+1}")

    gas = st.selectbox(
        f"Select gas {i+1}",
        list(gases.keys()),
        key=f"gas_{i}"
    )

    # Default critical properties
    Tc = gases[gas]["Tc"]
    Pc = gases[gas]["Pc"]
    omega = gases[gas]["omega"]

    # --- CUSTOM OPTION ---
    if gas == "Custom":
        st.warning("Enter custom critical properties for this gas:")

        Tc = st.number_input(
            f"Custom Tc (K) for species {i+1}",
            min_value=1.0,
            value=300.0,
            step=1.0,
            key=f"custom_Tc_{i}"
        )

        Pc = st.number_input(
            f"Custom Pc (bar) for species {i+1}",
            min_value=0.1,
            value=50.0,
            step=0.1,
            key=f"custom_Pc_{i}"
        )

        omega = st.number_input(
            f"Custom acentric factor (ω) for species {i+1}",
            min_value=-0.5,
            max_value=1.0,
            value=0.10,
            step=0.01,
            key=f"custom_omega_{i}"
        )

    mole_frac = st.number_input(
        f"Mole fraction y{i+1}",
        min_value=0.0, max_value=1.0,
        value=1.0 if i == 0 else 0.0,
        step=0.01,
        key=f"y_{i}"
    )

    species_inputs.append({
        "name": gas,
        "Tc": Tc,
        "Pc": Pc,
        "omega": omega,
        "y": mole_frac
    })

# ------------------------------------------------------------
# Required Operating Conditions
# ------------------------------------------------------------
st.header("🌡️ Required Operating Conditions")

col1, col2 = st.columns(2)
with col1:
    T = st.number_input("Temperature (T) [K]", min_value=1.0, value=300.0, step=0.1, help="Enter temperature in Kelvin")
with col2:
    P = st.number_input("Pressure (P) [bar]", min_value=0.01, value=10.0, step=0.1, help="Enter pressure in bar")

multi_calc = st.button("🧮 Calculate Fugacity and φ")

# ------------------------------------------------------------
# Multi-Species Calculation & Results
# ------------------------------------------------------------
def highlight_gradient(val, min_val, max_val, base="#ECEFF1", accent="#90CAF9"):
    """Apply a gradient background based on value."""
    try:
        val = float(val)
        ratio = (val - min_val) / (max_val - min_val) if max_val != min_val else 0
        def blend(c1, c2, r):
            return tuple(int(c1[i] + (c2[i] - c1[i]) * r) for i in range(3))
        base_rgb = tuple(int(base[i:i+2], 16) for i in (1, 3, 5))
        accent_rgb = tuple(int(accent[i:i+2], 16) for i in (1, 3, 5))
        blended = blend(base_rgb, accent_rgb, ratio)
        return f"background-color: rgb{blended}"
    except:
        return ""

if multi_calc:
    progress = st.progress(0)
    status = st.empty()

    for i in range(100):
        time.sleep(0.01)
        progress.progress(i+1)
        status.write(f"Computing thermodynamic properties... {i+1}%")

    progress.empty()
    status.empty()
    total_y = sum([s["y"] for s in species_inputs])
    if total_y > 1.0:
        st.error("❌ Total mole fraction exceeds 1. Please adjust inputs.")
    else:
        results = []
        for s in species_inputs:
            res = pitzer_fugacity(T, P, s["Tc"], s["Pc"], s["omega"])
            f_corrected = res["phi"] * s["y"] * P
            results.append({
                "Gas": s["name"],
                "y": f"{s['y']:.2f}",
                "Tr": f"{res['Tr']:.3f}",
                "Pr": f"{res['Pr']:.3f}",
                "B⁰": f"{res['B0']:.5f}",
                "B¹": f"{res['B1']:.5f}",
                "φ": f"{res['phi']:.5f}",
                "Fugacity (bar)": f"{f_corrected:.5f}"
            })

        df_multi = pd.DataFrame(results)

        st.success("✅ Multi-species calculation completed!")
        # Convert Fugacity column to float for styling
        df_multi["Fugacity (bar)"] = df_multi["Fugacity (bar)"].astype(float)

        # Get min and max for gradient scaling
        min_f = df_multi["Fugacity (bar)"].min()
        max_f = df_multi["Fugacity (bar)"].max()

        # Apply gradient styling to Fugacity column
        styled_df = df_multi.style.applymap(
            lambda v: highlight_gradient(v, min_f, max_f),
            subset=["Fugacity (bar)"]
        ).set_table_styles([
            {"selector": "thead th", "props": [
                ("background-color", "#172630"),
                ("color", "gray"),
                ("text-align", "center"),
                ("font-weight", "bold")
            ]},
            {"selector": "tbody td", "props": [
                ("text-align", "center"),
                ("padding", "6px 10px")
            ]},
            {"selector": "tbody tr:hover td", "props": [
                ("background-color", "#172630")
            ]}
        ])

        st.write(styled_df)



        st.caption("Each fugacity value is corrected by mole fraction (f × y).")
