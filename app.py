import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- CONFIG: PASSWORT & DATEI ---
SECRET_PASSWORD = "Schweiz2026"  # <-- ÄNDERE DEIN PASSWORT HIER!
DATA_FILE = "vermoegensdaten.csv"

# --- LOGIN FUNKTION ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]:
        return True

    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns()
    with col2:
        st.subheader("🔒 Privates Finanz-Dashboard")
        user_password = st.text_input("Passwort", type="password", key="login_password")
        if st.button("Anmelden"):
            if user_password == SECRET_PASSWORD:
                st.session_state["password_correct"] = True
                st.success("Login erfolgreich!")
                st.rerun()
            else:
                st.error("❌ Falsches Passwort.")
    return False

# --- MAIN APP START ---
if check_password():
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        st.error("Datei vermoegensdaten.csv nicht gefunden oder leer! Bitte erstelle sie im Ordner.")
    else:
        df_history = pd.read_csv(DATA_FILE)
        df_history['Datum'] = pd.to_datetime(df_history['Datum'])
        df_history = df_history.sort_values(by='Datum')
        latest_entry = df_history.iloc[-1]

        st.title("🦅 Dein Echtes Vermögens-Dashboard")
        if st.sidebar.button("🔒 Abmelden"):
            st.session_state["password_correct"] = False
            st.rerun()

        # --- BERECHNUNGEN ---
        total_liquid = latest_entry['Liquide_Mittel']
        total_invested = latest_entry['Sparvermoegen'] + latest_entry['Boerse']
        total_pension = latest_entry['Private_Vorsorge'] + latest_entry['LPP']
        total_assets = total_liquid + total_invested + total_pension

        # --- METRICS ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Gesamtvermögen (Assets)", f"{total_assets:,.0f} CHF")
        col2.metric("Investiertes Vermögen", f"{total_invested:,.0f} CHF")
        col3.metric("Vorsorge-Guthaben", f"{total_pension:,.0f} CHF")
        st.markdown("---")

        # --- LAYOUT SPALTEN ---
        col_left, col_right = st.columns()
        with col_left:
            st.markdown("### 📊 Aktuelle Verteilung")
            asset_data = pd.DataFrame({
                "Kategorie": ["Liquide Mittel", "Sparvermögen", "Investitionen Börse", "Private Vorsorge", "LPP"],
                "Betrag": [latest_entry['Liquide_Mittel'], latest_entry['Sparvermoegen'], latest_entry['Boerse'], latest_entry['Private_Vorsorge'], latest_entry['LPP']]
            })
            st.plotly_chart(px.pie(asset_data, values="Betrag", names="Kategorie", hole=0.4), use_container_width=True)

        with col_right:
            st.markdown("### 📝 Neuen Monat hinzufügen")
            with st.form("add_form", clear_on_submit=False):
                input_date = st.date_input("Stichtag", datetime.now())
                v_liq = st.number_input("Liquide Mittel (CHF)", value=float(latest_entry['Liquide_Mittel']))
                v_spar = st.number_input("Sparvermögen (CHF)", value=float(latest_entry['Sparvermoegen']))
                v_boerse = st.number_input("Investitionen Börse (CHF)", value=float(latest_entry['Boerse']))
                v_priv = st.number_input("Private Vorsorge (CHF)", value=float(latest_entry['Private_Vorsorge']))
                v_lpp = st.number_input("LPP (Pensionskasse - CHF)", value=float(latest_entry['LPP']))
                
                if st.form_submit_button("💾 Monat speichern"):
                    new_row = pd.DataFrame([{
                        "Datum": input_date.strftime("%Y-%m-%d"), "Liquide_Mittel": v_liq,
                        "Sparvermoegen": v_spar, "Boerse": v_boerse, "Private_Vorsorge": v_priv, "LPP": v_lpp
                    }])
                    df_history = df_history[df_history['Datum'] != pd.to_datetime(new_row['Datum'].iloc[0])]
                    df_all = pd.concat([df_history, new_row], ignore_index=True)
                    df_all.to_csv(DATA_FILE, index=False)
                    st.success("Erfolgreich gespeichert!")
                    st.rerun()

        # --- GRAPH ---
        st.markdown("---")
        st.markdown("### 📈 Kumulative Evolution")
        df_history['Liquidität'] = df_history['Liquide_Mittel']
        df_history['Investments'] = df_history['Sparvermoegen'] + df_history['Boerse']
        df_history['Vorsorge'] = df_history['Private_Vorsorge'] + df_history['LPP']

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=df_history['Datum'], y=df_history['Liquidität'], name="Liquide Mittel", stackgroup='one', line=dict(color='#2563eb')))
        fig_trend.add_trace(go.Scatter(x=df_history['Datum'], y=df_history['Investments'], name="Investments", stackgroup='one', line=dict(color='#f59e0b')))
        fig_trend.add_trace(go.Scatter(x=df_history['Datum'], y=df_history['Vorsorge'], name="Vorsorge (3a & LPP)", stackgroup='one', line=dict(color='#10b981')))
        st.plotly_chart(fig_trend, use_container_width=True)

        # --- TABLE ---
        st.markdown("### 🗒️ Komplette historische Tabelle")
        st.dataframe(df_history[['Datum', 'Liquide_Mittel', 'Sparvermoegen', 'Boerse', 'Private_Vorsorge', 'LPP']], use_container_width=True)

