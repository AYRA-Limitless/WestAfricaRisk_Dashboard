import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

st.title("WBG Piooneers - Country Risk Dashboard")
st.subheader("West African (ECOWAS) Country Risk Analysis")
st.write("This dashboard provides insights into country risk factors and their impact on global development. Explore the data and visualize trends to make informed decisions.")

df=pd.read_csv("risk_scores2024.csv")
st.subheader("Risk Scores and Categories for West African Countries (2024)")

# function to color cells based on risk category
def color_risk(val):
    if val == "Low Risk":
        color = "background-color: #1cfa50"

    elif val == "Medium Risk":
        color = "background-color: #fcb32d"

    else:
        color = "background-color: #fa3748"
    return color

#Apply the color function to the risk category column and display the styled dataframe in Streamlit
st.dataframe(df[["country name", "risk score","risk category"]].sort_values("risk score", ascending=True).style.map(color_risk, subset=["risk category"]))

# combo list to show country risks details
st.subheader("Country Detail")
selected_country= st.selectbox("Select a country to view its risk details", df["country name"].unique())
countrydata= df[df["country name"]==selected_country]
st.write(countrydata [["gdp_growth", "inflation", "external_debt", "reserves", "gdp_per_capita", "risk score","risk category"]])

#Risk score bar chart using Plotly Express
riskgraphic = px.bar(df.sort_values("risk score",ascending=True), x= "country name", y="risk score", color="risk category",color_discrete_map={"Low Risk": "#1cfa50", "Medium Risk": "#fcb32d", "High Risk": "#fa3748"}, title="Country Risk Scores -ECOWAS 2024")
st.plotly_chart(riskgraphic)

#Apply KMeans clustering to the z-scores of the economic indicators and display the cluster assignments
zscores= df[["gdp_growthz","inflationz","external_debtz","gdp_per_capitaz"]]
kmeans= KMeans( n_clusters=3, random_state=42,n_init=10)
df["cluster"]= kmeans.fit_predict(zscores)
df["cluster"]= df["cluster"].astype(str)
print(df[["country name","cluster"]].sort_values("cluster"))

#mapping to define the different clusters name
cluster_names={

    0: "Mixed Risk Signals",
    1: "Moderate & Stable Risk",
    2: "Inflation-Driven Risk"

}
df["cluster_name"]= df["cluster"].astype(int).map(cluster_names)

st.subheader("Country Clusters")
zscores_cluster= px.scatter(df,x="gdp_growth", y="inflation", color="cluster_name", hover_data=["country name"], title="Country Clusters based on Economic Indicators ")
st.plotly_chart(zscores_cluster)