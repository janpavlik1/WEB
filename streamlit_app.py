import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. KOMPLEXNÍ DESIGN (CSS) ---
st.markdown("""
    <style>
    /* Odstranění pozadí Streamlitu */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainBlockContainer"], 
    [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockBorderWrapper"], .stApp {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Skrytí sidebaru a nápovědy */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="InputInstructions"] { display: none !important; }
    
    /* Fixní černé pozadí */
    body { background-color: #000000 !important; }
    #canvas-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; }
    
    /* Centrální Branding */
    .logo-container { text-align: center; margin-top: 20px; margin-bottom: 5px; }
    .logo-text { font-family: 'Inter', sans-serif; font-weight: 800; font-size: 60px; letter-spacing: -2px; color: white; }
    .j-green { color: #2ecc71 !important; }
    .version-tag { color: #444; letter-spacing: 3px; font-size: 10px; margin-top: -10px; margin-bottom: 20px; text-align: center; }
    
    /* Vstupy Login - Centrování textu */
    .stTextInput>div>div>input {
        background-color: rgba(25, 25, 25, 0.9) !important;
        color: white !important;
        border: 1px solid #333 !important;
        text-align: center !important;
        height: 55px !important;
        border-radius: 6px !important;
    }
    .stTextInput>div>div:focus-within { border-color: #2ecc71 !important; box-shadow: none !important; }

    /* ŠEDÝ NAVIGAČNÍ PANEL */
    .nav-bar {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }

    /* Styl tlačítek v menu (Menší obdélníky) */
    div.stButton > button {
        background-color: #2ecc71 !important;
        color: white !important;
        border: none !important;
        height: 45px !important;
        width: 100% !important;
        border-radius: 4px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #27ae60 !important; }

    /* Speciální styl pro ODHLÁSIT SE (Červené okénko) */
    .logout-btn > div > button {
        background-color: #e74c3c !important;
        color: white !important;
    }
    .logout-btn > div > button:hover {
        background-color: #c0392b !important;
    }

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
    for (let i = 0; i < 45; i++) {
        candles.push({
            x: Math.random() * canvas.width, y: Math.random() * canvas.height,
            w: 12, h: Math.random() * 80 + 20,
            type: Math.random() > 0.5 ? '#2ecc71' : '#e74c3c',
            speed: Math.random() * 0.4 + 0.15
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

# --- 3. SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "OVERVIEW"

# --- 4. LOGIN SCREEN ---
if not st.session_state.authenticated:
    for _ in range(7): st.write("\n")
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div><div class="version-tag">TERMINAL v1.1</div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 0.7, 1])
    with col2:
        num = st.text_input("NUMBER", placeholder="PRIHLASOVACI CISLO", label_visibility="collapsed")
        pwd = st.text_input("PASSWORD", type="password", placeholder="HESLO", label_visibility="collapsed")
        if st.button("PRIHLASIT SE", use_container_width=True):
            if num == "1234" and pwd == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("PRISTUP ZAMITNUT")
    st.stop()

# --- 5. DASHBOARD (Po přihlášení) ---

# Horní Logo
st.markdown('<div class="logo-container"><div class="logo-text" style="font-size:45px;"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)

# ŠEDÝ NAVIGAČNÍ PANEL S TLAČÍTKY
st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns([1, 1, 1, 1])
with m1:
    if st.button("OVERVIEW"): st.session_state.current_page = "OVERVIEW"; st.rerun()
with m2:
    if st.button("KALENDAR"): st.session_state.current_page = "KALENDAR"; st.rerun()
with m3:
    if st.button("FEED"): st.session_state.current_page = "FEED"; st.rerun()
with m4:
    # Červené tlačítko pro odhlášení
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("ODHLASIT SE"): st.session_state.authenticated = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- LOGIKA OBSAHU ---

if st.session_state.current_page == "OVERVIEW":
    st.subheader("MARKET OVERVIEW")
    
    # Live Ticker Tape
    components.html("""
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
        { "symbols": [ {"proName": "FX_IDC:XAUUSD", "description": "GOLD"}, {"proName": "NASDAQ:NAS100", "description": "NASDAQ"}, {"proName": "CURRENCYCOM:DJ30", "description": "DOW JONES"} ], "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "cs" }
        </script>
    """, height=50)

    # 3 Živé karty
    c1, c2, c3 = st.columns(3)
    with c1: components.html("""<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>{ "symbol": "FX_IDC:XAUUSD", "width": "100%", "height": "220", "locale": "cs", "dateRange": "12M", "colorTheme": "dark", "trendLineColor": "#2ecc71", "underLineColor": "rgba(46, 204, 113, 0.15)", "isTransparent": true }</script>""", height=230)
    with c2: components.html("""<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>{ "symbol": "NASDAQ:NAS100", "width": "100%", "height": "220", "locale": "cs", "dateRange": "12M", "colorTheme": "dark", "trendLineColor": "#2ecc71", "underLineColor": "rgba(46, 204, 113, 0.15)", "isTransparent": true }</script>""", height=230)
    with c3: components.html("""<script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>{ "symbol": "CURRENCYCOM:DJ30", "width": "100%", "height": "220", "locale": "cs", "dateRange": "12M", "colorTheme": "dark", "trendLineColor": "#2ecc71", "underLineColor": "rgba(46, 204, 113, 0.15)", "isTransparent": true }</script>""", height=230)

    st.markdown('<div style="background-color:rgba(25,25,25,0.8); padding:20px; border-radius:10px; border-left:4px solid #2ecc71;"><h4>MARKET SENTIMENT</h4><p>GOLD TESTUJE SUPPORT. INDEXY VYCRAVAJI NA NY SESSION.</p></div>', unsafe_allow_html=True)

elif st.session_state.current_page == "KALENDAR":
    st.subheader("EKONOMICKY KALENDAR")
    components.html("""
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
        { "colorTheme": "dark", "isTransparent": true, "width": "100%", "height": "600", "locale": "cs", "importanceFilter": "-1,0,1" }
        </script>
    """, height=600)

elif st.session_state.current_page == "FEED":
    st.subheader("FUNDAMENTAL FEED")
    st.info("ZDE BUDOU PUBLIKOVANY DENNI ANALYZY.")
    st.markdown("---")
    st.write("SLEDUJEME AKTUALNI POHYBY NA TRHU.")
