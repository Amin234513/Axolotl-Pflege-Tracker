import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# ===== MAGISCHES AXOLOTL-DESIGN =====
st.set_page_config(
    layout="wide", 
    page_title="🧪 Axolotl-Oase", 
    page_icon="🐉",
    initial_sidebar_state="expanded"
)

# Custom CSS mit Unterwasser-Flair
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&family=Rubik+Doodle+Shadow&display=swap');
:root {
    --axo-pink: #ff6ec7;
    --axo-blue: #48d1cc;
    --deep-water: #0a2463;
}
body {
    background: linear-gradient(135deg, var(--deep-water), #1e3d59);
    font-family: 'Quicksand', sans-serif;
    color: #e0f7fa;
}
h1, h2, h3 {
    font-family: 'Rubik Doodle Shadow', cursive !important;
    color: var(--axo-pink) !important;
    text-shadow: 0 0 10px rgba(255, 110, 199, 0.7);
}
.stApp {
    background: rgba(10, 36, 99, 0.85) !important;
    backdrop-filter: blur(8px);
    border-radius: 20px;
    box-shadow: 0 0 25px rgba(72, 209, 204, 0.6);
    border: 2px solid var(--axo-blue);
}
.st-emotion-cache-1y4p8pa {
    background: url('https://i.imgur.com/7X8Phwe.png') no-repeat bottom right;
    background-size: 30%;
}
.stButton button {
    background: linear-gradient(90deg, var(--axo-pink), #c71585) !important;
    border-radius: 20px !important;
    font-weight: 700 !important;
    transition: all 0.3s ease !important;
}
.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px var(--axo-pink);
}
.stProgress > div > div {
    background: linear-gradient(90deg, var(--axo-blue), #20b2aa) !important;
    box-shadow: 0 0 10px var(--axo-blue);
}
.stCheckbox > label > div:first-child {
    background: rgba(72, 209, 204, 0.3) !important;
}
.water-card {
    background: rgba(26, 95, 122, 0.6) !important;
    border-radius: 15px;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid var(--axo-blue);
    box-shadow: 0 0 8px rgba(72, 209, 204, 0.5);
}
.alert-bubble {
    background: rgba(255, 110, 199, 0.25) !important;
    border: 2px dashed var(--axo-pink);
}
</style>
""", unsafe_allow_html=True)

# ===== DATENSTRUKTUREN =====
if 'log' not in st.session_state:
    st.session_state.log = {
        'dates': [],
        'temp': [],
        'ph': [],
        'nh3': [],
        'no2': [],
        'feeding': [],
        'health': []
    }

if 'tasks' not in st.session_state:
    st.session_state.tasks = {
        'water_change': datetime.now().date(),
        'filter_clean': datetime.now().date() + timedelta(days=7),
        'tank_clean': datetime.now().date() + timedelta(days=30)
    }

# ===== DASHBOARD-KOPF =====
st.title("🧪 Axolotl Pflege-Tracker")
st.subheader("Dein magischer Begleiter für perfekte Wasserbedingungen")

# ===== SIDEBAR FÜR EINGABEN =====
with st.sidebar:
    st.header("📝 Neue Eintragung")
    
    # Wasserparameter
    st.subheader("💧 Wasserwerte")
    col1, col2 = st.columns(2)
    with col1:
        temp = st.number_input("Temperatur (°C)", min_value=10.0, max_value=25.0, value=18.0, step=0.5)
        ph = st.number_input("pH-Wert", min_value=5.0, max_value=9.0, value=7.4, step=0.1)
    with col2:
        nh3 = st.number_input("Ammoniak (ppm)", min_value=0.0, max_value=2.0, value=0.0, step=0.01)
        no2 = st.number_input("Nitrit (ppm)", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    
    # Fütterung & Gesundheit
    st.subheader("🍽️ Fütterung & Gesundheit")
    feeding = st.selectbox("Futterart", ["Regenwürmer", "Pellets", "Garnelen", "Spezialmix"])
    health = st.multiselect("Verhalten/Gesundheit", 
                          ["Aktiv", "Guter Appetit", "Versteckt sich", "Appetitlos", "Kiemenverfärbung", "Hautprobleme"])
    
    if st.button("🚀 Eintrag speichern", use_container_width=True):
        today = datetime.now().date()
        st.session_state.log['dates'].append(today)
        st.session_state.log['temp'].append(temp)
        st.session_state.log['ph'].append(ph)
        st.session_state.log['nh3'].append(nh3)
        st.session_state.log['no2'].append(no2)
        st.session_state.log['feeding'].append(feeding)
        st.session_state.log['health'].append(", ".join(health))
        st.success("Eintrag gespeichert!")
    
    st.divider()
    st.image("https://i.imgur.com/Dw6Fks1.gif", caption="Dein Axolotl dankt dir!")

# ===== WASSERPARAMETER-ÜBERWACHUNG =====
st.header("🌡️ Wasserparameter-Analyse")

# Idealwerte
ideal_values = {'temp': (16, 18), 'ph': (7.0, 7.6), 'nh3': (0, 0.02), 'no2': (0, 0.2)}

if st.session_state.log['dates']:
    df = pd.DataFrame(st.session_state.log)
    df['date'] = pd.to_datetime(df['dates'])
    
    # Parameter-Karten
    cols = st.columns(4)
    params = ['temp', 'ph', 'nh3', 'no2']
    icons = ['🌡️', '🧪', '☠️', '⚠️']
    
    for i, param in enumerate(params):
        latest_val = df[param].iloc[-1]
        ideal_min, ideal_max = ideal_values[param]
        
        with cols[i]:
            st.markdown(f"<div class='water-card'>"
                        f"<h3>{icons[i]} {param.upper()}</h3>"
                        f"<h2>{latest_val}</h2>"
                        f"<div>Ideal: {ideal_min}-{ideal_max}</div>"
                        f"</div>", unsafe_allow_html=True)
            
            # Statusanzeige
            if ideal_min <= latest_val <= ideal_max:
                st.success("✅ Optimal")
            elif (param == 'temp' and latest_val > 20) or (param in ['nh3', 'no2'] and latest_val > ideal_max):
                st.error("❌ Gefährlich!")
            else:
                st.warning("⚠️ Achtung")
    
    # Verlaufsdiagramm
    fig = px.line(df, x='date', y=params,
                 title='<b>📈 Parameterverlauf</b>',
                 labels={'value': 'Wert', 'variable': 'Parameter'},
                 color_discrete_map={
                     'temp': '#ff6ec7',
                     'ph': '#48d1cc',
                     'nh3': '#ff4d4d',
                     'no2': '#ff9a3d'
                 })
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("⏳ Noch keine Daten gesammelt. Starte mit den Eingaben in der Sidebar!")

# ===== FÜTTERUNG & GESUNDHEIT =====
st.header("🍽️ Fütterungsprotokoll & Gesundheit")

if st.session_state.log['dates']:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Letzte Fütterungen")
        feeding_df = df[['dates', 'feeding']].tail(5)
        st.dataframe(feeding_df.set_index('dates'), height=200)
        
        # Fütterungsstatistik
        feeding_counts = df['feeding'].value_counts()
        fig1 = px.pie(feeding_counts, values=feeding_counts.values, names=feeding_counts.index,
                     title='<b>🥗 Futterverteilung</b>',
                     color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Gesundheitszustand")
        health_df = df[['dates', 'health']].tail(5)
        st.dataframe(health_df.set_index('dates'), height=200)
        
        # Gesundheitsindikatoren
        health_status = "Gut" if any("Aktiv" in h or "Guter Appetit" in h for h in df['health']) else "Achtung"
        health_color = "#2ecc71" if health_status == "Gut" else "#e74c3c"
        
        st.markdown(f"""
        <div style="text-align:center; padding:20px; background:{health_color}20; border-radius:15px; border:2px solid {health_color}">
            <h3>Gesundheitsstatus</h3>
            <h1 style="color:{health_color}">{health_status}</h1>
        </div>
        """, unsafe_allow_html=True)

# ===== PFLEGEAUFGABEN & ERINNERUNGEN =====
st.header("🔔 Pflegeplaner")

today = datetime.now().date()
tasks = st.session_state.tasks

# Aufgabenkarten
col1, col2, col3 = st.columns(3)
tasks_data = [
    {"name": "Wasserwechsel", "date": tasks['water_change'], "icon": "💧", "days": 7},
    {"name": "Filterreinigung", "date": tasks['filter_clean'], "icon": "🧽", "days": 14},
    {"name": "Komplettreinigung", "date": tasks['tank_clean'], "icon": "🧼", "days": 30}
]

for i, task in enumerate(tasks_data):
    with [col1, col2, col3][i]:
        days_left = (task['date'] - today).days
        status = "✅ Erledigt" if days_left < 0 else f"⏳ {days_left} Tage"
        color = "#27ae60" if days_left < 0 else ("#f39c12" if days_left <= 3 else "#3498db")
        
        st.markdown(f"""
        <div class="water-card">
            <div style="font-size:2em">{task['icon']}</div>
            <h3>{task['name']}</h3>
            <p>Fällig am: {task['date'].strftime('%d.%m.%Y')}</p>
            <div style="color:{color}; font-weight:bold">{status}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Als erledigt markieren", key=f"task_{i}"):
            st.session_state.tasks[list(tasks.keys())[i]] = today + timedelta(days=task['days'])
            st.experimental_rerun()

# ===== AXOLOTL-WISSEN =====
with st.expander("📚 Axolotl-Wissensdatenbank", expanded=True):
    st.markdown("""
    **💡 Pflege-Tipps:**
    - Temperatur: 16-18°C (nie über 22°C!)
    - pH-Wert: 7.0-7.6
    - Kein Ammoniak oder Nitrit tolerierbar
    - Wöchentlich 25% Wasserwechsel
    
    **⚠️ Warnsignale:**
    - Kiemen nach vorne geklappt = Stress
    - Appetitlosigkeit >3 Tage
    - Weiße Flecken auf der Haut
    - Aufgeblähter Bauch
    
    **🍽️ Futter-Empfehlungen:**
    1. Regenwürmer (Hauptnahrung)
    2. Spezialpellets für Axolotl
    3. Gefrorene Blutwürmer (Leckerbissen)
    4. Kleine Süßwassergarnelen
    """)

# ===== EXPORT FUNKTION =====
st.download_button(
    label="📥 Pflegeprotokoll exportieren",
    data=pd.DataFrame(st.session_state.log).to_csv().encode('utf-8'),
    file_name="axolotl_pflegeprotokoll.csv",
    mime="text/csv",
    use_container_width=True
)

# ===== UNTERWASSER-ANIMATION =====
st.markdown("""
<div style="height:100px; overflow:hidden; position:relative; margin-top:50px">
    <div style="position:absolute; bottom:0; width:100%; text-align:center">
        <span style="font-size:3em">🐠 🌊 🐚 🐌 🦀</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.caption("🖋️ Entwickelt mit Liebe für Axolotl-Liebhaber | Daten werden lokal gespeichert und sind privat")
