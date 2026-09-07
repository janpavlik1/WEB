import streamlit as st
import datetime
import pytz
import pandas as pd
import streamlit.components.v1 as components

# Konfigurace stránky
st.set_page_config(page_title="J.T CAPITAL | Terminal", layout="wide", initial_sidebar_state="collapsed")

if 'screen' not in st.session_state:
    st.session_state['screen'] = 'login'

# Vylepšená funkce pro CSS s ANIMACEMI
def inject_css(is_dark=True):
    # Definice CSS animací (Fade In a Slide Up)
    animations = '''
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Aplikace animací na hlavní kontejner Streamlitu */
    .block-container {
        animation: fadeIn 1s ease-out, slideUp 0.8s ease-out;
    }
    '''

    if is_dark:
        css = f'''
        <style>
            {animations}
            .stApp {{ background-color: #121212; color: #f5f5f5; transition: background-color 1s ease; }}
            h1, h2, h3, p {{ color: #d4af37 !important; }}
            .stTextInput > div > div > input {{ background-color: #1e1e1e; color: white; border: 1px solid #333; }}
            .stButton > button {{ background-color: #d4af37; color: black; transition: all 0.3s ease; border: none; }}
            .stButton > button:hover {{ transform: scale(1.05); background-color: #f1c40f; }}
            #MainMenu, footer, header {{visibility: hidden;}}
        </style>
        '''
    else:
        css = f'''
        <style>
            {animations}
            .stApp {{ background-color: #f8f9fa; color: #1a1a1a; transition: background-color 1s ease; }}
            h2, h3 {{ color: #1a1a1a !important; }}
            .stProgress > div > div > div {{ background-color: #d4af37; }}
            .stButton > button {{ background-color: #1a1a1a; color: white; transition: all 0.3s ease; }}
            .stButton > button:hover {{ background-color: #d4af37; color: black; }}
            #MainMenu, footer, header {{visibility: hidden;}}
        </style>
        '''
    st.markdown(css, unsafe_allow_html=True)

# ==========================================
# OBRAZOVKA 1: LOGIN
# ==========================================
if st.session_state['screen'] == 'login':
    inject_css(is_dark=True)
    st.markdown("<h1 style='text-align: center; margin-top: 15vh; font-size: 4rem; letter-spacing: 5px;'>J.T CAPITAL</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #888;'>Private Trading Terminal</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        st.write("")
        username = st.text_input("Přihlašovací číslo", placeholder="1234")
        password = st.text_input("Heslo", type="password", placeholder="jtcapital")
        
        if st.button("Vstoupit", use_container_width=True):
            if username == "1234" and password == "jtcapital":
                st.session_state['screen'] = 'welcome'
                st.rerun()
            else:
                st.error("Nesprávné přihlašovací údaje.")

# ==========================================
# OBRAZOVKA 2: UVÍTÁNÍ
# ==========================================
elif st.session_state['screen'] == 'welcome':
    inject_css(is_dark=True)
    st.markdown("<h1 style='text-align: center; margin-top: 20vh; font-size: 4rem; letter-spacing: 5px;'>J.T CAPITAL</h1>", unsafe_allow_html=True)
    
    tz = pytz.timezone('Europe/Prague')
    now = datetime.datetime.now(tz)
    ny_open = now.replace(hour=15, minute=30, second=0, microsecond=0)
    
    if now > ny_open:
        ny_open += datetime.timedelta(days=1)
        
    diff = ny_open - now
    hours = int(diff.total_seconds() // 3600)
    minutes = int((diff.total_seconds() % 3600) // 60)
    
    if 15 <= now.hour < 22 and (now.hour > 15 or now.minute >= 30):
        msg = "Pavlíku, vítej v J.T CAPITAL. Wall Street je aktuálně otevřena, soustřeď se na trh!"
    else:
        msg = f"Pavlíku, vítej v J.T CAPITAL.<br>Dle aktuálního času nám za {hours}h a {minutes}min otvírá Wall Street, mnoho štěstí!"
        
    st.markdown(f"<h3 style='text-align: center; color: #aaa; font-weight: normal; line-height: 1.5;'>{msg}</h3>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        if st.button("Přejít do Terminálu ➔", use_container_width=True):
            st.session_state['screen'] = 'terminal'
            st.rerun()

# ==========================================
# OBRAZOVKA 3: HLAVNÍ TERMINÁL
# ==========================================
elif st.session_state['screen'] == 'terminal':
    inject_css(is_dark=False) 
    
    st.markdown("<h2 style='text-align: center; color: #d4af37 !important; margin-bottom: 30px;'>J.T CAPITAL - TERMINAL</h2>", unsafe_allow_html=True)
    
    tz = pytz.timezone('Europe/Prague')
    now_str = datetime.datetime.now(tz).strftime('%H:%M:%S')
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Aktuální čas (CZ)", now_str)
    m2.metric("NY Session (Wall Street)", "15:30 - 22:00")
    m3.metric("London Session", "09:00 - 17:30")
    
    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Analýza Sentimentu (XAU/USD)")
        st.info("**Základní makro:** Americká inflace mírně klesla, což oslabuje tlak na FED ohledně dalšího zvýšení sazeb. Očekává se oslabení DXY, což tvoří silně býčí sentiment pro Zlato.")
        st.progress(0.80, text="80% Bullish (Dle makro modelů)")
        if st.button("Manuální obnova makra ⟳"):
            st.success("Makro data byla úspěšně aktualizována!")
        
        st.write("")
        st.subheader("Živý Graf (TradingView)")
        
        tv_html = '''
        <div class="tradingview-widget-container">
          <div id="tradingview_xauusd"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({
          "autosize": true,
          "height": 550,
          "symbol": "VANTAGE:XAUUSD",
          "interval": "D",
          "timezone": "Europe/Prague",
          "theme": "light",
          "style": "1",
          "locale": "cs",
          "enable_publishing": false,
          "container_id": "tradingview_xauusd"
        });
          </script>
        </div>
        '''
        components.html(tv_html, height=550)

    with col_right:
        st.subheader("Dnešní Makro (ForexFactory)")
        macro_data = pd.DataFrame({
            "Čas": ["14:30", "16:00"],
            "Událost": ["USA - JOLTS", "USA - CB Confidence"],
            "Impakt": ["Vysoký", "Vysoký"]
        })
        st.dataframe(macro_data, hide_index=True, use_container_width=True)
        
        st.write("")
        st.subheader("Centrální Banky - Radar")
        cb_data = pd.DataFrame({
            "Banka": ["ECB", "FED"],
            "Sazba": ["4.25%", "5.50%"],
            "Zasedání": ["10.09.2026", "18.09.2026"]
        })
        st.dataframe(cb_data, hide_index=True, use_container_width=True)
        
        with st.expander("ECB - Makroekonomický výhled", expanded=True):
            st.markdown('''**Poslední výstup (C. Lagarde):** "Inflace v eurozóně zůstává lepkavá. Nevylučujeme další hike."\n\n*Dopad:* Euro si udržuje sílu, trhy zaceňují 40% šanci na zvýšení.''')
            
        with st.expander("FED - Makroekonomický výhled"):
            st.markdown('''**Poslední výstup (J. Powell):** "Budeme postupovat opatrně, sazby mohou zůstat nahoře déle."\n\n*Dopad:* Zastavení oslabování dolaru (DXY).''')
