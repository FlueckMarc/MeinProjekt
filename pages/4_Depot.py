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


# =========================================================
# NAVIGATION
# =========================================================

nav1, nav2, nav3 = st.columns(3)

with nav1:
    st.page_link(
        "app.py",
        label="🏠 Übersicht"
    )

with nav2:
    st.page_link(
        "pages/2_Hypothek.py",
        label="🏡 Hypothek"
    )

with nav3:
    st.page_link(
        "pages/3_Prognose.py",
        label="🔮 Prognose"
    )

st.divider()


# =========================================================
# DEPOTPOSITIONEN
# =========================================================

positionen = [

    # -----------------------------------------------------
    # SWISSQUOTE
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # HYPOTHEKARBANK
    # -----------------------------------------------------

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

ubs_fonds_positionen = [

    {
        "Name": "VVA - Corporate Bonds F",
        "Valor": "52'700'098",
        "ISIN": "CH0527000985",
        "Anteile": 75,
        "Währung": "CHF",
        "URL": (
            "https://www.finanzen.ch/fonds/"
            "vva-corporate-bonds-f-ch0527000985"
        )
    },

    {
        "Name": "VVA - Global Bonds F",
        "Valor": "52'700'097",
        "ISIN": "CH0527000977",
        "Anteile": 72,
        "Währung": "CHF",
        "URL": (
            "https://www.finanzen.ch/fonds/"
            "vva-global-bonds-f-ch0527000977"
        )
    },

    {
        "Name": "UBS CH Equity Fund Mid Caps Switzerland F",
        "Valor": "21'501'769",
        "ISIN": "CH0215017697",
        "Anteile": 0.914,
        "Währung": "CHF",
        "URL": (
            "https://www.finanzen.ch/fonds/"
            "ubs-ch-equity-fund-mid-caps-switzerland-f-"
            "ch0215017697"
        )
    },

    {
        "Name": "VVA - Aktien Schweiz F",
        "Valor": "841'044",
        "ISIN": "CH0008410448",
        "Anteile": 65,
        "Währung": "CHF",
        "URL": (
            "https://www.finanzen.ch/fonds/"
            "vva-aktien-schweiz-f-ch0008410448"
        )
    },

    {
        "Name": "Focused Equity Overlay II CHF F",
        "Valor": "51'789'838",
        "ISIN": "LU2099998382",
        "Anteile": 71,
        "Währung": "CHF",
        "URL": (
            "https://www.finanzen.ch/fonds/"
            "focused-equity-overlay-ii-chff-lu2099998382"
        )
    },

    {
        "Name": "UBS MSCI ACWI SF ETF",
        "Valor": "28'650'087",
        "ISIN": "IE00BYM11H29",
        "Anteile": 61,
        "Währung": "USD",
        "URL": (
            "https://www.finanzen.ch/etf/"
            "ubs-msci-acwi-sf-etf-ie00bym11h29"
        )
    }
]


# =========================================================
# BCV FONDS
# =========================================================

bcv_fonds = {

    "Name": "BCV Fonds",

    "Valor": "11'863'121",

    "ISIN": "CH0118631214",

    "Anteile": 361,

    "Währung": "CHF",

    "URL": (
        "https://www.finanzen.ch/fonds/"
        "bcv-portfolio-pension-fund-"
        "bcv-pension-25-a-ch0118631214"
    ),

    "OFFICIAL_URL": (
        "https://www.gerifonds.ch/de/iframe/"
        "CH0118631214"
    )
}


# =========================================================
# FORMATIERUNG
# =========================================================

def format_chf(wert):

    if wert is None or pd.isna(wert):
        return "Nicht verfügbar"

    return (
        f"CHF {wert:,.0f}"
        .replace(",", "'")
    )


def format_variation(wert, prozent):

    if (
        wert is None
        or prozent is None
        or pd.isna(wert)
        or pd.isna(prozent)
    ):
        return "Nicht verfügbar"

    return (
        f"{wert:+,.0f} CHF "
        f"({prozent:+.2f} %)"
        .replace(",", "'")
    )


def format_percent(wert):

    if wert is None or pd.isna(wert):
        return "Nicht verfügbar"

    return f"{wert:+.2f} %"


# =========================================================
# YFINANCE
# =========================================================

def lade_kurs_yfinance(ticker):

    try:

        data = yf.Ticker(
            ticker
        ).history(
            period="10d",
            interval="1d",
            auto_adjust=False
        )

        if data.empty:
            return pd.Series(dtype=float)

        close = (
            data["Close"]
            .dropna()
        )

        return close

    except Exception:

        return pd.Series(dtype=float)


# =========================================================
# ROBOTICS & AI
# =========================================================

def lade_robotics_kurs():

    urls = [

        "https://www.finanzen.ch/derivate/ch0467720428",

        "https://www.finanzen.ch/derivate/ch0467720428/kurs"
    ]

    headers = {

        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0 Safari/537.36"
        ),

        "Accept-Language":
            "de-CH,de;q=0.9,en;q=0.8"
    }

    for url in urls:

        try:

            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )

            if response.status_code != 200:
                continue

            text = response.text

            text = (
                text
                .replace("&nbsp;", " ")
                .replace("&#39;", "'")
                .replace("&#x27;", "'")
                .replace("&#x2019;", "'")
            )

            patterns = [

                r"Aktueller Kurs.{0,500}?"
                r"(\d{1,4}(?:[.'’]\d{3})*(?:[.,]\d+)?)\s*USD",

                r"Kurs.{0,500}?"
                r"(\d{1,4}(?:[.'’]\d{3})*(?:[.,]\d+)?)\s*USD",

                r'"last"\s*:\s*"?(.*?)"?[,}]',

                r'"price"\s*:\s*"?(.*?)"?[,}]',

                r'"kurs"\s*:\s*"?(.*?)"?[,}]'
            ]

            for pattern in patterns:

                match = re.search(
                    pattern,
                    text,
                    re.IGNORECASE |
                    re.DOTALL
                )

                if not match:
                    continue

                wert = match.group(1)

                wert = (
                    wert
                    .replace("'", "")
                    .replace("’", "")
                    .replace("USD", "")
                    .strip()
                )

                if "," in wert and "." in wert:

                    if wert.rfind(",") > wert.rfind("."):

                        wert = (
                            wert
                            .replace(".", "")
                            .replace(",", ".")
                        )

                    else:

                        wert = wert.replace(
                            ",",
                            ""
                        )

                elif "," in wert:

                    wert = wert.replace(
                        ",",
                        "."
                    )

                try:

                    wert = float(
                        wert
                    )

                    if 1 < wert < 5000:

                        return pd.Series(
                            [wert]
                        )

                except Exception:
                    continue

        except Exception:
            continue

    return pd.Series(dtype=float)


# =========================================================
# KURSHISTORIE
# =========================================================

def lade_kurshistorie(ticker):

    if ticker == "ROBTTQ":

        return lade_robotics_kurs()


    if ticker == "ROG.SW":

        for alternative in [
            "ROG.SW",
            "ROP.SW",
            "RO.SW"
        ]:

            data = lade_kurs_yfinance(
                alternative
            )

            if not data.empty:
                return data

        return pd.Series(dtype=float)


    return lade_kurs_yfinance(
        ticker
    )


# =========================================================
# WECHSELKURS
# =========================================================

def lade_wechselkurs(von):

    if von == "CHF":
        return 1.0

    try:

        data = yf.Ticker(
            f"{von}CHF=X"
        ).history(
            period="10d",
            interval="1d",
            auto_adjust=False
        )

        if data.empty:
            return None

        close = (
            data["Close"]
            .dropna()
        )

        if close.empty:
            return None

        return float(
            close.iloc[-1]
        )

    except Exception:

        return None


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
        "EUR"
    ]:

        kurs = lade_wechselkurs(
            waehrung
        )

        if kurs is not None:

            waehrungen[
                waehrung
            ] = kurs


    for pos in positionen:

        historie = lade_kurshistorie(
            pos["Ticker"]
        )


        if historie.empty:

            kurs = float("nan")
            vorgaenger = float("nan")
            wochenkurs = float("nan")

        else:

            kurs = float(
                historie.iloc[-1]
            )

            vorgaenger = (
                float(historie.iloc[-2])
                if len(historie) >= 2
                else float("nan")
            )

            wochenkurs = (
                float(historie.iloc[-6])
                if len(historie) >= 6
                else float("nan")
            )


        wechselkurs = waehrungen.get(
            pos["Währung"],
            1.0
        )


        wert_chf = (
            pos["Anteile"]
            * kurs
            * wechselkurs
        )


        einstand_chf = (
            pos["Anteile"]
            * pos["Einstand"]
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


        if not pd.isna(vorgaenger):

            tagesvariation_original = (
                kurs
                - vorgaenger
            )

            tagesvariation_chf = (
                tagesvariation_original
                * pos["Anteile"]
                * wechselkurs
            )

            tagesvariation_prozent = (

                tagesvariation_original
                / vorgaenger
                * 100

                if vorgaenger != 0
                else 0
            )

        else:

            tagesvariation_chf = float("nan")
            tagesvariation_prozent = float("nan")


        if not pd.isna(wochenkurs):

            wochenvariation_original = (
                kurs
                - wochenkurs
            )

            wochenvariation_chf = (
                wochenvariation_original
                * pos["Anteile"]
                * wechselkurs
            )

            wochenvariation_prozent = (

                wochenvariation_original
                / wochenkurs
                * 100

                if wochenkurs != 0
                else 0
            )

        else:

            wochenvariation_chf = float("nan")
            wochenvariation_prozent = float("nan")


        ergebnisse.append({

            "Depot":
                pos["Depot"],

            "Name":
                pos["Name"],

            "Ticker":
                pos["Ticker"],

            "Anteile":
                pos["Anteile"],

            "Einstand":
                pos["Einstand"],

            "Kurs":
                kurs,

            "Währung":
                pos["Währung"],

            "Wert CHF":
                wert_chf,

            "Tagesvariation CHF":
                tagesvariation_chf,

            "Tagesvariation %":
                tagesvariation_prozent,

            "Wochenvariation CHF":
                wochenvariation_chf,

            "Wochenvariation %":
                wochenvariation_prozent,

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
# WEBSEITE LADEN
# =========================================================

def hole_webseite(url):

    headers = {

        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0 Safari/537.36"
        ),

        "Accept-Language":
            "de-CH,de;q=0.9,en-US;q=0.8,en;q=0.7",

        "Cache-Control":
            "no-cache"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        if response.status_code != 200:
            return ""

        return response.text

    except Exception:

        return ""


# =========================================================
# ZAHL BEREINIGEN
# =========================================================

def zahl_bereinigen(wert):

    if wert is None:
        return None

    wert = (
        str(wert)
        .replace("&nbsp;", " ")
        .replace("&#39;", "'")
        .replace("&#x27;", "'")
        .replace("&#x2019;", "'")
        .replace("’", "'")
        .replace("CHF", "")
        .replace("USD", "")
        .replace("EUR", "")
        .replace(" ", "")
        .strip()
    )


    if "'" in wert:

        wert = wert.replace(
            "'",
            ""
        )


    if "," in wert and "." in wert:

        if wert.rfind(",") > wert.rfind("."):

            wert = (
                wert
                .replace(".", "")
                .replace(",", ".")
            )

        else:

            wert = wert.replace(
                ",",
                ""
            )

    elif "," in wert:

        wert = wert.replace(
            ",",
            "."
        )


    try:

        return float(
            wert
        )

    except Exception:

        return None


# =========================================================
# NAV FINANZEN.CH
# =========================================================

def lade_fonds_nav(url):

    text = hole_webseite(
        url
    )

    if not text:
        return None


    text = (
        text
        .replace("&nbsp;", " ")
        .replace("&#39;", "'")
        .replace("&#x27;", "'")
        .replace("&#x2019;", "'")
    )


    patterns = [

        r"Nettoinventarwert\s*\(NAV\)"
        r".{0,1200}?"
        r"([0-9]{1,3}(?:[.'’][0-9]{3})*(?:[.,][0-9]+)?)"
        r"\s*(?:CHF|USD|EUR)",

        r"Nettoinventarwert"
        r".{0,1200}?"
        r"([0-9]{1,3}(?:[.'’][0-9]{3})*(?:[.,][0-9]+)?)"
        r"\s*(?:CHF|USD|EUR)",

        r"Aktueller Rücknahmepreis"
        r".{0,1200}?"
        r"([0-9]{1,3}(?:[.'’][0-9]{3})*(?:[.,][0-9]+)?)",

        r"Rücknahmepreis"
        r".{0,1200}?"
        r"([0-9]{1,3}(?:[.'’][0-9]{3})*(?:[.,][0-9]+)?)"
    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE |
            re.DOTALL
        )

        if match:

            wert = zahl_bereinigen(
                match.group(1)
            )

            if (
                wert is not None
                and wert > 0
            ):

                return wert


    return None


# =========================================================
# BCV NAV OFFIZIELLE GERIFONDS-SEITE
# =========================================================

def lade_bcv_nav_offiziell():

    text = hole_webseite(
        bcv_fonds["OFFICIAL_URL"]
    )

    if not text:
        return None


    text = (
        text
        .replace("&nbsp;", " ")
        .replace("&#39;", "'")
        .replace("&#x27;", "'")
        .replace("&#x2019;", "'")
    )


    patterns = [

        r"NIW.{0,500}?CHF\s*"
        r"([0-9]{1,4}(?:[.,][0-9]+)?)",

        r"NAV.{0,500}?CHF\s*"
        r"([0-9]{1,4}(?:[.,][0-9]+)?)",

        r"CHF\s*"
        r"([0-9]{2,4}[.,][0-9]{2,6})"
    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE |
            re.DOTALL
        )

        if match:

            wert = zahl_bereinigen(
                match.group(1)
            )

            if (
                wert is not None
                and 50 < wert < 500
            ):

                return wert


    return None


# =========================================================
# UBS FONDS
# =========================================================

@st.cache_data(ttl=1800)
def aktualisiere_ubs_fonds():

    ergebnisse = []

    gesamtwert = 0.0

    for fonds in ubs_fonds_positionen:

        nav = lade_fonds_nav(
            fonds["URL"]
        )


        if nav is None:

            wert_chf = float("nan")

        else:

            if fonds["Währung"] == "USD":

                fx = lade_wechselkurs(
                    "USD"
                )

                if fx is None:
                    fx = 1.0

            else:

                fx = 1.0


            wert_chf = (
                fonds["Anteile"]
                * nav
                * fx
            )


            gesamtwert += wert_chf


        ergebnisse.append({

            "Name":
                fonds["Name"],

            "Valor":
                fonds["Valor"],

            "ISIN":
                fonds["ISIN"],

            "Anteile":
                fonds["Anteile"],

            "NAV":
                nav,

            "Währung":
                fonds["Währung"],

            "Wert CHF":
                wert_chf
        })


    return (
        pd.DataFrame(ergebnisse),
        gesamtwert
    )


# =========================================================
# BCV FONDS
# =========================================================

@st.cache_data(ttl=1800)
def aktualisiere_bcv():

    # Versuch 1: finanzen.ch
    nav = lade_fonds_nav(
        bcv_fonds["URL"]
    )


    # Versuch 2: offizielle Gérifonds-Seite
    if nav is None:

        nav = lade_bcv_nav_offiziell()


    if nav is None:

        return (
            None,
            None
        )


    wert = (
        nav
        * bcv_fonds["Anteile"]
    )


    return (
        nav,
        wert
    )


# =========================================================
# HISTORIE
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

        datum = (
            pd.Timestamp.now()
            .normalize()
        )

    else:

        datum = (
            pd.to_datetime(datum)
            .normalize()
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

        alte_einzahlung = float(
            einzahlung
        )

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
    wert
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
            0.0
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

st.title(
    "📈 Depot"
)

st.caption(
    "Automatische Kursaktualisierung, "
    "Fondsbewertung und Performance"
)


# =========================================================
# AKTUALISIEREN
# =========================================================

if st.button(
    "🔄 Kurse aktualisieren"
):

    aktualisiere_depot.clear()
    aktualisiere_ubs_fonds.clear()
    aktualisiere_bcv.clear()

    st.rerun()


# =========================================================
# ALLE DATEN LADEN
# =========================================================

df, wechselkurse = (
    aktualisiere_depot()
)


find_df = (
    lade_findependent()
)


findependent_wert = (

    float(find_df["Wert"].iloc[-1])

    if not find_df.empty

    else 0.0
)


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


ubs_detail, ubs_wert = (
    aktualisiere_ubs_fonds()
)


bcv_nav, bcv_wert = (
    aktualisiere_bcv()
)


ubs_wert_sicher = (

    float(ubs_wert)

    if not pd.isna(ubs_wert)

    else 0.0
)


bcv_wert_sicher = (

    float(bcv_wert)

    if bcv_wert is not None

    else 0.0
)


# =========================================================
# GESAMTDEPOT
# =========================================================

gesamtdepot = (

    swissquote
    + hypi
    + ubs_wert_sicher
    + bcv_wert_sicher
    + findependent_wert
)


# =========================================================
# 1. DEPOTÜBERSICHT
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
        format_chf(ubs_wert_sicher)
    )


with c4:

    st.metric(
        "BCV",
        format_chf(bcv_wert_sicher)
    )


with c5:

    st.metric(
        "Findependent",
        format_chf(findependent_wert)
    )


st.metric(
    "💰 GESAMTDEPOT",
    format_chf(gesamtdepot)
)


# =========================================================
# HISTORIE SPEICHERN
# =========================================================

speichere_historie(
    gesamtdepot,
    0.0
)


# =========================================================
# 2. EINZAHLUNG ERFASSEN
# =========================================================

st.divider()

st.subheader(
    "💵 Einzahlung erfassen"
)


e1, e2, e3 = st.columns(3)


with e1:

    einzahlung_datum = st.date_input(
        "Datum der Einzahlung",
        value=date.today(),
        key="einzahlung_datum"
    )


with e2:

    einzahlung = st.number_input(
        "Einzahlung CHF",
        min_value=0.0,
        max_value=10_000_000.0,
        value=0.0,
        step=100.0,
        key="einzahlung"
    )


with e3:

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
# 3. AKTIEN
# =========================================================

st.divider()

st.subheader(
    "📋 Aktien"
)


# ---------------------------------------------------------
# TOTALS
# ---------------------------------------------------------

total_aktien_wert = (
    df["Wert CHF"]
    .sum()
)


total_tagesvariation = (
    df["Tagesvariation CHF"]
    .sum()
)


total_wochenvariation = (
    df["Wochenvariation CHF"]
    .sum()
)


total_gewinn = (
    df["Gewinn CHF"]
    .sum()
)


total_einstand = (
    total_aktien_wert
    - total_gewinn
)


total_tagesbasis = (
    total_aktien_wert
    - total_tagesvariation
)


total_wochenbasis = (
    total_aktien_wert
    - total_wochenvariation
)


total_tagesprozent = (

    total_tagesvariation
    / total_tagesbasis
    * 100

    if total_tagesbasis != 0

    else 0
)


total_wochenprozent = (

    total_wochenvariation
    / total_wochenbasis
    * 100

    if total_wochenbasis != 0

    else 0
)


total_gewinn_prozent = (

    total_gewinn
    / total_einstand
    * 100

    if total_einstand != 0

    else 0
)


# ---------------------------------------------------------
# AKTIENÜBERSICHT AUF EINER LINIE
# ---------------------------------------------------------

st.markdown(
    f"""
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:flex-start;
        gap:22px;
        padding:8px 2px 16px 2px;
        white-space:nowrap;
    ">

        <div style="flex:1;">
            <div style="
                font-size:0.86rem;
                color:#888;
            ">
                Aktienwert
            </div>

            <div style="
                font-size:1.15rem;
                font-weight:600;
            ">
                {format_chf(total_aktien_wert)}
            </div>
        </div>


        <div style="flex:1;">
            <div style="
                font-size:0.86rem;
                color:#888;
            ">
                Tagesvariation
            </div>

            <div style="
                font-size:1.15rem;
                font-weight:600;
            ">
                {format_variation(
                    total_tagesvariation,
                    total_tagesprozent
                )}
            </div>
        </div>


        <div style="flex:1;">
            <div style="
                font-size:0.86rem;
                color:#888;
            ">
                Wochenentwicklung
            </div>

            <div style="
                font-size:1.15rem;
                font-weight:600;
            ">
                {format_variation(
                    total_wochenvariation,
                    total_wochenprozent
                )}
            </div>
        </div>


        <div style="flex:1;">
            <div style="
                font-size:0.86rem;
                color:#888;
            ">
                Gewinn seit Kauf
            </div>

            <div style="
                font-size:1.15rem;
                font-weight:600;
            ">
                {format_variation(
                    total_gewinn,
                    total_gewinn_prozent
                )}
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# AKTIEN-TABELLE
# ---------------------------------------------------------

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


# KURS WIEDER SICHTBAR
anzeige["Kurs"] = (
    anzeige.apply(
        formatiere_kurs,
        axis=1
    )
)


anzeige["Tagesvariation"] = (
    anzeige.apply(
        lambda row:
        format_variation(
            row["Tagesvariation CHF"],
            row["Tagesvariation %"]
        ),
        axis=1
    )
)


anzeige["Wochenentwicklung"] = (
    anzeige.apply(
        lambda row:
        format_variation(
            row["Wochenvariation CHF"],
            row["Wochenvariation %"]
        ),
        axis=1
    )
)


anzeige["Wert CHF"] = (
    anzeige["Wert CHF"]
    .apply(
        format_chf
    )
)


anzeige["Gewinn CHF"] = (
    anzeige["Gewinn CHF"]
    .apply(
        format_chf
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
        "Tagesvariation",
        "Wochenentwicklung",
        "Wert CHF",
        "Gewinn CHF",
        "Gewinn %"
    ]
]


# TOTAL ALS ERSTE ZEILE

aktien_total_zeile = pd.DataFrame([{

    "Depot":
        "TOTAL",

    "Name":
        "ALLE AKTIEN",

    "Anteile":
        "",

    "Kurs":
        "",

    "Tagesvariation":
        format_variation(
            total_tagesvariation,
            total_tagesprozent
        ),

    "Wochenentwicklung":
        format_variation(
            total_wochenvariation,
            total_wochenprozent
        ),

    "Wert CHF":
        format_chf(
            total_aktien_wert
        ),

    "Gewinn CHF":
        format_chf(
            total_gewinn
        ),

    "Gewinn %":
        f"{total_gewinn_prozent:+.2f} %"
}])


anzeige = pd.concat(
    [
        aktien_total_zeile,
        anzeige
    ],
    ignore_index=True
)


st.dataframe(
    anzeige,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# 4. UBS FONDS
# =========================================================

st.divider()

st.subheader(
    "🏦 UBS Fonds"
)


if not ubs_detail.empty:

    ubs_anzeige = (
        ubs_detail.copy()
    )


    ubs_anzeige["NAV"] = (
        ubs_anzeige["NAV"]
        .apply(
            lambda x:
            "Nicht verfügbar"
            if pd.isna(x)
            else f"{x:,.4f}"
            .replace(",", "'")
        )
    )


    ubs_anzeige["Wert CHF"] = (
        ubs_anzeige["Wert CHF"]
        .apply(
            format_chf
        )
    )


    ubs_total_zeile = pd.DataFrame([{

        "Name":
            "TOTAL UBS FONDS",

        "Valor":
            "",

        "ISIN":
            "",

        "Anteile":
            "",

        "NAV":
            "",

        "Währung":
            "",

        "Wert CHF":
            format_chf(
                ubs_wert_sicher
            )
    }])


    ubs_anzeige = pd.concat(
        [
            ubs_total_zeile,
            ubs_anzeige
        ],
        ignore_index=True
    )


    st.dataframe(
        ubs_anzeige[
            [
                "Name",
                "Valor",
                "ISIN",
                "Anteile",
                "NAV",
                "Währung",
                "Wert CHF"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.error(
        "UBS Fonds konnten nicht aktualisiert werden."
    )


# =========================================================
# 5. BCV FONDS
# =========================================================

st.divider()

st.subheader(
    "🏦 BCV Fonds"
)


if bcv_nav is None:

    bcv_nav_anzeige = (
        "Nicht verfügbar"
    )

else:

    bcv_nav_anzeige = (
        f"CHF {bcv_nav:,.4f}"
        .replace(",", "'")
    )


# ALLES AUF EINER LINIE

st.markdown(
    f"""
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:flex-start;
        gap:24px;
        padding:8px 2px 14px 2px;
        white-space:nowrap;
    ">

        <div style="flex:1;">
            <div style="
                font-size:0.86rem;
                color:#888;
            ">
                ISIN
            </div>

            <div style="
                font-size:1.15rem;
                font-weight:600;
            ">
                {bcv_fonds["ISIN"]}
            </div>
        </div>


        <div style="flex:1;">
            <div style="
                font-size:0.86rem;
                color:#888;
            ">
                Anteile
            </div>

            <div style="
                font-size:1.15rem;
                font-weight:600;
            ">
                {bcv_fonds["Anteile"]}
            </div>
        </div>


        <div style="flex:1;">
            <div style="
                font-size:0.86rem;
                color:#888;
            ">
                Aktueller NAV
            </div>

            <div style="
                font-size:1.15rem;
                font-weight:600;
            ">
                {bcv_nav_anzeige}
            </div>
        </div>


        <div style="flex:1;">
            <div style="
                font-size:0.86rem;
                color:#888;
            ">
                Gesamtwert
            </div>

            <div style="
                font-size:1.15rem;
                font-weight:600;
            ">
                {format_chf(bcv_wert_sicher)}
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


if bcv_nav is None:

    st.warning(
        "Der aktuelle BCV-NAV konnte momentan "
        "nicht automatisch abgerufen werden."
    )


# =========================================================
# 6. FINDINDEPENDENT
# =========================================================

st.divider()

st.subheader(
    "🤖 Findependent"
)


f1, f2 = st.columns(2)


with f1:

    find_datum = st.date_input(
        "Datum",
        value=date.today(),
        key="find_datum"
    )


with f2:

    find_wert = st.number_input(
        "Aktueller Wert",
        min_value=0.0,
        max_value=10_000_000.0,
        value=float(
            findependent_wert
        ),
        step=100.0,
        key="find_wert"
    )


if st.button(
    "💾 Findependent-Wert speichern"
):

    speichere_findependent(
        find_datum,
        find_wert
    )

    st.success(
        "Findependent-Wert gespeichert."
    )

    st.rerun()


st.caption(
    "Einzahlungen auf Findependent werden oben "
    "unter «Einzahlung erfassen» erfasst."
)


# =========================================================
# 7. PERFORMANCE
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


        p1, p2, p3 = st.columns(3)


        with p1:

            st.metric(
                "Depotwert",
                format_chf(endwert)
            )


        with p2:

            st.metric(
                "Einzahlungen",
                format_chf(einzahlungen)
            )


        with p3:

            st.metric(
                "Kurs-/Wertentwicklung",
                format_chf(
                    echter_gewinn
                ),
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


        chart_df = (
            chart_df
            .set_index("Datum")
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
            .groupby(
                "Einzahlung Konto"
            )["Einzahlung"]
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
                .apply(
                    format_chf
                )
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
# 8. WECHSELKURSE
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

    st.markdown(
        """
        ### Gewinn seit Beginn

        Der Gewinn der einzelnen Aktien wird seit dem
        hinterlegten Einstand berechnet:

        **Aktueller Wert − Einstandswert**

        Die **Tagesvariation** zeigt die Veränderung
        gegenüber dem letzten verfügbaren Börsenkurs.

        Die **Wochenentwicklung** zeigt die Veränderung
        gegenüber ungefähr fünf Börsentagen zuvor.

        Die absoluten Tages- und Wochenveränderungen
        werden in CHF berechnet.

        Die Performance des Gesamtdepots berücksichtigt
        zusätzlich die erfassten Einzahlungen.
        """
    )


# =========================================================
# AKTUELLER DEPOTWERT FÜR ÜBERSICHT / PROGNOSE
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
        ubs_wert_sicher
    ],

    "BCV": [
        bcv_wert_sicher
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
    "Aktienkurse werden beim Aktualisieren neu abgerufen. "
    "Die UBS- und BCV-Fonds werden über die hinterlegten "
    "Valor-/ISIN-Daten aktualisiert. Fonds-NAVs können "
    "gegenüber Börsenkursen zeitverzögert sein."
)