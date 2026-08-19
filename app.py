import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING (Custom CSS für ein modernes UI) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1e293b; font-family: 'Inter', sans-serif; }
    
    /* Moderne KPI-Karten */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3b82f6;
        margin-bottom: 20px;
    }
    .metric-title { font-size: 14px; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .metric-value { font-size: 28px; color: #0f172a; font-weight: 700; margin: 5px 0; }
    .metric-delta { font-size: 14px; font-weight: 500; color: #10b981; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Interaktive Live-Datensteuerung) ---
st.sidebar.header("🕹️ Live-Daten anpassen")
st.sidebar.subheader("🏦 Bankkonten")
chf_privat = st.sidebar.number_input("Privatkonto (CHF)", value=12500, step=500)
chf_sparkonto = st.sidebar.number_input("Sparkonto (CHF)", value=45000, step=1000)

st.sidebar.subheader("📈 Investitionen")
chf_aktien = st.sidebar.number_input("Aktien & ETFs (CHF)", value=85000, step=1000)
chf_crypto = st.sidebar.number_input("Kryptowährungen (CHF)", value=8500, step=500)

st.sidebar.subheader("🛡️ Vorsorge")
chf_saeule3a = st.sidebar.number_input("Säule 3a (CHF)", value=34000, step=1000)
chf_pk = st.sidebar.number_input("Pensionskasse (CHF)", value=120000, step=5000)

st.sidebar.subheader("🛑 Verbindlichkeiten")
chf_schulden = st.sidebar.number_input("Kredite / Leasing (CHF)", value=15000, step=1000)

# --- DATEN-BERECHNUNG ---
total_liquid = chf_privat + chf_sparkonto
total_invested = chf_aktien + chf_crypto
total_pension = chf_saeule3a + chf_pk
total_assets = total_liquid + total_invested + total_pension
net_worth = total_assets - chf_schulden

# --- MAIN CONTENT ---
st.title("🦅 Vermögens-Dashboard")
st.markdown("Hier ist die visuelle Übersicht deiner gesamten finanziellen Situation.")
st.markdown("---")

# --- REIHE 1: KEY METRICS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'<div class="metric-card" style="border-left-color: #2563eb;"><div class="metric-title">Bruttovermögen</div><div class="metric-value">CHF {total_assets:,.2f}</div><div class="metric-delta">Gesamte Assets</div></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="metric-card" style="border-left-color: #10b981;"><div class="metric-title">Nettovermögen</div><div class="metric-value" style="color: #10b981;">CHF {net_worth:,.2f}</div><div class="metric-delta">Freies Vermögen</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="metric-card" style="border-left-color: #f59e0b;"><div class="metric-title">Investiert</div><div class="metric-value">CHF {total_invested:,.2f}</div><div class="metric-delta">Aktien & Krypto</div></div>', unsafe_allow_html=True)

with col4:
    st.markdown(f'<div class="metric-card" style="border-left-color: #ef4444;"><div class="metric-title">Verbindlichkeiten</div><div class="metric-value" style="color: #ef4444;">CHF {chf_schulden:,.2f}</div><div class="metric-delta" style="color: #ef4444;">Schulden / Leasing</div></div>', unsafe_allow_html=True)

# --- REIHE 2: DIAGRAMME ---
st.markdown("### 📊 Vermögensaufteilung & Struktur")
col_chart1, col_chart2 = st.columns(2)

asset_data = pd.DataFrame({
    "Kategorie": ["Privatkonto", "Sparkonto", "Aktien & ETFs", "Krypto", "Säule 3a", "Pensionskasse"],
    "Betrag": [chf_privat, chf_sparkonto, chf_aktien, chf_crypto, chf_saeule3a, chf_pk],
    "Klasse": ["Liquidität", "Liquidität", "Investments", "Investments", "Vorsorge", "Vorsorge"]
})

with col_chart1:
    fig_pie = px.pie(asset_data, values="Betrag", names="Kategorie", title="Verteilung nach Anlageklasse", hole=0.4, color_discrete_sequence=px.colors.sequential.Plasma)
    fig_pie.update_layout(margin=dict(t=40, b=0, l=0, r=0), legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    fig_sun = px.sunburst(asset_data, path=["Klasse", "Kategorie"], values="Betrag", title="Strukturierte Asset Allocation", color_discrete_sequence=px.colors.qualitative.Safe)
    fig_sun.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    st.plotly_chart(fig_sun, use_container_width=True)

# --- REIHE 3: ENTWICKLUNGSTREND ---
st.markdown("---")
st.markdown("### 🗓️ Vermögenswachstum (Historischer Trend)")

months = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug"]
history_liq = np.linspace(total_liquid*0.9, total_liquid, len(months))
history_inv = np.array([total_invested*0.85, total_invested*0.88, total_invested*0.92, total_invested*0.91, total_invested*0.95, total_invested*0.94, total_invested*0.98, total_invested])
history_pen = np.linspace(total_pension*0.96, total_pension, len(months))

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=months, y=history_liq, name="Liquidität", stackgroup='one', line=dict(color='#2563eb')))
fig_trend.add_trace(go.Scatter(x=months, y=history_inv, name="Investments", stackgroup='one', line=dict(color='#f59e0b')))
fig_trend.add_trace(go.Scatter(x=months, y=history_pen, name="Vorsorge", stackgroup='one', line=dict(color='#10b981')))

fig_trend.update_layout(title="Kumuliertes Wachstum über die letzten 8 Monate", xaxis_title="Monat", yaxis_title="Wert in CHF", legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig_trend, use_container_width=True)

