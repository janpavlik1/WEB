import streamlit as st

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GRAFIKA A ANIMOVANÉ POZADÍ (CSS + JS) ---
st.markdown("""
    <style>
    /* Absolutní vyčištění Streamlit prvků */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background: transparent !important;
        background-color: #000000 !important;
    }
    
    #canvas-container {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1;
        background-color: #000000;
    }

    /* Logo JT | CAPITAL */
    .logo-container { text-align: center; margin-top: 80px; margin-bottom: 20px; }
    .logo-text { font-family: 'Inter', sans-serif; font-weight: 900; font-size: 70px; letter-spacing: -3px; color: white; }
    .j-green { color: #2ecc71; }

    /* Stylování inputů */
    .stTextInput input {
        background-color: rgba(20, 20, 20, 0.9) !important;
        color: white !important;
        border: 1px solid #333 !important;
        text-align: center !important;
        border-radius: 5px !important;
    }

    /* Schování zbytečností */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Úprava slideru (Slide to Unlock) */
    div[data-baseweb="slider"] {
        background-color: rgba(46, 204, 113, 0.1);
        border-radius: 50px;
        padding: 10px;
        border: 1px solid #2ecc71;
    }
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
    # Logo
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        num = st.text_input("PŘIHLAŠOVACÍ ČÍSLO", placeholder="Zadejte číslo")
        pwd = st.text_input("HESLO", type="password", placeholder="Zadejte heslo")
        
        st.write("\n")
        # SLIDE TO UNLOCK
        unlock_slider = st.slider("POTAŽENÍM DOPRAVA VSTOUPÍTE", 0, 100, 0)
        
        if unlock_slider == 100:
            if num == "1234" and pwd == "admin":
                st.session_state.authenticated = True
                st.success("AUTORIZACE ÚSPĚŠNÁ...")
                st.rerun()
            else:
                st.error("PŘÍSTUP ZAMÍTNUT")
                st.info("Vraťte slider doleva a zkuste to znovu.")
    st.stop()

# --- 4. VNITŘEK APLIKACE (Po přihlášení) ---
st.sidebar.markdown('<div style="font-size: 24px; font-weight: bold;"><span style="color: #2ecc71;">J</span>T | CAPITAL</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
menu = st.sidebar.radio("NAVIGACE", ["DASHBOARD", "KALENDÁŘ", "ANALÝZA"])

if menu == "DASHBOARD":
    st.title("Market Terminal Overview")
    
    # Live TradingView Ticker
    st.components.v1.html("""
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
        { "symbols": [ {"proName": "FX_IDC:XAUUSD", "description": "GOLD"}, {"proName": "NASDAQ:NAS100", "description": "NAS100"}, {"proName": "FX:DXY", "description": "DXY"} ], "colorTheme": "dark", "isTransparent": true }
        </script>
    """, height=50)

    st.markdown("""
    <div style="background-color: rgba(20, 20, 20, 0.8); padding: 30px; border-radius: 15px; border: 1px solid #2ecc71; margin-top: 20px;">
        <h2 style="color: #2ecc71; margin-top:0;">VÍTEJTE V JT | CAPITAL TERMINAL</h2>
        <p>Všechny systémy jsou aktivní. Aktuálně sledujeme setupy na XAUUSD.</p>
    </div>
    """, unsafe_allow_html=True)
