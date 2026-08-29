import streamlit as st

# --- 1. KONFIGURACE STRÁNKY ---
st.set_page_config(
    page_title="JT | CAPITAL",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TOTÁLNÍ ČISTKA POZADÍ A STYLING ---
st.markdown("""
    <style>
    /* Odstranění všech vrstev pozadí Streamlitu */
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stMainBlockContainer"],
    .stApp {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Fixní černé pozadí úplně vespod */
    body {
        background-color: #000000 !important;
    }

    /* Plátno pro animaci grafu */
    #bg-canvas {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        z-index: -1;
    }

    /* LOGO JT | CAPITAL */
    .logo-container { 
        text-align: center; 
        margin-top: 100px; 
        margin-bottom: 30px; 
    }
    .logo-text { 
        font-family: 'Inter', sans-serif; 
        font-weight: 900; 
        font-size: 75px; 
        letter-spacing: -4px; 
        color: white; 
    }
    .j-green { color: #2ecc71; }

    /* INPUTY (Centrovaný text) */
    .stTextInput input {
        background-color: rgba(20, 20, 20, 0.9) !important;
        color: white !important;
        border: 1px solid #333 !important;
        height: 55px !important;
        border-radius: 6px !important;
        text-align: center !important; /* Text na střed */
        font-size: 16px !important;
        margin-bottom: 10px !important;
    }
    .stTextInput input:focus {
        border-color: #2ecc71 !important;
        box-shadow: 0 0 10px rgba(46, 204, 113, 0.2) !important;
    }

    /* ZELENÉ TLAČÍTKO (Centrované automaticky v col2) */
    .stButton > button {
        background-color: #2ecc71 !important;
        color: white !important;
        border: none !important;
        height: 55px !important;
        width: 100% !important;
        border-radius: 6px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #27ae60 !important;
        transform: scale(1.02);
    }

    /* Skrytí prvků Streamlitu */
    footer, header, #MainMenu { visibility: hidden; }
    </style>

    <canvas id="bg-canvas"></canvas>

    <script>
    const canvas = document.getElementById('bg-canvas');
    const ctx = canvas.getContext('2d');
    function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    window.addEventListener('resize', resize);
    resize();

    const candles = [];
    for (let i = 0; i < 45; i++) {
        candles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            w: 12, h: Math.random() * 80 + 20,
            type: Math.random() > 0.5 ? '#2ecc71' : '#e74c3c',
            speed: Math.random() * 0.5 + 0.2
        });
    }

    function animate() {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 0.25; 
        candles.forEach(c => {
            c.x -= c.speed;
            if (c.x < -20) { c.x = canvas.width + 20; c.y = Math.random() * canvas.height; }
            ctx.fillStyle = c.type;
            ctx.fillRect(c.x, c.y, c.w, c.h);
            ctx.fillRect(c.x + c.w/2 - 1, c.y - 15, 2, c.h + 30);
        });
        requestAnimationFrame(animate);
    }
    animate();
    </script>
    """, unsafe_allow_html=True)

# --- 3. LOGIN LOGIKA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Logo JT | CAPITAL
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)
    
    # Centrovací sloupec
    col1, col2, col3 = st.columns([1, 0.7, 1])
    with col2:
        num = st.text_input("NUM", placeholder="PŘIHLAŠOVACÍ ČÍSLO", label_visibility="collapsed")
        pwd = st.text_input("PWD", type="password", placeholder="HESLO", label_visibility="collapsed")
        
        st.write("\n")
        if st.button("PŘIHLÁSIT SE"):
            if num == "1234" and pwd == "admin":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("PŘÍSTUP ZAMÍTNUT")
    st.stop()

# --- 4. VNITŘEK APLIKACE (Po přihlášení) ---
st.sidebar.markdown('### JT | CAPITAL')
if st.sidebar.button("ODHLÁSIT SE"):
    st.session_state.authenticated = False
    st.rerun()

st.title("🏛 Dashboard")
st.write("Vítejte v uzavřené sekci JT | CAPITAL.")
