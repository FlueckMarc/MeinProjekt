import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# ---------------------------------------------------------
# KONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Prognose",
    page_icon="🔮",
    layout="wide"
)

# ---------------------------------------------------------
# DATEN LADEN
# ---------------------------------------------------------

DATA_FILE = Path(__file__).parent.parent / "vermoegensdaten.csv"

try:
    df = pd.read_csv(DATA_FILE)
except Exception:
    st.error("Die Datei 'vermoegensdaten.csv' wurde nicht gefunden.")
    st.stop()

# ---------------------------------------------------------
# DATEN AUFBEREITEN
# ---------------------------------------------------------

df.columns = [str(col).strip() for col in df.columns]

# Erste Spalte = Datum
datum_spalte = df.columns[0]

df[datum_spalte] = pd.to_datetime(df[datum_spalte], errors="coerce")

# Alle numerischen Spalten
numeric_columns = df.select_dtypes(include="number").columns.tolist()

if not numeric_columns:
    st.error("In der CSV wurden keine numerischen Vermögensdaten gefunden.")
    st.stop()

# Gesamtvermögen
df["Gesamtvermögen"] = df[numeric_columns].sum(axis=1)

df = df.dropna(subset=[datum_spalte])
df = df.sort_values(datum_spalte)

aktuelles_vermoegen = float(df["Gesamtvermögen"].iloc[-1])

# ---------------------------------------------------------
# TITEL
# ---------------------------------------------------------

st.title("🔮 Vermögensprognose")
st.caption("Wie entwickelt sich dein Vermögen unter verschiedenen Annahmen?")

st.divider()

# ---------------------------------------------------------
# EINSTELLUNGEN
# ---------------------------------------------------------

st.subheader("⚙️ Deine Annahmen")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Aktuelles Vermögen",
        f"CHF {aktuelles_vermoegen:,.0f}".replace(",", "'")
    )

with col2:
    sparrate = st.number_input(
        "Jährliche Sparrate",
        min_value=0,
        max_value=1_000_000,
        value=30_000,
        step=1_000
    )

with col3:
    rendite = st.slider(
        "Erwartete Rendite",
        min_value=0.0,
        max_value=10.0,
        value=4.0,
        step=0.5
    )

with col4:
    endjahr = st.slider(
        "Prognose bis",
        min_value=2027,
        max_value=2070,
        value=2050,
        step=1
    )

st.divider()

# ---------------------------------------------------------
# WEITERE OPTIONEN
# ---------------------------------------------------------

with st.expander("🔧 Weitere Einstellungen"):

    col1, col2 = st.columns(2)

    with col1:
        inflation = st.slider(
            "Inflation",
            min_value=0.0,
            max_value=5.0,
            value=1.5,
            step=0.1
        )

    with col2:
        sparraten_wachstum = st.slider(
            "Jährliche Erhöhung der Sparrate",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.5
        )

# ---------------------------------------------------------
# PROGNOSE BERECHNEN
# ---------------------------------------------------------

startjahr = pd.Timestamp.now().year

jahre = list(range(startjahr, endjahr + 1))

vermoegen_nominal = []
vermoegen_real = []

wert = aktuelles_vermoegen
sparrate_aktuell = sparrate

for jahr in jahre:

    if jahr == startjahr:
        vermoegen_nominal.append(wert)
        vermoegen_real.append(wert)

    else:
        # Rendite
        wert = wert * (1 + rendite / 100)

        # Sparrate
        wert += sparrate_aktuell

        vermoegen_nominal.append(wert)

        # Kaufkraftbereinigung
        jahre_seit_start = jahr - startjahr
        realwert = wert / ((1 + inflation / 100) ** jahre_seit_start)

        vermoegen_real.append(realwert)

        # Sparrate für nächstes Jahr erhöhen
        sparrate_aktuell *= (1 + sparraten_wachstum / 100)

prognose_df = pd.DataFrame({
    "Jahr": jahre,
    "Nominal": vermoegen_nominal,
    "Real": vermoegen_real
})

# ---------------------------------------------------------
# MEILENSTEINE
# ---------------------------------------------------------

def jahr_fuer_ziel(ziel):
    treffer = prognose_df[prognose_df["Nominal"] >= ziel]

    if len(treffer) > 0:
        return int(treffer.iloc[0]["Jahr"])

    return None


jahr_1mio = jahr_fuer_ziel(1_000_000)
jahr_1_5mio = jahr_fuer_ziel(1_500_000)
jahr_2mio = jahr_fuer_ziel(2_000_000)

# ---------------------------------------------------------
# SZENARIEN
# ---------------------------------------------------------

def berechne_szenario(rendite_szenario):

    werte = []
    wert = aktuelles_vermoegen
    sparrate_szenario = sparrate

    for jahr in jahre:

        if jahr == startjahr:
            werte.append(wert)

        else:
            wert = wert * (1 + rendite_szenario / 100)
            wert += sparrate_szenario

            werte.append(wert)

            sparrate_szenario *= (
                1 + sparraten_wachstum / 100
            )

    return werte


vorsichtig = berechne_szenario(2)
realistisch = berechne_szenario(4)
optimistisch = berechne_szenario(6)

# ---------------------------------------------------------
# KENNZAHLEN
# ---------------------------------------------------------

st.subheader("🎯 Deine Vermögensziele")

col1, col2, col3 = st.columns(3)

with col1:

    if jahr_1mio:
        st.metric(
            "CHF 1 Million",
            str(jahr_1mio)
        )
    else:
        st.metric(
            "CHF 1 Million",
            "nach Prognosezeitraum"
        )

with col2:

    if jahr_1_5mio:
        st.metric(
            "CHF 1.5 Millionen",
            str(jahr_1_5mio)
        )
    else:
        st.metric(
            "CHF 1.5 Millionen",
            "nach Prognosezeitraum"
        )

with col3:

    if jahr_2mio:
        st.metric(
            "CHF 2 Millionen",
            str(jahr_2mio)
        )
    else:
        st.metric(
            "CHF 2 Millionen",
            "nach Prognosezeitraum"
        )

st.divider()

# ---------------------------------------------------------
# ENDVERMÖGEN
# ---------------------------------------------------------

endwert = prognose_df["Nominal"].iloc[-1]
real_endwert = prognose_df["Real"].iloc[-1]

col1, col2 = st.columns(2)

with col1:

    st.metric(
        f"Prognose {endjahr}",
        f"CHF {endwert:,.0f}".replace(",", "'")
    )

with col2:

    st.metric(
        f"Kaufkraft {endjahr}",
        f"CHF {real_endwert:,.0f}".replace(",", "'")
    )

st.divider()

# ---------------------------------------------------------
# GRAFIK
# ---------------------------------------------------------

st.subheader("📈 Vermögensentwicklung")

fig = go.Figure()

# Vorsichtig
fig.add_trace(
    go.Scatter(
        x=jahre,
        y=vorsichtig,
        mode="lines",
        name="Vorsichtig – 2 %"
    )
)

# Realistisch
fig.add_trace(
    go.Scatter(
        x=jahre,
        y=realistisch,
        mode="lines",
        name="Realistisch – 4 %",
        line=dict(width=4)
    )
)

# Optimistisch
fig.add_trace(
    go.Scatter(
        x=jahre,
        y=optimistisch,
        mode="lines",
        name="Optimistisch – 6 %"
    )
)

# Kaufkraft
fig.add_trace(
    go.Scatter(
        x=jahre,
        y=vermoegen_real,
        mode="lines",
        name="Kaufkraftbereinigt",
        line=dict(dash="dot")
    )
)

# Ziel 1 Mio.
fig.add_hline(
    y=1_000_000,
    annotation_text="CHF 1 Mio.",
    annotation_position="top left"
)

# Ziel 2 Mio.
fig.add_hline(
    y=2_000_000,
    annotation_text="CHF 2 Mio.",
    annotation_position="top left"
)

fig.update_layout(
    height=550,
    xaxis_title="Jahr",
    yaxis_title="Vermögen in CHF",
    hovermode="x unified",
    legend_title="Szenario",
    margin=dict(l=20, r=20, t=40, b=20)
)

fig.update_yaxes(
    tickformat=",.0f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# TABELLE
# ---------------------------------------------------------

st.subheader("📊 Jahresübersicht")

tabelle = prognose_df.copy()

tabelle["Nominal"] = tabelle["Nominal"].apply(
    lambda x: f"CHF {x:,.0f}".replace(",", "'")
)

tabelle["Real"] = tabelle["Real"].apply(
    lambda x: f"CHF {x:,.0f}".replace(",", "'")
)

st.dataframe(
    tabelle,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# INFO
# ---------------------------------------------------------

st.divider()

st.caption(
    "Die Prognose ist eine Modellrechnung und keine Anlageberatung. "
    "Die tatsächliche Vermögensentwicklung kann deutlich abweichen."
)