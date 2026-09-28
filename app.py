import pandas as pd
import numpy as np
import streamlit as st
from streamlit_float import float_init
from database import init_db, fetch_all_expenses
from utils import bar, pie, area, display_formatting, get_excel_bytes, footer
from ui_components import render_fab, add_expense_dialog, delete_expense_dialog, clear_all_dialog

st.set_page_config(page_title="Expense Tracker", layout="wide")
float_init()

init_db()   # Initialize Database

COLUMN_LIST = ["Date", "Time", "Name", "Amount", "Category", "Notes"]
ALL_CATEGORIES = ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 'Health', 'Travel', 'Education', 'Other']

df = fetch_all_expenses()

df_filter = df.copy()
if not df_filter.empty:
    df_filter["date_dt"] = pd.to_datetime(df_filter["Date"], format="%d-%b-%Y", errors="coerce")

if "theme_name" not in st.session_state:
    st.session_state.theme_name = "teal"

# =================== UI Related Stuff ===================

# Floating Action Button (FAB)
render_fab(df)

if "open_add_flag" in st.session_state and st.session_state.open_add_flag:
    st.session_state.open_add_flag = False
    add_expense_dialog(ALL_CATEGORIES)

if "open_delete_flag" in st.session_state and st.session_state.open_delete_flag:
    st.session_state.open_delete_flag = False
    if not df.empty:
        delete_expense_dialog(df, COLUMN_LIST)

if "show_clear_popup" in st.session_state and st.session_state.show_clear_popup:
    st.session_state.show_clear_popup = False
    clear_all_dialog()

# CSS Styles
st.markdown("""
<style>
.bloom-card {
    position: relative;
    overflow: hidden;
    padding: 72px 64px;
    border-radius: 32px;
    background: var(--secondary-background-color);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(59,130,246,0.45);
    color: var(--text-color) !important;
    text-align: center;
    text-shadow: 0px 1px 2px rgba(0, 0, 0, 0.2);
    margin-top: 50px;
    box-shadow: inset 0 0 50px rgba(59,130,246,0.18);
}
.shimmer {
    position: absolute;
    top: 0;
    left: -120%;
    width: 60%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    transform: skewX(-20deg);
}
.bloom-card:hover .shimmer {
    left: 150%;
    transition: left 0.9s ease-in-out;
}
.empty-title {
    color: var(--text-color) !important;
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 18px;
}
.empty-desc { font-size: 22px; opacity: 0.85; margin-bottom: 34px; }
.empty-bullets { max-width: 460px; margin: 0 auto; text-align: left; font-size: 18px; line-height: 1.7; opacity: 0.9; }
.empty-bullets li { margin-bottom: 10px; }
.empty-cta { margin-top: 34px; font-size: 17px; font-weight: 600; color: #7dd3fc; letter-spacing: 0.3px; }
.main-title { font-size: 4em; font-weight: 900; color: transparent; letter-spacing: 3px; -webkit-text-stroke: 1px black;
    text-shadow: 2px 2px 4px rgba(255,255,255,0.4); padding-bottom: 10px; margin-bottom: 0px; 
    background: linear-gradient(45deg, #eeeeee, #63c3a4, #eeeeee, #63c3a4, #eeeeee); background-clip: text; }
</style>
""", unsafe_allow_html=True)

# EMPTY PAGE STATE
if df.empty:
    st.markdown("""
<div class="bloom-card">
<div class="shimmer"></div>
<div class="empty-title" style="color: var(--text-color);">📊 Expense Tracker</div>
<div class="empty-desc">Start tracking your spendings</div>
<ul class="empty-bullets">
    <li>Add, delete, and manage expenses instantly</li>
    <li>Analyze spending by category and date</li>
    <li>Export filtered data to CSV or Excel</li>
</ul>
<div class="empty-cta">Start by clicking <b>“Actions”</b> in the bottom-right</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("\n\n---\n")

    dummy_cat = pd.DataFrame({
        "Category": ["Food", "Bills", "Shopping", "Health", "Others"],
        "Amount": np.random.randint(30, 80, 5)
    })
    col1, col2 = st.columns(2)
    col1.plotly_chart(bar(dummy_cat, 'Category', "Top 5 Expenses (Bar - Demo)", st.session_state.theme_name), width='stretch')
    col2.plotly_chart(pie(dummy_cat, 'Category', "Top 5 Expenses (Pie - Demo)", st.session_state.theme_name), width='stretch')

    dummy_dates = ["01-Jan-2025", "02-Jan-2025", "03-Jan-2025", "04-Jan-2025", "05-Jan-2025", "07-Jan-2025", "10-Jan-2025"]
    dummy_amounts = np.random.randint(10, 70, 7)
    fig_dummy_area = area(dummy_dates, dummy_amounts, 'Date', "Line Chart (Demo)")
    st.plotly_chart(fig_dummy_area, width='stretch')
    st.markdown("---")
    footer()
    st.stop()


def apply_style():
    col.markdown(f"""
    <div class="bloom-card" style="padding: 1px 1px; margin-top: 0px; max-height: 80px; min-height: 80px; border-radius: 10px;">
        <div class="shimmer"></div>
        <div class="empty-cta" style="font-size: 14px; margin-top: 17px;">{label}</div>
        <div class="empty-cta" style="font-size: 18px; margin-top: 0px; margin-bottom: 0px;">{val}</div>
    </div>
    """, unsafe_allow_html=True)

# =================== MAIN APP CONTENT ===================

st.markdown('<div class="main-title" style="-webkit-text-stroke: 3px">EXPENSE TRACKER</div>', unsafe_allow_html=True)
st.markdown('\n')

# df_filter
min_date = df_filter["date_dt"].min().date()
max_date = df_filter["date_dt"].max().date()

with st.expander("🔍 Filters/Search/Export", expanded=False):
    preset_col, _, date_col, _ = st.columns([2, 0.3, 3, 0.1])
    preset_list = ["None", "Last 7 Days", "This Month", "Last Month", "This Year", "Last Year"]
    preset = preset_col.selectbox("Preset", preset_list, index=0)

    start_date, end_date = min_date, max_date
    with date_col:
        if min_date == max_date:
            st.info(f"**Slider Disabled:** Only one date exists ({min_date.strftime('%d-%b-%Y')})")
        elif preset == "None":
            start_date, end_date = st.slider("Date Range", min_value=min_date, max_value=max_date, value=(min_date, max_date))
        else:
            st.info("Slider disabled: Date range is controlled by the selected preset.")

    cat_col, _, amt_col, _ = st.columns([2, 0.3, 3, 0.1])
    categories = sorted(df_filter["Category"].dropna().unique())
    selected_categories = cat_col.multiselect("Categories", options=categories)

    min_amt = int(df_filter["Amount"].min())
    max_amt = int(df_filter["Amount"].max())

    if min_amt == max_amt:
        amt_col.info(f"**Slider Disabled:** Only One Amount(₹{min_amt}) exists")
        amount_range = (min_amt, max_amt)
    else:
        amount_range = amt_col.slider("Amount Range", min_value=min_amt, max_value=max_amt, value=(min_amt, max_amt))

    search_col, csv_col, excel_col = st.columns([4, 1, 1])
    search_query = search_col.text_input("Search (Name / Notes)", placeholder="Search by name or notes")
    
    with csv_col:
        st.markdown("<br>", unsafe_allow_html=True)
        csv_placeholder = st.empty()
    
    with excel_col:
        st.markdown("<br>", unsafe_allow_html=True)
        excel_placeholder = st.empty()

# Apply Presets
today = max_date
today1 = pd.Timestamp.today().date()
if preset != "None":
    if preset == "Last 7 Days":
        start_date = max(today1 - pd.Timedelta(days=6), min_date)
        end_date = today1
    elif preset == "This Month":
        start_date = max(today.replace(day=1), min_date)
        end_date = today
    elif preset == "Last Month":
        last_month_end = today.replace(day=1) - pd.Timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        start_date = max(last_month_start, min_date)
        end_date = min(last_month_end, max_date)
    elif preset == "This Year":
        start_date = max(today.replace(month=1, day=1), min_date)
        end_date = today
    elif preset == "Last Year":
        last_year_start = today.replace(year=today.year - 1, month=1, day=1)
        last_year_end = today.replace(year=today.year - 1, month=12, day=31)
        start_date = max(last_year_start, min_date)
        end_date = min(last_year_end, max_date)

# Filter Dataframe
filtered_df = df_filter.copy()
start_ts, end_ts = pd.Timestamp(start_date), pd.Timestamp(end_date)
filtered_df = filtered_df[(filtered_df["date_dt"] >= start_ts) & (filtered_df["date_dt"] <= end_ts)]

if selected_categories:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
filtered_df = filtered_df[(filtered_df["Amount"] >= amount_range[0]) & (filtered_df["Amount"] <= amount_range[1])]

if search_query.strip():
    q = search_query.lower()
    filtered_df = filtered_df[filtered_df["Name"].str.lower().str.contains(q, na=False) | filtered_df["Notes"].str.lower().str.contains(q, na=False)]

filtered_df = filtered_df.reset_index(drop=True)

# Export Buttons
export_df = filtered_df.drop(columns=["date_dt", "id"], errors="ignore")
can_export = not filtered_df.empty
csv_placeholder.download_button("Export CSV", export_df.to_csv(index=False) if can_export else "", "expenses_filtered.csv", "text/csv", disabled=not can_export)
excel_placeholder.download_button("Export Excel", get_excel_bytes(export_df) if can_export else b"", "expenses_filtered.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", disabled=not can_export)

# Metrics
df_total = filtered_df['Amount'].sum() if not filtered_df.empty else 0
df_max = filtered_df['Amount'].max() if not filtered_df.empty else 0
df_group = filtered_df.groupby('Name')['Amount'].max()
df_max_name = f"({df_group.idxmax()})" if not df_group.empty else ""
df_len = len(filtered_df)


col1, _, col2, _, col3 = st.columns([2, 0.35, 2, 0.35 ,2])
for col, label, val in zip([col1, col2, col3], ["TOTAL SPENT", "HIGHEST EXPENSE", "TOTAL TRANSACTIONS"], [f"₹{df_total}", f"₹{df_max}{df_max_name}", df_len]):
    apply_style()


st.markdown('---')

# Main Table
df_show = display_formatting(filtered_df)
if not df_show.empty:
    st.dataframe(df_show)
else:
    st.info("No expenses match the current filters.")

# Charts-------------------
# 1. top 5
with st.expander("Top 5 Expenses", expanded=True):
    top5 = filtered_df.sort_values(by='Amount', ascending=False).head().reset_index(drop=True)
    if top5.empty:
        st.info("No data available.")
    else:
        tab1, tab2 = st.tabs(["📊 Charts", '📄 Table'])
        with tab1:
            c1, c2 = st.columns(2)
            c1.plotly_chart(bar(top5, 'Name', "Top 5 Expenses (Bar)", st.session_state.theme_name), width='stretch')
            c2.plotly_chart(pie(top5, 'Name', "Top 5 Expenses (Pie)", st.session_state.theme_name), width='stretch')
        with tab2:
            st.dataframe(display_formatting(top5))

# 2. cat
with st.expander("Category Overview"):
    cat = filtered_df.groupby('Category')['Amount'].sum().sort_values(ascending=False).reset_index()
    if cat.empty:
        st.info("No data available.")
    else:
        tab1, tab2, tab3 = st.tabs(["📊 Charts", '📈 Line Chart', '📄 Table'])
        with tab1:
            c1, c2 = st.columns(2)
            c1.plotly_chart(bar(cat.head(), 'Category', "Top Categories", st.session_state.theme_name), width='stretch')
            c2.plotly_chart(pie(cat.head(), 'Category', "Top Categories", st.session_state.theme_name), width='stretch')
        with tab2:
            if len(cat) > 2:
                st.plotly_chart(area(cat['Category'], cat['Amount'], 'Category', "Category-wise Spending"))
            else:
                st.info("Add at least 3 categories for a line chart.")
        with tab3:
            st.dataframe(display_formatting(cat))

# 3. date
with st.expander("Date Overview"):
    date_df = filtered_df.groupby("Date")['Amount'].sum().sort_values(ascending=False).reset_index()
    if date_df.empty:
        st.info("No data available.")
    else:
        tab1, tab2, tab3 = st.tabs(["📊 Charts", '📈 Line Chart', '📄 Table'])
        with tab1:
            c1, c2 = st.columns(2)
            c1.plotly_chart(bar(date_df.head(), 'Date', "Top Dates", st.session_state.theme_name), width='stretch')
            c2.plotly_chart(pie(date_df.head(), 'Date', "Top Dates", st.session_state.theme_name), width='stretch')
        with tab2:
            if len(date_df) > 2:
                st.plotly_chart(area(date_df['Date'], date_df['Amount'], 'Date', 'Spending Over Time'))
            else:
                st.info("Add at least 3 dates for a line chart.")
        with tab3:
            st.dataframe(display_formatting(date_df))

# Theme Toggle
_, col_theme, _ = st.columns([5,5,5])
if col_theme.button("Switch Theme", width='stretch'):
    st.session_state.theme_name = "teal" if st.session_state.theme_name != "teal" else "not teal"
    st.rerun()

st.markdown("---")
footer()