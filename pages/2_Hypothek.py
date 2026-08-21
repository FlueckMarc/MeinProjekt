import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# ============================================================
# KONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Budget",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# DATEIEN
# ============================================================


DATA_FILE = "hypothekdaten.csv"


# ============================================================
# HEADER
# ============================================================

st.title("🏠 Hypothekar- & Tragbarkeitsrechner")

st.caption(
    "Schweizer Hypothekarberechnung und Tragbarkeit"
)


# ============================================================
# EINGABEN
# ============================================================

st.markdown("### 🏠 Immobilie & Finanzierung")

col1, col2, col3 = st.columns(3)

with col1:

    immobilienwert = st.number_input(
        "🏠 Immobilienwert / Kaufpreis (CHF)",
        min_value=0.0,
        value=1_500_000.0,
        step=10_000.0
    )

with col2:

    eigenkapital = st.number_input(
        "💰 Eigenkapital (CHF)",
        min_value=0.0,
        value=500_000.0,
        step=10_000.0
    )

with col3:

    hypothek = st.number_input(
        "🏦 Hypothek (CHF)",
        min_value=0.0,
        value=1_000_000.0,
        step=10_000.0
    )


# ============================================================
# ZINSEN
# ============================================================

st.markdown("---")

st.markdown("### 📈 Hypothekarzinsen")

col1, col2, col3 = st.columns(3)

with col1:

    zinssatz = st.number_input(
        "Aktueller Zinssatz (%)",
        min_value=0.0,
        value=1.50,
        step=0.05
    )

with col2:

    kalk_zinssatz = st.number_input(
        "Kalkulatorischer Zinssatz (%)",
        min_value=0.0,
        value=5.00,
        step=0.25
    )

with col3:

    amortisation = st.number_input(
        "Amortisation pro Jahr (CHF)",
        min_value=0.0,
        value=10_000.0,
        step=1_000.0
    )


# ============================================================
# UNTERHALT
# ============================================================

st.markdown("---")

st.markdown("### 🏡 Unterhalt & Einkommen")

col1, col2, col3 = st.columns(3)

with col1:

    unterhalt_prozent = st.number_input(
        "Unterhalt / Nebenkosten (% Immobilienwert)",
        min_value=0.0,
        value=1.00,
        step=0.10
    )

with col2:

    jahreseinkommen = st.number_input(
        "Brutto-Jahreseinkommen (CHF)",
        min_value=0.0,
        value=143_400.0,
        step=1_000.0
    )

with col3:

    weitere_einkommen = st.number_input(
        "Weitere Jahreseinkommen (CHF)",
        min_value=0.0,
        value=0.0,
        step=1_000.0
    )


# ============================================================
# BERECHNUNGEN
# ============================================================

if immobilienwert > 0:

    belehnung = (
        hypothek
        / immobilienwert
        * 100
    )

    eigenkapital_quote = (
        eigenkapital
        / immobilienwert
        * 100
    )

else:

    belehnung = 0
    eigenkapital_quote = 0


# ------------------------------------------------------------
# EFFEKTIVE ZINSKOSTEN
# ------------------------------------------------------------

effektive_zinsen = (
    hypothek
    * zinssatz
    / 100
)


# ------------------------------------------------------------
# KALKULATORISCHE ZINSKOSTEN
# ------------------------------------------------------------

kalk_zinsen = (
    hypothek
    * kalk_zinssatz
    / 100
)


# ------------------------------------------------------------
# UNTERHALT
# ------------------------------------------------------------

unterhaltskosten = (
    immobilienwert
    * unterhalt_prozent
    / 100
)


# ------------------------------------------------------------
# JÄHRLICHE BELASTUNG
# ------------------------------------------------------------

effektive_jahresbelastung = (
    effektive_zinsen
    + amortisation
    + unterhaltskosten
)


kalk_jahresbelastung = (
    kalk_zinsen
    + amortisation
    + unterhaltskosten
)


# ------------------------------------------------------------
# MONATLICHE BELASTUNG
# ------------------------------------------------------------

effektive_monatsbelastung = (
    effektive_jahresbelastung
    / 12
)

kalk_monatsbelastung = (
    kalk_jahresbelastung
    / 12
)


# ------------------------------------------------------------
# TRAGBARKEIT
# ------------------------------------------------------------

gesamteinkommen = (
    jahreseinkommen
    + weitere_einkommen
)


if gesamteinkommen > 0:

    tragbarkeit = (
        kalk_jahresbelastung
        / gesamteinkommen
        * 100
    )

else:

    tragbarkeit = 0


# ============================================================
# FINANZIERUNG
# ============================================================

st.markdown("---")

st.markdown("### 📊 Finanzierung")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🏦 Hypothek",
    f"{hypothek:,.0f} CHF"
)

col2.metric(
    "💰 Eigenkapital",
    f"{eigenkapital:,.0f} CHF"
)

col3.metric(
    "📊 Belehnung",
    f"{belehnung:.1f}%"
)

col4.metric(
    "💵 Eigenkapitalquote",
    f"{eigenkapital_quote:.1f}%"
)


# ============================================================
# KOSTEN
# ============================================================

st.markdown("---")

st.markdown("### 💸 Hypothekarbelastung")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Aktuelle Zinsen / Jahr",
    f"{effektive_zinsen:,.0f} CHF"
)

col2.metric(
    "Kalk. Zinsen / Jahr",
    f"{kalk_zinsen:,.0f} CHF"
)

col3.metric(
    "Amortisation / Jahr",
    f"{amortisation:,.0f} CHF"
)

col4.metric(
    "Unterhalt / Jahr",
    f"{unterhaltskosten:,.0f} CHF"
)


# ============================================================
# MONATLICHE BELASTUNG
# ============================================================

st.markdown("### 📅 Monatliche Belastung")

col1, col2 = st.columns(2)

with col1:

    st.info(
        f"""
        **Aktuelle Belastung**

        **CHF {effektive_monatsbelastung:,.0f} / Monat**

        Bei einem Zinssatz von {zinssatz:.2f} %
        """
    )

with col2:

    st.warning(
        f"""
        **Kalkulatorische Belastung**

        **CHF {kalk_monatsbelastung:,.0f} / Monat**

        Bei einem kalkulatorischen Zinssatz von
        {kalk_zinssatz:.2f} %
        """
    )


# ============================================================
# TRAGBARKEIT
# ============================================================

st.markdown("---")

st.markdown("### 🧮 Tragbarkeitsrechnung")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Brutto-Jahreseinkommen",
    f"{gesamteinkommen:,.0f} CHF"
)

col2.metric(
    "Kalk. Jahresbelastung",
    f"{kalk_jahresbelastung:,.0f} CHF"
)

col3.metric(
    "Tragbarkeitsquote",
    f"{tragbarkeit:.1f}%"
)


# ============================================================
# TRAGBARKEITSSTATUS
# ============================================================

if tragbarkeit <= 33:

    st.success(
        f"✅ Tragbarkeit ist mit {tragbarkeit:.1f}% "
        "unter der üblichen 33%-Grenze."
    )

elif tragbarkeit <= 40:

    st.warning(
        f"⚠️ Tragbarkeit liegt bei {tragbarkeit:.1f}%. "
        "Sie liegt über der üblichen 33%-Grenze."
    )

else:

    st.error(
        f"❌ Tragbarkeit liegt bei {tragbarkeit:.1f}% "
        "und damit deutlich über der üblichen 33%-Grenze."
    )


# ============================================================
# PROGRESS BAR
# ============================================================

st.markdown("### 📊 Tragbarkeit")

progress = min(
    tragbarkeit / 33,
    1
)

st.progress(
    progress
)

st.caption(
    f"{tragbarkeit:.1f}% von 33% "
    "maximaler Ziel-Tragbarkeit"
)


# ============================================================
# ZUSAMMENFASSUNG
# ============================================================

st.markdown("---")

st.markdown("### 📋 Zusammenfassung")

summary = pd.DataFrame({

    "Position": [

        "Immobilienwert",
        "Eigenkapital",
        "Hypothek",
        "Belehnung",
        "Aktueller Zinssatz",
        "Kalkulatorischer Zinssatz",
        "Aktuelle Zinsen",
        "Kalkulatorische Zinsen",
        "Amortisation",
        "Unterhalt",
        "Aktuelle Jahresbelastung",
        "Kalkulatorische Jahresbelastung",
        "Aktuelle Monatsbelastung",
        "Kalkulatorische Monatsbelastung",
        "Tragbarkeitsquote"
    ],

    "Wert": [

        f"{immobilienwert:,.0f} CHF",
        f"{eigenkapital:,.0f} CHF",
        f"{hypothek:,.0f} CHF",
        f"{belehnung:.1f} %",
        f"{zinssatz:.2f} %",
        f"{kalk_zinssatz:.2f} %",
        f"{effektive_zinsen:,.0f} CHF",
        f"{kalk_zinsen:,.0f} CHF",
        f"{amortisation:,.0f} CHF",
        f"{unterhaltskosten:,.0f} CHF",
        f"{effektive_jahresbelastung:,.0f} CHF",
        f"{kalk_jahresbelastung:,.0f} CHF",
        f"{effektive_monatsbelastung:,.0f} CHF",
        f"{kalk_monatsbelastung:,.0f} CHF",
        f"{tragbarkeit:.1f} %"
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SZENARIO SPEICHERN
# ============================================================

st.markdown("---")

st.markdown("### 💾 Szenario speichern")

scenario_name = st.text_input(
    "Name des Szenarios",
    value=f"Szenario {datetime.now().strftime('%Y-%m-%d')}"
)


if st.button(
    "💾 Hypothek-Szenario speichern",
    type="primary"
):

    scenario = pd.DataFrame([{

        "Datum": datetime.now(),

        "Szenario": scenario_name,

        "Immobilienwert": immobilienwert,

        "Eigenkapital": eigenkapital,

        "Hypothek": hypothek,

        "Belehnung": belehnung,

        "Zinssatz": zinssatz,

        "Kalk_Zinssatz": kalk_zinssatz,

        "Amortisation": amortisation,

        "Unterhalt": unterhaltskosten,

        "Jahreseinkommen": gesamteinkommen,

        "Jahresbelastung_kalk": kalk_jahresbelastung,

        "Monatsbelastung_kalk": kalk_monatsbelastung,

        "Tragbarkeit": tragbarkeit
    }])


    if os.path.exists(DATA_FILE):

        old_data = pd.read_csv(
            DATA_FILE
        )

        data = pd.concat(
            [
                old_data,
                scenario
            ],
            ignore_index=True
        )

    else:

        data = scenario


    data.to_csv(
        DATA_FILE,
        index=False
    )

    st.success(
        "🏠 Hypothek-Szenario gespeichert!"
    )

    st.rerun()


# ============================================================
# HISTORISCHE SZENARIEN
# ============================================================

if os.path.exists(DATA_FILE):

    history = pd.read_csv(
        DATA_FILE
    )

    if not history.empty:

        st.markdown("---")

        st.markdown(
            "### 🗂️ Gespeicherte Szenarien"
        )

        st.dataframe(
            history.sort_values(
                "Datum",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # SZENARIO LÖSCHEN
        # ====================================================

        scenario_list = history[
            "Szenario"
        ].tolist()

        selected_scenario = st.selectbox(
            "Szenario löschen",
            scenario_list
        )

        if st.button(
            "❌ Ausgewähltes Szenario löschen"
        ):

            history = history[
                history["Szenario"]
                != selected_scenario
            ]

            history.to_csv(
                DATA_FILE,
                index=False
            )

            st.success(
                f"Szenario '{selected_scenario}' gelöscht."
            )

            st.rerun()