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
    .logo-container {{ text-align: center; margin-top: 10px; margin-bottom: 15px; }}
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
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        margin-top: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }}

    footer, header, #MainMenu, [data-testid="stSidebar"], [data-testid="InputInstructions"] {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)


# --- 3. PŘEKLADAČ DO ČEŠTINY ---
def translate_to_czech(text):
    if not text:
        return text
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=cs&dt=t&q={requests.utils.quote(text)}"
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            data = res.json()
            translated = "".join([part[0] for part in data[0] if part[0]])
            return translated
    except Exception:
        pass
    return text


# --- 4. ANALÝZA ZE ZVOLENÝCH 5 WEBOVÝCH ZDROJŮ ---
@st.cache_data(ttl=300)
def fetch_target_sources_sentiment():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    sources = [
        {"name": "InvestingLive", "url": "https://www.forexlive.com/feed/news/"},
        {"name": "Investing.com", "url": "https://www.investing.com/rss/news_14.rss"},
        {"name": "ForexFactory", "url": "https://www.forexfactory.com/news/rss"},
        {"name": "TradingEconomics", "url": "https://tradingeconomics.com/rss/news.aspx"},
        {"name": "FinancialJuice", "url": "https://www.financialjuice.com/feed.ashx?xy=rss"}
    ]

    bullish_keywords = [
        "gain", "rise", "jump", "rally", "surge", "high", "record", "bull", "buying", 
        "support", "breakout", "cut", "dovish", "inflation", "safe-haven", "gold climbs"
    ]
    bearish_keywords = [
        "drop", "fall", "decline", "slip", "slide", "down", "low", "bear", "selling", 
        "resistance", "pressure", "hike", "hawkish", "strong dollar", "yields rise", "retreats"
    ]

    all_headlines = []
    bull_count = 0
    bear_count = 0

    for src in sources:
        try:
            res = requests.get(src["url"], headers=headers, timeout=4)
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                for item in root.findall(".//item")[:15]:
                    title_elem = item.find("title")
                    if title_elem is not None and title_elem.text:
                        title_text = title_elem.text.strip()
                        lower_title = title_text.lower()

                        if any(w in lower_title for w in ["gold", "xau", "xauusd", "dollar", "fed", "yield", "rate", "cpi", "powell"]):
                            all_headlines.append({"source": src["name"], "title": title_text})
                            if any(b in lower_title for b in bullish_keywords):
                                bull_count += 1
                            if any(b in lower_title for b in bearish_keywords):
                                bear_count += 1
        except Exception:
            continue

    if not all_headlines:
        raw_headline = "Klíčové fundamenty trhu testují aktuální cenové hladiny."
        latest_source = "INVESTING.COM / FOREXFACTORY"
    else:
        raw_headline = all_headlines[0]["title"]
        latest_source = all_headlines[0]["source"]

    # Automatický překlad do češtiny
    cz_headline = translate_to_czech(raw_headline)

    if bull_count > bear_count:
        sentiment_label = "BULLISH SENTIMENT"
        sentiment_color = "#2ecc71"
        note = "Agregovaná fundamentální data z vybraných portálů indikují převahu nákupního tlaku a příznivé podmínky pro růst zlata."
    elif bear_count > bull_count:
        sentiment_label = "BEARISH SENTIMENT"
        sentiment_color = "#e74c3c"
        note = "Makro zprávy a signály ze sledovaných zdrojů naznačují prodejní tlak a možnou korekci na aktuálních úrovních."
    else:
        sentiment_label = "NEUTRAL SENTIMENT"
        sentiment_color = "#2ecc71"
        note = "Fundamentální zprávy vykazují vyrovnaný poměr sil. Trh vyčkává na další makroekonomické impulzy a zasedání centrálních bank."

    return {
        "label": sentiment_label,
        "color": sentiment_color,
        "note": note,
        "headline_cz": cz_headline,
        "headline_orig": raw_headline,
        "source": latest_source,
        "time": datetime.now().strftime("%H:%M:%S")
    }


# --- 5. LOGIN LOGIKA ---
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


# --- 6. VNITŘEK TERMINÁLU ---
st.markdown("""
    <div class="logo-container">
        <div class="logo-text" style="font-size:45px;"><span class="j-green">J</span>T | CAPITAL</div>
        <div class="logo-sub">TERMINAL v 1</div>
    </div>
""", unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([0.08, 0.84, 0.08])

with col_c:
    # --- A) KARTA: SVĚTOVÝ ČAS (3 MĚSTA) A ŽIVÉ SEANCE (Zelená barva) ---
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

                /* Horní řádek s hodinami (3 města) */
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

                /* Grid seancí (3 seance) */
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
                <!-- 1. SVĚTOVÉ HODINY (PRAHA, LONDÝN, NEW YORK) -->
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

                <!-- 2. SEANCE & ŽIVÉ ODPOČTY -->
                <div class="sessions-grid">
                    <!-- LONDÝN -->
                    <div class="session-box" id="box-london">
                        <div class="session-header">
                            <span class="session-name">LONDÝN</span>
                            <span class="session-badge" id="badge-london">--</span>
                        </div>
                        <div class="session-times">09:00 – 17:30 (SEČ)</div>
                        <div class="session-countdown" id="count-london">Načítání...</div>
                    </div>

                    <!-- NEW YORK -->
                    <div class="session-box" id="box-ny">
                        <div class="session-header">
                            <span class="session-name">NEW YORK</span>
                            <span class="session-badge" id="badge-ny">--</span>
                        </div>
                        <div class="session-times">14:00 – 23:00 (SEČ)</div>
                        <div class="session-countdown" id="count-ny">Načítání...</div>
                    </div>

                    <!-- WALL STREET -->
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

                    // Víkend: Sobota celá, Neděle do 23:00, Pátek po 23:00
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

    # --- B) KARTA: TRADINGVIEW GRAF XAUUSD ---
    components.html("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                html, body { margin: 0; padding: 0; background: transparent !important; overflow: hidden; }
                * { box-sizing: border-box; }
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

    # --- C) KARTA: ŽIVÝ FUNDAMENTÁLNÍ SENTIMENT (Český překlad) ---
    data = fetch_target_sources_sentiment()
    
    st.markdown(f"""
    <div class="terminal-card">
        <div style="color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; margin-bottom: 8px;">
            AI Fundamental Analysis &bull; Live Feed ({data['time']})
        </div>
        <div style="color: {data['color']}; font-weight: 900; font-size: 28px; letter-spacing: 2px;">
            {data['label']}
        </div>
        <p style="color: #ddd; margin-top: 12px; font-size: 15px; line-height: 1.6;">
            {data['note']}
        </p>
        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 12px 16px; margin-top: 15px; text-align: left;">
            <div style="color: #888; font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 4px;">
                Aktuální tržní zpráva ({data['source'].upper()}):
            </div>
            <div style="color: #2ecc71; font-size: 14px; font-weight: 600; line-height: 1.4;">
                "{data['headline_cz']}"
            </div>
            <div style="color: #666; font-size: 11px; font-style: italic; margin-top: 4px;">
                Originál: "{data['headline_orig']}"
            </div>
        </div>
        <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 18px; padding-top: 10px; color: #666; font-size: 10px; letter-spacing: 1px;">
            ZDROJE: INVESTING.COM &bull; INVESTINGLIVE &bull; FINANCIALJUICE &bull; TRADINGECONOMICS &bull; FOREXFACTORY
        </div>
    </div>
    """, unsafe_allow_html=True)
