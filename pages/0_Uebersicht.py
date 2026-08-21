import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).parent.parent

DATA_FILE = BASE_DIR / "vermoegensdaten.csv"
DEPOT_FILE = BASE_DIR / "depot_aktuell.csv"

# Vermögensziele
ZIELVERMOEGEN = 1_000_000
ZIEL_FREIES_VERMOEGEN = 750_000
ZIEL_VORSORGE = 1_000_000

# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def format_chf(value):
    """Schweizer Zahlenformat"""

    return (
        f"{value:,.0f}"
        .replace(",", "'")
        + " CHF"
    )


def format_change(value):
    """Schweizer Zahlenformat mit Vorzeichen"""

    return (
        f"{value:+,.0f}"
        .replace(",", "'")
        + " CHF"
    )


def calculate_change(
    current,
    previous
):

    if (
        previous is None
        or previous == 0
    ):

        return 0, 0


    change_chf = (
        current
        - previous
    )


    change_percent = (
        (
            current
            - previous
        )
        / previous
        * 100
    )


    return (
        change_chf,
        change_percent
    )


def get_current_depot_value():

    """
    Liest den aktuell berechneten Depotwert
    aus depot_aktuell.csv.
    """

    if not os.path.exists(
        DEPOT_FILE
    ):

        return None


    try:

        df_depot = pd.read_csv(
            DEPOT_FILE
        )


        if df_depot.empty:

            return None


        return float(
            df_depot[
                "Depotwert"
            ].iloc[-1]
        )


    except Exception:

        return None


# ========================================================
# CHECK DATA FILE
# ========================================================

if (
    not os.path.exists(
        DATA_FILE
    )
    or
    os.stat(
        DATA_FILE
    ).st_size == 0
):

    st.error(
        "Datei vermoegensdaten.csv "
        "nicht gefunden oder leer!"
    )


else:


    # ====================================================
    # LOAD DATA
    # ====================================================

    df_history = pd.read_csv(
        DATA_FILE
    )


    df_history[
        "Datum"
    ] = pd.to_datetime(
        df_history[
            "Datum"
        ]
    )


    df_history = (
        df_history
        .sort_values(
            by="Datum"
        )
        .reset_index(
            drop=True
        )
    )


    # ====================================================
    # CURRENT / PREVIOUS ENTRY
    # ====================================================

    latest_entry = (
        df_history.iloc[-1]
    )


    if len(
        df_history
    ) >= 2:

        previous_entry = (
            df_history.iloc[-2]
        )

    else:

        previous_entry = None


    # ====================================================
    # CURRENT VALUES
    # ====================================================

    v_liq = (
        latest_entry[
            "Liquide_Mittel"
        ]
    )


    v_spar = (
        latest_entry[
            "Sparvermoegen"
        ]
    )


    # ----------------------------------------------------
    # AKTUELLEN DEPOTWERT AUTOMATISCH LADEN
    # ----------------------------------------------------

    current_depot = (
        get_current_depot_value()
    )


    if current_depot is not None:

        v_boerse = (
            current_depot
        )

        depot_automatisch = True


    else:

        v_boerse = (
            latest_entry[
                "Boerse"
            ]
        )

        depot_automatisch = False


    v_priv = (
        latest_entry[
            "Private_Vorsorge"
        ]
    )


    v_lpp = (
        latest_entry[
            "LPP"
        ]
    )


    # ====================================================
    # TOTAL WEALTH
    # ====================================================

    total_assets = (
        v_liq
        + v_spar
        + v_boerse
        + v_priv
        + v_lpp
    )


    # ====================================================
    # FREE WEALTH
    # ====================================================

    free_assets = (
        v_liq
        + v_spar
        + v_boerse
    )


    # ====================================================
    # RETIREMENT / PENSION ASSETS
    # ====================================================

    vorsorge = (
        v_priv
        + v_lpp
    )


    # ====================================================
    # PREVIOUS VALUES
    # ====================================================

    if previous_entry is not None:

        p_liq = (
            previous_entry[
                "Liquide_Mittel"
            ]
        )


        p_spar = (
            previous_entry[
                "Sparvermoegen"
            ]
        )


        p_boerse = (
            previous_entry[
                "Boerse"
            ]
        )


        p_priv = (
            previous_entry[
                "Private_Vorsorge"
            ]
        )


        p_lpp = (
            previous_entry[
                "LPP"
            ]
        )


        previous_total = (
            p_liq
            + p_spar
            + p_boerse
            + p_priv
            + p_lpp
        )


    else:

        p_liq = None
        p_spar = None
        p_boerse = None
        p_priv = None
        p_lpp = None

        previous_total = None


    # ====================================================
    # CHANGES VS PREVIOUS ENTRY
    # ====================================================

    (
        total_change,
        total_change_percent
    ) = calculate_change(
        total_assets,
        previous_total
    )


    (
        liq_change,
        liq_percent
    ) = calculate_change(
        v_liq,
        p_liq
    )


    (
        spar_change,
        spar_percent
    ) = calculate_change(
        v_spar,
        p_spar
    )


    (
        boerse_change,
        boerse_percent
    ) = calculate_change(
        v_boerse,
        p_boerse
    )


    (
        priv_change,
        priv_percent
    ) = calculate_change(
        v_priv,
        p_priv
    )


    (
        lpp_change,
        lpp_percent
    ) = calculate_change(
        v_lpp,
        p_lpp
    )


    # ====================================================
    # HEADER
    # ====================================================

    st.title(
        "寿 Mein Vermögens-Dashboard"
    )


    st.caption(
        f"Letzter Stichtag: "
        f"{latest_entry['Datum'].strftime('%d.%m.%Y')}"
    )


    # ====================================================
    # DEPOT STATUS
    # ====================================================

    if depot_automatisch:

        st.success(
            f"📈 Aktueller Depotwert automatisch "
            f"übernommen: **{format_chf(v_boerse)}**"
        )


    else:

        st.info(
            "ℹ️ Kein aktueller Depotwert gefunden. "
            "Der gespeicherte Wert aus "
            "vermoegensdaten.csv wird verwendet."
        )


    # ====================================================
    # YEAR-TO-DATE
    # ====================================================

    current_year = (
        latest_entry[
            "Datum"
        ].year
    )


    df_current_year = (
        df_history[
            df_history[
                "Datum"
            ].dt.year
            == current_year
        ]
        .copy()
    )


    df_current_year[
        "Gesamtvermoegen"
    ] = (
        df_current_year[
            "Liquide_Mittel"
        ]
        + df_current_year[
            "Sparvermoegen"
        ]
        + df_current_year[
            "Boerse"
        ]
        + df_current_year[
            "Private_Vorsorge"
        ]
        + df_current_year[
            "LPP"
        ]
    )


    first_year_entry = (
        df_current_year.iloc[0]
    )


    year_start_assets = (
        first_year_entry[
            "Gesamtvermoegen"
        ]
    )


    ytd_change = (
        total_assets
        - year_start_assets
    )


    if year_start_assets != 0:

        ytd_percent = (
            ytd_change
            / year_start_assets
            * 100
        )


    else:

        ytd_percent = 0


    # ====================================================
    # GESAMTVERMÖGEN & ENTWICKLUNG
    # ====================================================

    st.markdown(
        "## 寿 Gesamtvermögen"
    )


    (
        total_col1,
        total_col2,
        total_col3,
        total_col4
    ) = st.columns(4)


    with total_col1:

        st.metric(
            label="💰 Gesamtvermögen",

            value=format_chf(
                total_assets
            ),

            delta=(
                f"{format_change(total_change)} "
                f"({total_change_percent:+.2f}%)"
            )
        )


    with total_col2:

        st.metric(
            label="📅 Vermögen am Jahresanfang",

            value=format_chf(
                year_start_assets
            )
        )


    with total_col3:

        st.metric(
            label="📈 Veränderung seit Jahresbeginn",

            value=format_change(
                ytd_change
            ),

            delta=(
                f"{ytd_percent:+.2f}%"
            )
        )


    with total_col4:

        st.metric(
            label="💰 Aktuelles Vermögen",

            value=format_chf(
                total_assets
            )
        )


    # ====================================================
    # YTD GRAPH
    # ====================================================

    st.markdown(
        f"#### 📊 Gesamtvermögen "
        f"seit 1. Januar {current_year}"
    )


    fig_ytd = go.Figure()


    fig_ytd.add_trace(
        go.Scatter(

            x=df_current_year[
                "Datum"
            ],

            y=df_current_year[
                "Gesamtvermoegen"
            ],

            mode="lines+markers",

            name="Gesamtvermögen",

            line=dict(
                width=4,
                color="#16a34a"
            ),

            marker=dict(
                size=8
            ),

            hovertemplate=(
                "%{x|%d.%m.%Y}<br>"
                + "Gesamtvermögen: "
                + "%{y:,.0f} CHF"
                + "<extra></extra>"
            )
        )
    )


    fig_ytd.add_hline(
        y=year_start_assets,

        line_dash="dash",

        line_color="#64748b",

        annotation_text=(
            f"Jahresbeginn: "
            f"{year_start_assets:,.0f} CHF"
        ),

        annotation_position="top left"
    )


    fig_ytd.update_layout(

        yaxis_title="CHF",

        xaxis_title="",

        hovermode="x unified",

        margin=dict(
            t=30,
            b=20,
            l=20,
            r=20
        ),

        showlegend=False
    )


    st.plotly_chart(
        fig_ytd,
        use_container_width=True
    )


    # ====================================================
    # YTD SUMMARY
    # ====================================================

    if ytd_change > 0:

        st.success(
            f"📈 Dein Gesamtvermögen ist seit "
            f"Jahresbeginn um "
            f"**{format_chf(ytd_change)}** "
            f"bzw. **{ytd_percent:+.2f}%** gestiegen."
        )


    elif ytd_change < 0:

        st.error(
            f"📉 Dein Gesamtvermögen ist seit "
            f"Jahresbeginn um "
            f"**{format_chf(abs(ytd_change))}** "
            f"bzw. **{ytd_percent:.2f}%** gesunken."
        )


    else:

        st.info(
            "➡️ Dein Gesamtvermögen hat sich "
            "seit Jahresbeginn nicht verändert."
        )


    st.divider()


    # ====================================================
    # THREE FINANCIAL TARGETS
    # ====================================================

    st.markdown(
        "### 🎯 Meine finanziellen Ziele"
    )


    (
        target_col1,
        target_col2,
        target_col3
    ) = st.columns(3)


    # ----------------------------------------------------
    # TOTAL WEALTH TARGET
    # ----------------------------------------------------

    with target_col1:

        st.markdown(
            "#### 🎯 Vermögensziel"
        )


        target_percentage = (
            total_assets
            / ZIELVERMOEGEN
            * 100
        )


        target_percentage_display = min(
            max(
                target_percentage,
                0
            ),
            100
        )


        st.progress(
            target_percentage_display
            / 100
        )


        st.markdown(
            f"**{format_chf(total_assets)}** "
            f"/ **{format_chf(ZIELVERMOEGEN)}**"
        )


        st.markdown(
            f"**{target_percentage:.1f} % erreicht**"
        )


    # ----------------------------------------------------
    # FREE WEALTH TARGET
    # ----------------------------------------------------

    with target_col2:

        st.markdown(
            "#### 💰 Frei verfügbares Vermögen"
        )


        free_percentage = (
            free_assets
            / ZIEL_FREIES_VERMOEGEN
            * 100
        )


        free_percentage_display = min(
            max(
                free_percentage,
                0
            ),
            100
        )


        st.progress(
            free_percentage_display
            / 100
        )


        st.markdown(
            f"**{format_chf(free_assets)}** "
            f"/ **{format_chf(ZIEL_FREIES_VERMOEGEN)}**"
        )


        st.markdown(
            f"**{free_percentage:.1f} % erreicht**"
        )


    # ----------------------------------------------------
    # RETIREMENT TARGET
    # ----------------------------------------------------

    with target_col3:

        st.markdown(
            "#### 🛡️ Vorsorge"
        )


        vorsorge_percentage = (
            vorsorge
            / ZIEL_VORSORGE
            * 100
        )


        vorsorge_percentage_display = min(
            max(
                vorsorge_percentage,
                0
            ),
            100
        )


        st.progress(
            vorsorge_percentage_display
            / 100
        )


        st.markdown(
            f"**{format_chf(vorsorge)}** "
            f"/ **{format_chf(ZIEL_VORSORGE)}**"
        )


        st.markdown(
            f"**{vorsorge_percentage:.1f} % erreicht**"
        )


    st.divider()


    # ====================================================
    # ASSET METRICS
    # ====================================================

    st.markdown(
        "### 💰 Vermögenswerte"
    )


    (
        row1_col1,
        row1_col2,
        row1_col3
    ) = st.columns(3)


    with row1_col1:

        st.metric(
            label="💵 Liquide Mittel",

            value=format_chf(
                v_liq
            ),

            delta=(
                f"{format_change(liq_change)} "
                f"({liq_percent:+.2f}%)"
            )
        )


    with row1_col2:

        st.metric(
            label="🏦 Sparkapital",

            value=format_chf(
                v_spar
            ),

            delta=(
                f"{format_change(spar_change)} "
                f"({spar_percent:+.2f}%)"
            )
        )


    with row1_col3:

        st.metric(
            label="📈 Investiertes Kapital",

            value=format_chf(
                v_boerse
            ),

            delta=(
                f"{format_change(boerse_change)} "
                f"({boerse_percent:+.2f}%)"
            )
        )


    row2_col1, row2_col2 = (
        st.columns(2)
    )


    with row2_col1:

        st.metric(
            label="🛡️ Private Vorsorge",

            value=format_chf(
                v_priv
            ),

            delta=(
                f"{format_change(priv_change)} "
                f"({priv_percent:+.2f}%)"
            )
        )


    with row2_col2:

        st.metric(
            label="💼 LPP (Pensionskasse)",

            value=format_chf(
                v_lpp
            ),

            delta=(
                f"{format_change(lpp_change)} "
                f"({lpp_percent:+.2f}%)"
            )
        )


    st.divider()


    # ====================================================
    # TWO COLUMN LAYOUT
    # ====================================================

    col_left, col_right = (
        st.columns(2)
    )


    # ====================================================
    # ASSET DISTRIBUTION
    # ====================================================

    with col_left:

        st.markdown(
            "### 📊 Aktuelle Verteilung"
        )


        asset_data = pd.DataFrame({

            "Kategorie": [
                "Liquide Mittel",
                "Sparkapital",
                "Investiertes Kapital",
                "Private Vorsorge",
                "LPP"
            ],

            "Betrag": [
                v_liq,
                v_spar,
                v_boerse,
                v_priv,
                v_lpp
            ]
        })


        fig_pie = px.pie(
            asset_data,
            values="Betrag",
            names="Kategorie",
            hole=0.45
        )


        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )


        fig_pie.update_layout(
            margin=dict(
                t=20,
                b=20,
                l=20,
                r=20
            ),

            showlegend=True
        )


        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )


    # ====================================================
    # ADD NEW MONTH
    # ====================================================

    with col_right:

        st.markdown(
            "### 📝 Neuen Monat hinzufügen"
        )


        with st.form(
            "add_form",
            clear_on_submit=False
        ):

            input_date = (
                st.date_input(
                    "Stichtag",
                    datetime.now()
                )
            )


            v_liq_in = (
                st.number_input(
                    "Liquide Mittel (CHF)",
                    value=float(
                        v_liq
                    )
                )
            )


            v_spar_in = (
                st.number_input(
                    "Sparkapital (CHF)",
                    value=float(
                        v_spar
                    )
                )
            )


            v_boerse_in = (
                st.number_input(
                    "Investiertes Kapital (CHF)",
                    value=float(
                        v_boerse
                    )
                )
            )


            v_priv_in = (
                st.number_input(
                    "Private Vorsorge (CHF)",
                    value=float(
                        v_priv
                    )
                )
            )


            v_lpp_in = (
                st.number_input(
                    "LPP (Pensionskasse - CHF)",
                    value=float(
                        v_lpp
                    )
                )
            )


            if st.form_submit_button(
                "💾 Monat speichern"
            ):

                new_row = pd.DataFrame([{

                    "Datum":
                        input_date.strftime(
                            "%Y-%m-%d"
                        ),

                    "Liquide_Mittel":
                        v_liq_in,

                    "Sparvermoegen":
                        v_spar_in,

                    "Boerse":
                        v_boerse_in,

                    "Private_Vorsorge":
                        v_priv_in,

                    "LPP":
                        v_lpp_in
                }])


                df_history = df_history[
                    df_history[
                        "Datum"
                    ]
                    != pd.to_datetime(
                        new_row[
                            "Datum"
                        ].iloc[0]
                    )
                ]


                df_all = pd.concat(
                    [
                        df_history,
                        new_row
                    ],
                    ignore_index=True
                )


                df_all[
                    "Datum"
                ] = pd.to_datetime(
                    df_all[
                        "Datum"
                    ]
                )


                df_all = (
                    df_all
                    .sort_values(
                        by="Datum"
                    )
                )


                df_all.to_csv(
                    DATA_FILE,
                    index=False
                )


                st.success(
                    "Erfolgreich gespeichert!"
                )


                st.rerun()


        # =================================================
        # DELETE ENTRY
        # =================================================

        st.divider()


        st.markdown(
            "### 🗑️ Eintrag löschen"
        )


        df_history[
            "Datum_Str"
        ] = (
            df_history[
                "Datum"
            ]
            .dt.strftime(
                "%Y-%m-%d"
            )
        )


        all_dates = (
            df_history[
                "Datum_Str"
            ]
            .unique()
            .tolist()
        )


        with st.form(
            "delete_form",
            clear_on_submit=True
        ):

            date_to_delete = (
                st.selectbox(
                    "Wähle das Datum aus, das gelöscht werden soll:",
                    all_dates
                )
            )


            if st.form_submit_button(
                "❌ Ausgewählten Monat "
                "unwiderruflich löschen"
            ):

                df_all = df_history[
                    df_history[
                        "Datum_Str"
                    ]
                    != date_to_delete
                ]


                df_save = (
                    df_all.drop(
                        columns=[
                            "Datum_Str"
                        ],
                        errors="ignore"
                    )
                )


                df_save.to_csv(
                    DATA_FILE,
                    index=False
                )


                st.success(
                    f"Eintrag vom "
                    f"{date_to_delete} "
                    "wurde erfolgreich gelöscht!"
                )


                st.rerun()


    # ====================================================
    # TOTAL WEALTH EVOLUTION
    # ====================================================

    st.divider()


    st.markdown(
        "### 📈 Entwicklung Gesamtvermögen"
    )


    df_history[
        "Gesamtvermoegen"
    ] = (
        df_history[
            "Liquide_Mittel"
        ]
        + df_history[
            "Sparvermoegen"
        ]
        + df_history[
            "Boerse"
        ]
        + df_history[
            "Private_Vorsorge"
        ]
        + df_history[
            "LPP"
        ]
    )


    fig_total = go.Figure()


    fig_total.add_trace(
        go.Scatter(

            x=df_history[
                "Datum"
            ],

            y=df_history[
                "Gesamtvermoegen"
            ],

            mode="lines+markers",

            name="Gesamtvermögen",

            line=dict(
                width=4,
                color="#2563eb"
            ),

            hovertemplate=(
                "%{x|%d.%m.%Y}<br>"
                + "Gesamtvermögen: "
                + "%{y:,.0f} CHF"
                + "<extra></extra>"
            )
        )
    )


    fig_total.update_layout(

        yaxis_title="CHF",

        xaxis_title="",

        hovermode="x unified",

        margin=dict(
            t=20,
            b=20,
            l=20,
            r=20
        )
    )


    st.plotly_chart(
        fig_total,
        use_container_width=True
    )


    # ====================================================
    # STACKED ASSET EVOLUTION
    # ====================================================

    st.markdown(
        "### 📊 Entwicklung nach Vermögensklasse"
    )


    df_history[
        "Liquidität"
    ] = df_history[
        "Liquide_Mittel"
    ]


    df_history[
        "Sparkapital_Klasse"
    ] = df_history[
        "Sparvermoegen"
    ]


    df_history[
        "Investments"
    ] = df_history[
        "Boerse"
    ]


    df_history[
        "Vorsorge_Privat"
    ] = df_history[
        "Private_Vorsorge"
    ]


    df_history[
        "Pensionskasse_Klasse"
    ] = df_history[
        "LPP"
    ]


    fig_trend = go.Figure()


    fig_trend.add_trace(
        go.Scatter(
            x=df_history[
                "Datum"
            ],

            y=df_history[
                "Liquidität"
            ],

            name="Liquide Mittel",

            stackgroup="one",

            line=dict(
                color="#2563eb"
            )
        )
    )


    fig_trend.add_trace(
        go.Scatter(
            x=df_history[
                "Datum"
            ],

            y=df_history[
                "Sparkapital_Klasse"
            ],

            name="Sparkapital",

            stackgroup="one",

            line=dict(
                color="#38bdf8"
            )
        )
    )


    fig_trend.add_trace(
        go.Scatter(
            x=df_history[
                "Datum"
            ],

            y=df_history[
                "Investments"
            ],

            name="Investiertes Kapital",

            stackgroup="one",

            line=dict(
                color="#f59e0b"
            )
        )
    )


    fig_trend.add_trace(
        go.Scatter(
            x=df_history[
                "Datum"
            ],

            y=df_history[
                "Vorsorge_Privat"
            ],

            name="Private Vorsorge",

            stackgroup="one",

            line=dict(
                color="#10b981"
            )
        )
    )


    fig_trend.add_trace(
        go.Scatter(
            x=df_history[
                "Datum"
            ],

            y=df_history[
                "Pensionskasse_Klasse"
            ],

            name="LPP (Pensionskasse)",

            stackgroup="one",

            line=dict(
                color="#059669"
            )
        )
    )


    fig_trend.update_layout(

        hovermode="x unified",

        yaxis_title="CHF",

        xaxis_title="",

        margin=dict(
            t=20,
            b=20,
            l=20,
            r=20
        )
    )


    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )


    # ====================================================
    # HISTORICAL TABLE
    # ====================================================

    st.markdown(
        "### 🗒️ Komplette historische Tabelle"
    )


    st.dataframe(

        df_history[
            [
                "Datum",
                "Liquide_Mittel",
                "Sparvermoegen",
                "Boerse",
                "Private_Vorsorge",
                "LPP",
                "Gesamtvermoegen"
            ]
        ],

        use_container_width=True
    )