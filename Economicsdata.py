import requests
import pandas as pd

#fonction pour récuperer les données economiques via l'API de la banque mondiale
def Get_Indicator(indicator_code, countries="BEN;BFA;CPV;CIV;GMB;GHA;GIN;GNB;LBR;MLI;NER;NGA;SEN;SLE;TGO"):
    url= f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator_code}?format=json&date=2015:2024&per_page=1000"
    response = requests.get(url, timeout=60)
    economics_data= response.json()
    return economics_data

result=Get_Indicator("NY.GDP.MKTP.CD")

#Fonction permettant de trier les valeurs contenu dans le dictionnaire de l'indicateur et de les nettoyer pour obtenir un DataFrame contenant seulement les valeurs clés
def CleanIndicatorData(result, indicator_name):
    df=pd.DataFrame(result[1])
    df["country name"]= df["country"].apply(lambda x: x["value"])
    df_clean= df[["country name", "countryiso3code", "date", "value"]]
    df_clean=df_clean.rename(columns={"value": indicator_name})
    return df_clean

#Dictionnaire les contenant les codes des indicateurs et leurs noms correspondants
indicators = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "FP.CPI.TOTL.ZG": "inflation",
    "DT.DOD.DECT.GN.ZS": "external_debt",
    "FI.RES.TOTL.CD": "reserves",
    "NY.GDP.PCAP.CD": "gdp_per_capita",
}

#Boucle pour les codes des indicateurs et pour chaque code,
#on récupère les données via l'API, on nettoie les données et on les fusionne dans un DataFrame final
indicatorsdf = None
for code,name in indicators.items():
    result=Get_Indicator(code)
    df_clean=CleanIndicatorData(result, name)
    if indicatorsdf is None:
        indicatorsdf=df_clean
    else:
        indicatorsdf=pd.merge(indicatorsdf, df_clean, on=["country name", "countryiso3code", "date"])
        

#print(indicatorsdf.head())
#print(indicatorsdf.shape)      
#indicatorsdf.to_csv("indicators_data.csv", index=False)
history_df = pd.read_csv("indicators_data.csv")
print(history_df.columns)