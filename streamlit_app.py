import streamlit as st

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. KOMPLEXNÍ STYLING (Login, Pozadí, Custom Slider) ---
st.markdown("""
    <style>
    /* Absolutní černé pozadí */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {
        background: #000000 !important;
    }
    
    #canvas-container {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
    }

    /* Logo JT | CAPITAL */
    .logo-container { text-align: center; margin-top: 100px; margin-bottom: 30px; position: relative; z-index: 1; }
    .logo-text { font-family: 'Inter', sans-serif; font-weight: 900; font-size: 75px; letter-spacing: -4px; color: white; }
    .j-green { color: #2ecc71; }

    /* Input pole - sjednocený styl */
    .stTextInput input {
        background-color: rgba(15, 15, 15, 0.9) !important;
        color: white !important;
        border: 1px solid #222 !important;
        height: 50px !important;
        border-radius: 4px !important;
        text-align: center !important;
        font-size: 16px !important;
        margin-bottom: 10px !important;
    }
    .stTextInput input:focus { border-color: #2ecc71 !important; }

    /* --- CUSTOM SLIDE TO UNLOCK (Hacking Streamlit Slider) --- */
    /* Schování labelu a čísel slideru */
    div[data-testid="stSlider"] label, div[data-testid="stWidgetLabel"] { display: none; }
    div[data-testid="stSliderTickBar"] { display: none; }
    div[data-baseweb="slider"] > div:last-child { display: none; } /* Schová číslo u handle */

    /* Kolejnice slideru */
    div[data-baseweb="slider"] {
        background-color: rgba(20, 20, 20, 0.9) !important;
        border: 1px solid #222 !important;
        height: 50px !important;
        padding: 0px 5px !important;
        border-radius: 4px !important;
        margin-top: 5px !important;
    }

    /* Handle - Zelený čtverec s šipkou */
    div[role="slider"] {
        background-color: #2ecc71 !important;
        border-radius: 4px !important;
        width: 40px !important;
        height: 40px !important;
        border: none !important;
        box-shadow: 0 0 10px rgba(46, 204, 113, 0.5) !important;
        cursor: grab !important;
    }
    div[role="slider"]:active { cursor: grabbing !important; }
    
    /* Vložení šipky do handle */
    div[role="slider"]::after {
        content: "→";
        color: white;
        font-size: 24px;
        font-weight: bold;
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
    }

    /* Zelený progres při tažení */
    div[data-baseweb="slider"] div {
        background-color: transparent; /* Reset výchozích barev */
    }
    /* Selektor pro levou část kolejnice (progress) */
    div[data-baseweb="slider"] > div > div:first-child > div:first-child {
        background-color: rgba(46, 204, 113, 0.3) !important; /* Průhledná zelená pro progres */
        height: 40px !important;
        border-radius: 4px !important;
    }

    /* Ostatní UI */
    footer, header, #MainMenu { visibility: hidden; }
    </style>

    <div id="canvas-container"><canvas id="chartCanvas"></canvas></div>

    <script>
    const canvas = document.getElementById('chartCanvas');
    const ctx = canvas.getContext('2d');
    function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    window.addEventListener('resize', resize);
    resize();

    const candles = [];
    for (let i = 0; i < 40; i++) {
        candles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            w: 10, h: Math.random() * 60 + 20,
            type: Math.random() > 0.5 ? '#2ecc71' : '#e74c3c',
            speed: Math.random() * 0.4 + 0.1
        });
    }

    function animate() {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 0.15; 
        candles.forEach(c => {
            c.x -= c.speed;
            if (c.x < -20) { c.x = canvas.width + 20; c.y = Math.random() * canvas.height; }
            ctx.fillStyle = c.type;
            ctx.fillRect(c.x, c.y, c.w, c.h);
            ctx.fillRect(c.x + c.w/2 - 1, c.y - 10, 2, c.h + 20);
        });
        requestAnimationFrame(animate);
    }
    animate();
    </script>
    """, unsafe_allow_html=True)

# --- 3. LOGIN LOGIKA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 0.7, 1])
    with col2:
        num = st.text_input("NUM", placeholder="PŘIHLAŠOVACÍ ČÍSLO", label_visibility="collapsed")
        pwd = st.text_input("PWD", type="password", placeholder="HESLO", label_visibility="collapsed")
        
        # POTAŽENÍM DOPRAVA (Slider)
        unlock = st.slider("UNLOCK", 0, 100, 0, key="unlock_slider")
        
        if unlock == 100:
            if num == "1234" and pwd == "admin":
                st.session_state.authenticated = True
                st.success("AUTORIZACE ÚSPĚŠNÁ")
                st.rerun()
            else:
                st.error("PŘÍSTUP ZAMÍTNUT")
                # Reset slideru by vyžadoval rerun, pro teď stačí upozornění
                st.info("Vraťte posuvník doleva a zadejte správné údaje.")
    st.stop()

# --- 4. VNITŘEK APLIKACE ---
st.sidebar.markdown('### JT | CAPITAL')
if st.sidebar.button("ODHLÁSIT SE"):
    st.session_state.authenticated = False
    st.rerun()

st.title("🏛 Dashboard")
st.write("Vítejte v uzavřené sekci JT | CAPITAL.")
# Zde bude pokračovat tvůj dashboard...
