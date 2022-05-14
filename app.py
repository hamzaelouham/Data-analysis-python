import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


def getDataSets(arg):
    return pd.read_excel(arg)



data = getDataSets('datasets.xls')

data["Month"] = data['Order Date'].dt.month

chart_data = data.groupby(['Month']).sum()['Sales']

st.write('This is a chart')
st.bar_chart(chart_data)



