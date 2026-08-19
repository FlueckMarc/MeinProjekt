import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="🦅",
    layout="wide"
)

# ============================================================
# CONFIGURATION
# ============================================================

SECRET_PASSWORD = "viper01"
DATA_FILE = "vermoegensdaten.csv"

# Vermögensziele
ZIELVERMOEGEN = 1_000_000
ZIEL_FREIES_VERMOEGEN = 750_000


# ============================================================
# LOGIN
# ============================================================

def check_password():

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col2:

        st.subheader("🔒 Privates Finanz-Dashboard")

        user_password = st.text_input(
            "Passwort",
            type="password",
            key="login_password"
        )

        if st.button("Anmelden"):

            if user_password == SECRET_PASSWORD:

                st.session_state["password_correct"] = True
                st.success("Login erfolgreich!")
                st.rerun()

            else:

                st.error("❌ Falsches Passwort.")

    return False


# ============================================================
# MAIN APP
# ============================================================

if check_password():

    # --------------------------------------------------------
    # CHECK DATA FILE
    # --------------------------------------------------------

    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:

        st.error(
            "Datei vermoegensdaten.csv nicht gefunden oder leer!"
        )

    else:

        # ----------------------------------------------------
        # LOAD DATA
        # ----------------------------------------------------

        df_history = pd.read_csv(DATA_FILE)

        df_history["Datum"] = pd.to_datetime(
            df_history["Datum"]
        )

        df_history = df_history.sort_values(
            by="Datum"
        ).reset_index(drop=True)

        # ----------------------------------------------------
        # CURRENT / PREVIOUS ENTRY
        # ----------------------------------------------------

        latest_entry = df_history.iloc[-1]

        if len(df_history) >= 2:
            previous_entry = df_history.iloc[-2]
        else:
            previous_entry = None

        # ----------------------------------------------------
        # VALUES
        # ----------------------------------------------------

        v_liq = latest_entry["Liquide_Mittel"]
        v_spar = latest_entry["Sparvermoegen"]
        v_boerse = latest_entry["Boerse"]
        v_priv = latest_entry["Private_Vorsorge"]
        v_lpp = latest_entry["LPP"]

        total_assets = (
            v_liq
            + v_spar
            + v_boerse
            + v_priv
            + v_lpp
        )

        # ----------------------------------------------------
        # PREVIOUS VALUES
        # ----------------------------------------------------

        if previous_entry is not None:

            p_liq = previous_entry["Liquide_Mittel"]
            p_spar = previous_entry["Sparvermoegen"]
            p_boerse = previous_entry["Boerse"]
            p_priv = previous_entry["Private_Vorsorge"]
            p_lpp = previous_entry["LPP"]

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
        # HELPER FUNCTION
        # ====================================================

        def calculate_change(current, previous):

            if previous is None or previous == 0:

                return 0, 0

            change_chf = current - previous

            change_percent = (
                (current - previous) / previous
            ) * 100

            return change_chf, change_percent


        # ====================================================
        # CHANGES
        # ====================================================

        total_change, total_change_percent = calculate_change(
            total_assets,
            previous_total
        )

        liq_change, liq_percent = calculate_change(
            v_liq,
            p_liq
        )

        spar_change, spar_percent = calculate_change(
            v_spar,
            p_spar
        )

        boerse_change, boerse_percent = calculate_change(
            v_boerse,
            p_boerse
        )

        priv_change, priv_percent = calculate_change(
            v_priv,
            p_priv
        )

        lpp_change, lpp_percent = calculate_change(
            v_lpp,
            p_lpp
        )


        # ====================================================
        # HEADER
        # ====================================================

        st.title("🦅 Mein Vermögens-Dashboard")

        if st.sidebar.button("🔒 Abmelden"):

            st.session_state["password_correct"] = False
            st.rerun()


        # ====================================================
        # TOTAL WEALTH
        # ====================================================

        if total_change > 0:

            total_arrow = "▲"

        elif total_change < 0:

            total_arrow = "▼"

        else:

            total_arrow = "→"


        st.markdown(
            f"""
            <div style="
                background: linear-gradient(
                    135deg,
                    #1e3a8a,
                    #2563eb
                );
                padding: 30px;
                border-radius: 18px;
                text-align: center;
                margin-bottom: 25px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.15);
            ">

                <div style="
                    color:white;
                    font-size:20px;
                    font-weight:600;
                ">
                    🦅 GESAMTVERMÖGEN
                </div>

                <div style="
                    color:white;
                    font-size:44px;
                    font-weight:700;
                    margin-top:5px;
                ">
                    {total_assets:,.0f} CHF
                </div>

                <div style="
                    color:#dbeafe;
                    font-size:17px;
                    margin-top:5px;
                ">
                    {total_arrow}
                    {total_change:+,.0f} CHF
                    ({total_change_percent:+.2f}%)
                    gegenüber vorherigem Eintrag
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # WEALTH TARGET
        # ====================================================

        target_percentage = (
            total_assets / ZIELVERMOEGEN
        ) * 100

        target_percentage_display = min(
            target_percentage,
            100
        )

        st.markdown("### 🎯 Vermögensziel")

        st.progress(
            target_percentage_display / 100
        )

        col_target1, col_target2 = st.columns(2)

        with col_target1:

            st.markdown(
                f"**CHF {total_assets:,.0f}** "
                f"/ CHF {ZIELVERMOEGEN:,.0f}"
            )

        with col_target2:

            st.markdown(
                f"**{target_percentage:.1f} % erreicht**"
            )


        st.markdown("<br>", unsafe_allow_html=True)


        # ====================================================
        # FREE WEALTH
        # ====================================================

        free_assets = (
            v_liq
            + v_spar
            + v_boerse
        )

        free_percentage = (
            free_assets / ZIEL_FREIES_VERMOEGEN
        ) * 100

        free_percentage_display = min(
            free_percentage,
            100
        )

        st.markdown("### 💰 Frei verfügbares Vermögen")

        st.progress(
            free_percentage_display / 100
        )

        col_free1, col_free2 = st.columns(2)

        with col_free1:

            st.markdown(
                f"**CHF {free_assets:,.0f}** "
                f"/ CHF {ZIEL_FREIES_VERMOEGEN:,.0f}"
            )

        with col_free2:

            st.markdown(
                f"**{free_percentage:.1f} % erreicht**"
            )


        st.markdown("---")


        # ====================================================
        # METRICS
        # ====================================================

        def metric_text(title, value, change, percent):

    if change > 0:
        arrow = "▲"
        change_color = "#16a34a"  # Grün

    elif change < 0:
        arrow = "▼"
        change_color = "#dc2626"  # Rot

    else:
        arrow = "→"
        change_color = "#64748b"  # Grau

    return f"""
    <div style="
        padding:18px;
        border-radius:12px;
        background-color:#f8fafc;
        border:1px solid #e2e8f0;
        margin-bottom:10px;
    ">

        <div style="
            font-size:16px;
            font-weight:600;
        ">
            {title}
        </div>

        <div style="
            font-size:25px;
            font-weight:700;
            margin-top:5px;
        ">
            {value:,.0f} CHF
        </div>

        <div style="
            font-size:14px;
            font-weight:600;
            margin-top:4px;
            color:{change_color};
        ">
            {arrow}
            {change:+,.0f} CHF
            ({percent:+.2f}%)
        </div>

    </div>
    """


        row1_col1, row1_col2, row1_col3 = st.columns(3)

        with row1_col1:

            st.markdown(
                metric_text(
                    "💵 Liquide Mittel",
                    v_liq,
                    liq_change,
                    liq_percent
                ),
                unsafe_allow_html=True
            )

        with row1_col2:

            st.markdown(
                metric_text(
                    "🏦 Sparkapital",
                    v_spar,
                    spar_change,
                    spar_percent
                ),
                unsafe_allow_html=True
            )

        with row1_col3:

            st.markdown(
                metric_text(
                    "📈 Investiertes Kapital",
                    v_boerse,
                    boerse_change,
                    boerse_percent
                ),
                unsafe_allow_html=True
            )


        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:

            st.markdown(
                metric_text(
                    "🛡️ Private Vorsorge",
                    v_priv,
                    priv_change,
                    priv_percent
                ),
                unsafe_allow_html=True
            )

        with row2_col2:

            st.markdown(
                metric_text(
                    "💼 LPP (Pensionskasse)",
                    v_lpp,
                    lpp_change,
                    lpp_percent
                ),
                unsafe_allow_html=True
            )


        st.markdown("---")


        # ====================================================
        # TWO COLUMN LAYOUT
        # ====================================================

        col_left, col_right = st.columns(2)


        # ====================================================
        # ASSET DISTRIBUTION
        # ====================================================

        with col_left:

            st.markdown("### 📊 Aktuelle Verteilung")

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

            st.markdown("### 📝 Neuen Monat hinzufügen")

            with st.form(
                "add_form",
                clear_on_submit=False
            ):

                input_date = st.date_input(
                    "Stichtag",
                    datetime.now()
                )

                v_liq_in = st.number_input(
                    "Liquide Mittel (CHF)",
                    value=float(v_liq)
                )

                v_spar_in = st.number_input(
                    "Sparkapital (CHF)",
                    value=float(v_spar)
                )

                v_boerse_in = st.number_input(
                    "Investiertes Kapital (CHF)",
                    value=float(v_boerse)
                )

                v_priv_in = st.number_input(
                    "Private Vorsorge (CHF)",
                    value=float(v_priv)
                )

                v_lpp_in = st.number_input(
                    "LPP (Pensionskasse - CHF)",
                    value=float(v_lpp)
                )


                if st.form_submit_button(
                    "💾 Monat speichern"
                ):

                    new_row = pd.DataFrame([{

                        "Datum":
                            input_date.strftime("%Y-%m-%d"),

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
                        df_history["Datum"]
                        != pd.to_datetime(
                            new_row["Datum"].iloc[0]
                        )
                    ]


                    df_all = pd.concat(
                        [
                            df_history,
                            new_row
                        ],
                        ignore_index=True
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

            st.markdown("---")

            st.markdown(
                "### 🗑️ Eintrag löschen"
            )

            df_history["Datum_Str"] = (
                df_history["Datum"]
                .dt.strftime("%Y-%m-%d")
            )

            all_dates = (
                df_history["Datum_Str"]
                .unique()
                .tolist()
            )


            with st.form(
                "delete_form",
                clear_on_submit=True
            ):

                date_to_delete = st.selectbox(
                    "Wähle das Datum aus, das gelöscht werden soll:",
                    all_dates
                )


                if st.form_submit_button(
                    "❌ Ausgewählten Monat unwiderruflich löschen"
                ):

                    df_all = df_history[
                        df_history["Datum_Str"]
                        != date_to_delete
                    ]


                    df_save = df_all.drop(
                        columns=["Datum_Str"],
                        errors="ignore"
                    )


                    df_save.to_csv(
                        DATA_FILE,
                        index=False
                    )


                    st.success(
                        f"Eintrag vom {date_to_delete} "
                        "wurde erfolgreich gelöscht!"
                    )

                    st.rerun()


        # ====================================================
        # TOTAL WEALTH EVOLUTION
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### 📈 Entwicklung Gesamtvermögen"
        )


        df_history["Gesamtvermoegen"] = (
            df_history["Liquide_Mittel"]
            + df_history["Sparvermoegen"]
            + df_history["Boerse"]
            + df_history["Private_Vorsorge"]
            + df_history["LPP"]
        )


        fig_total = go.Figure()


        fig_total.add_trace(
            go.Scatter(
                x=df_history["Datum"],
                y=df_history["Gesamtvermoegen"],
                mode="lines+markers",
                name="Gesamtvermögen",
                line=dict(
                    width=4,
                    color="#2563eb"
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


        df_history["Liquidität"] = (
            df_history["Liquide_Mittel"]
        )

        df_history["Sparkapital_Klasse"] = (
            df_history["Sparvermoegen"]
        )

        df_history["Investments"] = (
            df_history["Boerse"]
        )

        df_history["Vorsorge_Privat"] = (
            df_history["Private_Vorsorge"]
        )

        df_history["Pensionskasse_Klasse"] = (
            df_history["LPP"]
        )


        fig_trend = go.Figure()


        fig_trend.add_trace(
            go.Scatter(
                x=df_history["Datum"],
                y=df_history["Liquidität"],
                name="Liquide Mittel",
                stackgroup="one",
                line=dict(
                    color="#2563eb"
                )
            )
        )


        fig_trend.add_trace(
            go.Scatter(
                x=df_history["Datum"],
                y=df_history["Sparkapital_Klasse"],
                name="Sparkapital",
                stackgroup="one",
                line=dict(
                    color="#38bdf8"
                )
            )
        )


        fig_trend.add_trace(
            go.Scatter(
                x=df_history["Datum"],
                y=df_history["Investments"],
                name="Investiertes Kapital",
                stackgroup="one",
                line=dict(
                    color="#f59e0b"
                )
            )
        )


        fig_trend.add_trace(
            go.Scatter(
                x=df_history["Datum"],
                y=df_history["Vorsorge_Privat"],
                name="Private Vorsorge",
                stackgroup="one",
                line=dict(
                    color="#10b981"
                )
            )
        )


        fig_trend.add_trace(
            go.Scatter(
                x=df_history["Datum"],
                y=df_history["Pensionskasse_Klasse"],
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