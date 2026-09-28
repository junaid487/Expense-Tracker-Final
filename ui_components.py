import streamlit as st
import time as t
import mysql.connector

from database import insert_expense, delete_expense, clear_all_expenses


def render_fab(df):
    if "show_fab_menu" not in st.session_state:
        st.session_state.show_fab_menu = False

    def toggle_fab_menu():
        st.session_state.show_fab_menu = not st.session_state.show_fab_menu

    fab_container = st.container()

    with fab_container:
        st.markdown(
            '<div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end;">',
            unsafe_allow_html=True
        )

        if st.session_state.show_fab_menu:
            if st.button("➕ Add Expense", type="secondary", width="stretch"):
                st.session_state.open_add_flag = True
                toggle_fab_menu()
                st.rerun()

            if st.button("🗑️ Delete Expense", type="secondary", disabled=df.empty, width="stretch"):
                st.session_state.open_delete_flag = True
                toggle_fab_menu()
                st.rerun()

            if st.button("🔥 Clear All", type="secondary", disabled=df.empty, width="stretch"):
                st.session_state.show_clear_popup = True
                toggle_fab_menu()
                st.rerun()

        main_button_label = "❌ Close Menu" if st.session_state.show_fab_menu else "➕ Actions"
        st.button(main_button_label, on_click=toggle_fab_menu, type="primary")

        st.markdown("</div>", unsafe_allow_html=True)

    fab_container.float("bottom: 15px; left: 25px; width: 170px; z-index: 1000;")


@st.dialog("Add Expense")
def add_expense_dialog(all_categories):
    error_text = st.empty()

    input_col1, input_col2 = st.columns(2)
    input_col3, input_col4 = st.columns(2)
    input_col5, input_col6 = st.columns(2)

    name = input_col1.text_input("Name", placeholder="e.g., Taxi, Coffee...")
    amount = input_col2.number_input("Amount", min_value=0)
    time = input_col3.time_input("Time")
    date = input_col4.date_input("Date")
    category = input_col5.selectbox("Category", all_categories)
    notes = input_col6.text_input("Notes", placeholder="Optional...")

    button_col1, button_col2 = st.columns(2)

    if button_col1.button("Add", type="primary", width="stretch"):
        if not name.strip():
            error_text.error("❗ Name cannot be empty")
            return

        if amount <= 0:
            error_text.error("❗ Please enter a numeric amount greater than 0")
            return

        try:
            insert_expense(
                date=date,
                time=time,
                name=name.strip().title(),
                amount=int(amount),
                category=category,
                notes=notes.strip().title() if notes else ""
            )

            st.session_state.show_add_popup = False
            st.toast("Expense Added Successfully")
            t.sleep(0.4)
            st.rerun()

        except mysql.connector.Error:
            error_text.error("❗ Failed to add expense to the database.")


    if button_col2.button("Cancel", width="stretch"):
        st.session_state.show_add_popup = False
        st.rerun()


@st.dialog("Delete an Expense")
def delete_expense_dialog(df):
    st.write("Select an expense you want to delete")

    df_local = df.copy()
    df_local["label"] = (
        df_local["Date"] + " | " +
        df_local["Name"] + " | ₹" +
        df_local["Amount"].astype(str)
    )

    choice = st.selectbox("Expense:", df_local["label"])

    delete_col, cancel_col = st.columns(2)

    if delete_col.button("Delete", type="primary", width="stretch"):
        expense_id = int(df_local[df_local["label"] == choice]["id"].iloc[0])

        try:
            delete_expense(expense_id)

            st.toast("Expense Deleted Successfully")
            t.sleep(0.4)
            st.session_state.show_delete = False
            st.rerun()

        except mysql.connector.Error:
            st.error("❗ Failed to delete expense from the database.")

    if cancel_col.button("Cancel", width="stretch"):
        st.session_state.show_delete = False
        st.rerun()


@st.dialog("Confirm Clear All")
def clear_all_dialog():
    st.write("This will delete all expenses permanently.")
    st.write("Are you sure you want to proceed?")

    col1, col2 = st.columns(2)

    if col1.button("Yes, Clear All", type="primary"):
        try:
            clear_all_expenses()

            st.session_state.clear_all_flag = False
            st.toast("All expenses cleared")
            st.rerun()

        except mysql.connector.Error:
            st.error("❗ Failed to clear all expenses from the database.")

    if col2.button("Cancel"):
        st.session_state.clear_all_flag = False
        st.rerun()