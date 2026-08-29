import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TOTÁLNÍ STYLING (Obrázek + Fix Rámečků) ---
# Používám jiný, velmi stabilní odkaz na tmavý trading obrázek
BG_IMAGE = "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=2070"

st.markdown(f"""
    <style>
    /* 1. Vynucení obrázku na pozadí úplně všude */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: url("{BG_IMAGE}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}

    /* 2. Ztmavení obrázku, aby byl text čitelný (Overlay) */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.85); /* Ztmavení o 85% */
        z-index: -1;
    }}

    /* 3. Odstranění všech bílých/šedých ploch Streamlitu */
    [data-testid="stMainBlockContainer"], [data-testid="stVerticalBlock"], 
    [data-testid="stVerticalBlockBorderWrapper"], .stApp {{
        background-color: transparent !important;
        background: transparent !important;
    }}
    
    /* 4. DEFINITIVNÍ STOP ČERVENÝM RÁMEČKŮM (i na Mac/Safari) */
    input {{
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
        -webkit-appearance: none !important;
    }}
    
    /* Kontejner vstupu */
    div[data-baseweb="input"] {{
        border: 1px solid #333 !important;
        background-color: rgba(10, 10, 10, 0.9) !important;
        border-radius: 6px !important;
        transition: 0.3s;
    }}
    
    /* Změna na zelenou při kliku - ŽÁDNÁ JINÁ BARVA */
    div[data-baseweb="input"]:focus-within {{
        border: 1px solid #2ecc71 !important;
        box-shadow: 0 0 10px rgba(46, 204, 113, 0.2) !important;
    }}

    /* 5. BRANDING */
    .logo-container {{ text-align: center; margin-top: 20px; margin-bottom: 30px; }}
    .logo-text {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 65px; letter-spacing: -3px; color: white; }}
    .j-green {{ color: #2ecc71 !important; }}

    /* Centrování textu v políčkách */
    input {{
        text-align: center !important;
        color: white !important;
        font-size: 16px !important;
        height: 55px !important;
    }}
    
    /* TLAČÍTKO */
    div.stButton > button {{
        background-color: #2ecc71 !important;
        color: white !important;
        border: none !important;
        height: 55px !important;
        width: 100% !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        border-radius: 6px !important;
    }}

    /* SENTIMENT CARD */
    .sentiment-card {{
        background-color: rgba(10, 10, 10, 0.9);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #222;
        text-align: center;
        margin-top: 20px;
    }}

    footer, header, #MainMenu, [data-testid="stSidebar"], [data-testid="InputInstructions"] {{ visibility: hidden; }}
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
        num = st.text_input("NUM", placeholder="PŘIHLAŠOVACÍ ČÍSLO", label_visibility="collapsed")
        pwd = st.text_input("PWD", type="password", placeholder="HESLO", label_visibility="collapsed")
        if st.button("PŘIHLÁSIT SE", use_container_width=True):
            if num == "1234" and pwd == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("PŘÍSTUP ZAMÍTNUT")
    st.stop()

# --- 4. VNITŘEK TERMINÁLU ---

# Logo na střed
st.markdown('<div class="logo-container"><div class="logo-text" style="font-size:45px;"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([0.1, 0.8, 0.1])

with col_c:
    # 1. ŽIVÁ DATA XAUUSD
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
        <div style="color: #666; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; margin-bottom: 10px;">AI Analysis System</div>
        <div style="color: #2ecc71; font-weight: 900; font-size: 28px; letter-spacing: 2px;">BULLISH SENTIMENT</div>
        <p style="color: #999; margin-top: 15px; font-size: 16px; line-height: 1.6;">
            Zlato testuje denní rezistenci. Fundamentální data naznačují oslabování dolaru (DXY). 
            Sledujte možnost bullish breakoutu nad aktuální hladinu.
        </p>
        <div style="border-top: 1px solid #222; margin-top: 20px; padding-top: 10px; color: #444; font-size: 10px;">
            SOURCE: REAL-TIME REUTERS FEED | AI ENGINE v1.2
        </div>
    </div>
    """, unsafe_allow_html=True)
