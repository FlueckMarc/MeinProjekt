import streamlit as st
import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import date

# =========================================================
# SEITENKONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Depot",
    page_icon="📈",
    layout="wide"
)

# =========================================================
# DATEIEN
# =========================================================

BASE_DIR = Path(__file__).parent.parent

HISTORIE_FILE = BASE_DIR / "depot_historie.csv"
FIND_FILE = BASE_DIR / "findependent_historie.csv"
AKTUELL_FILE = BASE_DIR / "depot_aktuell.csv"
FONDS_FILE = BASE_DIR / "fonds_historie.csv"


# =========================================================
# DEPOTPOSITIONEN
# =========================================================

positionen = [

    # =====================================================
    # SWISSQUOTE
    # =====================================================

    {
        "Depot": "Swissquote",
        "Name": "ABB",
        "Ticker": "ABBN.SW",
        "Anteile": 40,
        "Einstand": 25.09,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Accelleron",
        "Ticker": "ACLN.SW",
        "Anteile": 2,
        "Einstand": 36.48,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Novartis",
        "Ticker": "NOVN.SW",
        "Anteile": 25,
        "Einstand": 84.00,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Roche",
        "Ticker": "ROG.SW",
        "Anteile": 7,
        "Einstand": 311.15,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Sandoz",
        "Ticker": "SDZ.SW",
        "Anteile": 5,
        "Einstand": 31.80,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Nestlé",
        "Ticker": "NESN.SW",
        "Anteile": 20,
        "Einstand": 105.00,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Swiss Life",
        "Ticker": "SLHN.SW",
        "Anteile": 10,
        "Einstand": 415.40,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Zurich",
        "Ticker": "ZURN.SW",
        "Anteile": 10,
        "Einstand": 374.80,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Estée Lauder",
        "Ticker": "EL",
        "Anteile": 10,
        "Einstand": 258.92,
        "Währung": "USD"
    },

    {
        "Depot": "Swissquote",
        "Name": "Visa",
        "Ticker": "V",
        "Anteile": 11,
        "Einstand": 202.11,
        "Währung": "USD"
    },

    {
        "Depot": "Swissquote",
        "Name": "SAP",
        "Ticker": "SAP",
        "Anteile": 25,
        "Einstand": 131.15,
        "Währung": "EUR"
    },

    {
        "Depot": "Swissquote",
        "Name": "Salesforce",
        "Ticker": "CRM",
        "Anteile": 10,
        "Einstand": 238.85,
        "Währung": "USD"
    },

    {
        "Depot": "Swissquote",
        "Name": "Ballard Power",
        "Ticker": "BLDP",
        "Anteile": 25,
        "Einstand": 38.46,
        "Währung": "USD"
    },

    {
        "Depot": "Swissquote",
        "Name": "HIVE",
        "Ticker": "HIVE",
        "Anteile": 75,
        "Einstand": 2.00,
        "Währung": "USD"
    },

    {
        "Depot": "Swissquote",
        "Name": "Leclanché",
        "Ticker": "LECN.SW",
        "Anteile": 400,
        "Einstand": 1.02,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Leclanché",
        "Ticker": "LECN.SW",
        "Anteile": 600,
        "Einstand": 0.14,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Leclanché",
        "Ticker": "LECN.SW",
        "Anteile": 500,
        "Einstand": 0.10,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Nvidia",
        "Ticker": "NVDA",
        "Anteile": 25,
        "Einstand": 150.76,
        "Währung": "USD"
    },

    {
        "Depot": "Swissquote",
        "Name": "Robotics & AI",
        "Ticker": "ROBTTQ",
        "Anteile": 10,
        "Einstand": 165.67,
        "Währung": "USD"
    },


    # =====================================================
    # HYPOTHEKARBANK
    # =====================================================

    {
        "Depot": "Hypi",
        "Name": "Swiss Re",
        "Ticker": "SREN.SW",
        "Anteile": 10,
        "Einstand": 73.20,
        "Währung": "CHF"
    },

    {
        "Depot": "Hypi",
        "Name": "UBS",
        "Ticker": "UBSG.SW",
        "Anteile": 100,
        "Einstand": 11.66,
        "Währung": "CHF"
    },

    {
        "Depot": "Hypi",
         "Name": "Hypothekarbank Lenzburg",
         "Ticker": "HBLN.SW",
         "Anteile": 4,
         "Einstand": 4240.00,
         "Währung": "CHF"
    },

    {
        "Depot": "Hypi",
        "Name": "Vale",
        "Ticker": "VALE",
        "Anteile": 140,
        "Einstand": 34.77,
        "Währung": "USD"
    }
]


# =========================================================
# HILFSFUNKTIONEN
# =========================================================

def format_chf(wert):
    return f"CHF {wert:,.0f}".replace(",", "'")


def format_percent(wert):
    return f"{wert:+.2f} %"


# =========================================================
# KURS LADEN
# =========================================================

def lade_kurs(ticker):

    try:

        data = yf.Ticker(ticker).history(
            period="5d",
            auto_adjust=False
        )

        if data.empty:
            return None

        close = data["Close"].dropna()

        if close.empty:
            return None

        return float(close.iloc[-1])

    except Exception:

        return None


# =========================================================
# WECHSELKURS
# =========================================================

def lade_wechselkurs(von):

    if von == "CHF":
        return 1.0

    ticker = f"{von}CHF=X"

    return lade_kurs(ticker)


# =========================================================
# DEPOT AKTUALISIEREN
# =========================================================

@st.cache_data(ttl=300)
def aktualisiere_depot():

    ergebnisse = []

    waehrungen = {
        "CHF": 1.0
    }

    for waehrung in [
        "USD",
        "EUR",
        "GBP",
        "CAD"
    ]:

        kurs = lade_wechselkurs(
            waehrung
        )

        if kurs is not None:

            waehrungen[waehrung] = kurs


    for pos in positionen:

        kurs = lade_kurs(
            pos["Ticker"]
        )

        if kurs is None:

            kurs = 0.0


        wechselkurs = waehrungen.get(
            pos["Währung"],
            1.0
        )


        wert_original = (
            pos["Anteile"]
            * kurs
        )


        wert_chf = (
            wert_original
            * wechselkurs
        )


        einstand_original = (
            pos["Anteile"]
            * pos["Einstand"]
        )


        einstand_chf = (
            einstand_original
            * wechselkurs
        )


        gewinn = (
            wert_chf
            - einstand_chf
        )


        gewinn_prozent = (

            gewinn
            / einstand_chf
            * 100

            if einstand_chf != 0
            else 0
        )


        ergebnisse.append({

            "Depot": pos["Depot"],

            "Name": pos["Name"],

            "Ticker": pos["Ticker"],

            "Anteile": pos["Anteile"],

            "Einstand": pos["Einstand"],

            "Kurs": kurs,

            "Währung": pos["Währung"],

            "FX": wechselkurs,

            "Wert Original":
                wert_original,

            "Wert CHF":
                wert_chf,

            "Gewinn CHF":
                gewinn,

            "Gewinn %":
                gewinn_prozent
        })


    return (
        pd.DataFrame(ergebnisse),
        waehrungen
    )


# =========================================================
# DEPOTHISTORIE
# =========================================================

def lade_historie():

    if HISTORIE_FILE.exists():

        try:

            df = pd.read_csv(
                HISTORIE_FILE
            )

            if not df.empty:

                df["Datum"] = pd.to_datetime(
                    df["Datum"]
                )

                return df

        except Exception:

            pass


    return pd.DataFrame(
        columns=[
            "Datum",
            "Depotwert",
            "Einzahlung"
        ]
    )


# =========================================================
# HISTORIE SPEICHERN
# =========================================================

def speichere_historie(
    depotwert,
    einzahlung=0,
    datum=None
):

    df = lade_historie()

    if datum is None:

        datum = pd.Timestamp.now().normalize()

    else:

        datum = pd.to_datetime(
            datum
        ).normalize()


    neuer_eintrag = pd.DataFrame({

        "Datum": [
            datum
        ],

        "Depotwert": [
            float(depotwert)
        ],

        "Einzahlung": [
            float(einzahlung)
        ]
    })


    if not df.empty:

        df = df[
            df["Datum"].dt.normalize()
            != datum
        ]


    df = pd.concat(
        [
            df,
            neuer_eintrag
        ],
        ignore_index=True
    )


    df = df.sort_values(
        "Datum"
    )


    df.to_csv(
        HISTORIE_FILE,
        index=False
    )


# =========================================================
# FINDINDEPENDENT
# =========================================================

def lade_findependent():

    if FIND_FILE.exists():

        try:

            df = pd.read_csv(
                FIND_FILE
            )

            if not df.empty:

                df["Datum"] = pd.to_datetime(
                    df["Datum"]
                )

                return df

        except Exception:

            pass


    return pd.DataFrame(
        columns=[
            "Datum",
            "Wert",
            "Einzahlung"
        ]
    )


# =========================================================
# FINDINDEPENDENT SPEICHERN
# =========================================================

def speichere_findependent(
    datum,
    wert,
    einzahlung
):

    df = lade_findependent()


    neuer_eintrag = pd.DataFrame({

        "Datum": [
            pd.to_datetime(datum)
        ],

        "Wert": [
            float(wert)
        ],

        "Einzahlung": [
            float(einzahlung)
        ]
    })


    df = pd.concat(
        [
            df,
            neuer_eintrag
        ],
        ignore_index=True
    )


    df = df.sort_values(
        "Datum"
    )


    df.to_csv(
        FIND_FILE,
        index=False
    )


# =========================================================
# FONDS HISTORIE
# =========================================================

def lade_fonds():

    if FONDS_FILE.exists():

        try:

            df = pd.read_csv(
                FONDS_FILE
            )

            if not df.empty:

                df["Datum"] = pd.to_datetime(
                    df["Datum"]
                )

                return df

        except Exception:

            pass


    return pd.DataFrame(
        columns=[
            "Datum",
            "UBS",
            "BCV"
        ]
    )


# =========================================================
# FONDS SPEICHERN
# =========================================================

def speichere_fonds(
    datum,
    ubs,
    bcv
):

    df = lade_fonds()


    datum = pd.to_datetime(
        datum
    ).normalize()


    neuer_eintrag = pd.DataFrame({

        "Datum": [
            datum
        ],

        "UBS": [
            float(ubs)
        ],

        "BCV": [
            float(bcv)
        ]
    })


    if not df.empty:

        df = df[
            df["Datum"].dt.normalize()
            != datum
        ]


    df = pd.concat(
        [
            df,
            neuer_eintrag
        ],
        ignore_index=True
    )


    df = df.sort_values(
        "Datum"
    )


    df.to_csv(
        FONDS_FILE,
        index=False
    )


# =========================================================
# TITEL
# =========================================================

st.title("📈 Depot")

st.caption(
    "Automatische Kursaktualisierung und "
    "Performance deines gesamten Depots"
)


# =========================================================
# AKTUALISIEREN
# =========================================================

col1, col2 = st.columns(
    [1, 4]
)


with col1:

    if st.button(
        "🔄 Kurse aktualisieren",
        use_container_width=True
    ):

        aktualisiere_depot.clear()

        st.rerun()


# =========================================================
# KURSE LADEN
# =========================================================

df, wechselkurse = (
    aktualisiere_depot()
)


# =========================================================
# FINDINDEPENDENT
# =========================================================

find_df = lade_findependent()


st.subheader(
    "🤖 Findependent"
)


col1, col2, col3 = st.columns(3)


with col1:

    find_datum = st.date_input(
        "Datum",
        value=date.today(),
        key="find_datum"
    )


with col2:

    if not find_df.empty:

        letzter_find = float(
            find_df["Wert"].iloc[-1]
        )

    else:

        letzter_find = 0.0


    find_wert = st.number_input(
        "Aktueller Wert",
        min_value=0.0,
        max_value=10_000_000.0,
        value=float(letzter_find),
        step=100.0,
        key="find_wert"
    )


with col3:

    find_einzahlung = st.number_input(
        "Neue Einzahlung",
        min_value=0.0,
        max_value=10_000_000.0,
        value=0.0,
        step=100.0,
        key="find_einzahlung"
    )


if st.button(
    "💾 Findependent speichern"
):

    speichere_findependent(
        find_datum,
        find_wert,
        find_einzahlung
    )

    st.success(
        "Findependent-Wert gespeichert."
    )

    st.rerun()


# =========================================================
# AKTUELLER FINDINDEPENDENT WERT
# =========================================================

if not find_df.empty:

    findependent_wert = float(
        find_df["Wert"].iloc[-1]
    )

else:

    findependent_wert = 0.0


# =========================================================
# DEPOTWERTE
# =========================================================

depotwerte = (
    df.groupby("Depot")["Wert CHF"]
    .sum()
)


swissquote = float(
    depotwerte.get(
        "Swissquote",
        0.0
    )
)


hypi = float(
    depotwerte.get(
        "Hypi",
        0.0
    )
)


# =========================================================
# UBS / BCV FONDS
# =========================================================

fonds_df = lade_fonds()


if not fonds_df.empty:

    letzter_ubs = float(
        fonds_df["UBS"].iloc[-1]
    )

    letzter_bcv = float(
        fonds_df["BCV"].iloc[-1]
    )

else:

    letzter_ubs = 0.0
    letzter_bcv = 0.0


st.subheader(
    "🏦 Fonds"
)


col1, col2 = st.columns(2)


with col1:

    ubs_fonds = st.number_input(
        "UBS Fonds – Gesamtwert CHF",
        min_value=0.0,
        max_value=10_000_000.0,
        value=float(letzter_ubs),
        step=1000.0,
        key="ubs_fonds"
    )


with col2:

    bcv_fonds = st.number_input(
        "BCV Fonds – Gesamtwert CHF",
        min_value=0.0,
        max_value=10_000_000.0,
        value=float(letzter_bcv),
        step=1000.0,
        key="bcv_fonds"
    )


if st.button(
    "💾 Fondswerte speichern"
):

    speichere_fonds(
        date.today(),
        ubs_fonds,
        bcv_fonds
    )

    st.success(
        "UBS- und BCV-Werte gespeichert."
    )

    st.rerun()


# =========================================================
# GESAMTDEPOT
# =========================================================

gesamtdepot = (

    swissquote
    + hypi
    + ubs_fonds
    + bcv_fonds
    + findependent_wert
)


# =========================================================
# DEPOTÜBERSICHT
# =========================================================

st.divider()

st.subheader(
    "💰 Depotübersicht"
)


c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    st.metric(
        "Swissquote",
        format_chf(swissquote)
    )


with c2:

    st.metric(
        "Hypi",
        format_chf(hypi)
    )


with c3:

    st.metric(
        "UBS",
        format_chf(ubs_fonds)
    )


with c4:

    st.metric(
        "BCV",
        format_chf(bcv_fonds)
    )


with c5:

    st.metric(
        "Findependent",
        format_chf(findependent_wert)
    )


st.divider()


st.metric(
    "💰 GESAMTDEPOT",
    format_chf(gesamtdepot)
)


# =========================================================
# AKTUELLEN DEPOTWERT SPEICHERN
# =========================================================

speichere_historie(
    gesamtdepot,
    0
)


# =========================================================
# EINZAHLUNGEN
# =========================================================

st.subheader(
    "💵 Einzahlung erfassen"
)


col1, col2 = st.columns(2)


with col1:

    einzahlung_datum = st.date_input(
        "Datum der Einzahlung",
        value=date.today(),
        key="einzahlung_datum"
    )


with col2:

    einzahlung = st.number_input(
        "Einzahlung CHF",
        min_value=0.0,
        max_value=10_000_000.0,
        value=0.0,
        step=100.0,
        key="einzahlung"
    )


if st.button(
    "➕ Einzahlung speichern"
):

    if einzahlung > 0:

        speichere_historie(
            gesamtdepot,
            einzahlung,
            einzahlung_datum
        )

        st.success(
            "Einzahlung gespeichert."
        )

        st.rerun()


# =========================================================
# PERFORMANCE
# =========================================================

st.divider()

st.subheader(
    "📊 Performance"
)


hist = lade_historie()


if len(hist) >= 2:

    hist = hist.sort_values(
        "Datum"
    )


    heute = hist["Datum"].max()


    zeitraum = st.radio(
        "Zeitraum",
        [
            "Woche",
            "Monat",
            "Jahr",
            "YTD"
        ],
        horizontal=True,
        index=1
    )


    if zeitraum == "Woche":

        startdatum = (
            heute
            - pd.Timedelta(days=7)
        )

    elif zeitraum == "Monat":

        startdatum = (
            heute
            - pd.Timedelta(days=30)
        )

    elif zeitraum == "Jahr":

        startdatum = (
            heute
            - pd.Timedelta(days=365)
        )

    else:

        startdatum = pd.Timestamp(
            year=heute.year,
            month=1,
            day=1
        )


    periode = hist[
        hist["Datum"] >= startdatum
    ].copy()


    if len(periode) >= 2:

        startwert = float(
            periode["Depotwert"].iloc[0]
        )


        endwert = float(
            periode["Depotwert"].iloc[-1]
        )


        einzahlungen = float(
            periode["Einzahlung"].sum()
        )


        echter_gewinn = (
            endwert
            - startwert
            - einzahlungen
        )


        basis = (
            startwert
            + einzahlungen
        )


        performance_prozent = (

            echter_gewinn
            / basis
            * 100

            if basis != 0
            else 0
        )


        c1, c2, c3 = st.columns(3)


        with c1:

            st.metric(
                "Depotwert",
                format_chf(endwert)
            )


        with c2:

            st.metric(
                "Einzahlungen",
                format_chf(einzahlungen)
            )


        with c3:

            st.metric(
                "Kurs-/Wertentwicklung",
                format_chf(echter_gewinn),
                format_percent(
                    performance_prozent
                )
            )


        # =================================================
        # PERFORMANCE GRAFIK
        # =================================================

        chart_df = periode[
            [
                "Datum",
                "Depotwert"
            ]
        ].copy()


        chart_df = chart_df.set_index(
            "Datum"
        )


        st.line_chart(
            chart_df,
            y="Depotwert",
            use_container_width=True
        )


    else:

        st.info(
            "Für diesen Zeitraum sind noch "
            "nicht genügend historische Werte vorhanden."
        )


else:

    st.info(
        "Die Performance-Historie wird automatisch "
        "aufgebaut. Öffne die App regelmässig, damit "
        "immer mehr historische Daten entstehen."
    )


# =========================================================
# EINZELPOSITIONEN
# =========================================================

st.divider()

st.subheader(
    "📋 Einzelpositionen"
)


anzeige = df.copy()


anzeige["Kurs"] = anzeige.apply(

    lambda row:
        f"{row['Kurs']:,.2f} "
        f"{row['Währung']}"
        .replace(",", "'"),

    axis=1
)


anzeige["Wert CHF"] = (
    anzeige["Wert CHF"]
    .apply(format_chf)
)


anzeige["Gewinn CHF"] = (
    anzeige["Gewinn CHF"]
    .apply(format_chf)
)


anzeige["Gewinn %"] = (
    anzeige["Gewinn %"]
    .apply(
        lambda x:
        f"{x:+.2f} %"
    )
)


anzeige = anzeige[
    [
        "Depot",
        "Name",
        "Anteile",
        "Kurs",
        "Wert CHF",
        "Gewinn CHF",
        "Gewinn %"
    ]
]


st.dataframe(
    anzeige,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# WECHSELKURSE
# =========================================================

st.divider()

st.subheader(
    "💱 Wechselkurse"
)


fx_data = []


for waehrung, kurs in wechselkurse.items():

    fx_data.append({

        "Währung":
            waehrung,

        "CHF-Kurs":
            kurs
    })


fx_df = pd.DataFrame(
    fx_data
)


fx_df["CHF-Kurs"] = (
    fx_df["CHF-Kurs"]
    .apply(
        lambda x:
        f"{x:.4f}"
    )
)


st.dataframe(
    fx_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# INFO
# =========================================================

with st.expander(
    "ℹ️ Wie wird der Gewinn berechnet?"
):

    st.markdown("""
    ### Berechnung

    Der Depotwert wird aus den aktuellen Kursen und den
    hinterlegten Stückzahlen berechnet.

    Fremdwährungen werden zum aktuellen Wechselkurs in CHF
    umgerechnet.

    **Gewinn/Verlust:**

    `Endwert − Anfangswert − Einzahlungen`

    Dadurch werden zusätzliche Einzahlungen nicht als
    Anlagegewinn betrachtet.

    Beispiel:

    Anfangswert: CHF 180'000

    Einzahlung: CHF 10'000

    Endwert: CHF 195'000

    Tatsächliche Wertentwicklung:

    **CHF 195'000 − CHF 180'000 − CHF 10'000
    = CHF 5'000 Gewinn**

    Die historische Depotentwicklung wird bei den
    Aktualisierungen der App automatisch gespeichert.
    """)


# =========================================================
# AKTUELLER DEPOTWERT FÜR VERMÖGEN / PROGNOSE
# =========================================================

aktuell = pd.DataFrame({

    "Datum": [
        pd.Timestamp.now()
    ],

    "Swissquote": [
        swissquote
    ],

    "Hypi": [
        hypi
    ],

    "UBS": [
        ubs_fonds
    ],

    "BCV": [
        bcv_fonds
    ],

    "Findependent": [
        findependent_wert
    ],

    "Depotwert": [
        gesamtdepot
    ]
})


aktuell.to_csv(
    AKTUELL_FILE,
    index=False
)


# =========================================================
# ABSCHLUSS
# =========================================================

st.divider()

st.caption(
    "Die Marktdaten werden beim Aktualisieren der App "
    "neu abgerufen. Die Kursdaten können je nach Börse "
    "zeitverzögert sein."
)