# app.py  — Streamlit version of your Tkinter UI (same images & flow)

import streamlit as st
import numpy as np
import pickle
from datetime import date
import datetime
from PIL import Image
import io, base64
import matplotlib.pyplot as plt

# ------------------------
# CONFIG & ASSETS
# ------------------------
st.set_page_config(page_title="Heart Attack Prediction System",
                   page_icon="🫀",
                   layout="wide")

# Load model once
@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl", "rb"))

model = load_model()

# Helper: read image and return base64 for CSS/HTML embedding
def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Paths for your existing images (keep your folder structure)
IMG = {
    "icon": "Images/icon.png",
    "header": "Images/header.png",
    "rounded1": "Images/Rounded Rectangle 1.png",
    "rounded2": "Images/Rounded Rectangle 2.png",
    "report": "Images/Report.png",
    "info": "Images/info.png",
    "smoker": "Images/smoker.png",
    "non_smoker": "Images/non-smoker.png",
    "graph_tile": "Images/graph.png",
    "analysis_btn": "Images/Analysis.png",        # <- put your Analysis button image here
    "graph_small": "Images/graph.png",            # fallback if you only have one
}

# Background / theme colors (kept from your code)
BACKGROUND = "#f0ddd5"
FRAME_BG = "#62a7ff"
FRAME_FG = "#fefbfb"

# ------------------------
# LOGIN (same simple logic)
# ------------------------
def check_login(username, password):
    return username == "shallan" and password == "123abc000"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_view():
    st.markdown(
        f"""
        <style>
        .app-bg {{
            background: {BACKGROUND};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("🔒 Login")
    with st.form("login_form", clear_on_submit=False):
        c1, c2 = st.columns([1,1])
        with c1:
            username = st.text_input("Username")
        with c2:
            password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if check_login(username, password):
                st.session_state.logged_in = True
                st.success("Login Success — Welcome!")
            else:
                st.error("Invalid credentials")

if not st.session_state.logged_in:
    login_view()
    st.stop()

# ------------------------
# HEADER AREA (reusing header.png)
# ------------------------
header_col = st.container()
with header_col:
    try:
        st.image(IMG["header"], use_container_width=True)
    except Exception:
        st.write("")

# ------------------------
# REGISTRATION / NAME / DOB block (mirrors your red frame)
# ------------------------
st.markdown(
    f"""
    <div style="background:#df2d4b;border-radius:18px;padding:16px;margin-top:-10px;">
      <div style="display:flex;gap:24px;flex-wrap:wrap;">
        <div>
          <div style="color:{FRAME_FG};font-weight:600;">Registration No.</div>
          <img src="data:image/png;base64,{img_b64(IMG['rounded1'])}" style="height:42px;">
        </div>
        <div>
          <div style="color:{FRAME_FG};font-weight:600;">Date</div>
          <img src="data:image/png;base64,{img_b64(IMG['rounded1'])}" style="height:42px;">
        </div>
        <div>
          <div style="color:{FRAME_FG};font-weight:600;">Patient Name</div>
          <img src="data:image/png;base64,{img_b64(IMG['rounded2'])}" style="height:42px;">
        </div>
        <div>
          <div style="color:{FRAME_FG};font-weight:600;">Birth Year</div>
          <img src="data:image/png;base64,{img_b64(IMG['rounded2'])}" style="height:42px;">
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Actual inputs (bound to the visuals above)
reg_no_col, date_col, name_col, by_col = st.columns([1,1,1.2,1])
with reg_no_col:
    registration = st.number_input(" ", min_value=0, step=1, key="reg_no", label_visibility="hidden")
with date_col:
    today = date.today().strftime("%d/%m/%Y")
    the_date = st.text_input(" ", today, key="date_str", label_visibility="hidden")
with name_col:
    Name = st.text_input(" ", key="name", placeholder="Enter patient name", label_visibility="hidden")
with by_col:
    try:
        DOB = int(st.text_input(" ", value=str(date.today().year - 30), key="birth_year", label_visibility="hidden"))
    except:
        DOB = date.today().year - 30

# ------------------------
# MAIN BODY (left: controls, right: graphs + report)
# ------------------------
left, spacer, right = st.columns([0.9,0.05,1.05])

with left:
    st.markdown(f"""<div style="background:#dbe0e3;border-radius:18px;padding:16px;">""", unsafe_allow_html=True)
    st.markdown(f"<div style='color:{FRAME_FG};'>sex:</div>", unsafe_allow_html=True)
    sex = st.radio(" ", ["Male", "Female"], horizontal=True, label_visibility="hidden")
    st.markdown(f"<div style='color:{FRAME_FG};margin-top:6px;'>fbs:</div>", unsafe_allow_html=True)
    fbs_val = st.radio("  ", ["True", "False"], horizontal=True, label_visibility="hidden")
    st.markdown(f"<div style='color:{FRAME_FG};margin-top:6px;'>exang:</div>", unsafe_allow_html=True)
    exang_val = st.radio("   ", ["Yes", "No"], horizontal=True, label_visibility="hidden")

    st.markdown(f"<div style='color:{FRAME_FG};margin-top:8px;'>cp:</div>", unsafe_allow_html=True)
    cp = st.selectbox("cp", ["0 = typical angina", "1 = atypical angina", "2 = non-anginal pain", "3 = asymptomatic"], label_visibility="collapsed")

    st.markdown(f"<div style='color:{FRAME_FG};margin-top:6px;'>restecg:</div>", unsafe_allow_html=True)
    restecg = st.selectbox("restecg", ["0","1","2"], label_visibility="collapsed")

    st.markdown(f"<div style='color:{FRAME_FG};margin-top:6px;'>slope:</div>", unsafe_allow_html=True)
    slope = st.selectbox("slope", ["0 = upsloping","1 = flat","2 = downsloping"], label_visibility="collapsed")

    st.markdown(f"<div style='color:{FRAME_FG};margin-top:6px;'>ca:</div>", unsafe_allow_html=True)
    ca = st.selectbox("ca", ["0","1","2","3","4"], label_visibility="collapsed")

    st.markdown(f"<div style='color:{FRAME_FG};margin-top:6px;'>thal:</div>", unsafe_allow_html=True)
    thal = st.selectbox("thal", ["0","1","2","3"], label_visibility="collapsed")

    st.markdown("<hr style='opacity:.2;'>", unsafe_allow_html=True)
    col_smk, col_trest, col_chol = st.columns([1,1,1])
    with col_smk:
        st.write("Smoking:")
        # toggle image like your button
        if "smoking" not in st.session_state:
            st.session_state.smoking = True
        smk_img = IMG["smoker"] if st.session_state.smoking else IMG["non_smoker"]
        if st.button("Toggle Smoking"):
            st.session_state.smoking = not st.session_state.smoking
            smk_img = IMG["smoker"] if st.session_state.smoking else IMG["non_smoker"]
        st.image(smk_img, width=90)

    with col_trest:
        trestbps = st.number_input("trestbps", min_value=50, max_value=250, value=120)
    with col_chol:
        chol = st.number_input("chol", min_value=100, max_value=600, value=200)

    col_thal, col_oldpeak = st.columns([1,1])
    with col_thal:
        thalach = st.number_input("thalach", min_value=50, max_value=250, value=150)
    with col_oldpeak:
        oldpeak = st.number_input("oldpeak", min_value=0.0, max_value=10.0, step=0.1, value=1.0)

    st.markdown("</div>", unsafe_allow_html=True)  # end left panel

with right:
    # Analysis image acting as button (transparent real button on top)
    analysis_b64 = img_b64(IMG["analysis_btn"])
    st.markdown(
        f"""
        <style>
        .analysis-wrap {{ position: relative; width: 200px; height: 66px; }}
        .analysis-wrap img {{ position:absolute; left:0; top:0; width:200px; height:66px; border-radius:6px; }}
        div[data-testid="stButton"].analysis-btn > button {{
            position:absolute; left:0; top:0; width:200px; height:66px;
            opacity:0; border:0; background:transparent;
        }}
        </style>
        <div class="analysis-wrap">
            <img src="data:image/png;base64,{analysis_b64}">
        </div>
        """,
        unsafe_allow_html=True,
    )
    btn_container = st.container()
    with btn_container:
        st.markdown('<div class="analysis-btn">', unsafe_allow_html=True)
        clicked = st.button("Run Analysis")   # invisible, sits over the image
        st.markdown('</div>', unsafe_allow_html=True)

    # Report panel background image
    st.image(IMG["report"], caption=None, width=320)
    rep_spot = st.empty()
    rep_msg = st.empty()

    # Tile graphs (your four placeholders) + real matplotlib graphs later
    gcol1, gcol2 = st.columns(2)
    with gcol1:
        st.image(IMG["graph_tile"], width=280)
    with gcol2:
        st.image(IMG["graph_tile"], width=280)
    gcol3, gcol4 = st.columns(2)
    with gcol3:
        st.image(IMG["graph_tile"], width=280)
    with gcol4:
        st.image(IMG["graph_tile"], width=280)

# ------------------------
# INFO PANEL (your Info window -> expander)
# ------------------------
with st.expander("ℹ️ Information Related to Dataset"):
    st.markdown("""
- **age** — age in years  
- **sex** — (1 = male; 0 = female)  
- **cp** — chest pain type (0 = typical angina; 1 = atypical angina; 2 = non-anginal pain; 3 = asymptomatic)  
- **trestbps** — resting blood pressure (mm Hg)  
- **chol** — serum cholestoral (mg/dl)  
- **fbs** — fasting blood sugar > 120 mg/dl (1 = true; 0 = false)  
- **restecg** — resting ECG (0 = normal; 1 = ST-T abnormality; 2 = LVH)  
- **thalach** — maximum heart rate achieved  
- **exang** — exercise induced angina (1 = yes; 0 = no)  
- **oldpeak** — ST depression induced by exercise  
- **slope** — slope of peak exercise ST (0 = upsloping; 1 = flat; 2 = downsloping)  
- **ca** — number of major vessels (0–3) colored by fluoroscopy  
- **thal** — 0 = normal; 1 = fixed defect; 2 = reversible defect  
    """)

# ------------------------
# PREDICTION + CHARTS
# ------------------------
def to_numeric_selections():
    sex_val = 1 if sex == "Male" else 0
    fbs_v = 1 if fbs_val == "True" else 0
    exang_v = 1 if exang_val == "Yes" else 0
    cp_map = {"0 = typical angina":0,"1 = atypical angina":1,"2 = non-anginal pain":2,"3 = asymptomatic":3}
    slope_map = {"0 = upsloping":0,"1 = flat":1,"2 = downsloping":2}
    return (
        sex_val,
        fbs_v,
        exang_v,
        cp_map[cp],
        int(restecg),
        slope_map[slope],
        int(ca),
        int(thal)
    )

if clicked:
    A = datetime.date.today().year - int(DOB)   # age from birth year
    sex_val, fbs_v, exang_v, cp_v, restecg_v, slope_v, ca_v, thal_v = to_numeric_selections()

    input_data = np.array([[A, sex_val, cp_v, int(trestbps), int(chol),
                            fbs_v, restecg_v, int(thalach), exang_v,
                            float(oldpeak), slope_v, ca_v, thal_v]])
    pred = model.predict(input_data)[0]

    # Report UI (same green/red logic)
    if pred == 0:
        rep_spot.markdown("<h3 style='color:#8dc63f;margin-top:-120px;'>Report: 0</h3>", unsafe_allow_html=True)
        rep_msg.success(f"{Name or 'Patient'}, you do not have a heart disease.")
    else:
        rep_spot.markdown("<h3 style='color:#ed1c24;margin-top:-120px;'>Report: 1</h3>", unsafe_allow_html=True)
        rep_msg.error(f"{Name or 'Patient'}, you have a heart disease.")

    # Show your supplied small graph image
    st.image(IMG["graph_small"], width=120)

    # Also render 4 matplotlib charts like your original analysis()
    g1, g2 = st.columns(2)
    with g1:
        fig, ax = plt.subplots()
        ax.plot(["Sex","fbs","exang"], [sex_val, fbs_v, exang_v])
        ax.set_title("Binary Features")
        st.pyplot(fig)
    with g2:
        fig2, ax2 = plt.subplots()
        ax2.plot(["age","trestbps","chol","thalach"], [A, int(trestbps), int(chol), int(thalach)])
        ax2.set_title("Vitals")
        st.pyplot(fig2)
    g3, g4 = st.columns(2)
    with g3:
        fig3, ax3 = plt.subplots()
        ax3.plot(["oldpeak","restecg","cp"], [float(oldpeak), restecg_v, cp_v])
        ax3.set_title("ECG / Pain")
        st.pyplot(fig3)
    with g4:
        fig4, ax4 = plt.subplots()
        ax4.plot(["slope","ca","thal"], [slope_v, ca_v, thal_v])
        ax4.set_title("Angiographic")
        st.pyplot(fig4)

# ------------------------
# FOOTER ICON (uses your icon)
# ------------------------
st.sidebar.image(IMG["icon"], width=64)
st.sidebar.success("Ready.")
