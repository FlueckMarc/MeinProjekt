import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# SEITENKONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Prognose",
    page_icon="🔮",
    layout="wide"
)

# =========================================================
# DATEN LADEN
# =========================================================

DATA_FILE = Path(__file__).parent.parent / "vermoegensdaten.csv"

try:
    df = pd.read_csv(DATA_FILE)
except Exception:
    st.error("Die Datei 'vermoegensdaten.csv' wurde nicht gefunden.")
    st.stop()

df.columns = [str(col).strip() for col in df.columns]

# Erste Spalte als Datum
datum_spalte = df.columns[0]
df[datum_spalte] = pd.to_datetime(df[datum_spalte], errors="coerce")

df = df.dropna(subset=[datum_spalte])
df = df.sort_values(datum_spalte)

# =========================================================
# GESAMTVERMÖGEN AUS CSV
# =========================================================

numeric_columns = df.select_dtypes(include="number").columns.tolist()

if not numeric_columns:
    st.error("Keine numerischen Vermögensdaten in der CSV gefunden.")
    st.stop()

df["Gesamtvermögen"] = df[numeric_columns].sum(axis=1)

aktuelles_gesamtvermoegen = float(df["Gesamtvermögen"].iloc[-1])

# =========================================================
# TITEL
# =========================================================

st.title("🔮 Vermögensprognose")
st.caption("Individuelle Prognose für deine verschiedenen Vermögensbereiche")

st.divider()

# =========================================================
# INFO-BEREICH
# =========================================================

with st.expander("ℹ️ Wie wird die Prognose berechnet?"):

    st.markdown("""
    ### Berechnung

    Jeder Vermögensbereich wird **separat** berechnet.

    **Jahreswert:**

    `Vorjahreswert × (1 + Rendite) + jährliche Sparrate`

    Beispiel:

    Ein Bereich mit CHF 100'000 Startvermögen,
    5 % Rendite und CHF 10'000 jährlicher Einzahlung:

    **CHF 100'000 × 1,05 + CHF 10'000 = CHF 115'000**

    Im nächsten Jahr wird mit diesen CHF 115'000 weitergerechnet.

    Die drei Bereiche werden also **nicht mit einer durchschnittlichen
    Rendite vermischt**.

    Erst nachdem jeder Bereich separat berechnet wurde, werden sie zum
    **Gesamtvermögen** addiert.

    Dadurch können beispielsweise Wertschriften mit 5 %,
    Cash mit 1 % und Vorsorge mit 3 % gleichzeitig berücksichtigt werden.

    Die Berechnung ist eine Modellrechnung und keine Garantie für die
    tatsächliche zukünftige Entwicklung.
    """)

# =========================================================
# ALLGEMEINE EINSTELLUNGEN
# =========================================================

st.subheader("⚙️ Allgemeine Einstellungen")

col1, col2 = st.columns(2)

aktuelles_jahr = pd.Timestamp.now().year

with col1:
    endjahr = st.slider(
        "Prognose bis",
        min_value=aktuelles_jahr + 1,
        max_value=2070,
        value=2050,
        step=1
    )

with col2:
    inflation = st.slider(
        "Inflation",
        min_value=0.0,
        max_value=5.0,
        value=1.5,
        step=0.1,
        format="%.1f %%"
    )

st.divider()

# =========================================================
# BEREICHE
# =========================================================

st.subheader("💰 Deine Vermögensbereiche")

st.caption(
    "Passe Startvermögen, jährliche Sparrate und erwartete Rendite "
    "für jeden Bereich individuell an."
)

# ---------------------------------------------------------
# BEREICH 1
# ---------------------------------------------------------

with st.container(border=True):

    st.markdown("### 🟢 Bereich 1")

    col1, col2, col3 = st.columns(3)

    with col1:
        name1 = st.text_input(
            "Bezeichnung",
            value="Wertschriften",
            key="name1"
        )

    with col2:
        start1 = st.number_input(
            "Startvermögen",
            min_value=0,
            max_value=10_000_000,
            value=160_000,
            step=5_000,
            key="start1"
        )

    with col3:
        sparrate1 = st.number_input(
            "Sparrate pro Jahr",
            min_value=0,
            max_value=1_000_000,
            value=20_000,
            step=1_000,
            key="sparrate1"
        )

    rendite1 = st.slider(
        "Erwartete Rendite",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.5,
        format="%.1f %%",
        key="rendite1"
    )

# ---------------------------------------------------------
# BEREICH 2
# ---------------------------------------------------------

with st.container(border=True):

    st.markdown("### 🔵 Bereich 2")

    col1, col2, col3 = st.columns(3)

    with col1:
        name2 = st.text_input(
            "Bezeichnung",
            value="Cash",
            key="name2"
        )

    with col2:
        start2 = st.number_input(
            "Startvermögen",
            min_value=0,
            max_value=10_000_000,
            value=300_000,
            step=5_000,
            key="start2"
        )

    with col3:
        sparrate2 = st.number_input(
            "Sparrate pro Jahr",
            min_value=0,
            max_value=1_000_000,
            value=10_000,
            step=1_000,
            key="sparrate2"
        )

    rendite2 = st.slider(
        "Erwartete Rendite",
        min_value=0.0,
        max_value=15.0,
        value=1.0,
        step=0.5,
        format="%.1f %%",
        key="rendite2"
    )

# ---------------------------------------------------------
# BEREICH 3
# ---------------------------------------------------------

with st.container(border=True):

    st.markdown("### 🟠 Bereich 3")

    col1, col2, col3 = st.columns(3)

    with col1:
        name3 = st.text_input(
            "Bezeichnung",
            value="Vorsorge",
            key="name3"
        )

    with col2:
        start3 = st.number_input(
            "Startvermögen",
            min_value=0,
            max_value=10_000_000,
            value=400_000,
            step=5_000,
            key="start3"
        )

    with col3:
        sparrate3 = st.number_input(
            "Sparrate pro Jahr",
            min_value=0,
            max_value=1_000_000,
            value=15_000,
            step=1_000,
            key="sparrate3"
        )

    rendite3 = st.slider(
        "Erwartete Rendite",
        min_value=0.0,
        max_value=15.0,
        value=3.0,
        step=0.5,
        format="%.1f %%",
        key="rendite3"
    )

# =========================================================
# GESAMT DER STARTWERTE
# =========================================================

start_gesamt = start1 + start2 + start3

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Startvermögen Prognose",
        f"CHF {start_gesamt:,.0f}".replace(",", "'")
    )

with col2:
    st.metric(
        "CSV – aktuelles Gesamtvermögen",
        f"CHF {aktuelles_gesamtvermoegen:,.0f}".replace(",", "'")
    )

# =========================================================
# PROGNOSE BERECHNEN
# =========================================================

jahre = list(range(aktuelles_jahr, endjahr + 1))

werte1 = [float(start1)]
werte2 = [float(start2)]
werte3 = [float(start3)]

for jahr in range(aktuelles_jahr + 1, endjahr + 1):

    neuer_wert1 = (
        werte1[-1] * (1 + rendite1 / 100)
        + sparrate1
    )

    neuer_wert2 = (
        werte2[-1] * (1 + rendite2 / 100)
        + sparrate2
    )

    neuer_wert3 = (
        werte3[-1] * (1 + rendite3 / 100)
        + sparrate3
    )

    werte1.append(neuer_wert1)
    werte2.append(neuer_wert2)
    werte3.append(neuer_wert3)

gesamtwerte = [
    a + b + c
    for a, b, c in zip(werte1, werte2, werte3)
]

# Kaufkraftbereinigung

realwerte = []

for i, wert in enumerate(gesamtwerte):

    realwert = wert / (
        (1 + inflation / 100) ** i
    )

    realwerte.append(realwert)

prognose_df = pd.DataFrame({
    "Jahr": jahre,
    name1: werte1,
    name2: werte2,
    name3: werte3,
    "Gesamtvermögen": gesamtwerte,
    "Kaufkraftbereinigt": realwerte
})

# =========================================================
# ENDWERT
# =========================================================

endwert = gesamtwerte[-1]
real_endwert = realwerte[-1]

st.subheader(f"📅 Prognose {endjahr}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Gesamtvermögen",
        f"CHF {endwert:,.0f}".replace(",", "'")
    )

with col2:
    st.metric(
        "Kaufkraft",
        f"CHF {real_endwert:,.0f}".replace(",", "'")
    )

with col3:
    st.metric(
        "Gesamt Sparrate",
        f"CHF {sparrate1 + sparrate2 + sparrate3:,.0f}".replace(",", "'")
        + " / Jahr"
    )

with col4:
    gewichtete_rendite = (
        (
            start1 * rendite1
            + start2 * rendite2
            + start3 * rendite3
        ) / start_gesamt
        if start_gesamt > 0
        else 0
    )

    st.metric(
        "Startgewichtete Rendite",
        f"{gewichtete_rendite:.2f} %"
    )

# =========================================================
# ZIELE
# =========================================================

st.divider()

st.subheader("🎯 Vermögensziele")


def zieljahr(ziel):

    treffer = prognose_df[
        prognose_df["Gesamtvermögen"] >= ziel
    ]

    if not treffer.empty:
        return int(treffer.iloc[0]["Jahr"])

    return None


jahr_1mio = zieljahr(1_000_000)
jahr_1_5mio = zieljahr(1_500_000)
jahr_2mio = zieljahr(2_000_000)

col1, col2, col3 = st.columns(3)

with col1:

    if jahr_1mio:
        st.metric("CHF 1 Million", jahr_1mio)
    else:
        st.metric("CHF 1 Million", "nicht erreicht")

with col2:

    if jahr_1_5mio:
        st.metric("CHF 1,5 Millionen", jahr_1_5mio)
    else:
        st.metric("CHF 1,5 Millionen", "nicht erreicht")

with col3:

    if jahr_2mio:
        st.metric("CHF 2 Millionen", jahr_2mio)
    else:
        st.metric("CHF 2 Millionen", "nicht erreicht")

# =========================================================
# GRAFIK
# =========================================================

st.divider()

st.subheader("📈 Vermögensentwicklung")

fig = go.Figure()

# Bereich 1
fig.add_trace(
    go.Scatter(
        x=jahre,
        y=werte1,
        mode="lines",
        name=name1
    )
)

# Bereich 2
fig.add_trace(
    go.Scatter(
        x=jahre,
        y=werte2,
        mode="lines",
        name=name2
    )
)

# Bereich 3
fig.add_trace(
    go.Scatter(
        x=jahre,
        y=werte3,
        mode="lines",
        name=name3
    )
)

# Gesamtvermögen
fig.add_trace(
    go.Scatter(
        x=jahre,
        y=gesamtwerte,
        mode="lines",
        name="Gesamtvermögen",
        line=dict(width=5)
    )
)

# Kaufkraft
fig.add_trace(
    go.Scatter(
        x=jahre,
        y=realwerte,
        mode="lines",
        name="Kaufkraftbereinigt",
        line=dict(dash="dot")
    )
)

# Ziele
fig.add_hline(
    y=1_000_000,
    annotation_text="CHF 1 Mio.",
    annotation_position="top left"
)

fig.add_hline(
    y=2_000_000,
    annotation_text="CHF 2 Mio.",
    annotation_position="top left"
)

fig.update_layout(
    height=600,
    xaxis_title="Jahr",
    yaxis_title="Vermögen in CHF",
    hovermode="x unified",
    legend_title="Bereich",
    margin=dict(
        l=20,
        r=20,
        t=40,
        b=20
    )
)

fig.update_yaxes(
    tickformat=",.0f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# JAHRESÜBERSICHT
# =========================================================

st.subheader("📊 Jahresübersicht")

anzeige_df = prognose_df.copy()

for spalte in anzeige_df.columns[1:]:

    anzeige_df[spalte] = anzeige_df[spalte].apply(
        lambda x: f"CHF {x:,.0f}".replace(",", "'")
    )

st.dataframe(
    anzeige_df,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# ABSCHLUSS
# =========================================================

st.divider()

st.caption(
    "Die Prognose basiert auf den von dir eingegebenen Sparraten "
    "und erwarteten Renditen. Sie dient als Orientierung und stellt "
    "keine Anlageberatung oder Garantie dar."
)