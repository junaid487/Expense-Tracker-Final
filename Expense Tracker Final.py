# TODO 
# Next work on FAB - high priority --- Done
# Add Export actions 
# Then on filters if needed

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_float import *
import io
import matplotlib.pyplot as plt
import time as tm

st.set_page_config(page_title="Expense Tracker", layout="wide")
float_init()

#------------------------------------
filename = "expense_tracker.csv"
column_list = ["Date", "Time", "Name", "Amount", "Category", "Notes"]
categories = ['Food','Transport','Shopping','Bills','Entertainment','Health','Travel','Education','Other']

try:
    df = pd.read_csv(filename)
except:
    df = pd.DataFrame(columns=column_list)


#--------------Helper Functions------------
# bar chart
def bar(df,a,_title):
    fig = px.bar(df, x= a, y= 'Amount', title= _title, text= 'Amount', color= a, color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(width=0.6)
    return fig

# Pie chart
def pie(df,name,_title):
    fig = px.pie(df, names=name, values='Amount', title= _title, hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
    return fig

#Area chart
def area(a,b,x_title,_title):
    base_color = px.colors.qualitative.Set2[0]
    fade_color = "rgba(90, 196, 163, 0.2)"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a, y=b, mode="lines", line=dict(color=base_color, width=2, shape="spline", smoothing=1.2), fill="tozeroy", fillcolor=fade_color))
    fig.add_trace(go.Scatter(x=a, y=b, mode="markers", marker=dict(size=7, color='lightgrey')))
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=350, showlegend=False, xaxis_title= x_title, yaxis_title="Amount", title= _title)
    return fig

# df
def display_formatting(df):
    df_display = df.copy()
    df_display['S.no'] = df_display.index + 1
    df_display['Amount'] = "₹" + df_display['Amount'].astype(str)
    if 'Date' in df_display.columns:
        df_display['Date'] = pd.to_datetime(df_display['Date'], format="%d-%m-%Y")
        df_display['Date'] = df_display['Date'].dt.strftime("%d-%b-%Y")
    df_display = df_display.set_index('S.no', drop=True)
    return df_display


# =================== FLOATING ACTION BUTTON(FAB) ===================

if "show_fab_menu" not in st.session_state:
    st.session_state.show_fab_menu = False
if "open_add_flag" not in st.session_state:
    st.session_state.open_add_flag = False
if "open_delete_flag" not in st.session_state:
    st.session_state.open_delete_flag = False
if "clear_all_flag" not in st.session_state:
    st.session_state.clear_all_flag = False
if "show_clear_popup" not in st.session_state:
    st.session_state.show_clear_popup = False
if "show_add_popup" not in st.session_state:
    st.session_state.show_add_popup = False

#---------------------------------------------------
def toggle_fab_menu():
    st.session_state.show_fab_menu = not st.session_state.show_fab_menu

#---------------------------------------------------
fab_container = st.container()
with fab_container:
    st.markdown('<div style="text-align: right; display: flex; flex-direction: column; align-items: flex-end;">', unsafe_allow_html=True)
    if st.session_state.show_fab_menu:

        if st.button("➕ Add Expense", key="fab_add_expense", type="secondary", width='stretch'):
            st.session_state.open_add_flag = True
            toggle_fab_menu()
            st.rerun()
            
        if st.button("🗑️ Delete Expense", key="fab_delete_expense", type="secondary", disabled=df.empty, width='stretch'):
            st.session_state.open_delete_flag = True
            toggle_fab_menu()
            st.rerun()
            
        if st.button("🔥 Clear All", key="fab_clear_all", type="secondary", disabled=df.empty, width='stretch'):
            st.session_state.show_clear_popup = True
            toggle_fab_menu()
            st.rerun()
            
    main_button_label = "❌ Close Menu" if st.session_state.show_fab_menu else "➕ Actions"
    st.button(main_button_label, on_click=toggle_fab_menu, key="main_fab_toggle", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

fab_container.float("bottom: 20px; right: 20px; width: 170px; z-index: 1000;")

# ----------------- ADD EXPENSE DIALOG -----------------
if st.session_state.open_add_flag:
    st.session_state.show_add_popup = True
    st.session_state.open_add_flag = False

if st.session_state.show_add_popup:
    st.session_state.show_add_popup = False
    @st.dialog("Add Expense")
    def add_expense_popup():
        error_text = st.empty()

        input_col1, input_col2 = st.columns(2)
        input_col3, input_col4 = st.columns(2)
        input_col5, input_col6 = st.columns(2)

        name = input_col1.text_input("Name", placeholder="e.g., Taxi, Coffee...")
        amount = input_col2.number_input("Amount", min_value=0)
        time = input_col3.time_input("Time")
        date = input_col4.date_input("Date")
        category = input_col5.selectbox("Category", categories)
        notes = input_col6.text_input("Notes", placeholder="Optional...")

        button_col1, button_col2 = st.columns(2)

        if button_col1.button("Add", type="primary"):
            if not name.strip():
                error_text.error("❗ Name cannot be empty")
                return

            if amount <= 0:
                error_text.error("❗ Please enter a numeric amount greater than 0")
                return

            new_row = {
                "Date": date.strftime("%d-%m-%Y"),
                "Time": time.strftime("%H:%M"),
                "Name": name.strip().title(),
                "Amount": int(amount),
                "Category": category,
                "Notes": notes.strip().title() if notes else np.nan
            }

            df2 = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df2_size = len(df2)

            duplicates = ["Date", "Name", "Amount", "Category", "Notes"]
            df2 = df2.drop_duplicates(subset=duplicates).reset_index(drop=True)
            df2.to_csv(filename, index=False)

            if len(df2) == df2_size:
                st.session_state.show_add_popup = False
                st.toast("Expense Added Successfully")
                tm.sleep(0.5)
                st.rerun()
            else:
                error_text.error("❗ Expense already Added, pls try different values. Or if you want duplicates try adding Notes")

        if button_col2.button("Cancel"):
            st.session_state.show_add_popup = False
            st.rerun()

    add_expense_popup()

# ----------------- DELETE POPUP -----------------
if "show_delete" not in st.session_state:
    st.session_state.show_delete = False
if st.session_state.open_delete_flag and not df.empty:
    st.session_state.show_delete = True
    st.session_state.open_delete_flag = False

if st.session_state.show_delete:
    st.session_state.show_delete = False
    @st.dialog("Delete an Expense")
    def delete_expense_popup():
        st.write("Select an expense you want to delete")
        df_local = df.reset_index()
        df_local["label"] = df_local["Date"] + " | " + df_local["Name"] + " | ₹" + df_local["Amount"].astype(str)
        choice = st.selectbox("Expense:", df_local["label"])
        delete_col, empty_col1, empty_col2, cancel_col = st.columns(4)

        if delete_col.button("Delete", type="primary"):
            idx = df_local[df_local["label"] == choice]["index"].iloc[0]
            df2 = df_local.drop(idx).reset_index(drop=True)
            df2 = df2[column_list]
            df2.to_csv(filename, index=False)
            st.toast("Expense Deleted successfully")
            tm.sleep(0.5)
            st.session_state.show_delete = False
            st.rerun()

        if cancel_col.button("Cancel"):
            st.session_state.show_delete = False
            st.rerun()
            
    delete_expense_popup()

# ----------------- CLEAR ALL CONFIRMATION POPUP -----------------
if st.session_state.show_clear_popup:
    st.session_state.show_clear_popup = False

    @st.dialog("Confirm Clear All")
    def confirmation_popup():
        st.write("This will delete all expenses permanently.")
        st.write("Are you sure you want to proceed?")

        col1, col2 = st.columns(2)
        if col1.button("Yes, Clear All", type="primary"):
            df = pd.DataFrame(columns=column_list)
            df.to_csv(filename, index=False)
            st.toast("All expenses cleared")
            tm.sleep(0.5)
            st.session_state.clear_all_flag = False
            st.rerun()

        if col2.button("Cancel"):
            st.session_state.clear_all_flag = False
            st.rerun()

    confirmation_popup()


#--------------------EMPTY PAGE----------------------
st.markdown("""
<style>
.empty-card { padding: 80px; border-radius: 25px; background: linear-gradient(45deg, #63c3a488, #000000, #046276);
    text-align: center; color: lightyellow; margin-top: 40px; box-shadow: 0 0 5px rgba(255,255,255,0.35);}
.empty-title { font-size: 50px; margin-bottom: 20px; font-weight: bold; }
.empty-desc { font-size: 25px; opacity: 0.85; margin-bottom: 25px; }
.empty-bullets { font-size: 20px; text-align: left; margin: 0 auto; max-width: 350px; opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

if df.empty:
    st.markdown("""
    <div class="empty-card">
        <div class="empty-title">📊 WELCOME TO EXPENSE TRACKER</div>
        <div class="empty-desc">Start tracking your spendings.</div>
        <ul class="empty-bullets">
            <li>Add/Delete expenses using the Add button below</li>
            <li>View category and date summaries</li>
            <li>View and Interact with Line, Pie, and Bar Charts</li>
        </ul>
        <br>
        <div style="opacity:0.85;margin-top:15px;font-size:18px;color:yellow;">
            BEGIN BY ADDING YOUR FIRST EXPENSE USING THE "ACTIONS" BUTTON AT BOTTOM-RIGHT
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    st.markdown("---")

    dummy_cat = pd.DataFrame({
        "Category": ["Food", "Bills", "Shopping", "Health", "Others"],
        "Amount": np.random.randint(30,80,5)
    })
    col1, col2 = st.columns(2)

    col1.plotly_chart(bar(dummy_cat, 'Category', "Top 5 Expenses (Bar)"), width='stretch')
    col2.plotly_chart(pie(dummy_cat, 'Category', "Top 5 Expenses (Pie)"), width='stretch')

    # ---------- AREA CHART ----------
    dummy_dates = ["01-Jan-2025", "02-Jan-2025", "03-Jan-2025", "04-Jan-2025", "05-Jan-2025", "07-Jan-2025", "10-Jan-2025"]
    dummy_amounts = np.random.randint(10, 80, 7)

    fig_dummy_area = area(dummy_dates, dummy_amounts, 'Date', "Line Chart (Demo)", )
    fig_dummy_area.update_layout(title="Line Chart (Demo)")
    st.plotly_chart(fig_dummy_area, width='stretch')
    st.stop()


#=========================== Main APP ==========================#

#------------Page Title----------------
st.markdown("""
<style>
.main-title { font-size: 4em; font-weight: 900; color: transparent; letter-spacing: 3px; 
    text-shadow: 2px 2px 4px rgba(255,255,255,0.4); padding-bottom: 10px; margin-bottom: 0px; 
    background: linear-gradient(45deg, #eeeeee, #63c3a4, #eeeeee, #eeeeee, #eeeeee); background-clip: text; }
</style>
<div class="main-title">EXPENSE TRACKER</div>
""", unsafe_allow_html=True)

st.markdown('---')

#---------------Highest/Total etc---------
df_total = df['Amount'].sum()
df_max = df['Amount'].max()
df_group = df.groupby('Name')['Amount'].max()
df_max_name = df_group.idxmax()
df_len = len(df)

col1, emp1, col2, emp2, col3 = st.columns([2, 0.35, 2, 0.35 ,2])

col1.markdown(f"""
    <div style="padding: 10px; border-radius: 15px; background: linear-gradient(45deg, #63c3a488, #eeeeee, #046276); color: black; text-align: center; height: 100px;">
        <p style="margin-bottom: 3px; font-size: 18px; font-weight: bold;">💰 TOTAL SPENT</p>
        <h1 style="margin: 0; font-size: 26px;">₹{df_total}</h1>
    </div>
""", unsafe_allow_html=True)

col2.markdown(f"""
    <div style="padding: 10px; border-radius: 15px; background: linear-gradient(45deg, #046276, #eeeeee, #63c3a488); color: black; text-align: center; height: 100px;">
        <p style="margin-bottom: 3px; font-size: 18px; font-weight: bold;">📈 HIGHEST EXPENSE</p>
        <h1 style="margin: 0; font-size: 26px;">₹{df_max} ({df_max_name})</h1>
    </div>
""", unsafe_allow_html=True)

col3.markdown(f"""
    <div style="padding: 10px; border-radius: 15px; background: linear-gradient(45deg, #63c3a488, #eeeeee, #046276); color: black; text-align: center; height: 100px;">
        <p style="margin-bottom: 3px; font-size: 18px; font-weight: bold;">🔢 TOTAL TRANSACTIONS</p>
        <h1 style="margin: 0; font-size: 26px;">{df_len}</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown('---')

#---------------MAin Table----------
df_show = display_formatting(df)
st.dataframe(df_show)

#-----------------------------Charts/Tables/etc-----------------------------
#1. Top 5 Expenses
top5 = df.sort_values(by= 'Amount', ascending=False).head().reset_index(drop=True)

with st.expander("Top 5 Expenses", expanded=True):
    st.text('',help='you can always switch between Chart and Table mode using the tabs below')
    tab1, tab2 = st.tabs(["📊 Bar & Pie(Charts)", '📄 Table'])
    
    with tab1:
        col1, col2 = st.columns(2)

        col1.plotly_chart(bar(top5, 'Name', "Top 5 Expenses (Bar)"), width='stretch')
        col2.plotly_chart(pie(top5, 'Name', "Top 5 Expenses (Pie)"), width='stretch')

    with tab2:
        st.markdown('Top 5 Expenses (Table)')
        st.dataframe(display_formatting(top5))

#2. Category
cat = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).reset_index()
cat_chart = cat.head()

cat_table = cat.copy()
cat_table['Expense count'] = df.groupby("Category")["Amount"].count().reindex(cat_table['Category']).values
cat_table = cat_table.sort_values(by= 'Amount', ascending=False)

cat_line = df.groupby('Category')['Amount'].sum().reset_index()
x = cat_line['Category']
y = cat_line['Amount']

with st.expander("Category Overview"):
    tab1, tab2, tab3 = st.tabs(["📊 Bar & Pie(Charts)", '📈 Line Chart', '📄 Table'])

    with tab1:
        col1, col2 = st.columns(2)
        col1.plotly_chart(bar(cat_chart, 'Category', "Top 5 Categories (Bar)"), width='stretch')
        col2.plotly_chart(pie(cat_chart, 'Category', "Top 5 Categories (Pie)"), width='stretch')

    with tab2:
        if len(y) > 2:
            st.plotly_chart(area(x,y, 'Category', "Category-wise Spending"))
        else:
            st.error("❕ Not Enought Data, Add At Least 3 Different Categories for a Line Chart")
    with tab3:
        st.markdown('Top Categories by Amount (Table)')
        st.dataframe(display_formatting(cat_table))

# 3. Date
date_df = df.groupby("Date")['Amount'].sum().sort_values(ascending=False).reset_index()
date_chart = date_df.head()
date_chart['Date'] = pd.to_datetime(date_chart['Date'], format="%d-%m-%Y", errors= 'coerce')
date_chart['Date'] = date_chart['Date'].dt.strftime("%d-%b-%Y")

date_line = df.groupby("Date")['Amount'].sum().reset_index()
date_line['Date'] = pd.to_datetime(date_line['Date'], format="%d-%m-%Y", errors= 'coerce')
date_line['Date'] = date_line['Date'].dt.strftime("%d-%b-%Y")
x = date_line['Date']
y = date_line['Amount']

date_table = date_df.copy()
date_table['Expense Count'] = df.groupby("Date")["Amount"].count().reindex(date_table['Date']).values


with st.expander("Date Overview"):
    tab1, tab2, tab3 = st.tabs(["📊 Bar & Pie(Charts)", '📈 Line Chart', '📄 Table'])

    with tab1:
        col1, col2 = st.columns(2)

        col1.plotly_chart(bar(date_chart, 'Date', "Top 5 Dates (Bar)"), width='stretch')
        col2.plotly_chart(pie(date_chart, 'Date', "Top 5 Dates (Pie)"), width='stretch')

    with tab2:
        if len(y) > 2:
            st.plotly_chart(area(x,y, 'Date', 'Spending Over Time'))
        else:
            st.error("❕ Not Enought Data, Add At Least 3 Different Dates for a Line Chart")
    with tab3:
        st.markdown('Top Dates by Amount (Table)')
        st.dataframe(display_formatting(date_table))


