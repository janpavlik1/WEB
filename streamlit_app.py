import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. KOMPLEXNÍ DESIGN (CSS s obrázkem na pozadí) ---
# Odkaz na obrázek (lze kdykoliv vyměnit za jinou URL)
BG_IMAGE_URL = "https://images.unsplash.com/photo-1611974717482-75d31276a603?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
    <style>
    /* Nastavení obrázku na pozadí celé aplikace */
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), url("{BG_IMAGE_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Odstranění všech výchozích barev Streamlitu */
    [data-testid="stHeader"], [data-testid="stMainBlockContainer"], 
    [data-testid="stVerticalBlock"], [data-testid="stVerticalBlockBorderWrapper"], .stApp {{
        background: transparent !important;
        background-color: transparent !important;
    }}
    
    [data-testid="stSidebar"] {{ display: none !important; }}
    [data-testid="InputInstructions"] {{ display: none !important; }}
    
    /* DEFINITIVNÍ ODSTRANĚNÍ BAREVNÝCH RÁMEČKŮ */
    input {{
        outline: none !important;
        box-shadow: none !important;
        -webkit-box-shadow: none !important;
        border: none !important;
    }}
    .stTextInput>div>div {{
        border: 1px solid #444 !important;
        box-shadow: none !important;
        background-color: rgba(15, 15, 15, 0.95) !important;
    }}
    .stTextInput>div>div:focus-within {{
        border: 1px solid #2ecc71 !important;
        box-shadow: none !important;
    }}

    .logo-container {{ text-align: center; margin-top: 20px; margin-bottom: 30px; }}
    .logo-text {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 65px; letter-spacing: -3px; color: white; }}
    .j-green {{ color: #2ecc71 !important; }}

    /* Login Inputs */
    .stTextInput>div>div>input {{
        color: white !important;
        text-align: center !important;
        height: 55px !important;
        font-size: 16px !important;
    }}
    
    /* Login Button */
    div.stButton > button {{
        background-color: #2ecc71 !important;
        color: white !important;
        border: none !important;
        height: 55px !important;
        width: 100% !important;
        border-radius: 6px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        background-color: #27ae60 !important;
        transform: scale(1.01);
    }}

    /* Sentiment Box */
    .sentiment-card {{
        background-color: rgba(15, 15, 15, 0.95);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #333;
        text-align: center;
        margin-top: 20px;
    }}
    .sentiment-bullish {{ color: #2ecc71; font-weight: 900; font-size: 28px; letter-spacing: 2px; }}

    footer, header, #MainMenu {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN LOGIKA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    for _ in range(8): st.write("\n")
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
    st.markdown("""
    <div class="sentiment-card">
        <div style="color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; margin-bottom: 10px;">AI Terminal Analysis</div>
        <div class="sentiment-bullish">BULLISH SENTIMENT</div>
        <p style="color: #bbb; margin-top: 15px; font-size: 16px; line-height: 1.6;">
            Zlato testuje denní rezistenci. Fundamentální data naznačují oslabování dolaru (DXY). 
            Sledujte možnost bullish breakoutu nad aktuální hladinu.
        </p>
        <div style="border-top: 1px solid #333; margin-top: 20px; padding-top: 10px; color: #555; font-size: 11px;">
            POSLEDNÍ AKTUALIZACE: PŘED CHVÍLÍ | SOURCE: AI ENGINE 1.0
        </div>
    </div>
    """, unsafe_allow_html=True)
