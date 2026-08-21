import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# ============================================================
# KONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Budget",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# DATEIEN
# ============================================================


DATA_FILE = "budgetdaten.csv"
CATEGORY_FILE = "budget_kategorien.csv"


# ============================================================
# STANDARD-KATEGORIEN
# ============================================================

DEFAULT_CATEGORIES = {
    "Einnahmen": [
        "Bruttolohn",
        "Weitere Einnahmen"
    ],
    "Abzüge": [
        "Sozialabgaben",
        "Steuern"
    ],
    "Ausgaben": [
        "Wohnen / Hypothek / Miete",
        "Krankenkasse",
        "Auto / Transport",
        "Lebensmittel",
        "Freizeit",
        "Versicherungen",
        "Telefon / Internet",
        "Sonstiges"
    ]
}


# ============================================================
# KATEGORIEN LADEN
# ============================================================

def load_categories():

    if not os.path.exists(CATEGORY_FILE):

        rows = []

        for group, categories in DEFAULT_CATEGORIES.items():

            for category in categories:

                rows.append({
                    "Kategorie": category,
                    "Gruppe": group
                })

        category_df = pd.DataFrame(rows)

        category_df.to_csv(
            CATEGORY_FILE,
            index=False
        )

        return category_df

    return pd.read_csv(CATEGORY_FILE)


categories_df = load_categories()


# ============================================================
# DATEN LADEN
# ============================================================

def load_data():

    if not os.path.exists(DATA_FILE):

        return pd.DataFrame()

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        return df

    df["Datum"] = pd.to_datetime(
        df["Datum"]
    )

    return df.sort_values(
        "Datum"
    ).reset_index(drop=True)


df = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("💰 Budget & Cashflow")

st.caption(
    "Monatliche Einnahmen, Abzüge, Ausgaben und Sparquote"
)


# ============================================================
# KATEGORIEN VERWALTEN
# ============================================================

with st.expander("⚙️ Kategorien verwalten"):

    st.markdown(
        "Hier kannst du eigene Einnahmen oder Ausgaben "
        "hinzufügen oder bestehende Kategorien löschen."
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # NEUE KATEGORIE
    # --------------------------------------------------------

    with col1:

        st.markdown("#### ➕ Kategorie hinzufügen")

        new_category = st.text_input(
            "Name der Kategorie"
        )

        new_group = st.selectbox(
            "Bereich",
            [
                "Einnahmen",
                "Abzüge",
                "Ausgaben"
            ]
        )

        if st.button(
            "➕ Kategorie hinzufügen"
        ):

            if new_category.strip() == "":

                st.warning(
                    "Bitte einen Namen eingeben."
                )

            elif new_category in categories_df["Kategorie"].values:

                st.warning(
                    "Diese Kategorie existiert bereits."
                )

            else:

                new_row = pd.DataFrame([{
                    "Kategorie": new_category.strip(),
                    "Gruppe": new_group
                }])

                categories_df = pd.concat(
                    [
                        categories_df,
                        new_row
                    ],
                    ignore_index=True
                )

                categories_df.to_csv(
                    CATEGORY_FILE,
                    index=False
                )

                st.success(
                    f"Kategorie '{new_category}' hinzugefügt."
                )

                st.rerun()

    # --------------------------------------------------------
    # KATEGORIE LÖSCHEN
    # --------------------------------------------------------

    with col2:

        st.markdown("#### 🗑️ Kategorie löschen")

        category_to_delete = st.selectbox(
            "Kategorie auswählen",
            categories_df["Kategorie"].tolist()
        )

        if st.button(
            "🗑️ Kategorie löschen"
        ):

            categories_df = categories_df[
                categories_df["Kategorie"]
                != category_to_delete
            ]

            categories_df.to_csv(
                CATEGORY_FILE,
                index=False
            )

            st.success(
                f"'{category_to_delete}' wurde gelöscht."
            )

            st.rerun()


# ============================================================
# MONAT AUSWÄHLEN / ERSTELLEN
# ============================================================

st.markdown("---")

st.markdown("### 📝 Monatsbudget")

input_date = st.date_input(
    "Monat auswählen",
    datetime.now()
)

selected_date = pd.to_datetime(
    input_date
)


# ============================================================
# VORHANDENE DATEN DES MONATS
# ============================================================

existing_row = None

if not df.empty:

    matching = df[
        df["Datum"] == selected_date
    ]

    if not matching.empty:

        existing_row = matching.iloc[0]


# ============================================================
# EINGABEN
# ============================================================

income_values = {}
deduction_values = {}
expense_values = {}


col1, col2, col3 = st.columns(3)


# ============================================================
# EINNAHMEN
# ============================================================

with col1:

    st.markdown("### 💵 Einnahmen")

    income_categories = categories_df[
        categories_df["Gruppe"] == "Einnahmen"
    ]["Kategorie"].tolist()

    for category in income_categories:

        old_value = 0.0

        if existing_row is not None:
            if category in existing_row.index:
                old_value = float(
                    existing_row[category]
                )

        income_values[category] = st.number_input(
            category,
            min_value=0.0,
            value=old_value,
            step=100.0,
            key=f"income_{category}"
        )


# ============================================================
# ABZÜGE
# ============================================================

with col2:

    st.markdown("### 🧾 Abzüge")

    deduction_categories = categories_df[
        categories_df["Gruppe"] == "Abzüge"
    ]["Kategorie"].tolist()

    for category in deduction_categories:

        old_value = 0.0

        if existing_row is not None:
            if category in existing_row.index:
                old_value = float(
                    existing_row[category]
                )

        deduction_values[category] = st.number_input(
            category,
            min_value=0.0,
            value=old_value,
            step=50.0,
            key=f"deduction_{category}"
        )


# ============================================================
# AUSGABEN
# ============================================================

with col3:

    st.markdown("### 💸 Ausgaben")

    expense_categories = categories_df[
        categories_df["Gruppe"] == "Ausgaben"
    ]["Kategorie"].tolist()

    for category in expense_categories:

        old_value = 0.0

        if existing_row is not None:
            if category in existing_row.index:
                old_value = float(
                    existing_row[category]
                )

        expense_values[category] = st.number_input(
            category,
            min_value=0.0,
            value=old_value,
            step=50.0,
            key=f"expense_{category}"
        )


# ============================================================
# BERECHNUNG
# ============================================================

gross_income = sum(
    income_values.values()
)

total_deductions = sum(
    deduction_values.values()
)

net_income = (
    gross_income
    - total_deductions
)

total_expenses = sum(
    expense_values.values()
)

available_money = (
    net_income
    - total_expenses
)

if net_income > 0:

    savings_rate = (
        available_money
        / net_income
        * 100
    )

else:

    savings_rate = 0


# ============================================================
# VORSCHAU
# ============================================================

st.markdown("---")

st.markdown("### 📊 Monatsübersicht")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Bruttoeinnahmen",
    f"{gross_income:,.0f} CHF"
)

c2.metric(
    "Abzüge",
    f"-{total_deductions:,.0f} CHF"
)

c3.metric(
    "Nettoeinnahmen",
    f"{net_income:,.0f} CHF"
)

c4.metric(
    "Ausgaben",
    f"-{total_expenses:,.0f} CHF"
)

c5.metric(
    "💰 Überschuss",
    f"{available_money:,.0f} CHF",
    f"{savings_rate:.1f}% Sparquote"
)


# ============================================================
# SPEICHERN
# ============================================================

if st.button(
    "💾 Monat speichern",
    type="primary"
):

    new_data = {
        "Datum": selected_date
    }

    new_data.update(
        income_values
    )

    new_data.update(
        deduction_values
    )

    new_data.update(
        expense_values
    )

    new_row = pd.DataFrame([
        new_data
    ])

    # Alten Monat entfernen
    if not df.empty:

        df = df[
            df["Datum"] != selected_date
        ]

    # Neuer Monat hinzufügen
    df = pd.concat(
        [
            df,
            new_row
        ],
        ignore_index=True
    )

    df = df.sort_values(
        "Datum"
    )

    df.to_csv(
        DATA_FILE,
        index=False
    )

    st.success(
        f"💾 Budget für "
        f"{selected_date.strftime('%B %Y')} "
        f"gespeichert."
    )

    st.rerun()


# ============================================================
# HISTORISCHE ENTWICKLUNG
# ============================================================

if not df.empty:

    st.markdown("---")

    st.markdown(
        "### 📈 Historische Entwicklung"
    )

    history = []

    for _, row in df.iterrows():

        gross = 0
        deductions = 0
        expenses = 0

        for category in categories_df[
            categories_df["Gruppe"] == "Einnahmen"
        ]["Kategorie"]:

            if category in row.index:
                gross += float(
                    row[category]
                )

        for category in categories_df[
            categories_df["Gruppe"] == "Abzüge"
        ]["Kategorie"]:

            if category in row.index:
                deductions += float(
                    row[category]
                )

        for category in categories_df[
            categories_df["Gruppe"] == "Ausgaben"
        ]["Kategorie"]:

            if category in row.index:
                expenses += float(
                    row[category]
                )

        net = gross - deductions
        saving = net - expenses

        if net > 0:
            rate = saving / net * 100
        else:
            rate = 0

        history.append({

            "Datum": row["Datum"],

            "Einnahmen": net,

            "Ausgaben": expenses,

            "Überschuss": saving,

            "Sparquote": rate
        })

    history_df = pd.DataFrame(
        history
    )


    # --------------------------------------------------------
    # EINNAHMEN / AUSGABEN
    # --------------------------------------------------------

    fig = px.line(
        history_df,
        x="Datum",
        y=[
            "Einnahmen",
            "Ausgaben",
            "Überschuss"
        ],
        markers=True,
        labels={
            "value": "CHF",
            "variable": "Kategorie"
        }
    )

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # SPARQUOTE
    # --------------------------------------------------------

    st.markdown(
        "### 📊 Sparquote"
    )

    fig_savings = px.line(
        history_df,
        x="Datum",
        y="Sparquote",
        markers=True,
        labels={
            "Sparquote": "Sparquote (%)"
        }
    )

    st.plotly_chart(
        fig_savings,
        use_container_width=True
    )


# ============================================================
# AUSGABENVERTEILUNG
# ============================================================

if not df.empty:

    latest = df.iloc[-1]

    expense_categories = categories_df[
        categories_df["Gruppe"] == "Ausgaben"
    ]["Kategorie"].tolist()

    expense_data = []

    for category in expense_categories:

        if category in latest.index:

            value = float(
                latest[category]
            )

            if value > 0:

                expense_data.append({

                    "Kategorie": category,

                    "Betrag": value
                })

    if expense_data:

        expense_df = pd.DataFrame(
            expense_data
        )

        st.markdown(
            "### 🍕 Ausgabenverteilung"
        )

        fig_pie = px.pie(
            expense_df,
            values="Betrag",
            names="Kategorie",
            hole=0.4
        )

        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )


# ============================================================
# HISTORISCHE TABELLE
# ============================================================

if not df.empty:

    st.markdown("---")

    st.markdown(
        "### 🗒️ Historische Budgetdaten"
    )

    st.dataframe(
        df.sort_values(
            "Datum",
            ascending=False
        ),
        use_container_width=True
    )


# ============================================================
# MONAT LÖSCHEN
# ============================================================

if not df.empty:

    st.markdown("---")

    st.markdown(
        "### 🗑️ Monat löschen"
    )

    available_dates = (
        df["Datum"]
        .dt.strftime("%Y-%m-%d")
        .tolist()
    )

    delete_date = st.selectbox(
        "Monat auswählen",
        available_dates
    )

    if st.button(
        "❌ Monat endgültig löschen"
    ):

        df = df[
            df["Datum"]
            != pd.to_datetime(delete_date)
        ]

        df.to_csv(
            DATA_FILE,
            index=False
        )

        st.success(
            f"Budget für {delete_date} gelöscht."
        )

        st.rerun()