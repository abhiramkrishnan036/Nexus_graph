import streamlit as st
import requests
import time
import PyPDF2 
import base64
from datetime import datetime

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="NEXUS-GRAPH OS", page_icon="🧬", layout="wide")

# --- 2. HIGH-END VISUAL ENGINE (LOGO + ANIMATIONS + BG) ---
def get_base64_logo():
    # Placeholder for logo logic - using a stylized emoji-text logo for high-end look
    return "🧬 NEXUS-GRAPH OS"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono&display=swap');
    
    :root { 
        --primary: #7c4dff; 
        --secondary: #00ffd5; 
        --bg: #030406; 
        --glass: rgba(13, 14, 18, 0.9); 
        --glow: rgba(0, 255, 213, 0.2);
    }
    
    /* 1. ANIMATED NEURAL BACKGROUND */
    .stApp { 
        background: radial-gradient(circle at 50% 50%, #12141d 0%, #030406 100%);
        overflow: hidden;
    }
    .stApp::before {
        content: ""; position: absolute; width: 200%; height: 200%; top: -50%; left: -50%;
        background-image: radial-gradient(circle, rgba(124, 77, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px; animation: rotateBG 100s linear infinite; z-index: -1;
    }
    @keyframes rotateBG { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

    /* 2. LOGO DESIGN */
    .logo-container {
        padding: 20px 0; text-align: center;
        filter: drop-shadow(0 0 10px var(--primary));
        animation: pulse 3s ease-in-out infinite;
    }
    @keyframes pulse { 0%, 100% { opacity: 0.8; } 50% { opacity: 1; } }

    /* 3. NEON SHINE TITLE */
    .hero-title { 
        background: linear-gradient(90deg, #fff, var(--primary), var(--secondary), #fff);
        background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 2.8rem; letter-spacing: -2px; animation: shine 4s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* 4. QUANTUM POPUP CARDS (GLASSMORPHISM) */
    .dossier-card { 
        background: var(--glass); border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; 
        padding: 25px; margin-bottom: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        backdrop-filter: blur(15px); animation: quantumPopup 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes quantumPopup {
        0% { opacity: 0; transform: scale(0.95) translateY(20px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    /* 5. CHATBOT ENHANCEMENTS */
    .stChatMessage { 
        background: rgba(124, 77, 255, 0.05) !important; 
        border: 1px solid rgba(124, 77, 255, 0.1) !important;
        border-radius: 15px !important; margin-bottom: 12px !important;
        transition: all 0.3s ease;
    }
    .stChatMessage:hover { border-color: var(--secondary) !important; box-shadow: 0 0 15px var(--glow); }

    /* 6. CUSTOM SCROLLBAR */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONNECTION SYNC ---
BACKEND_URL = "http://127.0.0.1:8000"
is_alive = False
try:
    if requests.get(BACKEND_URL, timeout=1).status_code == 200: is_alive = True
except: is_alive = False

# --- 4. SIDEBAR (LOGO + STATUS) ---
with st.sidebar:
    st.markdown(f'<div class="logo-container"><h1 style="font-size:22px; color:white; margin:0;">🧬 NEXUS-GRAPH OS</h1><small style="color:var(--secondary)">ELITE_SYNC EDITION</small></div>', unsafe_allow_html=True)
    
    status_c = "#00ffd5" if is_alive else "#ff4b4b"
    st.markdown(f'<div style="background:rgba(255,255,255,0.03); padding:12px; border-radius:12px; border-left:4px solid {status_c}; margin: 10px 0;"><b>SYSTEM:</b> <span style="color:{status_c};">{"LINKED" if is_alive else "OFFLINE"}</span></div>', unsafe_allow_html=True)
    
    menu = st.radio("CORE_INTERFACE", ["✧ DISCOVER", "💬 RESEARCH_ASSISTANT", "📊 ANALYTICS"])
    st.markdown("---")
    st.caption(f"SESSION: {datetime.now().strftime('%H:%M:%S')} | MODEL: 8B_INSTANT")

# --- 5. FUNCTIONAL MODULES ---

# MODULE: DISCOVER (Research Engine)
if menu == "✧ DISCOVER":
    st.markdown('<h1 class="hero-title">Research Engine</h1>', unsafe_allow_html=True)
    q = st.text_input("QUERY", placeholder="Ask the knowledge network...", label_visibility="collapsed")
    if st.button("RUN DEEP RESEARCH"):
        if is_alive and q:
            with st.spinner("🧬 Navigating Knowledge Nodes..."):
                try:
                    res = requests.post(f"{BACKEND_URL}/ask", json={"text": f"Dossier research on: {q}"}, timeout=120).json().get("answer")
                    st.markdown(f'<div class="dossier-card"><b>📌 SYNTHESIZED DOSSIER:</b><br><br>{res}</div>', unsafe_allow_html=True)
                except: st.error("Sync Lost.")

# MODULE: RESEARCH ASSISTANT (Split View: Ingestion + Chat)
elif menu == "💬 RESEARCH_ASSISTANT":
    st.markdown('<h1 class="hero-title">Research Assistant</h1>', unsafe_allow_html=True)
    
    # High-End Split View
    col_left, col_right = st.columns([1, 1.2], gap="large")
    
    with col_left:
        st.markdown("### 📂 Data Ingestion")
        with st.expander("UPLOAD KNOWLEDGE SEED", expanded=True):
            up = st.file_uploader("PDF", type=['pdf'], label_visibility="collapsed")
            if up and st.button("EXECUTE SCAN"):
                with st.status("🛸 SCANNING NODES..."):
                    pdf = PyPDF2.PdfReader(up)
                    txt = "".join([p.extract_text() for p in pdf.pages])
                    res = requests.post(f"{BACKEND_URL}/ask", json={"text": f"Analyze: {txt[:3500]}"}).json().get("answer")
                    st.markdown(f'<div class="dossier-card"><b>📑 {up.name}</b><br><br>{res}</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown("### 💬 Quantum Chat")
        # Chat box with fixed height and glass styling
        chat_box = st.container(height=500, border=True)
        
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hey Abhi! Everything is updated. I'm ready to analyze your files or answer research questions."}]

        with chat_box:
            for m in st.session_state.messages:
                with st.chat_message(m["role"]): st.markdown(m["content"])

        if chat_input := st.chat_input("Ask a research follow-up..."):
            st.session_state.messages.append({"role": "user", "content": chat_input})
            with chat_box:
                with st.chat_message("user"): st.markdown(chat_input)
                with st.chat_message("assistant"):
                    try:
                        res = requests.post(f"{BACKEND_URL}/ask", json={"text": chat_input}).json().get("answer")
                        st.markdown(res)
                        st.session_state.messages.append({"role": "assistant", "content": res})
                    except: st.error("Backend link failed.")

# MODULE: ANALYTICS
elif menu == "📊 ANALYTICS":
    st.markdown('<h1 class="hero-title">Graph Vitals</h1>', unsafe_allow_html=True)
    st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="dossier-card" style="text-align:center;">
                <small style="color:var(--secondary)">KNOWLEDGE ENTITIES</small><h3>42,918</h3>
            </div>
            <div class="dossier-card" style="text-align:center;">
                <small style="color:var(--primary)">GRAPH EDGES</small><h3>187,402</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)