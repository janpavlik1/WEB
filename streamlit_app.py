import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TOTÁLNÍ DESIGN (v1.7 - Safari Kill & Unified Cards) ---
BG_IMAGE = "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=2070"

st.markdown(f"""
    <style>
    /* RESET PRO SAFARI - ZÁKAZ ČERVENÉ */
    input:invalid, input:out-of-range, input:required {{
        box-shadow: none !important;
        border: none !important;
    }}
    * {{
        -webkit-tap-highlight-color: transparent !important;
        outline: none !important;
    }}

    /* Pozadí a overlay */
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

    /* LOGIN INPUTY - OPRAVA RÁMEČKŮ */
    input {{
        -webkit-appearance: none !important;
        appearance: none !important;
        border: none !important;
        background: transparent !important;
        text-align: center !important;
        color: white !important;
        font-size: 16px !important;
        height: 55px !important;
    }}
    div[data-baseweb="input"] {{
        background-color: rgba(10, 10, 10, 0.95) !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
    }}
    div[data-baseweb="input"]:focus-within {{
        border: 1px solid #2ecc71 !important;
    }}

    /* Branding */
    .logo-container {{ text-align: center; margin-top: 20px; margin-bottom: 20px; }}
    .logo-text {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 65px; letter-spacing: -3px; color: white; }}
    .j-green {{ color: #2ecc71 !important; }}

    /* Tlačítko Přihlásit */
    div.stButton > button {{
        background-color: #2ecc71 !important;
        color: white !important;
        border: none !important;
        height: 55px !important;
        width: 100% !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        border-radius: 6px !important;
        margin-top: 10px;
    }}

    /* UNIFIED TERMINAL CARDS (Pro graf i sentiment) */
    .terminal-card {{
        background-color: #0a0a0a !important; /* Čistě černá */
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #222;
        margin-bottom: 30px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    }}

    .sentiment-title {{
        color: #2ecc71; font-weight: 900; font-size: 28px; 
        letter-spacing: 2px; text-align: center; margin-bottom: 15px;
    }}

    footer, header, #MainMenu, [data-testid="stSidebar"], [data-testid="InputInstructions"] {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN LOGIKA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Odsazení jen pomocí markdownu, aby nevyskakovaly texty kódu
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div><div style="color:#333; font-size:10px; letter-spacing:3px;">TERMINAL v1.7</div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 0.7, 1])
    with col2:
        num = st.text_input("NUM", placeholder="PŘIHLASOVACÍ ČÍSLO", label_visibility="collapsed")
        pwd = st.text_input("PWD", type="password", placeholder="HESLO", label_visibility="collapsed")
        if st.button("PŘIHLÁSIT SE"):
            if num == "1234" and pwd == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("PŘÍSTUP ZAMÍTNUT")
    st.stop()

# --- 4. VNITŘEK TERMINÁLU ---

# Logo na střed
st.markdown('<div class="logo-container"><div class="logo-text" style="font-size:45px; margin-top:10px;"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([0.1, 0.8, 0.1])

with col_c:
    # 1. KARTA S GRAFEM (Nyní v černém boxu)
    st.markdown('<div class="terminal-card">', unsafe_allow_html=True)
    components.html("""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
          {
          "symbols": [ ["FX_IDC:XAUUSD|12M"] ],
          "chartOnly": false, "width": "100%", "height": "400", "locale": "cs", "colorTheme": "dark",
          "gridLineColor": "rgba(42, 46, 57, 0)", "fontColor": "#787b86", "isTransparent": true,
          "showFloatingTooltip": true, "showVolume": false,
          "lineColor": "#2ecc71", "topColor": "rgba(46, 204, 113, 0.15)", "bottomColor": "rgba(46, 204, 113, 0)"
        }
          </script>
        </div>
    """, height=410)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. KARTA SE SENTIMENTEM
    st.markdown("""
    <div class="terminal-card">
        <div style="color: #666; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; margin-bottom: 10px; text-align: center;">Intelligence Analysis</div>
        <div class="sentiment-title">BULLISH SENTIMENT</div>
        <p style="color: #bbb; font-size: 16px; line-height: 1.6; text-align: center; margin-bottom: 20px;">
            Zlato testuje denní rezistenci. Fundamentální data naznačují oslabování dolaru (DXY). 
            Sledujte možnost bullish breakoutu nad aktuální hladinu.
        </p>
        <div style="border-top: 1px solid #222; padding-top: 15px; color: #444; font-size: 10px; text-align: center;">
            SYSTEM STATUS: ONLINE | SOURCE: AI ENGINE v1.7
        </div>
    </div>
    """, unsafe_allow_html=True)
