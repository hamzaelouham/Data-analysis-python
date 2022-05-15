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



#filter by Shipping mode
ship = st.sidebar.multiselect(
    "select ship mode  :",
    options=data["ShipMode"].unique(),
    default=data["ShipMode"].unique()
)


#filter by category 
category = st.sidebar.multiselect(
    "select products category :",
    options=data["Category"].unique(),
    default=data["Category"].unique()
)

department = st.sidebar.multiselect(
    "select Customer department :",
    options=data["Department"].unique(),
    default=data["Department"].unique()
)

# filter by region 
region =  st.sidebar.multiselect(
    "filter by  Customer region :",
    options=data["Region"].unique(),
    default=data["Region"].unique()
)

container = st.sidebar.multiselect(
    "filter by  container :",
    options=data["Container"].unique(),
    default=data["Container"].unique()
)


sales =  data.query(
    "Month == @salesbymounth & ShipMode == @ship & Category == @category & Department == @department & Region == @region & Container == @container "
)

# styling dasboard
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

total_sales = int(sales["Sales"].sum())
total_profit = int(sales["Profit"].sum())

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")

with right_column:
    st.subheader("Tolal profit:")
    st.subheader(f"US $ {total_profit}")

st.markdown("""---""")


st.dataframe(sales)
