import streamlit as st

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TOTÁLNÍ STYLING (Oprava rámečků a centrování) ---
st.markdown("""
    <style>
    /* Totální průhlednost všeho od Streamlitu */
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stVerticalBlockBorderWrapper"],
    .stApp {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Černé pozadí pod vším */
    body {
        background-color: #000000 !important;
    }

    #canvas-container {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1;
    }

    /* Logo JT | CAPITAL */
    .logo-container { text-align: center; margin-top: 100px; margin-bottom: 25px; }
    .logo-text { font-family: 'Inter', sans-serif; font-weight: 900; font-size: 70px; letter-spacing: -3px; color: white; }
    .j-green { color: #2ecc71; }

    /* --- STYL OBDEÉLNÍKŮ (Inputy) --- */
    .stTextInput div[data-baseweb="input"] {
        background-color: rgba(15, 15, 15, 0.9) !important;
        border: 1px solid #333 !important; /* Základní barva rámečku */
        border-radius: 6px !important;
        height: 55px !important;
        transition: all 0.3s ease;
    }

    /* Efekt při kliknutí (Focus) - Zelený rámeček */
    .stTextInput div[data-baseweb="input"]:focus-within {
        border: 1px solid #2ecc71 !important;
        box-shadow: 0 0 10px rgba(46, 204, 113, 0.2) !important;
    }

    /* Centrování textu uvnitř */
    .stTextInput input {
        color: white !important;
        text-align: center !important;
        font-size: 16px !important;
        background: transparent !important;
    }

    /* --- ZELENÉ TLAČÍTKO --- */
    div.stButton > button {
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
        margin-top: 10px;
        transition: 0.3s !important;
    }

    div.stButton > button:hover {
        background-color: #27ae60 !important;
        transform: scale(1.01);
        box-shadow: 0 0 20px rgba(46, 204, 113, 0.3) !important;
    }

    /* Skrytí UI Streamlitu */
    footer, header, #MainMenu { visibility: hidden; }
    </style>

    <div id="canvas-container"><canvas id="chartCanvas"></canvas></div>

    <script>
    const canvas = document.getElementById('chartCanvas');
    const ctx = canvas.getContext('2d');
    function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    window.addEventListener('resize', resize);
    resize();

    const candles = [];
    for (let i = 0; i < 50; i++) {
        candles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            w: 12, h: Math.random() * 90 + 20,
            type: Math.random() > 0.5 ? '#2ecc71' : '#e74c3c',
            speed: Math.random() * 0.5 + 0.15
        });
    }

    function animate() {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 0.3; 
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
    # Odsazení odshora
    for _ in range(7): st.write("\n")
    
    # Logo JT | CAPITAL
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)
    
    # Vycentrovaný sloupec
    col1, col2, col3 = st.columns([1, 0.7, 1])
    with col2:
        num = st.text_input("NUMBER", placeholder="PŘIHLAŠOVACÍ ČÍSLO", label_visibility="collapsed")
        pwd = st.text_input("PASSWORD", type="password", placeholder="HESLO", label_visibility="collapsed")
        
        if st.button("PŘIHLÁSIT SE", use_container_width=True):
            if num == "1234" and pwd == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("PŘÍSTUP ZAMÍTNUT")
    st.stop()

# --- 4. VNITŘEK APLIKACE ---
st.sidebar.markdown('### JT | CAPITAL')
if st.sidebar.button("ODHLÁSIT SE"):
    st.session_state.authenticated = False
    st.rerun()

st.title("🏛 Dashboard")
st.write("Vítejte v uzavřené sekci JT | CAPITAL.")
