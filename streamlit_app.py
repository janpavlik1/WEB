import streamlit as st
import streamlit.components.v1 as components
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

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

    /* 3. BRANDING */
    .logo-container {{ text-align: center; margin-top: 10px; margin-bottom: 20px; }}
    .logo-text {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 60px; letter-spacing: -3px; color: white; line-height: 1.1; }}
    .logo-sub {{ color: #777; font-size: 11px; letter-spacing: 4px; margin-top: 6px; text-transform: uppercase; font-weight: 600; }}
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


# --- 3. REÁLNÝ ENGINE PRO ANALÝZU SENTIMENTU XAUUSD ---
@st.cache_data(ttl=300)
def fetch_live_gold_sentiment():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    # 1. Získání reálných tržních dat (Zlato a Dolarový index)
    gold_price, gold_pct, dxy_pct = 0.0, 0.0, 0.0
    try:
        url_gold = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d&range=5d"
        res_g = requests.get(url_gold, headers=headers, timeout=5).json()
        meta_g = res_g['chart']['result'][0]['meta']
        gold_price = round(meta_g.get('regularMarketPrice', 0.0), 2)
        prev_close_g = meta_g.get('chartPreviousClose', gold_price)
        gold_pct = round(((gold_price - prev_close_g) / prev_close_g) * 100, 2) if prev_close_g else 0.0

        url_dxy = "https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB?interval=1d&range=5d"
        res_d = requests.get(url_dxy, headers=headers, timeout=5).json()
        meta_d = res_d['chart']['result'][0]['meta']
        dxy_price = meta_d.get('regularMarketPrice', 0.0)
        prev_close_d = meta_d.get('chartPreviousClose', dxy_price)
        dxy_pct = round(((dxy_price - prev_close_d) / prev_close_d) * 100, 2) if prev_close_d else 0.0
    except Exception:
        pass

    # 2. Získání nejnovějšího zprávového titulku (Google News RSS pro zlato)
    news_title = "Sledování klíčových hladin podpory a odporu na trhu se zlatem."
    news_source = "GLOBAL MARKET FEED"
    try:
        feed_url = "https://news.google.com/rss/search?q=gold+price+XAUUSD&hl=en-US&gl=US&ceid=US:en"
        feed_res = requests.get(feed_url, headers=headers, timeout=5)
        root = ET.fromstring(feed_res.content)
        item = root.find(".//item")
        if item is not None:
            raw_title = item.find("title").text
            if " - " in raw_title:
                parts = raw_title.rsplit(" - ", 1)
                news_title = parts[0]
                news_source = parts[1]
            else:
                news_title = raw_title
    except Exception:
        pass

    # 3. Vyhodnocení sentimentu na základě reálných tržních sil
    score = gold_pct - (dxy_pct * 1.5)
    
    if score >= 0.2:
        sentiment_label = "BULLISH SENTIMENT"
        sentiment_color = "#2ecc71"
        action_note = f"Zlato posiluje ({'+' if gold_pct > 0 else ''}{gold_pct} %) a tlak na USD ({'+' if dxy_pct > 0 else ''}{dxy_pct} %) otevírá prostor pro nákupní momentum."
    elif score <= -0.2:
        sentiment_label = "BEARISH SENTIMENT"
        sentiment_color = "#e74c3c"
        action_note = f"Rostoucí výnosy a silnější dolar ({'+' if dxy_pct > 0 else ''}{dxy_pct} %) vytvářejí prodejní tlak na zlato ({'+' if gold_pct > 0 else ''}{gold_pct} %)."
    else:
        sentiment_label = "NEUTRAL SENTIMENT"
        sentiment_color = "#f39c12"
        action_note = f"Trh konsoliduje kolem klíčových úrovní. Pohyb zlata: {'+' if gold_pct > 0 else ''}{gold_pct} %, DXY: {'+' if dxy_pct > 0 else ''}{dxy_pct} %."

    return {
        "label": sentiment_label,
        "color": sentiment_color,
        "price": gold_price,
        "gold_pct": gold_pct,
        "dxy_pct": dxy_pct,
        "note": action_note,
        "news_title": news_title,
        "news_source": news_source,
        "time": datetime.now().strftime("%H:%M:%S")
    }


# --- 4. LOGIN LOGIKA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    for _ in range(4): 
        st.write("\n")
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div>
            <div class="logo-sub">TERMINAL v 1</div>
        </div>
    """, unsafe_allow_html=True)
    
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

# --- 5. VNITŘEK TERMINÁLU ---
st.markdown("""
    <div class="logo-container">
        <div class="logo-text" style="font-size:45px;"><span class="j-green">J</span>T | CAPITAL</div>
        <div class="logo-sub">TERMINAL v 1</div>
    </div>
""", unsafe_allow_html=True)

# Načtení živých tržních dat
data = fetch_live_gold_sentiment()

col_l, col_c, col_r = st.columns([0.1, 0.8, 0.1])

with col_c:
    # 1. KARTA S GRAFEM (Jediný čistý zaoblený rámeček)
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
                }
                * {
                    box-sizing: border-box;
                }

                .terminal-card {
                    background-color: rgba(10, 10, 10, 0.6) !important;
                    backdrop-filter: blur(12px) !important;
                    -webkit-backdrop-filter: blur(12px) !important;
                    padding: 20px 25px;
                    border-radius: 15px !important;
                    border: 1px solid rgba(255, 255, 255, 0.08) !important;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
                    width: 100%;
                    overflow: hidden !important;
                }

                .tradingview-widget-container,
                .tradingview-widget-container > div,
                .tradingview-widget-container iframe {
                    background: transparent !important;
                    border: none !important;
                    box-shadow: none !important;
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
    """, height=395)

    # 2. KARTA SE ŽIVÝM SENTIMENTEM A AKTUÁLNÍMI DATY
    st.markdown(f"""
    <div class="terminal-card">
        <div style="color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; margin-bottom: 8px;">
            AI Real-Time Market Analysis &bull; Live Feed ({data['time']})
        </div>
        <div style="color: {data['color']}; font-weight: 900; font-size: 28px; letter-spacing: 2px;">
            {data['label']}
        </div>
        <p style="color: #ddd; margin-top: 12px; font-size: 15px; line-height: 1.6;">
            {data['note']}
        </p>
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 10px 14px; margin-top: 15px; text-align: left;">
            <div style="color: #888; font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 4px;">Top Market Headline:</div>
            <div style="color: #eee; font-size: 13px; font-weight: 500;">"{data['news_title']}"</div>
        </div>
        <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 18px; padding-top: 10px; color: #666; font-size: 10px; letter-spacing: 1px;">
            SOURCE: {data['news_source'].upper()} &bull; DXY INDEX ({'+' if data['dxy_pct'] > 0 else ''}{data['dxy_pct']}%) &bull; XAU SPOT ({data['price']} USD)
        </div>
    </div>
    """, unsafe_allow_html=True)
