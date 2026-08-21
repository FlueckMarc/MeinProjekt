import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="寿",
    layout="wide"
)


# ============================================================
# SIDEBAR AUSBLENDEN
# ============================================================

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# CONFIGURATION
# ============================================================

SECRET_PASSWORD = "viper01"


# ============================================================
# LOGIN
# ============================================================

def check_password():

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.markdown(
        "<br><br>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:

        st.markdown(
            "## 寿 Privates Finanz-Dashboard"
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

    return False


# ============================================================
# APP STARTEN
# ============================================================

if check_password():

    st.switch_page(
        "pages/0_Uebersicht.py"
    )