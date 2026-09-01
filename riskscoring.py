import pandas as pd

# on met le fichier csv dans un dataframe
df = pd.read_csv("indicators_data.csv")

# Calculer les scores de risque pour toutes les années
all_years = []
for year in df["date"].unique():
    year_df = df[df["date"] == year].copy()
    # Utiliser le z-score pour standardiser la valeur des différents indicateurs économiques
    year_df["gdp_growthz"] = (year_df["gdp_growth"] - year_df["gdp_growth"].mean()) / year_df["gdp_growth"].std()
    year_df["inflationz"] = (year_df["inflation"] - year_df["inflation"].mean()) / year_df["inflation"].std()
    year_df["external_debtz"] = (year_df["external_debt"] - year_df["external_debt"].mean()) / year_df["external_debt"].std()
    year_df["reservesz"] = (year_df["reserves"] - year_df["reserves"].mean()) / year_df["reserves"].std()
    year_df["gdp_per_capitaz"] = (year_df["gdp_per_capita"] - year_df["gdp_per_capita"].mean()) / year_df["gdp_per_capita"].std()
    # Un score de risque obtenu en sommant les différents indicateurs après standardisation
    year_df["risk_score"] = (-year_df["gdp_growthz"] + year_df["inflationz"] + year_df["external_debtz"] - year_df["gdp_per_capitaz"])
    # Un score de risque catégorisé en trois niveaux : faible, moyen et élevé
    year_df["risk_category"] = pd.qcut(year_df["risk_score"], q=3, labels=["Low Risk", "Medium Risk", "High Risk"])
    all_years.append(year_df)

full_df = pd.concat(all_years, ignore_index=True)

# Enregistrer les scores de risque de toutes les années dans un fichier csv
full_df.to_csv("risk_scores_all.csv", index=False)

# Enregistrer les scores de risque de 2024 dans un fichier csv (rétrocompatibilité)
full_df[full_df["date"] == 2024].to_csv("risk_scores2024.csv", index=False)

# Affiche les différents indicateurs standardisés pour 2024
print(full_df[full_df["date"] == 2024][["country_name", "gdp_growthz", "inflationz", "external_debtz", "reservesz", "gdp_per_capitaz"]])

# Affiche le score de risque pour chaque pays trier du moins risqué au plus risqué (2024)
print(full_df[full_df["date"] == 2024][["country_name", "risk_score", "risk_category"]].sort_values("risk_score", ascending=True))
