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
    col1, col2, col3 = st.columns(3)
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

        # --- EINZELWERTE AUSLESEN ---
        v_liq = latest_entry['Liquide_Mittel']
        v_spar = latest_entry['Sparvermoegen']
        v_boerse = latest_entry['Boerse']
        v_priv = latest_entry['Private_Vorsorge']
        v_lpp = latest_entry['LPP']
        total_assets = v_liq + v_spar + v_boerse + v_priv + v_lpp
        # --- METRICS ---
        row1_col1, row1_col2, row1_col3 = st.columns(3)
        row1_col1.metric("🦅 Gesamtkapital (Total Assets)", f"{total_assets:,.0f} CHF")
        row1_col2.metric("💵 Liquide Mittel", f"{v_liq:,.0f} CHF")
        row1_col3.metric("🏦 Sparkapital", f"{v_spar:,.0f} CHF")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        row2_col1, row2_col2, row2_col3 = st.columns(3)
        row2_col1.metric("📈 Investiertes Kapital", f"{v_boerse:,.0f} CHF")
        row2_col2.metric("🛡️ Private Vorsorge", f"{v_priv:,.0f} CHF")
        row2_col3.metric("💼 LPP (Pensionskasse)", f"{v_lpp:,.0f} CHF")
        
        st.markdown("---")

        # --- LAYOUT SPALTEN ---
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("### 📊 Aktuelle Verteilung")
            asset_data = pd.DataFrame({
                "Kategorie": ["Liquide Mittel", "Sparkapital", "Investiertes Kapital", "Private Vorsorge", "LPP"],
                "Betrag": [v_liq, v_spar, v_boerse, v_priv, v_lpp]
            })
            st.plotly_chart(px.pie(asset_data, values="Betrag", names="Kategorie", hole=0.4), use_container_width=True)

        with col_right:
            st.markdown("### 📝 Neuen Monat hinzufügen")
            with st.form("add_form", clear_on_submit=False):
                input_date = st.date_input("Stichtag", datetime.now())
                v_liq_in = st.number_input("Liquide Mittel (CHF)", value=float(v_liq))
                v_spar_in = st.number_input("Sparkapital (CHF)", value=float(v_spar))
                v_boerse_in = st.number_input("Investiertes Kapital (CHF)", value=float(v_boerse))
                v_priv_in = st.number_input("Private Vorsorge (CHF)", value=float(v_priv))
                v_lpp_in = st.number_input("LPP (Pensionskasse - CHF)", value=float(v_lpp))
                
                if st.form_submit_button("💾 Monat speichern"):
                    new_row = pd.DataFrame([{
                        "Datum": input_date.strftime("%Y-%m-%d"), "Liquide_Mittel": v_liq_in,
                        "Sparvermoegen": v_spar_in, "Boerse": v_boerse_in, "Private_Vorsorge": v_priv_in, "LPP": v_lpp_in
                    }])
                    df_history = df_history[df_history['Datum'] != pd.to_datetime(new_row['Datum'].iloc[0])]
                    df_all = pd.concat([df_history, new_row], ignore_index=True)
                    df_all.to_csv(DATA_FILE, index=False)
                    st.success("Erfolgreich gespeichert!")
                    st.rerun()

            # --- NEU: EINTRAG LÖSCHEN FORMULAR ---
            st.markdown("---")
            st.markdown("### 🗑️ Eintrag löschen")
            # Formatierte Datumsliste für das Dropdown erstellen
            df_history['Datum_Str'] = df_history['Datum'].dt.strftime('%Y-%m-%d')
            all_dates = df_history['Datum_Str'].unique().tolist()
            
            with st.form("delete_form", clear_on_submit=True):
                date_to_delete = st.selectbox("Wähle das Datum aus, das gelöscht werden soll:", all_dates)
                if st.form_submit_button("❌ Ausgewählten Monat unwiderruflich löschen"):
                    # Filtere die Zeile heraus
                    df_all = df_history[df_history['Datum_Str'] != date_to_delete]
                    # Hilfsspalten entfernen vor dem Speichern
                    df_save = df_all.drop(columns=['Datum_Str'], errors='ignore')
                    df_save.to_csv(DATA_FILE, index=False)
                    st.success(f"Eintrag vom {date_to_delete} wurde erfolgreich gelöscht!")
                    st.rerun()

        # --- GRAPH ---
        st.markdown("---")
        st.markdown("### 📈 Kumulative Evolution")
        # Hilfsspalten für den Graphen neu berechnen, falls vorher gelöscht wurde
        df_history['Liquidität'] = df_history['Liquide_Mittel']
        df_history['Sparkapital_Klasse'] = df_history['Sparvermoegen']
        df_history['Investments'] = df_history['Boerse']
        df_history['Vorsorge_Privat'] = df_history['Private_Vorsorge']
        df_history['Pensionskasse_Klasse'] = df_history['LPP']

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=df_history['Datum'], y=df_history['Liquidität'], name="Liquide Mittel", stackgroup='one', line=dict(color='#2563eb')))
        fig_trend.add_trace(go.Scatter(x=df_history['Datum'], y=df_history['Sparkapital_Klasse'], name="Sparkapital", stackgroup='one', line=dict(color='#38bdf8')))
        fig_trend.add_trace(go.Scatter(x=df_history['Datum'], y=df_history['Investments'], name="Investiertes Kapital", stackgroup='one', line=dict(color='#f59e0b')))
        fig_trend.add_trace(go.Scatter(x=df_history['Datum'], y=df_history['Vorsorge_Privat'], name="Private Vorsorge", stackgroup='one', line=dict(color='#10b981')))
        fig_trend.add_trace(go.Scatter(x=df_history['Datum'], y=df_history['Pensionskasse_Klasse'], name="LPP (Pensionskasse)", stackgroup='one', line=dict(color='#059669')))
        st.plotly_chart(fig_trend, use_container_width=True)

        # --- TABLE ---
        st.markdown("### 🗒️ Komplette historische Tabelle")
        st.dataframe(df_history[['Datum', 'Liquide_Mittel', 'Sparvermoegen', 'Boerse', 'Private_Vorsorge', 'LPP']], use_container_width=True)
