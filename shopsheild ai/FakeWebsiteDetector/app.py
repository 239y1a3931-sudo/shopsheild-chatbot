import streamlit as st
import base64
from chatbot import chat_with_ai

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="ShopShield AI",
    page_icon="🛡️",
    layout="centered"
)

# =========================
# LOAD BACKGROUND IMAGE
# =========================
def get_base64(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_img = get_base64("assets/chatbot_bg.jpg")

# =========================
# SIMPLE URL DETECTOR
# =========================
def check_url(url):
    url = url.lower()
    score = 0

    suspicious_words = ["login", "free", "offer", "deal", "win", "gift", "cheap", "discount"]
    fake_domains = [".xyz", ".top", ".shop", ".online", ".click", ".info"]

    for word in suspicious_words:
        if word in url:
            score += 2

    if any(domain in url for domain in fake_domains):
        score += 3

    if url.count("-") > 2:
        score += 1

    if any(char.isdigit() for char in url):
        score += 2

    trusted = ["amazon.in", "amazon.com", "flipkart.com", "google.com"]
    if any(t in url for t in trusted):
        score -= 4

    if score <= 1:
        return "🟢 SAFE WEBSITE"
    elif score <= 4:
        return "🟠 MEDIUM RISK"
    else:
        return "🔴 HIGH RISK WEBSITE"

# =========================
# CUSTOM CSS
# =========================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

html, body {{
    font-family: 'Poppins', sans-serif;
}}

.stApp {{
    background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.9)),
    url("data:image/jpg;base64,{bg_img}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

#MainMenu, footer, header {{
    visibility: hidden;
}}

.main-title {{
    text-align:center;
    font-size:60px;
    font-weight:800;
    background: linear-gradient(90deg,#00e5ff,#7c3aed,#ff00ff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}}

.subtitle {{
    text-align:center;
    color:white;
    margin-bottom:20px;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="main-title">🛡️ ShopShield AI</div>
<p class="subtitle">Fake Website Detector + AI Assistant</p>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# INPUT
# =========================
prompt = st.chat_input("Paste URL or ask question...")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # =========================
    # URL DETECTION LOGIC
    # =========================
    if "http" in prompt or ".com" in prompt or ".in" in prompt or ".xyz" in prompt:

        result = check_url(prompt)

        response = f"🔍 **Website Analysis Result:**\n\n{result}"

    else:
        # AI CHAT MODE
        try:
            response = chat_with_ai(prompt)
        except Exception as e:
            response = f"Error: {e}"

    # show assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)