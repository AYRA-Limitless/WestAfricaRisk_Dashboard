import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# Language selector
lang = st.sidebar.selectbox("Language / Langue", ["English", "Français"])

T = {
    "English": {
        "title": "ECOWAS Country Risk Dashboard",
        "role": "Data Analyst in training",
        "bio": """3rd-year MIAGE student at UFHB, passionate about economics and finance. Aiming to become a quant analyst;
Proficient in Excel, Python, Java, R and Power BI, with advanced skills in statistical analysis; I believe data and finance are keys to build a better future.""",
        "subheader": "West African (ECOWAS) Country Risk Analysis",
        "intro": """This dashboard provides insights into ECOWAS country risk factors and their impact on global development. The risk scores are calculated based on key economic indicators such as GDP growth, inflation, external debt, reserves, and GDP per capita. The data is sourced from the World Bank API and covers the years 2015 to 2024. The risk scores are categorized into three levels: Low Risk, Medium Risk, and High Risk. The dashboard also includes visualizations to help users understand the risk landscape of West African countries and make informed decisions. The countries with high risk score are considered to be more vulnerable due to high inflation, low GDP growth, high external debt and low reserves. The dashboard also provides a historical comparison of economic indicators for selected countries over the years.""",
        "select_year": "Select a year",
        "risk_scores_header": "Risk Scores and Categories for West African Countries",
        "low_risk": "Low Risk",
        "medium_risk": "Medium Risk",
        "high_risk": "High Risk",
        "riskgraphic": "ECOWAS Risk Score barchart",
        "clusters_header": "Country Clusters",
        "cluster_mixed": "Mixed Risk Signals",
        "cluster_moderate": "Moderate & Stable Risk",
        "cluster_inflation": "Inflation-Driven Risk",
        "clusters_title": "Country Clusters based on Economic Indicators",
        "comparison_header": "Historical Comparison of Economic Indicators (2015-2024)",
        "choose_indicator": "Choose an indicator",
        "select_countries": "Select countries to compare",
        "comparison_title": "Comparison of {indicator} for selected countries",
        "history_table_header": "Historical Data Table",
    },
    "Français": {
        "title": "Tableau de bord du risque pays de la CEDEAO",
        "role": "Data Analyst en formation",
        "bio": """Étudiant en 3e année MIAGE à l'UFHB, passionné d'économie et de finance. Objectif : devenir analyste quantitatif ;
Compétent en Excel, Python, Java, R et Power BI, avec des compétences avancées en analyse statistique ; je crois que les données et la finance sont les clés d'un avenir meilleur.""",
        "subheader": "Analyse du risque pays en Afrique de l'Ouest (CEDEAO)",
        "intro": """Ce tableau de bord fournit des informations sur les facteurs de risque pays de la CEDEAO et leur impact sur le développement mondial. Les scores de risque sont calculés à partir d'indicateurs économiques clés tels que la croissance du PIB, l'inflation, la dette extérieure, les réserves et le PIB par habitant. Les données proviennent de l'API de la Banque mondiale et couvrent les années 2015 à 2024. Les scores de risque sont classés en trois niveaux : risque faible, risque moyen et risque élevé. Le tableau de bord comprend également des visualisations pour aider les utilisateurs à comprendre le paysage du risque des pays d'Afrique de l'Ouest et à prendre des décisions éclairées. Les pays présentant un score de risque élevé sont considérés comme plus vulnérables en raison d'une inflation élevée, d'une faible croissance du PIB, d'une dette extérieure élevée et de réserves faibles. Le tableau de bord fournit également une comparaison historique des indicateurs économiques pour les pays sélectionnés au fil des années.""",
        "select_year": "Sélectionner une année",
        "risk_scores_header": "Scores de risque et catégories pour les pays d'Afrique de l'Ouest",
        "low_risk": "Risque faible",
        "medium_risk": "Risque moyen",
        "high_risk": "Risque élevé",
        "riskgraphic": "Graphique à barres du score de risque CEDEAO",
        "clusters_header": "Groupes de pays",
        "cluster_mixed": "Signaux de risque mixtes",
        "cluster_moderate": "Risque modéré et stable",
        "cluster_inflation": "Risque lié à l'inflation",
        "clusters_title": "Groupes de pays basés sur les similitudes économiques par rapport aux indicateurs",
        "comparison_header": "Comparaison historique des indicateurs économiques (2015-2024)",
        "choose_indicator": "Choisir un indicateur",
        "select_countries": "Sélectionner des pays à comparer",
        "comparison_title": "Comparaison de {indicator} pour les pays sélectionnés",
        "history_table_header": "Tableau des données historiques",
    },
}
t = T[lang]

st.title(t["title"])
col_bio, col_photo = st.columns([3, 1])
with col_bio:
    bio_one_line = " ".join(t["bio"].split())
    st.markdown(f"""
    ### Christ Armand AYRA
    #### {t['role']}
    {bio_one_line}
    """)
with col_photo:
    st.image("IMG_9855.jpg.jpeg", width=200)

st.subheader(t["subheader"])
st.write(t["intro"])

df = pd.read_csv("risk_scores_all.csv")
history_df = pd.read_csv("indicators_data.csv")

# Global year selector for all charts on the page
available_years = sorted(df["date"].unique())
year = st.sidebar.selectbox(t["select_year"], available_years, index=len(available_years) - 1)

# Filter data for the selected year
year_df = df[df["date"] == year]

st.subheader(f"{t['risk_scores_header']} ({year})")

# function to color cells based on risk category
def color_risk(val):
    if val == t["low_risk"]:
        color = "background-color: #1cfa50"
    elif val == t["medium_risk"]:
        color = "background-color: #fcb32d"
    else:
        color = "background-color: #fa3748"
    return color

# Apply the color function to the risk category column and display the styled dataframe in Streamlit
cat_translation = {T["English"]["low_risk"]: T["Français"]["low_risk"], T["English"]["medium_risk"]: T["Français"]["medium_risk"], T["English"]["high_risk"]: T["Français"]["high_risk"]}
table_for_display = year_df[["country_name", "risk_score", "risk_category"]].sort_values("risk_score", ascending=True).copy()
if lang == "Français":
    table_for_display["risk_category"] = table_for_display["risk_category"].map(cat_translation)
st.dataframe(table_for_display.style.map(color_risk, subset=["risk_category"]))

# Risk score bar chart using Plotly Express
riskgraphic = px.bar(year_df.sort_values("risk_score", ascending=True), x="country_name", y="risk_score", color="risk_category", color_discrete_map={T["English"]["low_risk"]: "#1cfa50", T["English"]["medium_risk"]: "#fcb32d", T["English"]["high_risk"]: "#fa3748"}, title=f"{t['riskgraphic']} ({year})")
st.plotly_chart(riskgraphic)

# Apply KMeans clustering to the z-scores of the economic indicators and display the cluster assignments
zscores = year_df[["gdp_growthz", "inflationz", "external_debtz", "gdp_per_capitaz"]].fillna(0)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
year_df = year_df.copy()
year_df["cluster"] = kmeans.fit_predict(zscores)
year_df["cluster"] = year_df["cluster"].astype(str)

# mapping to define the different clusters name
cluster_names = {
    0: t["cluster_mixed"],
    1: t["cluster_moderate"],
    2: t["cluster_inflation"]
}
year_df["cluster_name"] = year_df["cluster"].astype(int).map(cluster_names)

st.subheader(f"{t['clusters_header']} ({year})")
zscores_cluster = px.scatter(year_df, x="gdp_growth", y="inflation", color="cluster_name", hover_data=["country_name"], title=f"{t['clusters_title']} ({year})")
st.plotly_chart(zscores_cluster)

# Historical Comparison of Economic Indicators graphic
st.subheader(t["comparison_header"])
indicator_labels = {
    "gdp_growth": {"English": "GDP Growth", "Français": "Croissance du PIB"},
    "inflation": {"English": "Inflation", "Français": "Inflation"},
    "external_debt": {"English": "External Debt", "Français": "Dette extérieure"},
    "reserves": {"English": "Reserves", "Français": "Réserves"},
    "gdp_per_capita": {"English": "GDP per Capita", "Français": "PIB par habitant"},
}
selected_indicator = st.selectbox(t["choose_indicator"], list(indicator_labels.keys()), format_func=lambda k: indicator_labels[k][lang])
selected_countries = st.multiselect(t["select_countries"], year_df["country_name"].unique(), default=year_df["country_name"].unique().tolist())
filtered_history_df = history_df[(history_df["country_name"].isin(selected_countries)) &
    (history_df["date"] == year)]

unit_map = {
    "gdp_growth": "%",
    "inflation": "%",
    "external_debt": "% of GNI",
    "reserves": "US$",
    "gdp_per_capita": "US$"
}
unit = unit_map.get(selected_indicator, "")
indicator_label = indicator_labels[selected_indicator][lang]
fig_compare = px.bar(filtered_history_df, x="country_name", y=selected_indicator, color="country_name", barmode="stack", title=t["comparison_title"].format(indicator=indicator_label) + f" ({year})")
fig_compare.update_yaxes(title_text=f"{indicator_label} ({unit})", zeroline=True)
fig_compare.update_layout(bargap=0)
st.plotly_chart(fig_compare, use_container_width=True)

# Tableau des données historiques filtrées en bas de page
st.subheader(t["history_table_header"])
table_df = filtered_history_df.copy()
for col, u in unit_map.items():
    if col in table_df.columns:
        label = indicator_labels[col][lang]
        table_df = table_df.rename(columns={col: f"{label} ({u})"})
st.dataframe(table_df)
