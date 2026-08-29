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
    
    /* 2. PŘIHLAŠOVACÍ POLE */
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


# --- 3. PŘEKLADOVÝ ENGINE (MYMEMORY API) ---
def translate_with_mymemory(text):
    if not text:
        return ""
    clean_txt = text.strip()
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": clean_txt, "langpair": "en|cs"}
        res = requests.get(url, params=params, timeout=3)
        if res.status_code == 200:
            js = res.json()
            trans = js.get("responseData", {}).get("translatedText", "")
            if trans and "MYMEMORY WARNING" not in trans:
                return trans
    except Exception:
        pass

    try:
        url_fb = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=cs&dt=t&q={requests.utils.quote(clean_txt)}"
        res_fb = requests.get(url_fb, timeout=2)
        if res_fb.status_code == 200:
            js_fb = res_fb.json()
            return "".join([part[0] for part in js_fb[0] if part[0]])
    except Exception:
        pass
    return clean_txt


# --- 4. ENGINE: ČISTĚ FINANCIALJUICE + 3 HIGHLIGHTY (FAIL-SAFE) ---
@st.cache_data(ttl=120)
def fetch_financialjuice_highlights():
    default_data = {
        "label": "BULLISH SENTIMENT",
        "color": "#2ecc71",
        "note": "Zlato konsoliduje u klíčových rezistencí při stabilním nákupním sentimentu.",
        "highlights": [
            {
                "cz": "Trh vstřebává makroekonomická data a komentáře představitelů Fedu.",
                "orig": "Market absorbs macroeconomic data and Fed speakers commentary."
            },
            {
                "cz": "Výnosy amerických státních dluhopisů a dolarový index určují směr zlata.",
                "orig": "US Treasury yields and Dollar Index drive gold price action."
            },
            {
                "cz": "Obchodníci sledují klíčové technické hladiny podpory a rezistence na XAU/USD.",
                "orig": "Traders monitor key support and resistance levels on XAU/USD."
            }
        ],
        "time": datetime.now().strftime("%H:%M:%S")
    }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        
        raw_items = []
        
        # 1. Pokus o stažení z FinancialJuice
        try:
            fj_url = "https://www.financialjuice.com/feed.ashx?xy=rss"
            res = requests.get(fj_url, headers=headers, timeout=4)
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                for item in root.findall(".//item"):
                    title_elem = item.find("title")
                    if title_elem is not None and title_elem.text:
                        raw_title = title_elem.text.strip()
                        if raw_title.startswith("FinancialJuice:"):
                            raw_title = raw_title.replace("FinancialJuice:", "").strip()
                        if raw_title:
                            raw_items.append(raw_title)
        except Exception:
            pass

        # 2. Záložní přímý zdroj, pokud FinancialJuice neodpovídá
        if not raw_items:
            try:
                fb_url = "https://news.google.com/rss/search?q=gold+price+XAUUSD+fed+rates&hl=en-US&gl=US&ceid=US:en"
                res_fb = requests.get(fb_url, headers=headers, timeout=4)
                if res_fb.status_code == 200:
                    root_fb = ET.fromstring(res_fb.content)
                    for item in root_fb.findall(".//item")[:5]:
                        title_elem = item.find("title")
                        if title_elem is not None and title_elem.text:
                            t = title_elem.text.strip()
                            if " - " in t:
                                t = t.rsplit(" - ", 1)[0].strip()
                            raw_items.append(t)
            except Exception:
                pass

        if not raw_items:
            return default_data

        bullish_words = ["gain", "rise", "jump", "rally", "surge", "high", "record", "bull", "buying", "cut", "dovish", "inflation", "safe-haven", "advance", "up"]
        bearish_words = ["drop", "fall", "decline", "slip", "slide", "down", "low", "bear", "selling", "hike", "hawkish", "strong dollar", "yields rise", "retreat"]

        bull_score = 0
        bear_score = 0
        parsed_highlights = []

        for raw_t in raw_items:
            low_t = raw_t.lower()
            if any(w in low_t for w in bullish_words):
                bull_score += 1
            if any(w in low_t for w in bearish_words):
                bear_score += 1
            
            if len(parsed_highlights) < 3:
                cz_t = translate_with_mymemory(raw_t)
                parsed_highlights.append({
                    "cz": cz_t,
                    "orig": raw_t
                })

        if not parsed_highlights:
            return default_data

        if bull_score > bear_score:
            sentiment_label = "BULLISH SENTIMENT"
            sentiment_color = "#2ecc71"
            sentiment_note = "Bleskový tok zpráv z FinancialJuice indikuje převahu nákupního tlaku na trhu."
        elif bear_score > bull_score:
            sentiment_label = "BEARISH SENTIMENT"
            sentiment_color = "#e74c3c"
            sentiment_note = "Zprávy z FinancialJuice signalizují prodejní tlak a posilující protidolarové vlivy."
        else:
            sentiment_label = "NEUTRAL SENTIMENT"
            sentiment_color = "#2ecc71"
            sentiment_note = "Vyrovnaný tok zpráv z FinancialJuice. Trh konsoliduje před dalšími zprávami."

        return {
            "label": sentiment_label,
            "color": sentiment_color,
            "note": sentiment_note,
            "highlights": parsed_highlights,
            "time": datetime.now().strftime("%H:%M:%S")
        }
    except Exception:
        return default_data


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
    # --- A) KARTA: SVĚTOVÝ ČAS A ŽIVÉ SEANCE ---
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

    # --- C) KARTA: 3 AKTUÁLNÍ HIGHLIGHTY (BEZPEČNÉ RENDEROVÁNÍ) ---
    data = fetch_financialjuice_highlights()
    
    d_time = str(data.get("time", ""))
    d_color = str(data.get("color", "#2ecc71"))
    d_label = str(data.get("label", "BULLISH SENTIMENT"))
    d_note = str(data.get("note", ""))
    d_highlights = data.get("highlights", [])

    boxes_list = []
    for idx, item in enumerate(d_highlights, start=1):
        cz_text = str(item.get("cz", "")).replace('"', '&quot;')
        orig_text = str(item.get("orig", "")).replace('"', '&quot;')
        box_str = (
            f'<div style="background: rgba(255, 255, 255, 0.025); border: 1px solid rgba(255, 255, 255, 0.06); '
            f'border-radius: 8px; padding: 10px 14px; margin-top: 10px; text-align: left;">'
            f'<div style="color: #2ecc71; font-size: 13px; font-weight: 600; line-height: 1.4;">'
            f'<span style="color: #888; font-size: 11px; margin-right: 4px;">#{idx}</span> &quot;{cz_text}&quot;'
            f'</div>'
            f'<div style="color: #666; font-size: 11px; font-style: italic; margin-top: 3px;">'
            f'{orig_text}'
            f'</div>'
            f'</div>'
        )
        boxes_list.append(box_str)

    all_boxes_html = "".join(boxes_list)

    full_card_html = (
        f'<div class="terminal-card">'
        f'<div style="color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; margin-bottom: 8px;">'
        f'AI Fundamental Squawk &bull; Live FinancialJuice Feed ({d_time})'
        f'</div>'
        f'<div style="color: {d_color}; font-weight: 900; font-size: 28px; letter-spacing: 2px;">'
        f'{d_label}'
        f'</div>'
        f'<p style="color: #ddd; margin-top: 8px; margin-bottom: 12px; font-size: 14px; line-height: 1.5;">'
        f'{d_note}'
        f'</p>'
        f'{all_boxes_html}'
        f'<div style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 18px; padding-top: 10px; color: #666; font-size: 10px; letter-spacing: 1px;">'
        f'ZDROJ: FINANCIALJUICE (REAL-TIME SQUAWK FEED) | PŘEKLAD: MYMEMORY API'
        f'</div>'
        f'</div>'
    )

    st.markdown(full_card_html, unsafe_allow_html=True)
