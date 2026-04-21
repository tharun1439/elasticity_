import streamlit as st
import matplotlib.pyplot as plt
import time
import requests
from streamlit_lottie import st_lottie

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Elasticity Pro", page_icon="📊", layout="centered")

# ---------------- SESSION STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = 1

if "values" not in st.session_state or not isinstance(st.session_state.values, dict):
    st.session_state.values = {
        "p1": 10.0,
        "p2": 5.0,
        "q1": 100.0,
        "q2": 150.0
    }

# ---------------- LOAD LOTTIE ----------------
def load_lottie(url):
    try:
        return requests.get(url).json()
    except:
        return None

l1 = load_lottie("https://assets2.lottiefiles.com/packages/lf20_49rdyysj.json")
l2 = load_lottie("https://assets2.lottiefiles.com/packages/lf20_yd8fbnml.json")
l3 = load_lottie("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")

# ---------------- MOBILE CSS ----------------
st.markdown("""
<style>

/* Center container like phone */
.main {
    max-width: 420px;
    margin: auto;
}

/* App background */
.stApp {
    background: linear-gradient(180deg,#020617,#0f172a);
}

/* Card style */
.card {
    background: rgba(30,41,59,0.7);
    padding:20px;
    border-radius:20px;
    margin-top:20px;
    box-shadow:0 10px 30px rgba(0,0,0,0.3);
}

/* Title */
h1 {
    text-align:center;
    color:#22c55e;
}

/* Buttons (mobile style) */
.stButton>button {
    width:100%;
    height:55px;
    border-radius:15px;
    font-size:18px;
    background:#22c55e;
    color:white;
    margin-top:10px;
}

/* Progress dots */
.dots {
    text-align:center;
    font-size:20px;
    margin-bottom:10px;
    color:#94a3b8;
}

.active {
    color:#22c55e;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1>📊 Elasticity App</h1>", unsafe_allow_html=True)

# ---------------- STEP INDICATOR ----------------
dots = ["○", "○", "○"]
dots[st.session_state.step - 1] = "●"

st.markdown(f"<div class='dots'>{' '.join(dots)}</div>", unsafe_allow_html=True)

# ---------------- STEP 1 ----------------
if st.session_state.step == 1:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if l1:
        st_lottie(l1, height=180)

    st.subheader("Learn")

    st.write("""
Elasticity measures how demand reacts to price.

- Elastic (>1)
- Inelastic (<1)
- Unitary (=1)
""")

    if st.button("Start"):
        st.session_state.step = 2
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- STEP 2 ----------------
elif st.session_state.step == 2:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if l2:
        st_lottie(l2, height=180)

    st.subheader("Enter Values")

    p1 = st.number_input("Original Price", min_value=0.01,
                         value=st.session_state.values.get("p1", 10.0))

    q1 = st.number_input("Original Quantity", min_value=0.01,
                         value=st.session_state.values.get("q1", 100.0))

    p2 = st.number_input("New Price", min_value=0.01,
                         value=st.session_state.values.get("p2", 5.0))

    q2 = st.number_input("New Quantity", min_value=0.01,
                         value=st.session_state.values.get("q2", 150.0))

    if st.button("Calculate"):
        st.session_state.values.update({
            "p1": p1, "p2": p2, "q1": q1, "q2": q2
        })
        st.session_state.step = 3
        st.rerun()

    if st.button("Back"):
        st.session_state.step = 1
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- STEP 3 ----------------
elif st.session_state.step == 3:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if l3:
        st_lottie(l3, height=180)

    st.subheader("Results")

    data = st.session_state.values

    p1 = float(data.get("p1", 10))
    p2 = float(data.get("p2", 5))
    q1 = float(data.get("q1", 100))
    q2 = float(data.get("q2", 150))

    with st.spinner("Analyzing..."):
        time.sleep(1)

    delta_p = p2 - p1
    delta_q = q2 - q1

    ep_arc = ((q2 - q1)/(q2 + q1))*((p2 + p1)/(p2 - p1)) if (p2 - p1) != 0 else 0

    def status(v):
        v = abs(v)
        if v < 1: return "Inelastic 📉"
        elif v == 1: return "Unitary ⚖️"
        else: return "Elastic 📈"

    st.metric("Elasticity", round(ep_arc, 2))
    st.success(status(ep_arc))

    # Graph
    fig, ax = plt.subplots()
    ax.plot([q1, q2], [p1, p2], marker='o')
    ax.set_xlabel("Quantity")
    ax.set_ylabel("Price")
    st.pyplot(fig)

    if st.button("Restart"):
        st.session_state.step = 1
        st.rerun()

    if st.button("Back"):
        st.session_state.step = 2
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
