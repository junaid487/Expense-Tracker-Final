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


#--------------------Main APP----------------
def display_formatting():
    df_display = df.copy()
    df_display['S.no'] = df_display.index + 1
    df_display = df_display.set_index('S.no', drop=True)
    df_display['Amount'] = "₹" + df_display['Amount'].astype(str)
    return df_display


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
df_show = display_formatting()
st.dataframe(df_show)

#-----------------------------Charts/Tables/etc-----------------------------
#1. Top 5 Expenses
top5 = df.groupby("Name")['Amount'].sum().sort_values(ascending=False).head().reset_index()

with st.expander("Top 5 Expenses", expanded=True):
    st.text('',help='you can always switch between Chart and Table mode using the tabs below')
    tab1, tab2 = st.tabs(["📊 Bar & Pie(Charts)", "📄 Table"])
    
    with tab1:
        col1, col2 = st.columns(2)

        # 1.a) bar
        fig_top_bar = px.bar(top5, x= 'Name', y= 'Amount', title="Top 5 Expenses (bar)", text="Amount",
                                    color="Name", color_discrete_sequence=px.colors.qualitative.Set2)

        # 1.b) Pie
        fig_top_pie = px.pie(top5, names='Name', values='Amount', title="Top 5 Categories (bar)",
                                hole=0.4, color="Name", color_discrete_sequence=px.colors.qualitative.Set2)

        col1.plotly_chart(fig_top_bar, width='stretch')
        col2.plotly_chart(fig_top_pie, width='stretch')

#2. Category
cat = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).head().reset_index()

with st.expander("Category Overview"):
    tab1, tab2 = st.tabs(["📊 Bar & Pie(Charts)", '📄 Table'])

    with tab1:
        col1, col2 = st.columns(2)

        #2.a) Bar
        fig_cat_bar = px.bar(cat, x='Category', y='Amount', title="Top 5 Categories (bar)", text="Amount",
                                    color="Category", color_discrete_sequence=px.colors.qualitative.Set2)

        #2.b) pie
        fig_cat_pie = px.pie(cat, names='Category', values='Amount', title="Top 5 Categories (pie)",
                            hole=0.4, color="Category", color_discrete_sequence=px.colors.qualitative.Set2)

        col1.plotly_chart(fig_cat_bar, width='stretch')
        col2.plotly_chart(fig_cat_pie, width='stretch')