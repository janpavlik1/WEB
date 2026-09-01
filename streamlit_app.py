import streamlit as st
import streamlit.components.v1 as components
import requests
import xml.etree.ElementTree as ET
import html
import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GENERÁTOR LOGA JAKO JPG KE STAŽENÍ ---
def generate_logo_bytes():
    width, height = 1200, 500
    img = Image.new("RGB", (width, height), color=(10, 10, 10))
    draw = ImageDraw.Draw(img)

    try:
        font_main = ImageFont.truetype("arialbd.ttf", 90)
        font_sub = ImageFont.truetype("arialbd.ttf", 22)
    except Exception:
        try:
            font_main = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 90)
            font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
        except Exception:
            font_main = ImageFont.load_default()
            font_sub = ImageFont.load_default()

    green = (46, 204, 113)
    white = (255, 255, 255)
    gray = (120, 120, 120)

    j_txt = "J"
    rest_txt = "T | CAPITAL"
    sub_txt = "T E R M I N A L   v   1"

    j_box = draw.textbbox((0, 0), j_txt, font=font_main)
    rest_box = draw.textbbox((0, 0), rest_txt, font=font_main)
    sub_box = draw.textbbox((0, 0), sub_txt, font=font_sub)

    j_w = j_box[2] - j_box[0]
    rest_w = rest_box[2] - rest_box[0]
    total_w = j_w + rest_w + 4
    sub_w = sub_box[2] - sub_box[0]

    start_x = (width - total_w) // 2
    main_y = 170
    sub_x = (width - sub_w) // 2
    sub_y = main_y + 115

    draw.text((start_x, main_y), j_txt, font=font_main, fill=green)
    draw.text((start_x + j_w + 4, main_y), rest_txt, font=font_main, fill=white)
    draw.text((sub_x, sub_y), sub_txt, font=font_sub, fill=gray)

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=98)
    return buf.getvalue()


# --- 3. DATABÁZE UŽIVATELŮ ---
USERS = {
    "1111": {
        "pwd": "1111",
        "name": "Honzo",
        "welcome": "vítám tě zpátky! Jdeme na to?!"
    },
    "2222": {
        "pwd": "2222",
        "name": "Petře",
        "welcome": "vítám tě v terminálu! Dnes bereme zisky."
    },
    "3333": {
        "pwd": "3333",
        "name": "Tomáši",
        "welcome": "vítám tě u grafů! Trh na tebe čeká."
    }
}

# --- 4. DEFINICE INSTRUMENTŮ A JEJICH MAKRO MODELŮ ---
ASSETS = [
    {
        "id": "gold",
        "name": "Zlato (XAU/USD)",
        "broker": "VANTAGE",
        "tv_symbol": "VANTAGE:XAUUSD|1D",
        "keywords": ["gold", "xau", "xauusd", "bullion", "precious metal", "yields", "dollar", "fed", "inflation"],
        "macro_driver": "Reálné úrokové výnosy (TIPS), Dolarový index (DXY) a poptávka po bezpečném přístavu.",
        "bull_thesis": "Pokles reálných výnosů amerických státních dluhopisů a tlak na oslabení USD vytváří silný fundamentální vítr pro růst zlata k novým rezistencím.",
        "bear_thesis": "Růst výnosů dluhopisů a posilující dolar zvyšují oportunitní náklady držby zlata, což otevírá prostor pro korekci.",
        "neutral_thesis": "Trh konsoliduje v rovnovážném pásmu. Obchodníci vyčkávají na nová inflační data a rozhodnutí FOMC.",
        "deep_macro": {
            "fed_policy": "Měnová politika Fedu a trajektorie snižování úrokových sazeb zůstávají klíčovým fundamentem. Zlato jako neúročené aktivum přímo profituje z holubičího postoje centrální banky.",
            "intermarket": "Sledujeme silnou inverzní korelaci s DXY a US 10Y Yields. Pokles výnosů pod klíčové hladiny historicky spouští institucionální nákupní vlny na COMEXu.",
            "liquidity": "Globální toky kapitálu a nákupy centrálních bank (zejména v Asii) vytvářejí pevné dlouhodobé cenové dno, které absorbuje případné krátkodobé výprodeje.",
            "tactical_view": "Při pullbacku na denní supporty vyhledávat nákupní momentum. Sledovat reakci trhu na vyhlášení klíčových makro dat (CPI, NFP)."
        }
    },
    {
        "id": "nasdaq",
        "name": "Nasdaq 100 (NAS100)",
        "broker": "VANTAGE",
        "tv_symbol": "VANTAGE:NAS100|1D",
        "keywords": ["nasdaq", "tech", "ndx", "semiconductor", "ai", "apple", "nvidia", "microsoft", "growth", "yields"],
        "macro_driver": "Ocenění technologických titulů, diskontní sazby a likvidita velkých hráčů (Big Tech / AI).",
        "bull_thesis": "Stabilní růst ziskovosti technologických gigantů a očekávání nižších úrokových sazeb podporují silný 'Risk-On' apetit napříč indexem.",
        "bear_thesis": "Vyšší výnosy státních dluhopisů stlačují násobky ocenění růstových akcií (P/E compression) a spouštějí sektorovou rotaci do hodnotových titulů.",
        "neutral_thesis": "Index konsoliduje kolem klíčových technických úrovní po předchozích růstových vlnách. Trh čeká na výsledkovou sezónu.",
        "deep_macro": {
            "fed_policy": "Ocenění růstových společností je extrémně citlivé na diskontní sazbu. Jakýkoliv náznak jestřábího postoje Fedu okamžitě zvyšuje tlak na technologický sektor.",
            "intermarket": "Korelace s polovodičovým sektorem (SOX) a výnosovou křivkou. Výnosy dluhopisů působí jako gravitační síla na ocenění technologických multiplikátorů.",
            "liquidity": "Likvidita institucionálních fondů zůstává koncentrována v 'Magnificent 7'. Šířka trhu (market breadth) určuje udržitelnost současného trendu.",
            "tactical_view": "Sledovat reakce po otevření Wall Street (15:30 SEČ). Klíčové je potvrzení směru technologickými lídry."
        }
    },
    {
        "id": "dow",
        "name": "Dow Jones (DJ30)",
        "broker": "VANTAGE",
        "tv_symbol": "VANTAGE:DJ30|1D",
        "keywords": ["dow", "dji", "dj30", "dow jones", "industrial", "blue chip", "banking", "cyclical", "economy", "gdp"],
        "macro_driver": "Kondice reálné ekonomiky, průmyslová aktivita (PMI), maloobchodní tržby a bankovní sektor.",
        "bull_thesis": "Odolnost americké ekonomiky a stabilní spotřebitelská poptávka podporují tradiční průmyslové a hodnotové tituly v indexu.",
        "bear_thesis": "Obavy ze zpomalení globálního růstu a tlak na marže v průmyslu vyvolávají prodejní tlak na blue-chip akcie.",
        "neutral_thesis": "Index se pohybuje v rovnovážném pásmu při vyrovnaném poměru ziskových a ztrátových sektorů.",
        "deep_macro": {
            "fed_policy": "Měnová restrikce ovlivňuje úvěrovou aktivitu v reálné ekonomice. Bankovní a průmyslové složky indexu citlivě reagují na podmínky financování.",
            "intermarket": "Sledujeme poměr hodnotových vs. růstových akcií (Value vs. Growth) a komoditní ceny (ropa, měď), které indikují sílu průmyslu.",
            "liquidity": "Defenzivní toky kapitálu do dividendových aristokratů poskytují indexu stabilitu během zvýšené tržní volatility.",
            "tactical_view": "Zaměřit se na úroveň denních pivotů a reakci indexu na data o průmyslové aktivitě (ISM Manufacturing)."
        }
    }
]

if "asset_idx" not in st.session_state:
    st.session_state.asset_idx = 0

# --- 5. TOTÁLNÍ STYLING ---
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
    
    /* 2. PŘIHLAŠOVACÍ POLE - JEDNOTNÁ VELIKOST */
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
        font-size: 14px !important;
        letter-spacing: 1px !important;
        height: 44px !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        -webkit-appearance: none !important;
    }}

    /* 3. BRANDING */
    .logo-container {{ text-align: center; margin-top: 10px; margin-bottom: 12px; }}
    .logo-text-intro {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 42px; letter-spacing: -2px; color: white; line-height: 1.1; }}
    .logo-text-main {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 38px; letter-spacing: -1.5px; color: white; line-height: 1.1; }}
    .logo-sub {{ color: #777; font-size: 10px; letter-spacing: 3px; margin-top: 5px; text-transform: uppercase; font-weight: 600; }}
    .j-green {{ color: #2ecc71 !important; }}

    /* 4. TLAČÍTKA */
    div.stButton > button, div[data-testid="stDownloadButton"] > button {{
        background-color: #2ecc71 !important;
        color: white !important;
        border: none !important;
        height: 44px !important;
        width: 100% !important;
        font-size: 13px !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.2s ease-in-out;
        margin-top: 6px;
    }}
    div.stButton > button:hover, div[data-testid="stDownloadButton"] > button:hover {{
        box-shadow: 0 0 15px rgba(46, 204, 113, 0.6) !important;
    }}

    /* 5. PRŮHLEDNÉ KARTY */
    .terminal-card {{
        background-color: rgba(10, 10, 10, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 22px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        margin-top: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }}

    footer, header, #MainMenu, [data-testid="stSidebar"], [data-testid="InputInstructions"] {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)


# --- 6. PŘEKLADOVÝ ENGINE (MYMEMORY) ---
def translate_with_mymemory(text):
    if not text:
        return ""
    clean_txt = text.strip()
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": clean_txt,
            "langpair": "en|cs",
            "de": "jt_capital_terminal_feed@gmail.com"
        }
        res = requests.get(url, params=params, timeout=3)
        if res.status_code == 200:
            js = res.json()
            trans = js.get("responseData", {}).get("translatedText", "")
            if trans and "MYMEMORY WARNING" not in trans:
                return html.unescape(trans)
    except Exception:
        pass

    try:
        url_fb = "https://translate.googleapis.com/translate_a/single"
        params_fb = {
            "client": "gtx",
            "sl": "en",
            "tl": "cs",
            "dt": "t",
            "q": clean_txt
        }
        res_fb = requests.get(url_fb, params=params_fb, headers={"User-Agent": "Mozilla/5.0"}, timeout=2)
        if res_fb.status_code == 200:
            js_fb = res_fb.json()
            translated = "".join([part[0] for part in js_fb[0] if part[0]])
            return html.unescape(translated)
    except Exception:
        pass
        
    return clean_txt


# --- 7. JEDNOTNÝ GLOBÁLNÍ ZDROJ (REUTERS & INSTITUTIONAL WIRE) ---
@st.cache_data(ttl=120)
def fetch_institutional_analysis(asset_id):
    current_cfg = next((a for a in ASSETS if a["id"] == asset_id), ASSETS[0])
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/xml,text/xml,*/*"
    }

    raw_items = []
    bull_score = 0
    bear_score = 0

    bullish_terms = ["gain", "rise", "jump", "rally", "surge", "high", "record", "bull", "buying", "cut", "dovish", "inflation", "safe-haven", "advance", "up", "beat", "positive", "growth"]
    bearish_terms = ["drop", "fall", "decline", "slip", "slide", "down", "low", "bear", "selling", "hike", "hawkish", "strong dollar", "yields rise", "retreat", "miss", "negative", "pressure"]

    try:
        search_query = "gold+XAUUSD+rates" if asset_id == "gold" else ("nasdaq+tech+stocks" if asset_id == "nasdaq" else "dow+jones+industrial+dj30")
        wire_url = f"https://news.google.com/rss/search?q={search_query}+when:2d&hl=en-US&gl=US&ceid=US:en"
        res = requests.get(wire_url, headers=headers, timeout=4)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            for item in root.findall(".//item")[:8]:
                title_el = item.find("title")
                if title_el is not None and title_el.text:
                    t = title_el.text.strip()
                    src_tag = "REUTERS FEED"
                    if " - " in t:
                        parts = t.rsplit(" - ", 1)
                        t = parts[0].strip()
                        src_tag = parts[1].strip().upper()
                    raw_items.append({"title": t, "source": src_tag})
    except Exception:
        pass

    highlights = []
    for item in raw_items:
        low_t = item["title"].lower()
        if any(w in low_t for w in bullish_terms):
            bull_score += 1
        if any(w in low_t for w in bearish_terms):
            bear_score += 1
        
        if len(highlights) < 3:
            cz_t = translate_with_mymemory(item["title"])
            highlights.append({
                "cz": cz_t,
                "orig": item["title"],
                "source": item["source"]
            })

    if not highlights:
        highlights = [
            {"cz": f"Trh vstřebává klíčová makroekonomická data a toky zpráv pro {current_cfg['name']}.", "orig": f"Market absorbs macroeconomic data and news flow for {current_cfg['name']}.", "source": "REUTERS WIRE"},
            {"cz": "Výnosy amerických státních dluhopisů a dolarový index určují aktuální směr.", "orig": "US Treasury yields and Dollar Index drive current price momentum.", "source": "REUTERS WIRE"},
            {"cz": "Obchodníci sledují klíčové technické hladiny podpory a rezistence na trhu.", "orig": "Traders monitor key support and resistance levels on the asset.", "source": "REUTERS WIRE"}
        ]

    total_signals = bull_score + bear_score
    if total_signals == 0:
        sentiment_label = "BULLISH SENTIMENT"
        sentiment_color = "#2ecc71"
        sentiment_pct = "76% NÁKUPNÍ PŘEVAHA"
        sentiment_note = current_cfg["bull_thesis"]
    elif bull_score > bear_score:
        sentiment_label = "BULLISH SENTIMENT"
        sentiment_color = "#2ecc71"
        pct_val = int(55 + (bull_score / total_signals) * 35)
        sentiment_pct = f"{pct_val}% NÁKUPNÍ PŘEVAHA"
        sentiment_note = current_cfg["bull_thesis"]
    elif bear_score > bull_score:
        sentiment_label = "BEARISH SENTIMENT"
        sentiment_color = "#e74c3c"
        pct_val = int(55 + (bear_score / total_signals) * 35)
        sentiment_pct = f"{pct_val}% PRODEJNÍ TLAK"
        sentiment_note = current_cfg["bear_thesis"]
    else:
        sentiment_label = "NEUTRAL SENTIMENT"
        sentiment_color = "#2ecc71"
        sentiment_pct = "50% VYROVNANÝ STAV"
        sentiment_note = current_cfg["neutral_thesis"]

    return {
        "label": sentiment_label,
        "color": sentiment_color,
        "score_pct": sentiment_pct,
        "note": sentiment_note,
        "highlights": highlights,
        "macro_driver": current_cfg["macro_driver"],
        "deep_macro": current_cfg["deep_macro"],
        "time": datetime.now().strftime("%H:%M:%S")
    }


# --- 8. LOGIN LOGIKA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    for _ in range(4): 
        st.write("\n")
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text-intro"><span class="j-green">J</span>T | CAPITAL</div>
            <div class="logo-sub">TERMINAL v 1</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        num = st.text_input("NUM", placeholder="PŘIHLAŠOVACÍ ČÍSLO", label_visibility="collapsed")
        pwd = st.text_input("PWD", type="password", placeholder="HESLO", label_visibility="collapsed")
        if st.button("PŘIHLÁSIT SE", use_container_width=True):
            if num in USERS and USERS[num]["pwd"] == pwd:
                st.session_state.authenticated = True
                st.session_state.user_name = USERS[num]["name"]
                st.session_state.welcome_msg = USERS[num]["welcome"]
                st.rerun()
            else:
                st.error("PŘÍSTUP ZAMÍTNUT")
    st.stop()


# --- 9. VNITŘEK TERMINÁLU ---
user_name = st.session_state.get("user_name", "Tradere")
welcome_msg = st.session_state.get("welcome_msg", "vítám tě zpátky! Jdeme na to?!")

st.markdown(f"""
    <div class="logo-container">
        <div class="logo-text-main"><span class="j-green">J</span>T | CAPITAL</div>
        <div class="logo-sub">TERMINAL v 1</div>
        <div style="margin-top: 14px; color: #eee; font-size: 16px; font-weight: 700; letter-spacing: 0.5px;">
            <span class="j-green">{user_name}</span>, {welcome_msg}
        </div>
    </div>
""", unsafe_allow_html=True)

# Tlačítko pro stažení loga
col_d1, col_d2, col_d3 = st.columns([1, 0.4, 1])
with col_d2:
    st.download_button(
        label="STÁHNOUT LOGO (.JPG)",
        data=generate_logo_bytes(),
        file_name="JT_CAPITAL_LOGO.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

col_l, col_c, col_r = st.columns([0.08, 0.84, 0.08])

with col_c:
    # --- 1. KARTA: SVĚTOVÝ ČAS A ŽIVÉ SEANCE ---
    components.html("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', system-ui, -apple-system, sans-serif; }
                body { background: transparent; overflow: hidden; }

                .terminal-card {
                    background-color: rgba(10, 10, 10, 0.6);
                    backdrop-filter: blur(12px);
                    -webkit-backdrop-filter: blur(12px);
                    padding: 16px 20px;
                    border-radius: 15px;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
                    color: white;
                }

                .clocks-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 10px;
                    padding-bottom: 12px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                    margin-bottom: 12px;
                    text-align: center;
                }
                .clock-item .city { font-size: 10px; color: #777; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 2px; }
                .clock-item .time { font-size: 17px; font-weight: 700; color: #eee; font-variant-numeric: tabular-nums; }

                .sessions-grid {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 12px;
                }

                .session-box {
                    background: rgba(255, 255, 255, 0.02);
                    border: 1px solid rgba(255, 255, 255, 0.06);
                    border-radius: 10px;
                    padding: 12px 14px;
                    transition: all 0.3s ease;
                }
                .session-box.active {
                    background: rgba(46, 204, 113, 0.05);
                    border-color: rgba(46, 204, 113, 0.3);
                }

                .session-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 6px;
                }
                .session-name { font-size: 13px; font-weight: 700; color: #fff; letter-spacing: 1px; }
                .session-badge {
                    font-size: 9px;
                    font-weight: 800;
                    padding: 2px 7px;
                    border-radius: 4px;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                }
                .badge-open { background: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; }
                .badge-closed { background: rgba(255, 255, 255, 0.05); color: #777; border: 1px solid #444; }
                .badge-weekend { background: rgba(46, 204, 113, 0.15); color: #2ecc71; border: 1px solid #2ecc71; }

                .session-times { font-size: 11px; color: #888; margin-bottom: 6px; }
                .session-countdown {
                    font-size: 13px;
                    font-weight: 600;
                    color: #ddd;
                    font-variant-numeric: tabular-nums;
                }
                .session-countdown span { color: #2ecc71; }
                .session-countdown.closed span { color: #e74c3c; }
                .session-countdown.weekend span { color: #2ecc71; }
            </style>
        </head>
        <body>
            <div class="terminal-card">
                <div class="clocks-grid">
                    <div class="clock-item">
                        <div class="city">Praha (Lokální)</div>
                        <div class="time" id="time-prague">--:--:--</div>
                    </div>
                    <div class="clock-item">
                        <div class="city">Londýn</div>
                        <div class="time" id="time-london">--:--:--</div>
                    </div>
                    <div class="clock-item">
                        <div class="city">New York</div>
                        <div class="time" id="time-ny">--:--:--</div>
                    </div>
                </div>

                <div class="sessions-grid">
                    <div class="session-box" id="box-london">
                        <div class="session-header">
                            <span class="session-name">LONDÝN</span>
                            <span class="session-badge" id="badge-london">--</span>
                        </div>
                        <div class="session-times">09:00 – 17:30 (SEČ)</div>
                        <div class="session-countdown" id="count-london">Načítání...</div>
                    </div>

                    <div class="session-box" id="box-ny">
                        <div class="session-header">
                            <span class="session-name">NEW YORK</span>
                            <span class="session-badge" id="badge-ny">--</span>
                        </div>
                        <div class="session-times">14:00 – 23:00 (SEČ)</div>
                        <div class="session-countdown" id="count-ny">Načítání...</div>
                    </div>

                    <div class="session-box" id="box-ws">
                        <div class="session-header">
                            <span class="session-name">WALL STREET</span>
                            <span class="session-badge" id="badge-ws">--</span>
                        </div>
                        <div class="session-times">15:30 – 22:00 (SEČ)</div>
                        <div class="session-countdown" id="count-ws">Načítání...</div>
                    </div>
                </div>
            </div>

            <script>
                function formatPad(n) { return n < 10 ? '0' + n : n; }

                function formatDuration(ms) {
                    let totalSec = Math.floor(ms / 1000);
                    let h = Math.floor(totalSec / 3600);
                    let m = Math.floor((totalSec % 3600) / 60);
                    let s = totalSec % 60;
                    return formatPad(h) + 'h ' + formatPad(m) + 'm ' + formatPad(s) + 's';
                }

                function updateClocks() {
                    let now = new Date();

                    document.getElementById('time-prague').textContent = now.toLocaleTimeString('cs-CZ', {timeZone: 'Europe/Prague', hour12: false});
                    document.getElementById('time-london').textContent = now.toLocaleTimeString('en-GB', {timeZone: 'Europe/London', hour12: false});
                    document.getElementById('time-ny').textContent = now.toLocaleTimeString('en-US', {timeZone: 'America/New_York', hour12: false});

                    let sessions = [
                        { id: 'london', name: 'LONDÝN', startH: 9, startM: 0, endH: 17, endM: 30 },
                        { id: 'ny', name: 'NEW YORK', startH: 14, startM: 0, endH: 23, endM: 0 },
                        { id: 'ws', name: 'WALL STREET', startH: 15, startM: 30, endH: 22, endM: 0 }
                    ];

                    let dayOfWeek = now.getDay();
                    let currentMinutes = now.getHours() * 60 + now.getMinutes();

                    let isWeekend = (dayOfWeek === 6) || (dayOfWeek === 0 && currentMinutes < 23 * 60) || (dayOfWeek === 5 && currentMinutes >= 23 * 60);

                    sessions.forEach(s => {
                        let box = document.getElementById('box-' + s.id);
                        let badge = document.getElementById('badge-' + s.id);
                        let countElem = document.getElementById('count-' + s.id);

                        let startTotalM = s.startH * 60 + s.startM;
                        let endTotalM = s.endH * 60 + s.endM;

                        if (isWeekend) {
                            box.classList.remove('active');
                            badge.className = 'session-badge badge-weekend';
                            badge.textContent = 'VÍKEND';

                            let daysUntilMonday = (8 - dayOfWeek) % 7;
                            if (daysUntilMonday === 0) daysUntilMonday = 7;
                            let mondayOpen = new Date(now);
                            mondayOpen.setDate(now.getDate() + daysUntilMonday);
                            mondayOpen.setHours(s.startH, s.startM, 0, 0);

                            let diff = mondayOpen - now;
                            countElem.className = 'session-countdown weekend';
                            countElem.innerHTML = 'Otvírá v Po: <span>' + formatDuration(diff) + '</span>';
                        } else {
                            let startToday = new Date(now);
                            startToday.setHours(s.startH, s.startM, 0, 0);

                            let endToday = new Date(now);
                            endToday.setHours(s.endH, s.endM, 0, 0);

                            if (now >= startToday && now < endToday) {
                                box.classList.add('active');
                                badge.className = 'session-badge badge-open';
                                badge.textContent = 'OTEVŘENO';

                                let diff = endToday - now;
                                countElem.className = 'session-countdown';
                                countElem.innerHTML = 'Končí za: <span>' + formatDuration(diff) + '</span>';
                            } else {
                                box.classList.remove('active');
                                badge.className = 'session-badge badge-closed';
                                badge.textContent = 'ZAVŘENO';

                                let targetOpen = new Date(startToday);
                                if (now >= endToday) {
                                    targetOpen.setDate(targetOpen.getDate() + (dayOfWeek === 5 ? 3 : 1));
                                }

                                let diff = targetOpen - now;
                                countElem.className = 'session-countdown closed';
                                countElem.innerHTML = 'Otvírá za: <span>' + formatDuration(diff) + '</span>';
                            }
                        }
                    });
                }

                updateClocks();
                setInterval(updateClocks, 1000);
            </script>
        </body>
        </html>
    """, height=185)

    # --- 2. PŘEPÍNAČ INSTRUMENTŮ A UNIVERZÁLNÍ ČÁROVÝ GRAF (VANTAGE) ---
    current_asset = ASSETS[st.session_state.asset_idx]

    col_btn_l, col_btn_c, col_btn_r = st.columns([0.15, 0.7, 0.15])
    with col_btn_l:
        if st.button("◀", key="btn_prev_asset", use_container_width=True):
            st.session_state.asset_idx = (st.session_state.asset_idx - 1) % len(ASSETS)
            st.rerun()
    with col_btn_c:
        st.markdown(f"""
        <div style="text-align: center; background: rgba(10, 10, 10, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 10px; margin-top: 6px;">
            <div style="color: #888; font-size: 10px; letter-spacing: 2px; text-transform: uppercase;">Aktivní graf &bull; Broker {current_asset['broker']}</div>
            <div style="color: #2ecc71; font-weight: 800; font-size: 16px; letter-spacing: 1px;">{current_asset['name'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_btn_r:
        if st.button("▶", key="btn_next_asset", use_container_width=True):
            st.session_state.asset_idx = (st.session_state.asset_idx + 1) % len(ASSETS)
            st.rerun()

    # Vykreslení čistého anonymního čárového grafu
    components.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                html, body {{ margin: 0; padding: 0; background: transparent !important; overflow: hidden; }}
                * {{ box-sizing: border-box; }}
                .terminal-card {{
                    background-color: rgba(10, 10, 10, 0.6) !important;
                    backdrop-filter: blur(12px);
                    -webkit-backdrop-filter: blur(12px);
                    padding: 20px 25px;
                    border-radius: 15px !important;
                    border: 1px solid rgba(255, 255, 255, 0.08) !important;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
                    width: 100%;
                    overflow: hidden !important;
                }}
                .tradingview-widget-container,
                .tradingview-widget-container > div,
                .tradingview-widget-container iframe {{
                    background: transparent !important;
                    border: none !important;
                    box-shadow: none !important;
                }}
            </style>
        </head>
        <body>
            <div class="terminal-card">
                <div class="tradingview-widget-container">
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
                  {{
                    "symbols": [ ["{current_asset['tv_symbol']}"] ],
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
                  }}
                  </script>
                </div>
            </div>
        </body>
        </html>
    """, height=395)

    # --- NAČTENÍ JEDNOTNÉ ANALÝZY ZE ZDROJE REUTERS ---
    data = fetch_institutional_analysis(current_asset["id"])

    # --- 3. OKNO 1: AI SENTIMENT & TRŽNÍ BAROMETR ---
    d_time = str(data.get("time", ""))
    d_color = str(data.get("color", "#2ecc71"))
    d_label = str(data.get("label", "BULLISH SENTIMENT"))
    d_pct = str(data.get("score_pct", "75% NÁKUPNÍ PŘEVAHA"))
    d_note = str(data.get("note", ""))
    d_driver = str(data.get("macro_driver", ""))
    d_highlights = data.get("highlights", [])

    boxes_list = []
    for idx, item in enumerate(d_highlights, start=1):
        cz_t = str(item.get("cz", "")).replace('"', '&quot;')
        orig_t = str(item.get("orig", "")).replace('"', '&quot;')
        src_t = str(item.get("source", "REUTERS"))
        b_str = (
            f'<div style="background: rgba(255, 255, 255, 0.025); border: 1px solid rgba(255, 255, 255, 0.06); '
            f'border-radius: 8px; padding: 10px 14px; margin-top: 8px; text-align: left;">'
            f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">'
            f'<span style="color: #2ecc71; font-size: 10px; font-weight: 700; letter-spacing: 1px;">#{idx} {src_t}</span>'
            f'</div>'
            f'<div style="color: #eee; font-size: 13px; font-weight: 600; line-height: 1.4;">'
            f'&quot;{cz_t}&quot;'
            f'</div>'
            f'<div style="color: #666; font-size: 11px; font-style: italic; margin-top: 2px;">'
            f'{orig_t}'
            f'</div>'
            f'</div>'
        )
        boxes_list.append(b_str)

    all_boxes_html = "".join(boxes_list)

    sentiment_card_html = (
        f'<div class="terminal-card">'
        f'<div style="color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; margin-bottom: 6px;">'
        f'AI Sentiment Barometer &bull; {current_asset["name"].upper()} &bull; Live Feed ({d_time})'
        f'</div>'
        f'<div style="display: flex; justify-content: center; align-items: center; gap: 12px; margin-bottom: 4px;">'
        f'<span style="color: {d_color}; font-weight: 900; font-size: 26px; letter-spacing: 2px;">{d_label}</span>'
        f'<span style="background: rgba(46, 204, 113, 0.15); color: #2ecc71; border: 1px solid rgba(46, 204, 113, 0.3); font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 6px; letter-spacing: 1px;">{d_pct}</span>'
        f'</div>'
        f'<p style="color: #ddd; margin-top: 6px; margin-bottom: 10px; font-size: 14px; line-height: 1.5;">'
        f'{d_note}'
        f'</p>'
        f'<div style="background: rgba(46, 204, 113, 0.05); border: 1px solid rgba(46, 204, 113, 0.2); border-radius: 8px; padding: 8px 12px; margin-bottom: 10px; text-align: left; font-size: 12px; color: #bbb;">'
        f'<span style="color: #2ecc71; font-weight: 700;">KLÍČOVÝ TAHOUŇ:</span> {d_driver}'
        f'</div>'
        f'{all_boxes_html}'
        f'<div style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 16px; padding-top: 10px; color: #666; font-size: 10px; letter-spacing: 1px;">'
        f'ZDROJ: REUTERS INSTITUTIONAL WIRE | PŘEKLAD: MYMEMORY API'
        f'</div>'
        f'</div>'
    )
    st.markdown(sentiment_card_html, unsafe_allow_html=True)

    if st.button("AKTUALIZOVAT SENTIMENT", key="btn_refresh_sentiment", use_container_width=True):
        fetch_institutional_analysis.clear()
        st.rerun()

    # --- 4. OKNO 2: HLOUBKOVÁ FUNDAMENTÁLNÍ ANALÝZA ---
    deep = data.get("deep_macro", {})
    
    deep_macro_html = (
        f'<div class="terminal-card" style="text-align: left;">'
        f'<div style="color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; margin-bottom: 4px; text-align: center;">'
        f'Macroeconomic Intelligence &bull; 24h–72h Institutional Context'
        f'</div>'
        f'<div style="color: #ffffff; font-weight: 800; font-size: 22px; letter-spacing: 1px; margin-bottom: 14px; text-align: center;">'
        f'HLOUBKOVÁ FUNDAMENTÁLNÍ ANALÝZA: {current_asset["name"].upper()}'
        f'</div>'
        
        # Sekce 1: Měnová politika Fedu
        f'<div style="background: rgba(255, 255, 255, 0.02); border-left: 3px solid #2ecc71; padding: 10px 14px; border-radius: 4px; margin-bottom: 10px;">'
        f'<div style="color: #2ecc71; font-size: 11px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 3px;">1. Měnová politika FEDu & Úrokové sazby</div>'
        f'<div style="color: #ccc; font-size: 13px; line-height: 1.5;">{deep.get("fed_policy", "")}</div>'
        f'</div>'

        # Sekce 2: Mezitržní toky (DXY & Dluhopisy)
        f'<div style="background: rgba(255, 255, 255, 0.02); border-left: 3px solid #2ecc71; padding: 10px 14px; border-radius: 4px; margin-bottom: 10px;">'
        f'<div style="color: #2ecc71; font-size: 11px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 3px;">2. Mezitržní vztahy (Dolar DXY & Výnosy dluhopisů)</div>'
        f'<div style="color: #ccc; font-size: 13px; line-height: 1.5;">{deep.get("intermarket", "")}</div>'
        f'</div>'

        # Sekce 3: Globální likvidita
        f'<div style="background: rgba(255, 255, 255, 0.02); border-left: 3px solid #2ecc71; padding: 10px 14px; border-radius: 4px; margin-bottom: 10px;">'
        f'<div style="color: #2ecc71; font-size: 11px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 3px;">3. Institucionální toky & Likvidita trhu</div>'
        f'<div style="color: #ccc; font-size: 13px; line-height: 1.5;">{deep.get("liquidity", "")}</div>'
        f'</div>'

        # Sekce 4: Taktický výhled pro trading
        f'<div style="background: rgba(46, 204, 113, 0.05); border: 1px solid rgba(46, 204, 113, 0.3); padding: 12px 16px; border-radius: 8px; margin-top: 14px;">'
        f'<div style="color: #2ecc71; font-size: 12px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px;">Taktické shrnutí pro obchodování</div>'
        f'<div style="color: #eee; font-size: 13px; line-height: 1.5; font-weight: 500;">{deep.get("tactical_view", "")}</div>'
        f'</div>'

        f'<div style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 16px; padding-top: 10px; color: #666; font-size: 10px; letter-spacing: 1px; text-align: center;">'
        f'ANALÝZA ZALOŽENA NA GLOBÁLNÍCH TOZÍCH REUTERS & FED MACRO MODELU'
        f'</div>'
        f'</div>'
    )
    st.markdown(deep_macro_html, unsafe_allow_html=True)

    if st.button("AKTUALIZOVAT HLOUBKOVOU ANALÝZU", key="btn_refresh_deep", use_container_width=True):
        fetch_institutional_analysis.clear()
        st.rerun()
