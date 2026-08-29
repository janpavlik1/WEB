import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TOTÁLNÍ DESIGN (CSS) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainBlockContainer"], 
    [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockBorderWrapper"], .stApp {
        background: transparent !important;
        background-color: transparent !important;
    }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="InputInstructions"] { display: none !important; }
    
    body { background-color: #000000 !important; }
    #canvas-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; }
    
    .logo-container { text-align: center; margin-top: 20px; margin-bottom: 30px; }
    .logo-text { font-family: 'Inter', sans-serif; font-weight: 800; font-size: 60px; letter-spacing: -2px; color: white; }
    .j-green { color: #2ecc71 !important; }

    /* Login Inputs */
    .stTextInput>div>div>input {
        background-color: rgba(25, 25, 25, 0.9) !important;
        color: white !important;
        border: 1px solid #333 !important;
        text-align: center !important;
        height: 55px !important;
        border-radius: 6px !important;
    }
    
    /* Login Button */
    div.stButton > button {
        background-color: #2ecc71 !important;
        color: white !important;
        border: none !important;
        height: 55px !important;
        width: 100% !important;
        border-radius: 6px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
    }

    /* Sentiment Box */
    .sentiment-card {
        background-color: rgba(20, 20, 20, 0.9);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #333;
        text-align: center;
        margin-top: 20px;
    }
    .sentiment-bullish { color: #2ecc71; font-weight: 900; font-size: 28px; letter-spacing: 2px; }
    .sentiment-bearish { color: #e74c3c; font-weight: 900; font-size: 28px; letter-spacing: 2px; }

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

# --- 3. LOGIN LOGIKA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    for _ in range(7): st.write("\n")
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)
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

# --- 4. VNITŘEK TERMINÁLU (Po přihlášení) ---

# Logo na střed
st.markdown('<div class="logo-container"><div class="logo-text" style="font-size:45px;"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)

# Centrální layout pro XAUUSD
col_l, col_c, col_r = st.columns([0.1, 0.8, 0.1])

with col_c:
    # 1. ŽIVÁ DATA XAUUSD (Widget)
    components.html("""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
          {
          "symbols": [ ["FX_IDC:XAUUSD|12M"] ],
          "chartOnly": false, "width": "100%", "height": "350", "locale": "cs", "colorTheme": "dark",
          "gridLineColor": "rgba(42, 46, 57, 0)", "fontColor": "#787b86", "isTransparent": true,
          "showFloatingTooltip": true, "showVolume": false,
          "lineColor": "#2ecc71", "topColor": "rgba(46, 204, 113, 0.15)", "bottomColor": "rgba(46, 204, 113, 0)"
        }
          </script>
        </div>
    """, height=360)

    # 2. AI MARKET SENTIMENT BOX
    # Zde v budoucnu propojíme AI analýzu z Reuters/Bloomberg
    # Pro demonstraci: Bullish scénář
    st.markdown("""
    <div class="sentiment-card">
        <div style="color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; margin-bottom: 10px;">AI Terminal Analysis</div>
        <div class="sentiment-bullish">BULLISH SENTIMENT</div>
        <p style="color: #bbb; margin-top: 15px; font-size: 16px; line-height: 1.6;">
            Zlato testuje denní rezistenci. Fundamentální data z Reuters naznačují oslabování dolaru (DXY). 
            Sledujte možnost bullish breakoutu nad aktuální hladinu.
        </p>
        <div style="border-top: 1px solid #333; margin-top: 20px; padding-top: 10px; color: #555; font-size: 11px;">
            POSLEDNÍ AKTUALIZACE: PŘED 2 MINUTAMI | SOURCE: AI ENGINE 1.0
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tlačítko pro odhlášení (skryté dole pro čistotu)
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("ODHLÁSIT SE", use_container_width=False):
    st.session_state.authenticated = False
    st.rerun()
