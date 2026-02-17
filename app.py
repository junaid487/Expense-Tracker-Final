import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_float import float_init
import io
import time as t
import gspread
from google.oauth2.service_account import Credentials


st.set_page_config(page_title="Expense Tracker", layout="wide")
float_init()

SPREADSHEET_ID = "12QYnLxNedt623UW80Q7hFOFT41sPRsVjKH7FRp_cfqk"
SHEET_NAME = "Sheet1"

#---------------------------------------
@st.cache_resource
def get_gs_client():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    return gspread.authorize(creds)

#------------------------------------
@st.cache_data(ttl=30)
def load_expenses_from_sheet():
    client = get_gs_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    records = sheet.get_all_records()
    if not records:
        return pd.DataFrame(columns=column_list)

    return pd.DataFrame(records)

#-----------------------------------------
def write_expenses_to_sheet(df):
    client = get_gs_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

    clean_df = (df.replace([np.inf, -np.inf], "").fillna(""))
    sheet.clear()
    sheet.update([clean_df.columns.values.tolist()] + clean_df.astype(str).values.tolist())

#------------------------------------------------------

column_list = ["Date", "Time", "Name", "Amount", "Category", "Notes"]
all_categories = ['Food','Transport','Shopping','Bills','Entertainment','Health','Travel','Education','Other']

df = load_expenses_from_sheet()

df_filter = df.copy()
df_filter["date_dt"] = pd.to_datetime(df_filter["Date"], format="%d-%m-%Y", errors="coerce")

#--------------Helper Functions------------
# bar chart
def bar(df,a,_title):
    fig = px.bar(df, x= a, y= 'Amount', title= _title, text= 'Amount', color= a, color_discrete_sequence=px.colors.sequential.Teal_r)    #qualitative.Set2
    fig.update_traces(width=0.6)
    return fig

# Pie chart
def pie(df,name,_title):
    fig = px.pie(df, names=name, values='Amount', title= _title, hole=0.4, color_discrete_sequence= px.colors.sequential.Teal_r)
    return fig

#Area chart
def area(a,b,x_title,_title):
    base_color = px.colors.sequential.Teal_r[0]
    fade_color = "rgba(34, 89, 121, 0.4)"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a, y=b, mode="lines", line=dict(color=base_color, width=2, shape="spline", smoothing=1.2), fill="tozeroy", fillcolor=fade_color))
    fig.add_trace(go.Scatter(x=a, y=b, mode="markers", marker=dict(size=7, color='lightgrey')))
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=350, showlegend=False, xaxis_title= x_title, yaxis_title="Amount", title= _title)
    return fig

# df
def display_formatting(df):
    df_display = df.copy()
    if "date_dt" in df_display.columns:
        df_display = df_display.drop(columns=["date_dt"])

    df_display['S.no'] = df_display.index + 1
    df_display['Amount'] = "₹" + df_display['Amount'].astype(str)

    if 'Date' in df_display.columns:
        df_display['Date'] = pd.to_datetime(df_display['Date'], format="%d-%m-%Y")
        df_display['Date'] = df_display['Date'].dt.strftime("%d-%b-%Y")

    df_display = df_display.set_index('S.no', drop=True)
    return df_display
#------------------------------------------------------------------

def get_excel_bytes(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Expenses")
    return buffer.getvalue()

#------------------------------------------------------------------
def footer():
    st.markdown("""
    <br>
    <p style="text-align:center; color:#555555; font-size:12px;">
        Built by <span style="font-weight:700; font-size:14px;">Junaid</span>
    </p>

    <p style="text-align:center; font-size:12px;">
        <a href="https://github.com/junaid487" target="_blank" style="color:#555555; text-decoration:none;">GitHub  |  </a> 
        <a href="https://junaid487.github.io/" target="_blank" style="color:#555555; text-decoration:none;">Portfolio  |  </a>
        <a href="https://www.linkedin.com/in/junaid-alam-81aba93a8/" target="_blank" style="color:#555555; text-decoration:none;">LinkedIn</a>
    </p>    """, unsafe_allow_html=True)

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

        if st.button("➕ Add Expense", type= "secondary", width= 'stretch'):
            st.session_state.open_add_flag = True
            toggle_fab_menu()
            st.rerun()
            
        if st.button("🗑️ Delete Expense", type= "secondary", disabled= df.empty, width= 'stretch'):
            st.session_state.open_delete_flag = True
            toggle_fab_menu()
            st.rerun()
            
        if st.button("🔥 Clear All", type= "secondary", disabled= df.empty, width= 'stretch'):
            st.session_state.show_clear_popup = True
            toggle_fab_menu()
            st.rerun()
            
    main_button_label = "❌ Close Menu" if st.session_state.show_fab_menu else "➕ Actions"
    st.button(main_button_label, on_click=toggle_fab_menu, type= "primary")
    st.markdown('</div>', unsafe_allow_html=True)

fab_container.float("bottom: 15px; left: 25px; width: 170px; z-index: 1000;")

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
        category = input_col5.selectbox("Category", all_categories)
        notes = input_col6.text_input("Notes", placeholder="Optional...")

        button_col1, button_col2 = st.columns(2)

        if button_col1.button("Add", type="primary", width= 'stretch'):
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
                "Notes": notes.strip().title() if notes else ""
            }

            df2 = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df2_size = len(df2)

            duplicates = ["Date", "Name", "Amount", "Category", "Notes"]
            df2 = df2.drop_duplicates(subset=duplicates).reset_index(drop=True)
            write_expenses_to_sheet(df2)
            load_expenses_from_sheet.clear()


            if len(df2) == df2_size:
                st.session_state.show_add_popup = False
                st.toast("Expense Added Successfully")
                t.sleep(0.5)
                st.rerun()
            else:
                error_text.error("❗ Expense already Added, pls try different values. Or if you want duplicates try adding Notes")

        if button_col2.button("Cancel", width= 'stretch'):
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
        delete_col, cancel_col = st.columns(2)

        if delete_col.button("Delete", type="primary", width= 'stretch'):
            idx = df_local[df_local["label"] == choice]["index"].iloc[0]
            df2 = df_local.drop(idx).reset_index(drop=True)
            df2 = df2[column_list]
            write_expenses_to_sheet(df2)
            load_expenses_from_sheet.clear()
            st.toast("Expense Deleted successfully")
            t.sleep(0.5)
            st.session_state.show_delete = False
            st.rerun()

        if cancel_col.button("Cancel", width= 'stretch'):
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
            write_expenses_to_sheet(pd.DataFrame(columns=column_list))
            load_expenses_from_sheet.clear()

            st.session_state.clear_all_flag = False
            st.toast("All expenses cleared")

            st.rerun()


        if col2.button("Cancel"):
            st.session_state.clear_all_flag = False
            st.rerun()

    confirmation_popup()


#--------------------EMPTY PAGE----------------------
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

    box-shadow:
        inset 0 0 50px rgba(59,130,246,0.18);
}

.shimmer {
    position: absolute;
    top: 0;
    left: -120%;
    width: 60%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255,255,255,0.08),
        transparent
    );
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

.empty-desc {
    font-size: 22px;
    opacity: 0.85;
    margin-bottom: 34px;
}

.empty-bullets {
    max-width: 460px;
    margin: 0 auto;
    text-align: left;
    font-size: 18px;
    line-height: 1.7;
    opacity: 0.9;
}

.empty-bullets li {
    margin-bottom: 10px;
}

.empty-cta {
    margin-top: 34px;
    font-size: 17px;
    font-weight: 600;
    color: #7dd3fc;
    letter-spacing: 0.3px;
}
</style>
""", unsafe_allow_html=True)


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

<div class="empty-cta">
    Start by clicking <b>“Actions”</b> in the bottom-right
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

    col1.plotly_chart(bar(dummy_cat, 'Category', "Top 5 Expenses (Bar - Demo)"), width='stretch')
    col2.plotly_chart(pie(dummy_cat, 'Category', "Top 5 Expenses (Pie - Demo)"), width='stretch')

    # ---------- AREA CHART ----------
    dummy_dates = ["01-Jan-2025", "02-Jan-2025", "03-Jan-2025", "04-Jan-2025", "05-Jan-2025", "07-Jan-2025", "10-Jan-2025"]
    dummy_amounts = np.random.randint(10, 80, 7)

    fig_dummy_area = area(dummy_dates, dummy_amounts, 'Date', "Line Chart (Demo)", )
    fig_dummy_area.update_layout(title="Line Chart (Demo)")
    st.plotly_chart(fig_dummy_area, width='stretch')
    st.markdown("---")
    footer()
    st.stop()


#=========================== Main APP ==========================#

#------------Page Title----------------
st.markdown("""
<style>
.main-title { font-size: 4em; font-weight: 900; color: transparent; letter-spacing: 3px; -webkit-text-stroke: 1px black;
    text-shadow: 2px 2px 4px rgba(255,255,255,0.4); padding-bottom: 10px; margin-bottom: 0px; 
    background: linear-gradient(45deg, #eeeeee, #63c3a4, #eeeeee, #63c3a4, #eeeeee); background-clip: text; }
</style>
<div class="main-title" style="-webkit-text-stroke: 3px">EXPENSE TRACKER</div>
""", unsafe_allow_html=True)

st.markdown('\n')

start_date = None
end_date = None

#------------------------------------ Filters/Search/Export --------------------------------
min_date = df_filter["date_dt"].min().date()
max_date = df_filter["date_dt"].max().date()

with st.expander("🔍 Filters/Search/Export", expanded=False):

# ---------- DATE PRESET + RANGE ----------
    preset_col, _, date_col, _ = st.columns([2, 0.3, 3, 0.1])

    preset_list = ["None", "Last 7 Days", "This Month", "Last Month", "This Year", "Last Year"]
    preset = preset_col.selectbox("Preset", preset_list, index=0)

    with date_col:
        if min_date == max_date:
            st.info(f"**Slider Disabled:** Only one date exists ({min_date.strftime('%d-%b-%Y')})")
            start_date = min_date
            end_date = min_date

        elif preset == "None":
            start_date, end_date = st.slider("Date Range", min_value= min_date, max_value= max_date, value=(min_date, max_date))

        else:
            st.info("Slider disabled: Date range is controlled by the selected preset.")


    # ---------- CATEGORY + AMOUNT ----------
    cat_col, _, amt_col, _ = st.columns([2, 0.3, 3, 0.1])

    categories = sorted(df_filter["Category"].dropna().unique())

    selected_categories = cat_col.multiselect(
        "Categories",
        options=categories
    )

    if not df_filter.empty:
        min_amt = int(df_filter["Amount"].min())
        max_amt = int(df_filter["Amount"].max())

    else:
        min_amt = max_amt = 0

    if min_amt == max_amt:
        amt_col.info(f"**Slider Disabled:** Only One Amount(₹{min_amt}) exists")
        amount_range = (min_amt, max_amt)
    else:
        amount_range = amt_col.slider("Amount Range", min_value=min_amt, max_value=max_amt, value=(min_amt, max_amt))

    # ---------- SEARCH ----------
    search_col, csv_col, excel_col = st.columns([4, 1, 1])
    search_query = search_col.text_input("Search (Name / Notes)", placeholder="Search by name or notes")
    
    with csv_col:
        st.markdown("<br>", unsafe_allow_html=True)
        csv_placeholder = csv_col.empty()
    
    with excel_col:
        st.markdown("<br>", unsafe_allow_html=True)
        excel_placeholder = excel_col.empty()

st.markdown('\n')

# ---------- APPLY PRESET ----------
today = max_date
today1 = pd.Timestamp.today().date()

if preset != "None":

    if preset == "Last 7 Days":
        start_date = max(today1 - pd.Timedelta(days=6), min_date)
        end_date = today1

    elif preset == "This Month":
        start_date = max(
            today.replace(day=1),
            min_date
        )
        end_date = today

    elif preset == "Last Month":
        last_month_end = today.replace(day=1) - pd.Timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        start_date = max(last_month_start, min_date)
        end_date = min(last_month_end, max_date)

    elif preset == "This Year":
        start_date = max(
            today.replace(month=1, day=1),
            min_date
        )
        end_date = today

    elif preset == "Last Year":
        last_year_start = today.replace(year=today.year - 1, month=1, day=1)
        last_year_end = today.replace(year=today.year - 1, month=12, day=31)

        start_date = max(last_year_start, min_date)
        end_date = min(last_year_end, max_date)


#------------------------filtered-df--------------------------
filtered_df = df_filter.copy()

if start_date is not None and end_date is not None:
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)

    filtered_df = filtered_df[(filtered_df["date_dt"] >= start_ts) & (filtered_df["date_dt"] <= end_ts)]

if selected_categories:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]

filtered_df = filtered_df[(filtered_df["Amount"] >= amount_range[0]) & (filtered_df["Amount"] <= amount_range[1])]

if search_query.strip():
    q = search_query.lower()

    filtered_df = filtered_df[filtered_df["Name"].str.lower().str.contains(q, na=False) | filtered_df["Notes"].str.lower().str.contains(q, na=False)]

filtered_df = filtered_df.reset_index(drop=True)

#--------------------------------------------------------------
#Export buttons behaviour
export_df = filtered_df.drop(columns=["date_dt"], errors="ignore")
can_export = not filtered_df.empty


with csv_placeholder:
    st.download_button(
        label= "Export CSV",
        data= export_df.to_csv(index=False) if can_export else "",
        file_name= "expenses_filtered.csv",
        mime= "text/csv",
        disabled= not can_export,
        width= "stretch"
    )

with excel_placeholder:
    st.download_button(
        label= "Export Excel",
        data= get_excel_bytes(export_df) if can_export else b"",
        file_name= "expenses_filtered.xlsx",
        mime= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        disabled= not can_export,
        width= "stretch"
    )

#---------------Highest/Total etc---------
df_total = filtered_df['Amount'].sum() if not filtered_df.empty else 0
df_max = filtered_df['Amount'].max() if not filtered_df.empty else 0
df_group = filtered_df.groupby('Name')['Amount'].max()
df_max_name = f"({df_group.idxmax()})" if not df_group.empty else ""
df_len = len(filtered_df)

col1, _, col2, _, col3 = st.columns([2, 0.35, 2, 0.35 ,2])

col1.markdown(f"""
<div class="bloom-card" style="padding: 1px 1px; margin-top: 0px; max-height: 80px; min-height: 80px; border-radius: 10px;">
    <div class="shimmer"></div>
    <div class="empty-cta" style="font-size: 14px; margin-top: 17px;">TOTAL SPENT</div>
    <div class="empty-cta" style="font-size: 18px; margin-top: 0px; margin-bottom: 0px;">₹{df_total}</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="bloom-card" style="padding: 1px 1px;margin-top: 0px; max-height: 80px; min-height: 80px; border-radius: 10px;">
    <div class="shimmer"></div>
    <div class="empty-cta" style="font-size: 14px; margin-top: 17px;">HIGHEST EXPENSE</div>
    <div class="empty-cta" style="font-size: 18px; margin-top: 0px; margin-bottom: 0px;">₹{df_max}{df_max_name}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="bloom-card" style="padding: 1px 1px; margin-top: 0px; max-height: 80px; min-height: 80px; border-radius: 10px;">
    <div class="shimmer"></div>
    <div class="empty-cta" style="font-size: 14px; margin-top: 17px;">TOTAL TRANSACTIONS</div>
    <div class="empty-cta" style="font-size: 18px; margin-top: 0px; margin-bottom: 0px;">{df_len}</div>
</div>
""", unsafe_allow_html=True)
st.markdown('---')

#---------------MAin Table----------
df_show = display_formatting(filtered_df)
if not df_show.empty:
    st.dataframe(df_show)
else:
    st.info("No expenses match the current filters.")

#-----------------------------Charts/Tables/etc-----------------------------
#1. Top 5 Expenses
top5 = filtered_df.sort_values(by= 'Amount', ascending=False).head().reset_index(drop=True)

with st.expander("Top 5 Expenses", expanded=True):
    if top5.empty:
        st.info("No data available for TOP 5 with current filters.")

    else:
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
cat = filtered_df.groupby('Category')['Amount'].sum().sort_values(ascending=False).reset_index()
cat_chart = cat.head()

cat_table = cat.copy()
cat_table['Expense count'] = filtered_df.groupby("Category")["Amount"].count().reindex(cat_table['Category']).values
cat_table = cat_table.sort_values(by= 'Amount', ascending=False)

cat_line = filtered_df.groupby('Category')['Amount'].sum().reset_index()
x = cat_line['Category']
y = cat_line['Amount']

with st.expander("Category Overview"):
    if cat.empty:
        st.info("No data available for Category with current filters.")
    else:
        tab1, tab2, tab3 = st.tabs(["📊 Bar & Pie(Charts)", '📈 Line Chart', '📄 Table'])

        with tab1:
            col1, col2 = st.columns(2)
            col1.plotly_chart(bar(cat_chart, 'Category', "Top 5 Categories (Bar)"), width='stretch')
            col2.plotly_chart(pie(cat_chart, 'Category', "Top 5 Categories (Pie)"), width='stretch')

        with tab2:
            if len(y) > 2:
                st.plotly_chart(area(x,y, 'Category', "Category-wise Spending"))
            else:
                st.info("Not Enought Data, Add At Least 3 Different Categories for a Line Chart")
        with tab3:
            st.markdown('Top Categories by Amount (Table)')
            st.dataframe(display_formatting(cat_table))

# 3. Date.
date_df = filtered_df.groupby("Date")['Amount'].sum().sort_values(ascending=False).reset_index()
date_chart = date_df.head()
date_chart['Date'] = pd.to_datetime(date_chart['Date'], format="%d-%m-%Y", errors= 'coerce')
date_chart['Date'] = date_chart['Date'].dt.strftime("%d-%b-%Y")

date_line = filtered_df.groupby("Date")['Amount'].sum().reset_index()
date_line['Date'] = pd.to_datetime(date_line['Date'], format="%d-%m-%Y", errors= 'coerce')
date_line['Date'] = date_line['Date'].dt.strftime("%d-%b-%Y")
x = date_line['Date']
y = date_line['Amount']

date_table = date_df.copy()
date_table['Expense Count'] = filtered_df.groupby("Date")["Amount"].count().reindex(date_table['Date']).values


with st.expander("Date Overview"):
    if date_df.empty:
        st.info("No data available for Date with current filters.")
    else:
        tab1, tab2, tab3 = st.tabs(["📊 Bar & Pie(Charts)", '📈 Line Chart', '📄 Table'])

        with tab1:
            col1, col2 = st.columns(2)

            col1.plotly_chart(bar(date_chart, 'Date', "Top 5 Dates (Bar)"), width='stretch')
            col2.plotly_chart(pie(date_chart, 'Date', "Top 5 Dates (Pie)"), width='stretch')

        with tab2:
            if len(y) > 2:
                st.plotly_chart(area(x,y, 'Date', 'Spending Over Time'))
            else:
                st.info("Not Enought Data, Add At Least 3 Different Dates for a Line Chart")
        with tab3:
            st.markdown('Top Dates by Amount (Table)')
            st.dataframe(display_formatting(date_table))

st.markdown("---")

# _, col_help, _, = st.columns([5,5,5])
# col_help.button("How to use", use_container_width=True)


footer()