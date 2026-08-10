import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

st.title("ECOWAS Country Risk Dashboard")
st.markdown("""
# Christ Armand AYRA
## Data Analyst in training
 3rd-year MIAGE student at UFHB, passionate about economics and finance. Aiming to become a quant analyst;
Proficient in Excel, Python, Java, R and Power BI, with advanced skills in statistical analysis; I believe data and finance are keys to build a better future.

My deep interest in finance and economics was sparked by my financial management 
professor, Mr. Tembely Salifou. 
My leitmotiv is *"I can learn anything."*
""")
tab1, tab2 = st.tabs(["Country Risk Dashboard", "Methodology"])

with tab1:
    st.subheader("West African (ECOWAS) Country Risk Analysis")
    st.write("This dashboard provides insights into country risk factors and their impact on global development. Explore the data and visualize trends to make informed decisions.")

    df = pd.read_csv("risk_scores2024.csv")
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

    # Apply the color function to the risk category column and display the styled dataframe in Streamlit
    st.dataframe(df[["country name", "risk score", "risk category"]].sort_values("risk score", ascending=True).style.map(color_risk, subset=["risk category"]))

    # combo list to show country risks details
    units = {
        'gdp_growth': '%',
        'reserves': 'US$',
        'inflation': '%',
        'external_debt': '% of GNI',
        'gdp_per_capita': 'US$',
        'risk_score': '',
        'risk_category': ''
    }

    # Tableau pour afficher les détails du pays sélectionné
    st.subheader("Country Detail for 2024")
    selected_country = st.selectbox("Select a country to view its risk details", df["country name"].unique())
    countrydata = df[df["country name"] == selected_country].iloc[0]

    indicators_to_show = ["gdp_growth","reserves","inflation", "external_debt", "gdp_per_capita"]
    detail_rows = []
    for col in indicators_to_show:
        value = countrydata[col]
        unit = units[col]
        if pd.isna(value):
            value_str = "N/A"
        else:
            value_str = f"{value:.2f} {unit}"
        detail_rows.append({"Indicator": col, "Value": value_str})

    detail_df = pd.DataFrame(detail_rows)
    st.dataframe(detail_df, hide_index=True)

    # Risk score bar chart using Plotly Express
    riskgraphic = px.bar(df.sort_values("risk score", ascending=True), x="country name", y="risk score", color="risk category", color_discrete_map={"Low Risk": "#1cfa50", "Medium Risk": "#fcb32d", "High Risk": "#fa3748"}, title="ECOWAS Risk Score barchart")
    st.plotly_chart(riskgraphic)

    # Apply KMeans clustering to the z-scores of the economic indicators and display the cluster assignments
    zscores = df[["gdp_growthz", "inflationz", "external_debtz", "gdp_per_capitaz"]]
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(zscores)
    df["cluster"] = df["cluster"].astype(str)

    # mapping to define the different clusters name
    cluster_names = {
        0: "Mixed Risk Signals",
        1: "Moderate & Stable Risk",
        2: "Inflation-Driven Risk"
    }
    df["cluster_name"] = df["cluster"].astype(int).map(cluster_names)

    st.subheader("Country Clusters")
    zscores_cluster = px.scatter(df, x="gdp_growth", y="inflation", color="cluster_name", hover_data=["country name"], title="Country Clusters based on Economic Indicators")
    st.plotly_chart(zscores_cluster)

with tab2:
    st.subheader("Methodology Note")
    st.write("This page explains how the country risk scores and categories are computed.")

    st.subheader("1. Objective")
    st.markdown("""
This dashboard provides a macroeconomic overview of West African (ECOWAS) countries. 
It was built using various indicators obtained via the World Bank API, 
in order to support my application to the WBG Pioneers program.
""")

    st.subheader("2. Data Sources")
    st.markdown("""
The data used comes from the World Bank Open Data API, a free and public source 
provided by the World Bank. The analysis covers the 15 ECOWAS member countries 
(Benin, Burkina Faso, Cabo Verde, Côte d'Ivoire, Gambia, Ghana, Guinea, Guinea-Bissau, 
Liberia, Mali, Niger, Nigeria, Senegal, Sierra Leone, Togo), over the period 2015-2024. 
The risk score and clustering are calculated on the most recent available data (2024), 
while earlier years allow trends to be observed over time.
""")

    st.subheader("3. Selected Indicators")
    st.markdown("""
Four indicators were selected, corresponding to the classic pillars of sovereign risk 
analysis: GDP growth (overall economic health), inflation (monetary stability), 
external debt as a % of GNI (solvency), and GDP per capita (level of development). 
These indicators are commonly used by rating agencies to assess a country's 
macroeconomic vulnerability.
""")

    st.subheader("4. Handling Missing Data")
    st.markdown("""
Foreign exchange reserves were excluded from the composite risk score: WAEMU member 
countries (8 of the 15 ECOWAS countries) pool their reserves through the BCEAO, a 
shared central bank, and therefore do not have individual country-level data in the 
World Bank database. This information is still displayed for reference when available.
""")

    st.subheader("5. Risk Score Methodology")
    st.markdown("""
Each indicator is standardized (z-score) to make the different scales comparable. 
Indicators where a higher value is favorable (growth, GDP per capita) are inverted, 
so that a higher composite score always means higher risk. Countries are then classified 
into three categories (Low/Medium/High Risk) by tercile, a classification relative to 
the sample of 15 ECOWAS countries rather than an absolute threshold.
""")

    st.subheader("6. Complementary Clustering")
    st.markdown("""
A k-means clustering (k=3) was applied in addition to the risk score, to identify 
similar economic profiles between countries rather than a simple ranking. This analysis 
revealed a group of countries marked by strong inflationary pressure (Ghana, Nigeria, 
Sierra Leone), a group of atypical profiles (Cabo Verde, Senegal), and a group 
representing the average regional profile.
""")

    st.subheader("7. Limitations")
    st.markdown("""
This score relies on equal weighting of indicators, a simplifying methodological choice 
rather than expert-based weighting. The data used corresponds to the most recent 
available year (2024), which may vary slightly in freshness depending on the country 
and indicator.
""")
