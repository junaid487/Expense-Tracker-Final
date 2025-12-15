import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_float import *
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expense Tracker", layout="wide")

#------------------------------------
filename = "expense_tracker.csv"
column_list = ['S.no', "Date", "Time", "Name", "Amount", "Category", "Notes"]
categories = ['Food','Transport','Shopping','Bills','Entertainment','Health','Travel','Education','Other']

try:
    df = pd.read_csv(filename)
except:
    df = pd.DataFrame(columns=column_list)


#--------------------EMPTY PAGE----------------------

#------------------------------------------------------


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

#--------------------Main APP----------------

#------------Page Title----------------
st.header('EXPENSE TRACKER')
st.markdown('---')

#---------------Highest/Total etc---------
df_total = df['Amount'].sum()
df_max = df['Amount'].max()
df_group = df.groupby('Name')['Amount'].max()
df_max_name = df_group.idxmax()
df_len = len(df)

col1, col2, col3 = st.columns(3)

col1.metric("Total Spent", "₹" + str(df_total))
col2.metric("Highest Expense", "₹" + str(df_max), df_max_name)
col3.metric("Total Count", df_len)
st.markdown('---')

#---------------MAin Table----------
df_show = display_formatting(df)
st.dataframe(df_show)

#-----------------------------Charts/Tables/etc-----------------------------
#1. Top 5 Expenses
top5 = df.sort_values('Amount', ascending=False).head().reset_index()

with st.expander("Top 5 Expenses", expanded=True):
    st.text('',help='you can always switch between Chart and Table mode using the tabs below')
    tab1, tab2 = st.tabs(["📊 Bar & Pie(Charts)", "📄 Table"])
    
    with tab1:
        col1, col2 = st.columns(2)

        col1.plotly_chart(bar(top5, 'Name', "Top 5 Expenses (Bar)"), width='stretch')
        col2.plotly_chart(pie(top5, 'Name', "Top 5 Expenses (Pie)"), width='stretch')

    with tab2:
        top5_table = top5.drop('index', axis=1)
        st.markdown('Top 5 Expenses (Table)')
        st.dataframe(display_formatting(top5_table))

#2. Category
cat = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).reset_index()
cat_chart = cat.head()

with st.expander("Category Overview"):
    tab1, tab2 = st.tabs(["📊 Bar & Pie(Charts)", '📄 Table'])

    with tab1:
        col1, col2 = st.columns(2)

        col1.plotly_chart(bar(cat_chart, 'Category', "Top 5 Categories (Bar)"), width='stretch')
        col2.plotly_chart(pie(cat_chart, 'Category', "Top 5 Categories (Pie)"), width='stretch')
        
    with tab2:
        st.markdown('Top Categories by Amount (Table)')
        st.dataframe(display_formatting(cat))

# 3. Date
date_df = df.groupby("Date")['Amount'].sum().sort_values(ascending=False).reset_index()
date_chart = date_df.head()
date_chart['Date'] = pd.to_datetime(date_chart['Date'], format="%d-%m-%Y", errors= 'coerce')
date_chart['Date'] = date_chart['Date'].dt.strftime("%d-%b-%Y")

# df_date_count = pd.DataFrame(date_df)
# df_date_count["Number of Expenses"] = df.groupby("Date")["Amount"].count().values
# df_date_count = df_date_count.sort_values(by= 'Amount', ascending=False).reset_index(drop=True)


with st.expander("Date Overview"):
    tab1, tab2 = st.tabs(["📊 Bar & Pie(Charts)", '📄 Table'])

    with tab1:
        col1, col2 = st.columns(2)

        col1.plotly_chart(bar(date_chart, 'Date', "Top 5 Dates (Bar)"), width='stretch')
        col2.plotly_chart(pie(date_chart, 'Date', "Top 5 Dates (Pie)"), width='stretch')

    with tab2:
        st.markdown('Top Dates by Amount (Table)')
        st.dataframe(display_formatting(date_df))
