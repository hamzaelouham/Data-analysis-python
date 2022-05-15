from unicodedata import category
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


def getDataSets(arg):
    return pd.read_excel(arg)


data = getDataSets('datasets.xls')

data["Month"] = data['Order Date'].dt.month

data['Month'] = pd.to_datetime(data['Month'], format='%m').dt.month_name().str.slice(stop=3)


#ounth_data = data.groupby(['Month']).sum()['Sales']

#filter by mounth sales data

st.sidebar.header("Please Filter Here:")

salesbymounth =  st.sidebar.multiselect(
    "select mounth :",
    options=data["Month"].unique(),
    default=data["Month"].unique()
)

shipModeOptions = data['ShipMode'].unique()

#filter by Shipping mode
ship = st.sidebar.selectbox(
    "select ship mode  :",
    shipModeOptions
)

#filter by category 
category = st.sidebar.multiselect(
    "select products category :",
    options=data["Category"].unique(),
    default=data["Category"].unique()
)




sales =  data.query(
    "Month == @salesbymounth & ShipMode == @ship & Category == @category"
)

st.dataframe(sales)
