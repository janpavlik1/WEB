import streamlit as st

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. JS ANIMACE + TOTÁLNÍ PŘEBITÍ DESIGNU ---
st.markdown("""
    <style>
    /* Totální odstranění výchozího pozadí Streamlitu */
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    .stApp {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Fixní černé pozadí pod canvasem */
    body {
        background-color: #000000 !important;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }

    /* Canvas jako absolutní pozadí */
    #bg-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1; /* Musí být úplně vzadu */
        background-color: #000000;
    }

    /* Stylizace loga */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .logo-text {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 65px;
        letter-spacing: -3px;
        color: white;
    }
    .j-green { color: #2ecc71; }

    /* Stylizace přihlašovacího boxu */
    .login-box {
        background-color: rgba(15, 15, 15, 0.85);
        padding: 40px;
        border-radius: 15px;
        border: 1px solid rgba(46, 204, 113, 0.3);
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
    }

    /* Úprava vstupních polí */
    input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #333 !important;
    }

    /* Skrytí Streamlit prvků */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>

    <!-- HTML Canvas pro animaci -->
    <canvas id="bg-canvas"></canvas>

    <script>
    const canvas = document.getElementById('bg-canvas');
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    let candles = [];
    // Vytvoříme počáteční svíčky
    for (let i = 0; i < 40; i++) {
        candles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            w: 12,
            h: Math.random() * 100 + 20,
            color: Math.random() > 0.5 ? '#2ecc71' : '#e74c3c',
            speed: Math.random() * 0.6 + 0.2
        });
    }

    function draw() {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.globalAlpha = 0.25; // Průhlednost grafu na pozadí

        candles.forEach(c => {
            c.x -= c.speed;
            if (c.x < -20) {
                c.x = canvas.width + 20;
                c.y = Math.random() * canvas.height;
            }
            
            ctx.fillStyle = c.color;
            // Tělo
            ctx.fillRect(c.x, c.y, c.w, c.h);
            // Knot
            ctx.fillRect(c.x + c.w/2 - 1, c.y - 15, 2, c.h + 30);
        });

        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """, unsafe_allow_html=True)

# --- 3. LOGIN LOGIKA ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Odsazení odshora
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    
    # Logo JT | CAPITAL
    st.markdown('<div class="logo-container"><div class="logo-text"><span class="j-green">J</span>T | CAPITAL</div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        # Průhledný box pro login
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            num = st.text_input("Přihlašovací číslo", placeholder="1234")
            pwd = st.text_input("Heslo", type="password", placeholder="admin")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("PŘIHLÁSIT SE", use_container_width=True):
                if num == "1234" and pwd == "admin":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Nesprávné údaje.")
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 4. VNITŘEK APLIKACE (Po přihlášení) ---
# Zde se změní rozvržení na dashboard, ale animace na pozadí může zůstat tlumená
st.sidebar.markdown('<div style="font-size: 24px; font-weight: bold;"><span style="color: #2ecc71;">J</span>T | CAPITAL</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
menu = st.sidebar.radio("NAVIGACE", ["DASHBOARD", "KALENDÁŘ", "STRATEGIE"])

if menu == "DASHBOARD":
    st.title("Market Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.metric("XAUUSD", "2,405.30", "+0.25%")
    c2.metric("NAS100", "18,480.00", "-0.10%")
    c3.metric("DJ30", "39,210.00", "+0.02%")
    
    st.markdown("""
    <div style="background-color: rgba(20, 20, 20, 0.8); padding: 25px; border-radius: 10px; border: 1px solid #2ecc71;">
        <h3 style="color: #2ecc71;">Vítejte zpět</h3>
        <p>Právě sledujete živý feed JT | CAPITAL. Všechny systémy jsou online.</p>
    </div>
    """, unsafe_allow_html=True)
