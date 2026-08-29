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
        # Data pro zlato (GC=F)
        res_g = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d&range=5d", headers=headers, timeout=5).json()
        meta_g = res_g['chart']['result'][0]['meta']
        gold_price = round(meta_g.get('regularMarketPrice', 0.0), 2)
        prev_close_g = meta_g.get('chartPreviousClose', gold_price)
        gold_pct = round(((gold_price - prev_close_g) / prev_close_g) * 100, 2) if prev_close_g else 0.0

        # Data pro DXY (USD Index)
        res_d = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB?interval=1d&range=5d", headers=headers, timeout=5).json()
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
        feed_url = "https://news.google.com/rss/search?q=gold+price+XAUUSD+when:2d
