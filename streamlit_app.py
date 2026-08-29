import streamlit as st

# --- 1. KONFIGURACE ---
st.set_page_config(
    page_title="JT | CAPITAL",
    page_icon="📈",
    layout="wide"
)

# --- 2. ANIMOVANÉ POZADÍ + CSS (JT | CAPITAL Branding) ---
st.markdown("""
    <style>
    /* Fixní pozadí pro animaci */
    #canvas-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background-color: #05070a;
    }

    .stApp {
        background: transparent;
    }

    /* Branding Loga */
    .logo-text {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 56px;
        letter-spacing: -2px;
        text-align: center;
        margin-bottom: 5px;
        color: white;
    }
    .j-letter { color: #2ecc71; }
    
    /* Vstupy a tlačítka */
    .stTextInput>div>div>input {
        background-color: rgba(22, 26, 31, 0.8) !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    
    .stButton>button {
        background-color: #2ecc71 !important;
        color: white !important;
        border-radius: 4px !important;
        width: 100% !important;
        font-weight: bold !important;
        height: 50px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3);
    }

    /* Skrytí menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>

    <div id="canvas-container">
        <canvas id="chartCanvas"></canvas>
    </div>

    <script>
    const canvas = document.getElementById('chartCanvas');
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    const candles = [];
    const candleCount = 60;
    const spacing = 25;

    for (let i = 0; i < candleCount; i++) {
        candles.push({
            x: i * spacing,
            y: Math.random() * canvas.height,
            w: 12,
            h: Math.random() * 100 + 20,
            type: Math.random() > 0.5 ? '#2ecc71' : '#e74c3c',
            speed: Math.random() * 0.5 + 0.2
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.globalAlpha = 0.15; // Tlumené pozadí

        candles.forEach(c => {
            c.x -= c.speed;
            if (c.x < -20) {
                c.x = canvas.width + 20;
                c.y = Math.random() * canvas.height;
            }

            ctx.fillStyle = c.type;
            // Tělo svíčky
            ctx.fillRect(c.x, c.y, c.w, c.h);
            // Knot svíčky
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
    # Vertikální centrování
    for _ in range(8): st.write("\n")
    
    st.markdown('<div class="logo-text"><span class="j-letter">J</span>T | CAPITAL</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 0.8, 1])
    with col2:
        login_number = st.text_input("Přihlašovací číslo", placeholder="Např. 1234")
        password = st.text_input("Heslo", type="password", placeholder="••••••••")
        
        st.write("") # Mezera
        if st.button("PŘIHLÁSIT SE"):
            if login_number == "1234" and password == "jt2024":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Neplatné údaje.")
    st.stop()

# --- 4. VNITŘEK APLIKACE (Po přihlášení) ---
# Zde kód pokračuje jako v minulé verzi, ale pozadí zůstává aktivní
st.sidebar.markdown('<div style="font-size: 24px; font-weight: bold;"><span style="color: #2ecc71;">J</span>T | CAPITAL</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
menu = st.sidebar.radio("NAVIGACE", ["DASHBOARD", "KALENDÁŘ", "ADMIN"])

if menu == "DASHBOARD":
    st.title("Market Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("XAUUSD", "2,398.10", "+1.15%")
    c2.metric("NAS100", "18,420.50", "-0.45%", delta_color="inverse")
    c3.metric("DJ30", "39,120.00", "+0.05%")
    
    st.markdown("""
    <div style="background-color: rgba(22, 26, 31, 0.7); padding: 20px; border-radius: 10px; border: 1px solid #333;">
        <h3>Vítej v JT | CAPITAL</h3>
        <p>Systém je připraven. Sledujte dnešní fundamentální střípky v sekci analýz.</p>
    </div>
    """, unsafe_allow_html=True)
