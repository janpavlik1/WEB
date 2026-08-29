import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TOTÁLNÍ STYLING (Vynucený design a Safari Border Kill) ---
BG_IMAGE = "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=2070"

st.markdown(f"""
    <style>
    /* 1. GLOBÁLNÍ RESET - ZÁKAZ VŠECH RÁMEČKŮ (PRO SAFARI) */
    * {{
        outline: none !important;
        box-shadow: none !important;
        -webkit-tap-highlight-color: transparent !important;
    }}

    /* Pozadí aplikace */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: url("{BG_IMAGE}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}
    [data-testid="stAppViewContainer"]::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.9); z-index: -1;
    }}
    [data-testid="stMainBlockContainer"], [data-testid="stVerticalBlock"], 
    [data-testid="stVerticalBlockBorderWrapper"], .stApp {{
        background-color: transparent !important;
    }}

    /* --- LOGIN INPUTY - DEFINITIVNÍ OPRAVA --- */
    input {{
        border: none !important;
        background: transparent !important;
        text-align: center !important;
        color: white !important;
        font-size: 16px !important;
        height: 55px !important;
    }}
    
    /* Obalový obdélník vstupu */
    div[data-baseweb="input"] {{
        background-color: rgba(15, 15, 15, 0.95) !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
        transition: 0.3s;
    }}
    
    /* Zelený rámeček POUZE při aktivaci */
    div[data-baseweb="input"]:focus-within {{
        border: 1px solid #2ecc71 !important;
    }}

    /* Branding */
    .logo-container {{ text-align: center; margin-top: 20px; margin-bottom: 30px; }}
    .logo-text {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 65px; letter-spacing: -3px; color: white; }}
    .j-green {{ color: #2ecc71 !important; }}

    /* Tlačítko */
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

    /* TERMINAL CARDS (Sjednocené podsvícení pro Graf i Sentiment) */
    .terminal-card {{
        background-color: rgba(12, 12, 12, 0.92) !important; /* Černé podsvícení */
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #222;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}

    .sentiment-bullish {{ color: #2ecc71; font-weight: 900; font-size: 28px; letter-spacing: 2px; text-align: center; }}

    footer, header, #MainMenu, [data-testid="stSidebar"], [data-testid="InputInstructions"] {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN LOGIKA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    for _ in range(8): st.write("\n")
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div><div style="color:#333; font-size:10px; letter-spacing:3px;">v1.5 TERMINAL</div></div>', unsafe_allow_html=True)
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

# Logo
st.markdown('<div class="logo-container"><div class="logo-text" style="font-size:45px;"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([0.1, 0.8, 0.1])

with col_c:
    # 1. KARTA S GRAFEM (S černým podsvícením)
    st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. KARTA SE SENTIMENTEM (Identický styl)
    st.markdown("""
    <div class="terminal-card">
        <div style="color: #666; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; margin-bottom: 10px; text-align: center;">Intelligence Analysis</div>
        <div class="sentiment-bullish">BULLISH SENTIMENT</div>
        <p style="color: #999; margin-top: 15px; font-size: 16px; line-height: 1.6; text-align: center;">
            Zlato testuje denní rezistenci. Fundamentální data naznačují oslabování dolaru (DXY). 
            Sledujte možnost bullish breakoutu nad aktuální hladinu.
        </p>
        <div style="border-top: 1px solid #222; margin-top: 20px; padding-top: 10px; color: #444; font-size: 10px; text-align: center;">
            SYSTEM STATUS: ONLINE | ANALYZING DATA
        </div>
    </div>
    """, unsafe_allow_html=True)
