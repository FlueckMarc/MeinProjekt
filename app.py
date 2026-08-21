import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💎",
    layout="wide"
)


# ============================================================
# CONFIGURATION
# ============================================================

SECRET_PASSWORD = "viper01"


# ============================================================
# SESSION STATE
# ============================================================

if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False


# ============================================================
# LOGIN-SEITE
# ============================================================

def login_page():

    st.markdown(
        "<br><br>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:

        st.markdown(
            "## 💎 Privates Finanz-Dashboard"
        )

        st.caption(
            "Bitte anmelden, um das Dashboard zu öffnen."
        )

        user_password = st.text_input(
            "Passwort",
            type="password",
            key="login_password"
        )

        if st.button(
            "Anmelden",
            type="primary"
        ):

            if user_password == SECRET_PASSWORD:

                st.session_state[
                    "password_correct"
                ] = True

                st.rerun()

            else:

                st.error(
                    "❌ Falsches Passwort."
                )


# ============================================================
# NICHT EINGELOGGT
# ============================================================

if not st.session_state["password_correct"]:

    login = st.Page(
        login_page,
        title="Login",
        default=True
    )

    pg = st.navigation(
        [login],
        position="hidden"
    )

    pg.run()


# ============================================================
# EINGELOGGT
# ============================================================

else:

    # ========================================================
    # SEITEN DEFINIEREN
    # ========================================================

    uebersicht = st.Page(
        "pages/0_Uebersicht.py",
        title="Übersicht",
        icon="💎",
        default=True
    )

    budget = st.Page(
        "pages/1_Budget.py",
        title="Budget",
        icon="💰"
    )

    hypothek = st.Page(
        "pages/2_Hypothek.py",
        title="Hypothek",
        icon="🏠"
    )

    prognose = st.Page(
        "pages/3_Prognose.py",
        title="Prognose",
        icon="🔮"
    )

    depot = st.Page(
        "pages/4_Depot.py",
        title="Depot",
        icon="📈"
    )


    # ========================================================
    # NAVIGATION OBEN
    # ========================================================

    pg = st.navigation(
        [
            uebersicht,
            budget,
            hypothek,
            prognose,
            depot
        ],
        position="top"
    )


    # ========================================================
    # ABMELDEN
    # ========================================================

    logout_col1, logout_col2 = st.columns(
        [6, 1]
    )

    with logout_col2:

        if st.button(
            "🔒 Abmelden"
        ):

            st.session_state[
                "password_correct"
            ] = False

            if "login_password" in st.session_state:
                del st.session_state[
                    "login_password"
                ]

            st.rerun()


    # ========================================================
    # AKTUELLE SEITE AUSFÜHREN
    # ========================================================

    pg.run()