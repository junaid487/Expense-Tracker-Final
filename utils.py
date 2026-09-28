import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import io

def get_theme(theme_name):
    if theme_name == "teal":
        return px.colors.sequential.Teal_r
    else:
        return px.colors.qualitative.Set2

def bar(df, a, _title, theme_name):    
    fig = px.bar(df, x=a, y='Amount', title=_title, text='Amount', color=a, color_discrete_sequence=get_theme(theme_name))
    fig.update_traces(width=0.6)
    return fig

def pie(df, name, _title, theme_name):
    fig = px.pie(df, names=name, values='Amount', title=_title, hole=0.4, color_discrete_sequence=get_theme(theme_name))
    return fig

def area(a, b, x_title, _title):
    base_color = px.colors.sequential.Teal_r[0]
    fade_color = "rgba(34, 89, 121, 0.4)"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a, y=b, mode="lines", line=dict(color=base_color, width=2, shape="spline", smoothing=1.2), fill="tozeroy", fillcolor=fade_color))
    fig.add_trace(go.Scatter(x=a, y=b, mode="markers", marker=dict(size=7, color='lightgrey')))
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=350, showlegend=False, xaxis_title=x_title, yaxis_title="Amount", title=_title)
    return fig

def display_formatting(df):
    df_display = df.copy()
    if "date_dt" in df_display.columns:
        df_display = df_display.drop(columns=["date_dt"])
    
    if "id" in df_display.columns:
        df_display = df_display.drop(columns=["id"])

    df_display['S.no'] = range(1, len(df_display) + 1)
    df_display['Amount'] = "₹" + df_display['Amount'].astype(str)

    if 'Date' in df_display.columns:
        df_display['Date'] = pd.to_datetime(df_display['Date'], format="%d-%b-%Y")
        df_display['Date'] = df_display['Date'].dt.strftime("%d-%b-%Y")

    
    df_display = df_display.set_index('S.no', drop=True)
    return df_display

def get_excel_bytes(df):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Expenses")
    return buffer.getvalue()

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
