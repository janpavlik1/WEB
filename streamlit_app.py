import streamlit as st

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TOTÁLNÍ DESIGN (CSS) ---
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

    /* Vypnutí nápovědy "Press Enter to apply" pod políčky */
    [data-testid="InputInstructions"] {
        display: none !important;
    }

    /* Fixní černé pozadí pod canvasem */
    body {
        background-color: #000000 !important;
    }

    #canvas-container {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1;
    }

    /* Branding Loga */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .logo-text {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 60px;
        letter-spacing: -2px;
        color: white;
    }
    .j-green { 
        color: #2ecc71 !important; 
    }
    
    /* Vstupy (Inputy) */
    .stTextInput>div>div>input {
        background-color: rgba(22, 26, 31, 0.9) !important;
        color: white !important;
        border: 1px solid #333 !important;
        text-align: center !important; /* TEXT NA STŘED */
        height: 50px !important;
        border-radius: 5px !important;
    }

    /* ODSTRANĚNÍ RÁMEČKU při kliknutí */
    .stTextInput>div>div:focus-within {
        border-color: #2ecc71 !important;
        box-shadow: none !important;
    }
    .stTextInput input:focus {
        outline: none !important;
        border: 1px solid #2ecc71 !important;
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

    /* Skrytí menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>

    <div id="canvas-container">
        <canvas id="chartCanvas"></canvas>
    </div>

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
            w: 12, h: Math.random() * 80 + 20,
            type: Math.random() > 0.5 ? '#2ecc71' : '#e74c3c',
            speed: Math.random() * 0.5 + 0.2
        });
    }

    function animate() {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 0.2; 
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
    ## Odsazení odshora
    for _ in range(7): st.write("\n")
    
    # Logo JT | CAPITAL (Opravená třída pro zelenou barvu)
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)
    
    # Vycentrovaný sloupec
    col1, col2, col3 = st.columns([1, 0.7, 1])
    with col2:
        num = st.text_input("NUMBER", placeholder="PŘIHLAŠOVACÍ ČÍSLO", label_visibility="collapsed")
        pwd = st.text_input("PASSWORD", type="password", placeholder="HESLO", label_visibility="collapsed")
        
        st.write("") 
        if st.button("PŘIHLÁSIT SE", use_container_width=True):
            if num == "1234" and pwd == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("PŘÍSTUP ZAMÍTNUT")
    st.stop()

# --- 4. VNITŘEK APLIKACE ---
st.sidebar.markdown('<div style="font-size: 24px; font-weight: bold;"><span style="color: #2ecc71;">J</span>T | CAPITAL</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
menu = st.sidebar.radio("NAVIGACE", ["DASHBOARD", "KALENDÁŘ", "ADMIN"])

if menu == "DASHBOARD":
    st.title("Market Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("XAUUSD", "2,401.50", "+0.45%")
    c2.metric("NAS100", "18,450.00", "-0.12%", delta_color="inverse")
    c3.metric("DJ30", "39,200.00", "+0.08%")
    
    st.markdown("""
    <div style="background-color: rgba(30, 30, 30, 0.8); padding: 25px; border-radius: 10px; border: 1px solid #2ecc71; margin-top: 20px;">
        <h3 style="color: #2ecc71;">Vítejte v JT | CAPITAL TERMINAL</h3>
        <p>Všechny systémy jsou aktivní. Aktuálně sledujeme volatilitu na XAUUSD.</p>
    </div>
    """, unsafe_allow_html=True)
