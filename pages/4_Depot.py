import streamlit as st
import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import date
import requests
import re


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
# NAVIGATION
# =========================================================

st.markdown(
    """
    <style>

    .nav-container {
        display: flex;
        gap: 18px;
        align-items: center;
        margin-top: -10px;
        margin-bottom: 18px;
        font-size: 0.88rem;
    }

    .nav-container a {
        text-decoration: none;
        color: inherit;
        opacity: 0.65;
    }

    .nav-container a:hover {
        opacity: 1;
    }

    .nav-current {
        font-weight: 600;
        opacity: 1 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    st.page_link(
        "app.py",
        label="Übersicht"
    )

with nav2:
    st.page_link(
        "pages/prognose.py",
        label="🔮 Prognose"
    )

with nav3:
    st.page_link(
        "pages/hypothek.py",
        label="🏠 Hypothek"
    )

with nav4:
    st.page_link(
        "pages/budget.py",
        label="💰 Budget"
    )


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
# UBS FONDS
# =========================================================

ubs_fonds = [

    {
        "Valor": "52700098",
        "ISIN": "CH0527000985",
        "Name": "VVA - Corporate Bonds F",
        "Anteile": 75,
        "Währung": "CHF"
    },

    {
        "Valor": "52700097",
        "ISIN": "CH0527000977",
        "Name": "VVA - Global Bonds F",
        "Anteile": 72,
        "Währung": "CHF"
    },

    {
        "Valor": "21501769",
        "ISIN": "CH0215017697",
        "Name": "UBS Equity Fund Mid Caps Switzerland F",
        "Anteile": 0.914,
        "Währung": "CHF"
    },

    {
        "Valor": "841044",
        "ISIN": "CH0008410448",
        "Name": "VVA - Aktien Schweiz F",
        "Anteile": 65,
        "Währung": "CHF"
    },

    {
        "Valor": "51789838",
        "ISIN": "LU2099998382",
        "Name": "Focused SICAV Equity Overlay II CHF",
        "Anteile": 71,
        "Währung": "CHF"
    },

    {
        "Valor": "28650087",
        "ISIN": "IE00BYM11H29",
        "Name": "UBS MSCI ACWI SF UCITS ETF",
        "Anteile": 61,
        "Währung": "USD"
    }
]


# =========================================================
# BCV FONDS
# =========================================================

bcv_fonds = {

    "Valor": "11863121",
    "ISIN": "CH0118631214",
    "Name": "BCV Pension 25 A",
    "Anteile": 361,
    "Währung": "CHF"
}


# =========================================================
# HILFSFUNKTIONEN
# =========================================================

def format_chf(wert):

    if pd.isna(wert):
        return "Nicht verfügbar"

    return (
        f"CHF {wert:,.0f}"
        .replace(",", "'")
    )


def format_percent(wert):

    if pd.isna(wert):
        return "Nicht verfügbar"

    return f"{wert:+.2f} %"


def format_variation(absolut, prozent, waehrung):

    if pd.isna(absolut) or pd.isna(prozent):

        return "Nicht verfügbar"

    return (
        f"{absolut:+.2f} {waehrung} "
        f"({prozent:+.2f} %)"
    )


# =========================================================
# YFINANCE
# =========================================================

def lade_historie_yfinance(ticker):

    try:

        data = yf.Ticker(ticker).history(
            period="10d",
            auto_adjust=False
        )

        if data.empty:
            return None

        data = data["Close"].dropna()

        if data.empty:
            return None

        return data

    except Exception:

        return None


def lade_kurs_yfinance(ticker):

    data = lade_historie_yfinance(ticker)

    if data is None:
        return None

    return float(data.iloc[-1])


# =========================================================
# ROBOTICS & AI
# =========================================================

def lade_robotics_kurs():

    try:

        url = (
            "https://www.finanzen.ch/derivate/"
            "ch0467720428"
        )

        headers = {
            "User-Agent":
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/151.0 Safari/537.36"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return None

        text = response.text

        pattern = r"(\d{2,3}\.\d{2,3})\s*USD"

        matches = re.findall(
            pattern,
            text
        )

        werte = []

        for match in matches:

            try:

                wert = float(match)

                if 50 < wert < 1000:
                    werte.append(wert)

            except Exception:
                pass

        if werte:
            return werte[0]

    except Exception:
        pass

    return None


# =========================================================
# AKTIENKURS
# =========================================================

def lade_aktien_historie(ticker):

    if ticker == "ROBTTQ":

        data = lade_historie_yfinance("ROBTTQ")

        if data is not None:
            return data

        data = lade_historie_yfinance("ROBTTQ.SW")

        if data is not None:
            return data

        kurs = lade_robotics_kurs()

        if kurs is not None:

            return pd.Series(
                [kurs],
                index=[
                    pd.Timestamp.now()
                ]
            )

        return None

    if ticker == "ROG.SW":

        alternativen = [
            "ROG.SW",
            "ROP.SW",
            "RO.SW"
        ]

        for alternative in alternativen:

            data = lade_historie_yfinance(
                alternative
            )

            if data is not None:
                return data

        return None

    return lade_historie_yfinance(
        ticker
    )


# =========================================================
# WECHSELKURS
# =========================================================

def lade_wechselkurs(von):

    if von == "CHF":
        return 1.0

    ticker = f"{von}CHF=X"

    kurs = lade_kurs_yfinance(
        ticker
    )

    return kurs


# =========================================================
# DEPOT AKTUALISIEREN
# =========================================================

@st.cache_data(ttl=300)
def aktualisiere_depot():

    ergebnisse = []

    waehrungen = {
        "CHF": 1.0
    }

    # -----------------------------------------------------
    # WECHSELKURSE
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # AKTIEN
    # -----------------------------------------------------

    for pos in positionen:

        historische_kurse = (
            lade_aktien_historie(
                pos["Ticker"]
            )
        )

        if (
            historische_kurse is None
            or historische_kurse.empty
        ):

            kurs = float("nan")
            tagesvariation = float("nan")
            tagesvariation_prozent = float("nan")
            wochenvariation = float("nan")
            wochenvariation_prozent = float("nan")

        else:

            kurs = float(
                historische_kurse.iloc[-1]
            )

            if len(historische_kurse) >= 2:

                vortag = float(
                    historische_kurse.iloc[-2]
                )

                tagesvariation = (
                    kurs - vortag
                )

                tagesvariation_prozent = (
                    tagesvariation
                    / vortag
                    * 100
                    if vortag != 0
                    else 0
                )

            else:

                tagesvariation = float("nan")
                tagesvariation_prozent = float("nan")


            if len(historische_kurse) >= 6:

                wochen_start = float(
                    historische_kurse.iloc[-6]
                )

                wochenvariation = (
                    kurs - wochen_start
                )

                wochenvariation_prozent = (
                    wochenvariation
                    / wochen_start
                    * 100
                    if wochen_start != 0
                    else 0
                )

            else:

                wochenvariation = float("nan")
                wochenvariation_prozent = float("nan")


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

            "Tagesvariation":
                tagesvariation,

            "Tagesvariation %":
                tagesvariation_prozent,

            "Wochenvariation":
                wochenvariation,

            "Wochenvariation %":
                wochenvariation_prozent,

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
# FONDS-DATEN VON FINANZEN.CH
# =========================================================

def lade_fondskurs_finanzen(isin):

    try:

        url = (
            "https://www.finanzen.ch/"
            f"fonds/{isin.lower()}"
        )

        headers = {
            "User-Agent":
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/151.0 Safari/537.36"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return None

        text = response.text

        patterns = [

            r"Nettoinventarwert\s*\(NAV\).*?"
            r"(\d[\d'.,]*\d)\s*(?:CHF|USD|EUR)",

            r"aktueller Rücknahmepreis.*?"
            r"(\d[\d'.,]*\d)",

            r'"price"\s*:\s*"?(\
\d[\d.,]*)'

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE |
                re.DOTALL
            )

            if match:

                wert = match.group(1)

                wert = (
                    wert
                    .replace("'", "")
                    .replace(",", "")
                )

                try:

                    return float(wert)

                except Exception:
                    pass

    except Exception:
        pass

    return None


# =========================================================
# BESSERE FONDS-URLS
# =========================================================

def lade_fondskurs(isin):

    # -----------------------------------------------------
    # FINANZEN.CH DIREKT
    # -----------------------------------------------------

    bekannte_urls = {

        "CH0527000985":
            "https://www.finanzen.ch/fonds/"
            "vva-corporate-bonds-f-ch0527000985",

        "CH0527000977":
            "https://www.finanzen.ch/fonds/"
            "vva-global-bonds-f-ch0527000977",

        "CH0215017697":
            "https://www.finanzen.ch/fonds/"
            "ubs-ch-equity-fund-mid-caps-switzerland-f-"
            "ch0215017697",

        "CH0008410448":
            "https://www.finanzen.ch/fonds/"
            "vva-aktien-schweiz-f-ch0008410448",

        "LU2099998382":
            "https://www.finanzen.ch/fonds/"
            "focused-equity-overlay-ii-chff-lu2099998382",

        "IE00BYM11H29":
            "https://www.finanzen.ch/etf/"
            "ubs-msci-acwi-sf-etf-ie00bym11h29",

        "CH0118631214":
            "https://www.finanzen.ch/fonds/"
            "bcv-portfolio-pension-fund-"
            "bcv-pension-25-a-ch0118631214"
    }


    url = bekannte_urls.get(
        isin
    )

    if url is None:
        return None


    try:

        headers = {
            "User-Agent":
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/151.0 Safari/537.36"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return None

        text = response.text


        # -------------------------------------------------
        # NAV
        # -------------------------------------------------

        patterns = [

            r"Nettoinventarwert\s*\(NAV\)"
            r".{0,1000}?"
            r"(\d[\d'.,]*)\s*CHF",

            r"aktueller Rücknahmepreis"
            r".{0,500}?"
            r"(\d[\d'.,]*)",

            r'"price"\s*:\s*"'
            r"(\d[\d.,]*)",

            r'"nav"\s*:\s*"'
            r"(\d[\d.,]*)"
        ]


        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE |
                re.DOTALL
            )

            if match:

                wert = match.group(1)

                wert = (
                    wert
                    .replace("'", "")
                    .replace(",", "")
                )

                try:

                    wert = float(wert)

                    if wert > 0:
                        return wert

                except Exception:
                    continue

    except Exception:
        pass


    return None


# =========================================================
# FONDS AKTUALISIEREN
# =========================================================

@st.cache_data(ttl=1800)
def aktualisiere_fonds():

    ergebnisse = []


    # -----------------------------------------------------
    # UBS
    # -----------------------------------------------------

    for fonds in ubs_fonds:

        kurs = lade_fondskurs(
            fonds["ISIN"]
        )


        if kurs is None:

            wert_original = float("nan")
            wert_chf = float("nan")

        else:

            wert_original = (
                fonds["Anteile"]
                * kurs
            )

            if fonds["Währung"] == "USD":

                fx = lade_wechselkurs(
                    "USD"
                )

                if fx is None:
                    fx = 1.0

            else:

                fx = 1.0


            wert_chf = (
                wert_original
                * fx
            )


        ergebnisse.append({

            "Depot": "UBS",

            "Name": fonds["Name"],

            "Valor": fonds["Valor"],

            "ISIN": fonds["ISIN"],

            "Anteile": fonds["Anteile"],

            "Kurs": kurs,

            "Währung": fonds["Währung"],

            "Wert CHF": wert_chf
        })


    # -----------------------------------------------------
    # BCV
    # -----------------------------------------------------

    kurs = lade_fondskurs(
        bcv_fonds["ISIN"]
    )


    if kurs is None:

        wert_chf = float("nan")

    else:

        wert_chf = (
            bcv_fonds["Anteile"]
            * kurs
        )


    ergebnisse.append({

        "Depot": "BCV",

        "Name": bcv_fonds["Name"],

        "Valor": bcv_fonds["Valor"],

        "ISIN": bcv_fonds["ISIN"],

        "Anteile": bcv_fonds["Anteile"],

        "Kurs": kurs,

        "Währung": "CHF",

        "Wert CHF": wert_chf
    })


    return pd.DataFrame(
        ergebnisse
    )


# =========================================================
# DEPOTHISTORIE LADEN
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

                if "Einzahlung Konto" not in df.columns:
                    df["Einzahlung Konto"] = ""

                if "Einzahlung" not in df.columns:
                    df["Einzahlung"] = 0.0

                df["Einzahlung"] = pd.to_numeric(
                    df["Einzahlung"],
                    errors="coerce"
                ).fillna(0.0)

                df["Einzahlung Konto"] = (
                    df["Einzahlung Konto"]
                    .fillna("")
                    .astype(str)
                )

                return df

        except Exception:
            pass


    return pd.DataFrame(
        columns=[
            "Datum",
            "Depotwert",
            "Einzahlung",
            "Einzahlung Konto"
        ]
    )


# =========================================================
# HISTORIE SPEICHERN
# =========================================================

def speichere_historie(
    depotwert,
    einzahlung=0.0,
    datum=None,
    konto=""
):

    df = lade_historie()


    if datum is None:

        datum = pd.Timestamp.now().normalize()

    else:

        datum = pd.to_datetime(
            datum
        ).normalize()


    einzahlung = float(
        einzahlung
    )


    if not df.empty:

        bestehend = df[
            df["Datum"].dt.normalize()
            == datum
        ]

    else:

        bestehend = pd.DataFrame()


    if (
        einzahlung == 0
        and not bestehend.empty
    ):

        alte_einzahlung = float(
            bestehend.iloc[-1]["Einzahlung"]
        )

        altes_konto = str(
            bestehend.iloc[-1]["Einzahlung Konto"]
        )

    else:

        alte_einzahlung = einzahlung
        altes_konto = konto


    if not df.empty:

        df = df[
            df["Datum"].dt.normalize()
            != datum
        ]


    neuer_eintrag = pd.DataFrame({

        "Datum": [datum],

        "Depotwert": [
            float(depotwert)
        ],

        "Einzahlung": [
            alte_einzahlung
        ],

        "Einzahlung Konto": [
            altes_konto
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

if st.button(
    "🔄 Kurse aktualisieren",
    use_container_width=True
):

    aktualisiere_depot.clear()
    aktualisiere_fonds.clear()

    st.rerun()


# =========================================================
# KURSE LADEN
# =========================================================

df, wechselkurse = (
    aktualisiere_depot()
)


fonds_df = (
    aktualisiere_fonds()
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
# FONDSWERTE
# =========================================================

ubs_wert = float(
    fonds_df[
        fonds_df["Depot"] == "UBS"
    ]["Wert CHF"]
    .sum()
)


bcv_wert = float(
    fonds_df[
        fonds_df["Depot"] == "BCV"
    ]["Wert CHF"]
    .sum()
)


# =========================================================
# FONDSÜBERSICHT
# =========================================================

st.divider()

st.subheader(
    "🏦 Fonds"
)


fonds_anzeige = fonds_df.copy()


fonds_anzeige["Kurs"] = (
    fonds_anzeige["Kurs"]
    .apply(
        lambda x:
        "Nicht verfügbar"
        if pd.isna(x)
        else f"{x:,.2f}"
        .replace(",", "'")
    )
)


fonds_anzeige["Wert CHF"] = (
    fonds_anzeige["Wert CHF"]
    .apply(
        lambda x:
        "Nicht verfügbar"
        if pd.isna(x)
        else format_chf(x)
    )
)


fonds_anzeige = fonds_anzeige[
    [
        "Depot",
        "Name",
        "Valor",
        "ISIN",
        "Anteile",
        "Kurs",
        "Währung",
        "Wert CHF"
    ]
]


st.dataframe(
    fonds_anzeige,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# GESAMTDEPOT
# =========================================================

gesamtdepot = (

    swissquote
    + hypi
    + ubs_wert
    + bcv_wert
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
        format_chf(ubs_wert)
    )


with c4:

    st.metric(
        "BCV",
        format_chf(bcv_wert)
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
    0.0
)


# =========================================================
# EINZAHLUNGEN
# =========================================================

st.subheader(
    "💵 Einzahlung erfassen"
)

col1, col2, col3 = st.columns(3)


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


with col3:

    einzahlung_konto = st.selectbox(
        "Einzahlung auf Konto",
        [
            "Swissquote",
            "Hypi",
            "UBS",
            "BCV",
            "Findependent"
        ],
        key="einzahlung_konto"
    )


if st.button(
    "➕ Einzahlung speichern"
):

    if einzahlung > 0:

        speichere_historie(
            gesamtdepot,
            einzahlung,
            einzahlung_datum,
            einzahlung_konto
        )

        st.success(
            f"Einzahlung von "
            f"{format_chf(einzahlung)} "
            f"auf {einzahlung_konto} gespeichert."
        )

        st.rerun()

    else:

        st.warning(
            "Bitte zuerst einen Einzahlungsbetrag eingeben."
        )


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


        konto_einzahlungen = (
            periode[
                periode["Einzahlung"] > 0
            ]
            .groupby("Einzahlung Konto")[
                "Einzahlung"
            ]
            .sum()
        )


        if not konto_einzahlungen.empty:

            st.markdown(
                "#### 💳 Einzahlungen nach Konto"
            )


            konto_df = (
                konto_einzahlungen
                .reset_index()
            )


            konto_df.columns = [
                "Konto",
                "Einzahlungen CHF"
            ]


            konto_df[
                "Einzahlungen CHF"
            ] = (
                konto_df[
                    "Einzahlungen CHF"
                ]
                .apply(format_chf)
            )


            st.dataframe(
                konto_df,
                use_container_width=True,
                hide_index=True
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


def formatiere_kurs(row):

    kurs = row["Kurs"]

    if pd.isna(kurs):
        return "Nicht verfügbar"

    return (
        f"{kurs:,.2f} "
        f"{row['Währung']}"
        .replace(",", "'")
    )


anzeige["Kurs"] = anzeige.apply(
    formatiere_kurs,
    axis=1
)


anzeige["Heute"] = anzeige.apply(

    lambda row:
    format_variation(
        row["Tagesvariation"],
        row["Tagesvariation %"],
        row["Währung"]
    ),

    axis=1
)


anzeige["1 Woche"] = anzeige.apply(

    lambda row:
    format_variation(
        row["Wochenvariation"],
        row["Wochenvariation %"],
        row["Währung"]
    ),

    axis=1
)


anzeige["Wert CHF"] = (
    anzeige["Wert CHF"]
    .apply(
        lambda x:
        "Nicht verfügbar"
        if pd.isna(x)
        else format_chf(x)
    )
)


anzeige["Gewinn seit Kauf"] = (
    anzeige["Gewinn CHF"]
    .apply(
        lambda x:
        "Nicht verfügbar"
        if pd.isna(x)
        else format_chf(x)
    )
)


anzeige["Gewinn %"] = (
    anzeige["Gewinn %"]
    .apply(
        lambda x:
        "Nicht verfügbar"
        if pd.isna(x)
        else f"{x:+.2f} %"
    )
)


anzeige = anzeige[
    [
        "Depot",
        "Name",
        "Anteile",
        "Kurs",
        "Heute",
        "1 Woche",
        "Wert CHF",
        "Gewinn seit Kauf",
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
        ubs_wert
    ],

    "BCV": [
        bcv_wert
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
# INFO
# =========================================================

with st.expander(
    "ℹ️ Berechnung"
):

    st.markdown("""
    ### Gewinn seit Kauf

    Der Gewinn einer Aktienposition wird anhand des
    hinterlegten Einstandspreises berechnet:

    `Aktueller Wert − Einstandswert`

    Die Prozentzahl entspricht der Entwicklung seit Kauf.

    ### Tagesentwicklung

    Die Tagesentwicklung vergleicht den aktuellen Kurs
    mit dem letzten verfügbaren Börsenkurs.

    ### Wochenentwicklung

    Die Wochenentwicklung vergleicht den aktuellen Kurs
    mit dem Kurs vor ungefähr fünf Börsentagen.

    Die Tages- und Wochenentwicklung wird in der
    jeweiligen Originalwährung angezeigt.

    Der Depotwert wird anschliessend mit dem aktuellen
    Wechselkurs in CHF umgerechnet.

    ### Findependent

    Findependent wird weiterhin manuell erfasst.

    ### Fonds

    Die UBS- und BCV-Fonds werden anhand der hinterlegten
    Anzahl Anteile und des jeweils verfügbaren NAV
    automatisch bewertet.
    """)


# =========================================================
# ABSCHLUSS
# =========================================================

st.divider()

st.caption(
    "Aktienkurse werden automatisch aktualisiert. "
    "Fondswerte basieren auf den verfügbaren NAV-Daten "
    "und können gegenüber Börsenkursen zeitlich verzögert sein."
)