import pandas as pd

# on met le fichier csv dans un dataframe
df= pd.read_csv("indicators_data.csv")
filtered_df = df[df['date'] == 2024].copy()

#Utiliser le z-score pour standardiser la valeur des différents indicateurs économiques
filtered_df["gdp_growthz"] = (filtered_df["gdp_growth"] - filtered_df["gdp_growth"].mean()) / filtered_df["gdp_growth"].std()
filtered_df["inflationz"] = (filtered_df["inflation"] - filtered_df["inflation"].mean()) / filtered_df["inflation"].std()
filtered_df["external_debtz"] = (filtered_df["external_debt"] - filtered_df["external_debt"].mean()) / filtered_df["external_debt"].std()
filtered_df["reservesz"] = (filtered_df["reserves"] - filtered_df["reserves"].mean()) / filtered_df["reserves"].std()
filtered_df["gdp_per_capitaz"] = (filtered_df["gdp_per_capita"] - filtered_df["gdp_per_capita"].mean()) / filtered_df["gdp_per_capita"].std()

#Un score de risque obtenu en sommant les différents indicateurs après standardisation
filtered_df["risk_score"]=(-filtered_df["gdp_growthz"] + filtered_df["inflationz"] + filtered_df["external_debtz"]- filtered_df["gdp_per_capitaz"]) 

filtered_df["risk_category"]= pd.qcut(filtered_df["risk_score"],q=3, labels=["Low Risk", "Medium Risk", "High Risk"])
#Affiche les différents indicateurs standardisés
print(filtered_df[["country_name", "gdp_growthz", "inflationz", "external_debtz", "reservesz", "gdp_per_capitaz"]])

#Affiche le score de risque pour chaque pays trier du moins risqué au plus risqué
print(filtered_df[["country_name", "risk_score","risk_category"]].sort_values("risk_score", ascending=True))

#Enregistrer les differents scores de risque et les catégories dans un fichier csv pour l'utiliser dans l'application streamlit
filtered_df.to_csv("risk_scores2024.csv", index=False)
