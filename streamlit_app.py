import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TOTÁLNÍ DESIGN (Vynucená černá, zelená a centrování) ---
st.markdown("""
    <style>
    /* 1. Odstranění barev pozadí Streamlitu */
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"],
    .stApp {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* 2. Vypnutí nápovědy "Press Enter" pod políčky */
    [data-testid="InputInstructions"] {
        display: none !important;
    }

    /* 3. Fixní černé pozadí */
    body {
        background-color: #000000 !important;
    }

    #canvas-container {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1;
    }

    /* 4. Branding Loga - OPRAVA ZELENÉ BARVY */
    .logo-container {
        text-align: center;
        margin-bottom: 10px;
    }
    .logo-text {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 65px;
        letter-spacing: -3px;
        color: white;
    }
    .j-green { 
        color: #2ecc71 !important; 
    }
    
    /* 5. Vstupy (Inputy) - CENTROVÁNÍ TEXTU */
    .stTextInput>div>div>input {
        background-color: rgba(25, 25, 25, 0.95) !important;
        color: white !important;
        border: 1px solid #333 !important;
        text-align: center !important; /* TEXT DO STŘEDU */
        height: 55px !important;
        border-radius: 6px !important;
        font-size: 16px !important;
    }

    /* Odstranění rámečků při kliku */
    .stTextInput>div>div:focus-within {
        border-color: #2ecc71 !important;
        box-shadow: none !important;
    }

    /* 6. ZELENÉ TLAČÍTKO */
    div.stButton > button {
        background-color: #2ecc71 !important;
        color: white !important;
        border: none !important;
        height: 55px !important;
        width: 100% !important;
        border-radius: 6px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        margin-top: 15px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #27ae60 !important;
        transform: scale(1.01);
    }
    </style>

    <!-- Hýbající se svíčky na pozadí -->
    <div id="canvas-container"><canvas id="chartCanvas"></canvas></div>
    <script>
    const canvas = document.getElementById('chartCanvas');
    const ctx = canvas.getContext('2d');
    function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    window.addEventListener('resize', resize);
    resize();
    const candles = [];
    for (let i = 0; i < 45; i++) {
        candles.push({
            x: Math.random() * canvas.width, y: Math.random() * canvas.height,
            w: 12, h: Math.random() * 80 + 20,
            type: Math.random() > 0.5 ? '#2ecc71' : '#e74c3c',
            speed: Math.random() * 0.5 + 0.2
        });
    }
    function animate() {
        ctx.fillStyle = '#000000'; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 0.2; 
        candles.forEach(c => {
            c.x -= c.speed;
            if (c.x < -20) { c.x = canvas.width + 20; c.y = Math.random() * canvas.height; }
            ctx.fillStyle = c.type; ctx.fillRect(c.x, c.y, c.w, c.h);
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
    for _ in range(7): st.write("\n")
    # LOGO s třídou j-green pro zelené J
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div><div style="color:#444; letter-spacing:3px; font-size:10px;">TERMINAL v1.0</div></div>', unsafe_allow_html=True)
    
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

# --- 4. VNITŘEK APLIKACE (Po přihlášení) ---
st.sidebar.markdown('<div style="font-size: 24px; font-weight: bold; color: white;"><span style="color: #2ecc71;">J</span>T | CAPITAL</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
menu = st.sidebar.radio("NAVIGACE", ["🏛 DASHBOARD", "📅 KALENDÁŘ", "🛠 ADMIN"])

if menu == "🏛 DASHBOARD":
    st.title("Market Overview")

    # 1. LIVE TICKER TAPE (Běžící pás)
    components.html("""
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
        {
          "symbols": [
            {"proName": "FX_IDC:XAUUSD", "description": "Zlato"},
            {"proName": "NASDAQ:NAS100", "description": "Nasdaq 100"},
            {"proName": "CURRENCYCOM:DJ30", "description": "Dow Jones 30"},
            {"proName": "FX:DXY", "description": "DXY"}
          ],
          "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "cs"
        }
        </script>
    """, height=50)

    # 2. ŽIVÉ KARTY PÁRŮ
    c1, c2, c3 = st.columns(3)
    with c1:
        components.html("""
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
            { "symbol": "FX_IDC:XAUUSD", "width": "100%", "height": "220", "locale": "cs", "dateRange": "12M", "colorTheme": "dark", "trendLineColor": "#2ecc71", "underLineColor": "rgba(46, 204, 113, 0.15)", "isTransparent": true }
            </script>
        """, height=230)
    with c2:
        components.html("""
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
            { "symbol": "NASDAQ:NAS100", "width": "100%", "height": "220", "locale": "cs", "dateRange": "12M", "colorTheme": "dark", "trendLineColor": "#2ecc71", "underLineColor": "rgba(46, 204, 113, 0.15)", "isTransparent": true }
            </script>
        """, height=230)
    with c3:
        components.html("""
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
            { "symbol": "CURRENCYCOM:DJ30", "width": "100%", "height": "220", "locale": "cs", "dateRange": "12M", "colorTheme": "dark", "trendLineColor": "#2ecc71", "underLineColor": "rgba(46, 204, 113, 0.15)", "isTransparent": true }
            </script>
        """, height=230)

    st.markdown("---")
    st.subheader("💡 Fundamentální analýza dne")
    st.info("Zlato: Dnes očekáváme testování rezistence. Sledujte DXY pro potvrzení směru.")

if st.sidebar.button("ODHLÁSIT SE"):
    st.session_state.authenticated = False
    st.rerun()
