import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TOTÁLNÍ STYLING ---
BG_IMAGE = "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=2070"

st.markdown(f"""
    <style>
    /* 1. GLOBÁLNÍ RESET */
    * {{
        outline: none !important;
        box-shadow: none !important;
        -webkit-tap-highlight-color: transparent !important;
    }}

    /* Pozadí a ztmavení */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: url("{BG_IMAGE}") no-repeat center center fixed !important;
        background-size: cover !important;
    }}
    [data-testid="stAppViewContainer"]::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.85); z-index: -1;
    }}

    /* Odstranění výchozích ploch Streamlitu a iframe artefaktů */
    [data-testid="stMainBlockContainer"], [data-testid="stVerticalBlock"], 
    [data-testid="stVerticalBlockBorderWrapper"], .stApp,
    iframe, [data-testid="stCustomComponentV1"], [data-testid="stIFrame"] {{
        background-color: transparent !important;
        border: none !important;
    }}
    
    /* 2. PŘIHLAŠOVACÍ POLE - VÝCHOZÍ ŠEDÝ RÁMEČEK */
    [data-testid="stTextInput"] > div,
    [data-testid="stTextInput"] > div > div,
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="input"] > div {{
        border: 1px solid #333 !important;
        background-color: rgba(10, 10, 10, 0.75) !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        outline: none !important;
        transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
    }}

    /* ZELENÉ ROZSVÍCENÍ PŘI NAJETÍ KURZOREM NEBO AKTIVACI POLE */
    [data-testid="stTextInput"] > div:hover,
    [data-testid="stTextInput"] > div > div:hover,
    div[data-baseweb="input"]:hover,
    div[data-baseweb="base-input"]:hover,
    [data-testid="stTextInput"] > div:focus-within,
    [data-testid="stTextInput"] > div > div:focus-within,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="base-input"]:focus-within {{
        border: 1.5px solid #2ecc71 !important;
        box-shadow: 0 0 12px rgba(46, 204, 113, 0.4) !important;
        outline: none !important;
    }}
    
    input, input:invalid, input:required, input:focus {{
        text-align: center !important;
        color: white !important;
        font-size: 16px !important;
        height: 52px !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        -webkit-appearance: none !important;
    }}

    /* 3. BRANDING (Menší mezery) */
    .logo-container {{ text-align: center; margin-top: 10px; margin-bottom: 20px; }}
    .logo-text {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 60px; letter-spacing: -3px; color: white; line-height: 1.1; }}
    .j-green {{ color: #2ecc71 !important; }}

    /* 4. TLAČÍTKO */
    div.stButton > button {{
        background-color: #2ecc71 !important;
        color: white !important;
        border: none !important;
        height: 52px !important;
        width: 100% !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.2s ease-in-out;
        margin-top: 5px;
    }}
    div.stButton > button:hover {{
        box-shadow: 0 0 15px rgba(46, 204, 113, 0.6) !important;
    }}

    /* 5. PRŮHLEDNÉ KARTY */
    .terminal-card {{
        background-color: rgba(10, 10, 10, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }}

    footer, header, #MainMenu, [data-testid="stSidebar"], [data-testid="InputInstructions"] {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN LOGIKA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    for _ in range(4): 
        st.write("\n")
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div><div style="color:#666; font-size:11px; letter-spacing:4px; margin-top:5px;">TERMINAL 1</div></div>', unsafe_allow_html=True)
    
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
st.markdown('<div class="logo-container"><div class="logo-text" style="font-size:45px;"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([0.1, 0.8, 0.1])

with col_c:
    # 1. KARTA S GRAFEM (1:1 stylovaná stejně jako spodní sentiment karta)
    components.html("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                html, body {
                    margin: 0;
                    padding: 0;
                    background: transparent !important;
                    overflow: hidden;
                    font-family: sans-serif;
                }
                * {
                    box-sizing: border-box;
                }

                /* Identický styl jako .terminal-card */
                .terminal-card {
                    background-color: rgba(10, 10, 10, 0.6) !important;
                    backdrop-filter: blur(12px) !important;
                    -webkit-backdrop-filter: blur(12px) !important;
                    padding: 25px 30px;
                    border-radius: 15px;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
                    width: calc(100% - 10px);
                    margin: 5px auto;
                    overflow: hidden;
                    transform: translateZ(0);
                }

                /* Zaoblení samotného TradingView grafu uvnitř karty */
                .tradingview-widget-container,
                .tradingview-widget-container > div,
                .tradingview-widget-container iframe {
                    border-radius: 10px !important;
                    overflow: hidden !important;
                    transform: translateZ(0) !important;
                }
            </style>
        </head>
        <body>
            <div class="terminal-card">
                <div class="tradingview-widget-container">
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
                  {
                    "symbols": [ ["FX_IDC:XAUUSD|12M"] ],
                    "chartOnly": false, 
                    "width": "100%", 
                    "height": "350", 
                    "locale": "cs", 
                    "colorTheme": "dark",
                    "gridLineColor": "rgba(42, 46, 57, 0)", 
                    "fontColor": "#787b86", 
                    "isTransparent": true,
                    "showFloatingTooltip": true, 
                    "showVolume": false,
                    "lineColor": "#2ecc71", 
                    "topColor": "rgba(46, 204, 113, 0.15)", 
                    "bottomColor": "rgba(46, 204, 113, 0)"
                  }
                  </script>
                </div>
            </div>
        </body>
        </html>
    """, height=425)

    # 2. KARTA SE SENTIMENTEM
    st.markdown("""
    <div class="terminal-card">
        <div style="color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; margin-bottom: 10px;">AI Analysis System</div>
        <div style="color: #2ecc71; font-weight: 900; font-size: 28px; letter-spacing: 2px;">BULLISH SENTIMENT</div>
        <p style="color: #bbb; margin-top: 15px; font-size: 16px; line-height: 1.6;">
            Zlato testuje denní rezistenci. Fundamentální data naznačují oslabování dolaru (DXY). 
            Sledujte možnost bullish breakoutu nad aktuální hladinu.
        </p>
        <div style="border-top: 1px solid rgba(255, 255, 255, 0.1); margin-top: 20px; padding-top: 10px; color: #666; font-size: 10px;">
            SOURCE: REAL-TIME REUTERS FEED | AI ENGINE v1.8
        </div>
    </div>
    """, unsafe_allow_html=True)
