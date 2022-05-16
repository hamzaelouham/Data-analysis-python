from urllib import response
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
from plotly.subplots import make_subplots 
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

def getDataSets(arg):
    return pd.read_excel(arg)

data = getDataSets('datasets.xls')

#convert date to  mounth 

data["Month"] = data['Order Date'].dt.month

data['Month'] = pd.to_datetime(data['Month'], format='%m').dt.month_name().str.slice(stop=3)


geoloctionsDF = pd.DataFrame()

geoloctionsDF['city'] =  data['City'].unique()




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
orders = int(sales["Order Quantity"].sum())

left_column,middle_column,right_column = st.columns(3)

with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")

with right_column:
    st.subheader("Tolal profit:")
    st.subheader(f"US $ {total_profit}")
with  middle_column:
     st.subheader("Tolal Orders :")
     st.subheader(f"{orders}")

st.markdown("""---""")

#sales by mounth 


st.dataframe(sales)

sales_By_Mounths = (
    sales.groupby(by=['Month']).sum()['Sales']
)


fig_mounthly_sales = px.bar(
    sales_By_Mounths,
    x="Sales",
    y=sales_By_Mounths.index,
    orientation="h",
    title="<b> mounthly sales </b>",
    color_discrete_sequence=["#0083B8"] * len(sales_By_Mounths),
    template="plotly_white",
)


fig_mounthly_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


fig_shipMode = px.pie(sales, values='Sales', names='ShipMode',title='<b>Ship Mode chart</b>' )


#donut chart for Containers
figDuont1 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
figDuont1.add_trace(go.Pie(labels=sales['Container'], name="Packge container"),1, 1)
figDuont1.update_traces(hole=.4, hoverinfo="label+percent+name")

#donut chart for departements
figDuont2 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
figDuont2.add_trace(go.Pie(labels=sales['Department'], name="customer Departement"),1, 1)
figDuont2.update_traces(hole=.4, hoverinfo="label+percent+name")

#plot sales by product Name
sales_by_product_name = (sales.groupby(by=['Product name']).sum()['Sales'])
sales_by_product_name = sales_by_product_name.sort_values(ascending=False).head()

fig_sales_by_products = px.bar(sales_by_product_name, x='Sales',
    title="<b> Top 5 products Sales </b>",
    color_discrete_sequence=["#0083B8"] * len(sales_By_Mounths),
    template="plotly_white")

sales_profit = px.bar(sales.groupby(by=['Month']).sum()['Profit'],
    title="<b>profit every month </b>",
    color_discrete_sequence=["#0083B8"] * len(sales_By_Mounths),
    template="plotly_white"
)

#plot states in the map

statesLoctions = pd.read_csv('withLatLng.csv')

st.map(statesLoctions)

st.plotly_chart(fig_mounthly_sales)
st.plotly_chart(sales_profit)
st.plotly_chart(fig_sales_by_products)
st.plotly_chart(fig_shipMode)
st.write("Container charts")
st.plotly_chart(figDuont1)
st.write("departement charts")
st.plotly_chart(figDuont2)
