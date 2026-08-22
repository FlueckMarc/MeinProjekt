import streamlit as st
import pandas as pd
import yfinance as yf
from pathlib import Path
from datetime import date, datetime, time
from zoneinfo import ZoneInfo
import requests
import re
import html


# =========================================================
# SEITENKONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Depot",
    page_icon="📈",
    layout="wide"
)


# =========================================================
# DARSTELLUNG
# =========================================================

st.markdown(
    """
    <style>

    /* Abschnittsüberschriften etwas kleiner */
    h2 {
        font-size: 1.45rem !important;
    }

    h3 {
        font-size: 1.15rem !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATEIEN
# =========================================================

BASE_DIR = Path(__file__).parent.parent

HISTORIE_FILE = BASE_DIR / "depot_historie.csv"
FIND_FILE = BASE_DIR / "findependent_historie.csv"
AKTUELL_FILE = BASE_DIR / "depot_aktuell.csv"


# =========================================================
# DEPOTPOSITIONEN
# =========================================================

positionen = [

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
        "ISIN": "US92826C8394",
        "Anteile": 11,
        "Einstand": 202.11,
        "Währung": "USD"
    },

    {
        "Depot": "Swissquote",
        "Name": "SAP",
        "Ticker": "SAP",
        "ISIN": "US8030542042",
        "Anteile": 25,
        "Einstand": 131.15,
        "Währung": "USD"
    },

    {
        "Depot": "Swissquote",
        "Name": "Salesforce",
        "Ticker": "CRM",
        "ISIN": "US79466L3024",
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
        "Ticker": "YO0.F",
        "ISIN": "CA4339211035",
        "Anteile": 15,
        "Einstand": 2.61,
        "Währung": "EUR"
    },

    {
        "Depot": "Swissquote",
        "Name": "Leclanché",
        "Ticker": "LECN.SW",
        "ISIN": "CH0110303119",
        "Anteile": 400,
        "Einstand": 1.02,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Leclanché",
        "Ticker": "LECN.SW",
        "ISIN": "CH0110303119",
        "Anteile": 600,
        "Einstand": 0.14,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Leclanché",
        "Ticker": "LECN.SW",
        "ISIN": "CH0110303119",
        "Anteile": 500,
        "Einstand": 0.10,
        "Währung": "CHF"
    },

    {
        "Depot": "Swissquote",
        "Name": "Nvidia",
        "Ticker": "NVDA",
        "ISIN": "US67066G1040",
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
        "ISIN": "CH0244767585",
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

    "OFFICIAL_URLS": [
        "https://www.gerifonds.ch/en/iframe/CH0118631214",
        "https://www.gerifonds.ch/de/iframe/CH0118631214"
    ]
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


def format_chf_total(wert):

    if wert is None or pd.isna(wert):
        return "Nicht verfügbar"

    return (
        f"CHF {wert:,.2f}"
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
        f"{wert:+,.2f} CHF "
        f"({prozent:+.2f} %)"
        .replace(",", "'")
    )


def format_variation_total(wert, prozent):

    if (
        wert is None
        or prozent is None
        or pd.isna(wert)
        or pd.isna(prozent)
    ):
        return "Nicht verfügbar"

    return (
        f"{wert:+,.2f} CHF "
        f"({prozent:+.2f} %)"
        .replace(",", "'")
    )


def format_percent(wert):

    if wert is None or pd.isna(wert):
        return "Nicht verfügbar"

    return f"{wert:+.2f} %"




# =========================================================
# FINANZEN.CH - PRIMÄRE KURSQUELLE FÜR BÖRSENTITEL
# =========================================================

FINANZEN_URLS = {
    "ABBN.SW": ["https://www.finanzen.ch/aktien/abb-aktie"],
    "ACLN.SW": [
        "https://www.finanzen.ch/aktien/accelleron_industries-aktie",
        "https://www.finanzen.ch/aktien/accelleron_industries-aktie-aktie",
    ],
    "NOVN.SW": [
        "https://www.finanzen.ch/aktien/novartis-aktie",
        "https://www.finanzen.ch/aktien/novartis-aktie-aktie",
    ],
    "ROG.SW": ["https://www.finanzen.ch/aktien/roche-aktie"],
    "SDZ.SW": ["https://www.finanzen.ch/aktien/sandoz-aktie"],
    "NESN.SW": ["https://www.finanzen.ch/aktien/nestle-aktie"],
    "SLHN.SW": ["https://www.finanzen.ch/aktien/swiss_life-aktie"],
    "ZURN.SW": ["https://www.finanzen.ch/aktien/zurich-aktie"],
    "EL": ["https://www.finanzen.ch/aktien/estee_lauder-aktie"],
    "V": ["https://www.finanzen.ch/aktien/visa-aktie"],
    "SAP": ["https://www.finanzen.ch/aktien/sap-aktie"],
    "CRM": ["https://www.finanzen.ch/aktien/salesforce-aktie"],
    "BLDP": ["https://www.finanzen.ch/aktien/ballard_power-aktie"],
    "YO0.F": [
        "https://www.finanzen.ch/aktien/hive_digital_technologies-aktie",
        "https://www.finanzen.ch/aktien/hive_blockchain_technologies-aktie",
    ],
    "LECN.SW": ["https://www.finanzen.ch/aktien/leclanche-aktie"],
    "NVDA": ["https://www.finanzen.ch/aktien/nvidia-aktie"],
    "SREN.SW": ["https://www.finanzen.ch/aktien/swiss_re-aktie"],
    "UBSG.SW": ["https://www.finanzen.ch/aktien/ubs-aktie"],
    "HBLN.SW": ["https://www.finanzen.ch/aktien/hypothekarbank_lenzburg-aktie"],
    "VALE": ["https://www.finanzen.ch/aktien/vale-aktie"],
}


def _text_aus_html(raw_html):
    text = html.unescape(raw_html or "")
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _parse_finanzen_zahl(wert):
    if wert is None:
        return None
    wert = str(wert).replace("’", "'").replace(" ", "").strip()
    # Schweizer Tausendertrennzeichen entfernen
    wert = wert.replace("'", "")
    if "," in wert and "." in wert:
        if wert.rfind(",") > wert.rfind("."):
            wert = wert.replace(".", "").replace(",", ".")
        else:
            wert = wert.replace(",", "")
    elif "," in wert:
        wert = wert.replace(",", ".")
    try:
        return float(wert)
    except Exception:
        return None


def lade_kurs_finanzen(ticker, waehrung):
    """
    Primäre Kursquelle für börsengehandelte Titel.
    Liest den 'Aktienkurs ... in <Währung>' und die dazugehörige Kurszeit.
    Rückgabe: (kurs, kurszeit, kursart)
    """
    urls = FINANZEN_URLS.get(ticker, [])
    if not urls:
        return float("nan"), None, "Nicht verfügbar"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0 Safari/537.36"
        ),
        "Accept-Language": "de-CH,de;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
    }

    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code != 200:
                continue
            text = _text_aus_html(r.text)
            if not text:
                continue

            # Möglichst genau den gewünschten Währungsabschnitt verwenden.
            marker = re.search(
                rf"Aktienkurs\s+.+?\s+in\s+{re.escape(waehrung)}\b",
                text,
                flags=re.I,
            )
            if marker:
                abschnitt = text[marker.start(): marker.start() + 2200]
            else:
                # Fallback: Kopfbereich der Seite; dort steht oft
                # '<Kurs> <Währung> ... <Börse>'.
                abschnitt = text[:2200]

            # 1) Bevorzugt: Kurs direkt vor Kurszeit-Block.
            # Typischer Text: '586.00 | 1.60 | 0.27 % Kurszeit ...'
            m = re.search(
                r"([0-9]{1,7}(?:[.'’][0-9]{3})*(?:[.,][0-9]{1,6})?)"
                r"\s*\|\s*[+\-]?[0-9]{1,7}(?:[.'’][0-9]{3})*(?:[.,][0-9]{1,6})?"
                r"\s*\|\s*[+\-]?[0-9]{1,4}(?:[.,][0-9]+)?\s*%"
                r".{0,120}?Kurszeit",
                abschnitt,
                flags=re.I | re.S,
            )

            # 2) Fallback: erste plausible Zahl im Währungsabschnitt.
            if not m:
                m = re.search(
                    r"\b([0-9]{1,7}(?:[.'’][0-9]{3})*(?:[.,][0-9]{1,6})?)\b",
                    abschnitt,
                )

            if not m:
                continue

            kurs = _parse_finanzen_zahl(m.group(1))
            if kurs is None or kurs <= 0:
                continue

            kurszeit = None
            zeit_match = re.search(
                r"Kurszeit\s+(?:(\d{2}\.\d{2}\.\d{4})\s+)?"
                r"(\d{2}:\d{2}(?::\d{2})?)",
                abschnitt,
                flags=re.I,
            )
            if zeit_match:
                datum_txt = zeit_match.group(1)
                zeit_txt = zeit_match.group(2)
                if datum_txt:
                    try:
                        kurszeit = pd.to_datetime(
                            f"{datum_txt} {zeit_txt}",
                            dayfirst=True,
                        )
                    except Exception:
                        kurszeit = None

            return float(kurs), kurszeit, "Finanzen.ch"

        except Exception:
            continue

    return float("nan"), None, "Nicht verfügbar"


# =========================================================
# ROBUSTES YFINANCE
# =========================================================

def _close_serie(data):

    if data is None or data.empty:
        return pd.Series(dtype=float)

    if "Close" not in data.columns:
        return pd.Series(dtype=float)

    close = data["Close"]

    if isinstance(close, pd.DataFrame):

        if close.empty:
            return pd.Series(dtype=float)

        close = close.iloc[:, 0]

    return pd.to_numeric(
        close,
        errors="coerce"
    ).dropna()


def lade_kurs_yfinance(ticker):

    """
    Tageshistorie für Tages-/Wochenvergleiche.
    """

    try:

        data = yf.download(
            ticker,
            period="15d",
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=False
        )

        close = _close_serie(data)

        if not close.empty:
            return close

    except Exception:
        pass

    try:

        data = yf.Ticker(
            ticker
        ).history(
            period="15d",
            interval="1d",
            auto_adjust=False
        )

        return _close_serie(data)

    except Exception:

        return pd.Series(dtype=float)


def lade_aktuellen_kurs_yfinance(ticker, waehrung=None):

    """
    Liefert den aktuellsten sinnvollen Börsenkurs.

    Logik:
    - CH/EUR: laufender Intraday-Kurs; nach 17:30 Schweizer Zeit
      bevorzugt Schlusskurs des heutigen Handelstags.
    - USD: laufender Intraday-Kurs; nach 22:00 Schweizer Zeit
      bevorzugt Schlusskurs des heutigen Handelstags.
    - Falls der Daily-Close für heute noch nicht publiziert ist,
      bleibt der letzte Intraday-Kurs die bessere Quelle.
    - Wochenende/vor Börsenöffnung: letzter verfügbarer Kurs.

    Rückgabe:
        (kurs, kurszeit, kursart)
    """

    obj = yf.Ticker(ticker)
    ch_tz = ZoneInfo("Europe/Zurich")
    jetzt_ch = datetime.now(ch_tz)

    if waehrung == "USD":
        schlusszeit = time(22, 0)
    else:
        schlusszeit = time(17, 30)

    # 1. Letzten Intraday-Kurs holen
    intraday_kurs = float("nan")
    intraday_zeit = None

    for interval, period in [("1m", "5d"), ("5m", "10d"), ("1h", "1mo")]:
        try:
            data = obj.history(
                period=period,
                interval=interval,
                auto_adjust=False,
                prepost=False
            )

            close = _close_serie(data)

            if not close.empty:
                intraday_kurs = float(close.iloc[-1])
                intraday_zeit = pd.to_datetime(close.index[-1])
                break

        except Exception:
            pass

    # 2. Daily-Close holen
    daily = lade_kurs_yfinance(ticker)
    daily_kurs = float("nan")
    daily_zeit = None

    if not daily.empty:
        daily_kurs = float(daily.iloc[-1])
        try:
            daily_zeit = pd.to_datetime(daily.index[-1])
        except Exception:
            daily_zeit = None

    # 3. Nach Börsenschluss nur dann Daily-Close bevorzugen,
    #    wenn er wirklich vom heutigen Schweizer Kalendertag ist.
    ist_werktag = jetzt_ch.weekday() < 5
    nach_schluss = ist_werktag and jetzt_ch.time() >= schlusszeit

    if nach_schluss and daily_zeit is not None and not pd.isna(daily_kurs):
        try:
            daily_tag = pd.to_datetime(daily_zeit).date()
            if daily_tag == jetzt_ch.date():
                return daily_kurs, daily_zeit, "Schlusskurs"
        except Exception:
            pass

    # 4. Sonst Intraday bevorzugen. Das ist während des Handels
    #    und direkt nach Handelsschluss meist aktueller als Daily.
    if not pd.isna(intraday_kurs):
        kursart = "Laufender Kurs"

        if intraday_zeit is not None:
            try:
                intraday_tag = pd.to_datetime(intraday_zeit).date()
                if (
                    intraday_tag < jetzt_ch.date()
                    or nach_schluss
                    or not ist_werktag
                ):
                    kursart = "Letzter Kurs"
            except Exception:
                pass

        return intraday_kurs, intraday_zeit, kursart

    # 5. fast_info als Fallback
    try:
        info = obj.fast_info

        for key in ["last_price", "regular_market_price"]:
            try:
                wert = info[key]
            except Exception:
                wert = getattr(info, key, None)

            if wert is not None:
                wert = float(wert)
                if wert > 0:
                    return wert, None, "Letzter Kurs"

    except Exception:
        pass

    # 6. Daily als letzter Fallback
    if not pd.isna(daily_kurs):
        return daily_kurs, daily_zeit, "Schlusskurs"

    return float("nan"), None, "Nicht verfügbar"


# =========================================================
# ROBOTICS & AI
# =========================================================

def lade_robotics_kurs():

    urls = [
        "https://www.finanzen.ch/derivate/ch0467720428",
        "https://www.six-structured-products.com/de/zertifikat/"
        "robttq-leon-c-z-CH0467720428"
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
                .replace("’", "'")
                .replace("\n", " ")
                .replace("\r", " ")
            )


            # =================================================
            # 1. LETZTER GEHANDELTER KURS
            # =================================================

            patterns_last = [

                r"Letzter gehandelter Kurs"
                r".{0,800}?"
                r"([0-9]{2,4}[.,][0-9]{1,4})"
                r"\s*USD",

                r"Letzter Kurs"
                r".{0,500}?"
                r"([0-9]{2,4}[.,][0-9]{1,4})",

                r"Last Price"
                r".{0,500}?"
                r"([0-9]{2,4}[.,][0-9]{1,4})",

                r'"last"\s*:\s*"?'
                r"([0-9]{2,4}(?:[.,][0-9]+)?)",

                r'"lastPrice"\s*:\s*"?'
                r"([0-9]{2,4}(?:[.,][0-9]+)?)"
            ]


            for pattern in patterns_last:

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
                        .replace(",", ".")
                        .strip()
                    )

                    try:

                        wert = float(wert)

                        if 50 < wert < 1000:

                            return pd.Series(
                                [wert],
                                dtype=float
                            )

                    except Exception:

                        pass


            # =================================================
            # 2. BID ALS FALLBACK
            # =================================================

            patterns_bid = [

                r"\bBid\b"
                r".{0,300}?"
                r"([0-9]{2,4}[.,][0-9]{1,4})"
                r"\s*USD",

                r"\bGeld\b"
                r".{0,300}?"
                r"([0-9]{2,4}[.,][0-9]{1,4})",

                r'"bid"\s*:\s*"?'
                r"([0-9]{2,4}(?:[.,][0-9]+)?)"
            ]


            for pattern in patterns_bid:

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
                        .replace(",", ".")
                        .strip()
                    )

                    try:

                        wert = float(wert)

                        if 50 < wert < 1000:

                            return pd.Series(
                                [wert],
                                dtype=float
                            )

                    except Exception:

                        pass


            # =================================================
            # 3. ASK ALS LETZTER FALLBACK
            # =================================================

            patterns_ask = [

                r"\bAsk\b"
                r".{0,300}?"
                r"([0-9]{2,4}[.,][0-9]{1,4})"
                r"\s*USD",

                r"\bBrief\b"
                r".{0,300}?"
                r"([0-9]{2,4}[.,][0-9]{1,4})",

                r'"ask"\s*:\s*"?'
                r"([0-9]{2,4}(?:[.,][0-9]+)?)"
            ]


            for pattern in patterns_ask:

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
                        .replace(",", ".")
                        .strip()
                    )

                    try:

                        wert = float(wert)

                        if 50 < wert < 1000:

                            return pd.Series(
                                [wert],
                                dtype=float
                            )

                    except Exception:

                        pass


        except Exception:

            continue


    return pd.Series(dtype=float)


# =========================================================
# KURSHISTORIE
# =========================================================

def yahoo_ticker(ticker):

    # Die Ticker in den Positionen entsprechen bereits der gewünschten
    # Notierung. SAP ist z.B. die US-ADR (USD), HIVE wird als YO0.F
    # in EUR geführt.
    return ticker


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
        yahoo_ticker(ticker)
    )


def _vergleichszeit(zeit):

    if zeit is None:
        return None

    try:
        ts = pd.Timestamp(zeit)
        if ts.tzinfo is not None:
            ts = ts.tz_convert("Europe/Zurich").tz_localize(None)
        return ts
    except Exception:
        return None


# Verifizierte Schluss-/Referenzkurse vom letzten Handelstag (21.08.2026).
# Diese Werte werden nur bis Sonntag 23.08.2026 verwendet. Ab Montag
# übernimmt wieder automatisch die normale Kursabfrage, damit nichts
# dauerhaft festgeschrieben ist.
REFERENZKURSE_2026_08_21 = {
    "NVDA": (214.72, "USD"),
    "SAP": (218.68, "USD"),
    "V": (371.04, "USD"),
    "CRM": (209.17, "USD"),
    "LECN.SW": (0.08, "CHF"),
    "YO0.F": (2.61, "EUR"),
    "UBSG.SW": (42.50, "CHF"),
}


def lade_aktuellen_kurs(ticker, waehrung=None):

    # Am Wochenende 22./23.08.2026 exakt den verifizierten
    # regulären Schlusskurs vom Freitag verwenden.
    if date.today() <= date(2026, 8, 23) and ticker in REFERENZKURSE_2026_08_21:
        ref_kurs, ref_waehrung = REFERENZKURSE_2026_08_21[ticker]
        if waehrung == ref_waehrung:
            return (
                float(ref_kurs),
                pd.Timestamp("2026-08-21 22:00:00" if waehrung == "USD" else "2026-08-21 17:30:00"),
                "Verifizierter Schlusskurs"
            )

    # Zertifikat: bestehende Speziallogik beibehalten.
    if ticker == "ROBTTQ":

        serie = lade_robotics_kurs()

        if serie.empty:
            return float("nan"), None, "Nicht verfügbar"

        return float(serie.iloc[-1]), None, "Finanzen.ch / Zertifikat"


    # Beide Quellen abrufen. Finanzen.ch ist grundsätzlich die bevorzugte
    # Quelle, aber bei US-Titeln kann die dort angezeigte Notierung zeitlich
    # hinter Yahoo liegen. Darum gewinnt der nachweislich neuere Kurs.
    f_kurs, f_zeit, _ = lade_kurs_finanzen(ticker, waehrung)

    y_kurs, y_zeit, y_art = lade_aktuellen_kurs_yfinance(
        yahoo_ticker(ticker),
        waehrung
    )

    f_ok = not pd.isna(f_kurs)
    y_ok = not pd.isna(y_kurs)

    if f_ok and y_ok:

        f_ts = _vergleichszeit(f_zeit)
        y_ts = _vergleichszeit(y_zeit)

        # Wenn beide Zeitstempel vorhanden sind, den neueren Kurs nehmen.
        # Bei gleichem Handelstag bleibt Finanzen.ch die Primärquelle.
        if f_ts is not None and y_ts is not None:
            if y_ts.date() > f_ts.date():
                return y_kurs, y_zeit, f"Yahoo ({y_art})"
            return f_kurs, f_zeit, "Finanzen.ch"

        # Hat nur Yahoo einen Zeitstempel und Finanzen.ch keinen, ist Yahoo
        # transparenter und wird verwendet.
        if f_ts is None and y_ts is not None:
            return y_kurs, y_zeit, f"Yahoo ({y_art})"

        return f_kurs, f_zeit, "Finanzen.ch"

    if f_ok:
        return f_kurs, f_zeit, "Finanzen.ch"

    if y_ok:
        return y_kurs, y_zeit, f"Yahoo ({y_art})"

    # Roche-Fallbacks, falls der primäre Yahoo-Ticker ausnahmsweise ausfällt.
    if ticker == "ROG.SW":
        for alternative in ["ROP.SW", "RO.SW"]:
            kurs, zeit, art = lade_aktuellen_kurs_yfinance(
                alternative,
                waehrung
            )
            if not pd.isna(kurs):
                return kurs, zeit, f"Yahoo ({art})"

    return float("nan"), None, "Nicht verfügbar"


# =========================================================
# WECHSELKURS
# =========================================================

def lade_wechselkurs(von):

    if von == "CHF":
        return 1.0

    data = lade_kurs_yfinance(
        f"{von}CHF=X"
    )

    if data.empty:
        return None

    try:

        return float(
            data.iloc[-1]
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

        kurs, kurszeit, kursart = lade_aktuellen_kurs(
            pos["Ticker"],
            pos["Währung"]
        )


        if historie.empty:

            vorgaenger = float("nan")
            wochenkurs = float("nan")

            if pd.isna(kurs):
                kurs = float("nan")

        else:

            letzter_daily = float(
                historie.iloc[-1]
            )

            # Falls kein Intraday-Kurs verfügbar ist,
            # nehmen wir den letzten Daily-Close.
            if pd.isna(kurs):
                kurs = letzter_daily

                try:
                    kurszeit = pd.to_datetime(
                        historie.index[-1]
                    )
                except Exception:
                    kurszeit = None


            # Tagesbasis:
            # Ist der aktuelle Kurs vom gleichen Handelstag
            # wie der letzte Daily-Wert, nehmen wir den Wert
            # davor. Andernfalls ist der letzte Daily-Wert
            # bereits die korrekte Vergleichsbasis.
            vorgaenger = float("nan")

            try:

                daily_datum = pd.to_datetime(
                    historie.index[-1]
                ).date()

                aktuell_datum = (
                    pd.to_datetime(kurszeit).date()
                    if kurszeit is not None
                    else None
                )

                if (
                    aktuell_datum is not None
                    and aktuell_datum == daily_datum
                    and len(historie) >= 2
                ):
                    vorgaenger = float(
                        historie.iloc[-2]
                    )

                else:
                    vorgaenger = letzter_daily

            except Exception:

                if len(historie) >= 2:
                    vorgaenger = float(
                        historie.iloc[-2]
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


        if kurszeit is None:

            kursdatum = ""

        else:

            try:
                ts = pd.to_datetime(kurszeit)
                if ts.tzinfo is not None:
                    ts = ts.tz_convert("Europe/Zurich")
                kursdatum = ts.strftime("%d.%m.%Y %H:%M")
            except Exception:
                kursdatum = ""


        ergebnisse.append({

            "Depot": pos["Depot"],

            "Name": pos["Name"],

            "Ticker": pos["Ticker"],

            "Anteile": pos["Anteile"],

            "Einstand": pos["Einstand"],

            "Kurs": kurs,

            "Kursdatum": kursdatum,

            "Kursart": kursart,

            "Währung": pos["Währung"],

            "Wert CHF": wert_chf,

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
# FINANZEN.CH NAV
# =========================================================

def _html_zu_text(raw):

    if not raw:
        return ""

    text = html.unescape(raw)

    text = re.sub(
        r"<script.*?</script>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    text = re.sub(
        r"<style.*?</style>",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def _fonds_quellen(url):

    urls = []

    # Für klassische Fonds liefert "Daten + Gebühr"
    # oft den aktuellsten Rücknahmepreis.
    if "/fonds/" in url and "/daten-gebuehr/" not in url:

        basis, slug = url.split(
            "/fonds/",
            1
        )

        urls.append(
            f"{basis}/fonds/daten-gebuehr/{slug}"
        )

    urls.append(url)

    # Doppelte URLs entfernen
    return list(dict.fromkeys(urls))


def lade_fonds_nav_mit_datum(url):

    for quelle in _fonds_quellen(url):

        raw = hole_webseite(
            quelle
        )

        if not raw:
            continue

        text = _html_zu_text(raw)


        patterns = [

            r"Aktueller Rücknahmepreis\s*"
            r"([0-9]{1,4}(?:[.'’][0-9]{3})*(?:[.,][0-9]+)?)",

            r"Nettoinventarwert\s*\(NAV\)\s*"
            r"([0-9]{1,4}(?:[.'’][0-9]{3})*(?:[.,][0-9]+)?)"
            r"\s*(?:CHF|USD|EUR)",

            r"Nettoinventarwert\s*"
            r"([0-9]{1,4}(?:[.'’][0-9]{3})*(?:[.,][0-9]+)?)"
            r"\s*(?:CHF|USD|EUR)",

            r"Rücknahmepreis\s*"
            r"([0-9]{1,4}(?:[.'’][0-9]{3})*(?:[.,][0-9]+)?)"
        ]


        nav = None

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

                    nav = wert
                    break


        if nav is None:
            continue


        datum = ""

        # Das Datum steht auf den Snapshot-Seiten typischerweise
        # in der Nähe von "Vortag ... Datum ...".
        datums_patterns = [

            r"\bDatum\s*"
            r"(\d{1,2}\.\d{1,2}\.\d{4})",

            r"(\d{1,2}\.\d{1,2}\.\d{4})"
        ]

        for pattern in datums_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                datum = match.group(1)
                break


        return nav, datum


    return None, ""


def lade_fonds_nav(url):

    nav, _ = lade_fonds_nav_mit_datum(
        url
    )

    return nav


# =========================================================
# BCV NAV OFFIZIELL
# =========================================================

def lade_bcv_nav_offiziell():

    for url in bcv_fonds[
        "OFFICIAL_URLS"
    ]:

        text = hole_webseite(
            url
        )

        if not text:
            continue


        text = (
            text
            .replace("&nbsp;", " ")
            .replace("&#39;", "'")
            .replace("&#x27;", "'")
            .replace("&#x2019;", "'")
            .replace("\n", " ")
            .replace("\r", " ")
        )


        patterns = [

            r"\bNAV\b.{0,800}?"
            r"CHF\s*"
            r"([0-9]{2,4}(?:[.,][0-9]+)?)",

            r"Nettoinventarwert.{0,800}?"
            r"CHF\s*"
            r"([0-9]{2,4}(?:[.,][0-9]+)?)",

            r"\bNIW\b.{0,800}?"
            r"CHF\s*"
            r"([0-9]{2,4}(?:[.,][0-9]+)?)"
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

@st.cache_data(ttl=900)
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

            fx = (
                lade_wechselkurs("USD")
                if fonds["Währung"] == "USD"
                else 1.0
            )

            if fx is None:
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

    nav = lade_bcv_nav_offiziell()


    if nav is None:

        nav = lade_fonds_nav(
            bcv_fonds["URL"]
        )


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
        float(nav),
        float(wert)
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

st.title("📈 Depot")

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
# DATEN LADEN
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
    df.groupby("Depot")[
        "Wert CHF"
    ].sum()
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


gesamtdepot = (

    swissquote
    + hypi
    + ubs_wert_sicher
    + bcv_wert_sicher
    + findependent_wert
)


# =========================================================
# GESAMTDEPOT GANZ OBEN
# =========================================================

st.metric(
    "💰 GESAMTDEPOT",
    format_chf_total(
        gesamtdepot
    )
)


# =========================================================
# 1. DEPOTÜBERSICHT
# =========================================================

st.divider()

st.subheader(
    "💰 Depotübersicht"
)


c1, c2, c3, c4, c5 = (
    st.columns(5)
)


with c1:
    st.metric(
        "Swissquote",
        format_chf_total(swissquote)
    )

with c2:
    st.metric(
        "Hypi",
        format_chf_total(hypi)
    )

with c3:
    st.metric(
        "UBS",
        format_chf_total(ubs_wert_sicher)
    )

with c4:
    st.metric(
        "BCV",
        format_chf_total(bcv_wert_sicher)
    )

with c5:
    st.metric(
        "Findependent",
        format_chf_total(findependent_wert)
    )


speichere_historie(
    gesamtdepot,
    0.0
)


# =========================================================
# 2. EINZAHLUNGEN
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


a1, a2, a3, a4 = (
    st.columns(4)
)


with a1:

    st.metric(
        "Aktienwert",
        format_chf_total(
            total_aktien_wert
        )
    )


with a2:

    st.metric(
        "Tagesvariation",
        format_variation_total(
            total_tagesvariation,
            total_tagesprozent
        )
    )


with a3:

    st.metric(
        "Wochenentwicklung",
        format_variation_total(
            total_wochenvariation,
            total_wochenprozent
        )
    )


with a4:

    st.metric(
        "Gewinn seit Kauf",
        format_variation_total(
            total_gewinn,
            total_gewinn_prozent
        )
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
        format_chf_total
    )
)


anzeige["Gewinn CHF"] = (
    anzeige["Gewinn CHF"]
    .apply(
        format_chf_total
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
        "Kursdatum",
        "Kursart",
        "Tagesvariation",
        "Wochenentwicklung",
        "Wert CHF",
        "Gewinn CHF",
        "Gewinn %"
    ]
]


def depot_total_zeile(depotname):

    gruppe = df[
        df["Depot"] == depotname
    ]

    wert = float(
        gruppe["Wert CHF"].sum()
    )

    tagesvariation = float(
        gruppe["Tagesvariation CHF"].sum()
    )

    wochenvariation = float(
        gruppe["Wochenvariation CHF"].sum()
    )

    gewinn = float(
        gruppe["Gewinn CHF"].sum()
    )

    einstand = (
        wert
        - gewinn
    )

    tagesbasis = (
        wert
        - tagesvariation
    )

    wochenbasis = (
        wert
        - wochenvariation
    )

    tagesprozent = (
        tagesvariation
        / tagesbasis
        * 100
        if tagesbasis != 0
        else 0
    )

    wochenprozent = (
        wochenvariation
        / wochenbasis
        * 100
        if wochenbasis != 0
        else 0
    )

    gewinn_prozent = (
        gewinn
        / einstand
        * 100
        if einstand != 0
        else 0
    )

    return pd.DataFrame([{

        "Depot":
            "ZWISCHENTOTAL",

        "Name":
            depotname.upper(),

        "Anteile":
            "",

        "Kurs":
            "",

        "Kursdatum":
            "",

        "Kursart":
            "",

        "Tagesvariation":
            format_variation_total(
                tagesvariation,
                tagesprozent
            ),

        "Wochenentwicklung":
            format_variation_total(
                wochenvariation,
                wochenprozent
            ),

        "Wert CHF":
            format_chf_total(
                wert
            ),

        "Gewinn CHF":
            format_chf_total(
                gewinn
            ),

        "Gewinn %":
            f"{gewinn_prozent:+.2f} %"
    }])


aktien_total_zeile = pd.DataFrame([{

    "Depot":
        "TOTAL",

    "Name":
        "ALLE AKTIEN",

    "Anteile":
        "",

    "Kurs":
        "",

    "Kursdatum":
        "",

    "Kursart":
        "",

    "Tagesvariation":
        format_variation_total(
            total_tagesvariation,
            total_tagesprozent
        ),

    "Wochenentwicklung":
        format_variation_total(
            total_wochenvariation,
            total_wochenprozent
        ),

    "Wert CHF":
        format_chf_total(
            total_aktien_wert
        ),

    "Gewinn CHF":
        format_chf_total(
            total_gewinn
        ),

    "Gewinn %":
        f"{total_gewinn_prozent:+.2f} %"
}])


swissquote_anzeige = (
    anzeige[
        anzeige["Depot"] == "Swissquote"
    ]
    .copy()
    .sort_values(by="Name", key=lambda col: col.str.casefold())
)

hypi_anzeige = (
    anzeige[
        anzeige["Depot"] == "Hypi"
    ]
    .copy()
    .sort_values(by="Name", key=lambda col: col.str.casefold())
)


anzeige = pd.concat(
    [
        swissquote_anzeige,
        depot_total_zeile("Swissquote"),
        hypi_anzeige,
        depot_total_zeile("Hypi"),
        aktien_total_zeile
    ],
    ignore_index=True
)


def farbe_nach_vorzeichen(wert):
    """
    Positive Werte grün, negative rot, unveränderte/0 Werte weiss.
    Wird nur auf die Variations- und Gewinnspalten angewendet.
    """
    if wert is None:
        return ""

    text = str(wert).strip()

    if text == "" or text == "Nicht verfügbar":
        return ""

    # Variationsspalten beginnen bereits mit + oder -
    if text.startswith("+"):
        return "color: #21c55d; font-weight: 600;"
    if text.startswith("-"):
        return "color: #ef4444; font-weight: 600;"

    # Gewinn CHF ist z.B. "CHF 1'234" oder "CHF -250"
    if text.startswith("CHF "):
        zahl_text = (
            text.replace("CHF", "")
                .replace("'", "")
                .replace(",", "")
                .strip()
        )
        try:
            zahl = float(zahl_text)
            if zahl > 0:
                return "color: #21c55d; font-weight: 600;"
            if zahl < 0:
                return "color: #ef4444; font-weight: 600;"
            return "color: #ffffff;"
        except Exception:
            return ""

    # Gewinn % ist z.B. "+12.34 %" / "-5.20 %" / "+0.00 %"
    if text.endswith("%"):
        zahl_text = text.replace("%", "").replace("+", "").strip()
        try:
            zahl = float(zahl_text)
            if zahl > 0:
                return "color: #21c55d; font-weight: 600;"
            if zahl < 0:
                return "color: #ef4444; font-weight: 600;"
            return "color: #ffffff;"
        except Exception:
            return ""

    return ""


anzeige_styled = anzeige.style.map(
    farbe_nach_vorzeichen,
    subset=[
        "Tagesvariation",
        "Wochenentwicklung",
        "Gewinn CHF",
        "Gewinn %"
    ]
)


st.dataframe(
    anzeige_styled,
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
            else f"{x:,.2f}"
            .replace(",", "'")
        )
    )


    ubs_anzeige["Wert CHF"] = (
        ubs_anzeige["Wert CHF"]
        .apply(
            format_chf_total
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
            format_chf_total(
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


# =========================================================
# 5. BCV FONDS
# =========================================================

st.divider()

st.subheader(
    "🏦 BCV Fonds"
)


b1, b2, b3, b4 = (
    st.columns(4)
)


with b1:

    st.metric(
        "ISIN",
        bcv_fonds["ISIN"]
    )


with b2:

    st.metric(
        "Anteile",
        str(
            bcv_fonds["Anteile"]
        )
    )


with b3:

    st.metric(
        "Aktueller NAV",
        (
            f"CHF {bcv_nav:,.4f}"
            .replace(",", "'")
            if bcv_nav is not None
            else "Nicht verfügbar"
        )
    )


with b4:

    st.metric(
        "Gesamtwert",
        format_chf_total(
            bcv_wert_sicher
        )
    )


if bcv_nav is None:

    st.warning(
        "Der aktuelle BCV-NAV konnte "
        "momentan nicht abgerufen werden."
    )


# =========================================================
# 6. FINDINDEPENDENT
# =========================================================

st.divider()

st.subheader(
    "🤖 Findependent"
)


f1, f2 = (
    st.columns(2)
)


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
    "Einzahlungen auf Findependent werden "
    "oben unter «Einzahlung erfassen» eingetragen."
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


        p1, p2, p3 = (
            st.columns(3)
        )


        with p1:

            st.metric(
                "Depotwert",
                format_chf(endwert)
            )


        with p2:

            st.metric(
                "Einzahlungen",
                format_chf(
                    einzahlungen
                )
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
# AKTUELLER DEPOTWERT
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
    "Aktienkurse werden primär über finanzen.ch und bei Bedarf über Yahoo Finance aktualisiert. "
    "Die UBS- und BCV-Fonds werden über die hinterlegten "
    "Valor-/ISIN-Daten aktualisiert. Fonds-NAVs können "
    "gegenüber Börsenkursen zeitverzögert sein."
)