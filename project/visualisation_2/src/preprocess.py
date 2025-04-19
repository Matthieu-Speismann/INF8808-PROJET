"""
    use the "get_data()" function to 
"""

from pathlib import Path
import os
import pandas as pd
import csv

# Définition des chemins vers les fichiers de données
DATA_FOLDER = Path(os.path.abspath(__file__)).parent.parent.parent.parent / "data"
PATH_ATHLETE_GAMES = DATA_FOLDER / "all_athlete_games.csv"
PATH_REGIONS = DATA_FOLDER / "all_regions.csv"
PATH_PIB_PER_CAPITA = DATA_FOLDER / "WEO_database_Apre2024.csv" # Données provenant du site IMF
PATH_COUNTRIES_PER_CONTINENT = DATA_FOLDER / "countries_per_continent.csv" # Données provenant du site World Population Review
PATH_POPULATION_PER_COUNTRY = DATA_FOLDER / "SP_POP_TOTL.csv" # Données provenant du site World Bank
PATH_AVERAGE_TEMPERATURE_PER_COUNTRY = DATA_FOLDER / "average_temperature_per_country.csv"

# Fonction pour charger un fichier CSV en DataFrame
def get_df(path: Path) -> pd.DataFrame:
    with open(path, encoding="ISO-8859-1") as data_file:
        data = list(csv.reader(data_file))
    df = pd.DataFrame(data[1:], columns=data[0])  # Crée un DataFrame avec les colonnes du fichier CSV
    return df

# Chargement des données des athlètes
def get_athlete_games() -> pd.DataFrame:
    return get_df(PATH_ATHLETE_GAMES)

# Chargement des données des régions
def get_regions() -> pd.DataFrame:
    return get_df(PATH_REGIONS)

# Chargement et transformation des données du PIB par habitant
def get_pib_per_capita() -> pd.DataFrame:
    df = get_df(PATH_PIB_PER_CAPITA)

    df["ISO"] = df["ï»¿ISO"]  # Correction du nom de colonne encodé

    # Transformation des données pour les rendre exploitables
    df_melted = df.melt(id_vars=["ISO", "WEO Subject Code", "Country", "Subject Descriptor", 
                              "Subject Notes", "Units", "Scale"],
                     var_name="Year", value_name="PIB_per_Capita")

    df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors="coerce")  # Conversion des années en numérique
    df_melted["PIB_per_Capita"] = df_melted["PIB_per_Capita"].replace({',': ''}, regex=True)  # Suppression des virgules
    df_melted["PIB_per_Capita"] = pd.to_numeric(df_melted["PIB_per_Capita"], errors="coerce")  # Conversion en numérique
    
    # Conversion en entier (en ignorant les erreurs)
    df_melted["PIB_per_Capita"] = df_melted["PIB_per_Capita"].astype("Int64", errors="ignore")

    # Suppression des valeurs manquantes
    df_melted = df_melted.dropna(subset=["PIB_per_Capita"])
    df_melted = df_melted.reset_index(drop=True)

    # Filtrage des données pertinentes
    df_melted = df_melted[
        (df_melted["WEO Subject Code"] == "PPPPC") &
        (df_melted["Year"].notna()) &
        (df_melted["Year"] <= 2025)
    ]

    # Création de groupes d'années
    df_melted["Year_Group"] = df_melted["Year"].apply(lambda x: "1945-1990" if 1945 <= x <= 1990 else "1991-2020")
    df_melted["Region"] = df_melted["Country"]

    return df_melted[["ISO", "Region", "Year_Group", "Year", "PIB_per_Capita"]]

# Chargement des données des pays par continent
def get_countries_per_continents():
    df = get_df(PATH_COUNTRIES_PER_CONTINENT)
    df["Region"] = df["country"]

    return df[["Region", "continent"]]

# Chargement des données de population par pays
def get_population_per_country():
    df = get_df(PATH_POPULATION_PER_COUNTRY)
    df["Region"] = df["ï»¿Country Name"]
    df = df.melt(id_vars=["Region"],
                    var_name="Year", value_name="Population")

    df["Population"] = pd.to_numeric(df["Population"], errors="coerce")  # Conversion en numérique
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Year_Group"] = df["Year"].apply(lambda x: "1945-1990" if 1945 <= x <= 1990 else "1991-2020")

    df = df[["Region", "Year_Group", "Population"]]
    return df

# Chargement des données de température moyenne par pays
def get_temp_per_country():
    df = get_df(PATH_AVERAGE_TEMPERATURE_PER_COUNTRY)

    df["Average Temperature"] = pd.to_numeric(df["Average Temperature"], errors="coerce")
    df["Climate"] = df["Average Temperature"].apply(
        lambda x: "Hot climate (>25 C)" if x > 25 else ("Moderate climate (5 C-25 C)" if x > 5 else "Cold climate (<=5 C)")
    )

    return df[["Region", "Climate"]]

# Génération des données pour les graphiques "médailles vs PIB"
def generate_data_medals_vs_pib(graph_id: int = 1):
    athlete_df = get_athlete_games()
    athlete_df["Year"] = athlete_df["Year"].astype(int)

    # Définition des colonnes pour le groupement
    if graph_id == 1:
        mean_group_by_columns_athlete = ["Year_Group", "Region"]
        group_by_columns_final = ["Year_Group", "continent", "Region", "Population", "Climate", "nb_medals", "PIB_per_Capita"]
    else:
        mean_group_by_columns_athlete = ["Year_Group", "Region", "Season"]
        group_by_columns_final = ["Year_Group", "continent", "Region", "Population", "Season", "Climate", "nb_medals", "PIB_per_Capita"]

    # Calcul du nombre moyen de médailles par groupe
    athlete_df = athlete_df.groupby(["Year", "NOC", "Season"]).size().reset_index(name="nb_medals")
    athlete_df["Year_Group"] = athlete_df["Year"].apply(lambda x: "1945-1990" if 1945 <= x <= 1990 else "1991-2020")

    athlete_df = athlete_df.merge(get_regions(), on="NOC", how="left")
    athlete_df = athlete_df.groupby(mean_group_by_columns_athlete)["nb_medals"].mean().reset_index()

    # Fusion avec les données du PIB
    pib_df = get_pib_per_capita().groupby(["Year_Group", "Region"])["PIB_per_Capita"].mean().reset_index()
    athlete_pib_df = athlete_df.merge(pib_df, on=["Year_Group", "Region"], how="left")

    # Fusion avec les données des continents
    athlete_pib_continent_df = athlete_pib_df.merge(get_countries_per_continents(), on="Region", how="left")

    # Fusion avec les données de population
    populations_df = get_population_per_country().groupby(["Year_Group", "Region"])["Population"].mean().reset_index()
    final_df = athlete_pib_continent_df.merge(populations_df, on=["Year_Group", "Region"], how="left")

    # Fusion avec les données de température
    final_df = final_df.merge(get_temp_per_country(), on="Region", how="left")

    # Calcul du taux de correspondance
    final_df = final_df.dropna(subset=["continent", "Population", "PIB_per_Capita"])
    print(f"Final (hit) rate: {(len(final_df)/len(athlete_df)):.2%}")

    # Sélection des colonnes finales et export en CSV
    final_df = final_df[group_by_columns_final]
    final_df.to_csv(f"vis_2_processed_data_{graph_id}.csv", index=False)

    return final_df

# Arrondir les valeurs numériques dans un DataFrame
def round_decimals(df):
    df["Population"] = df["Population"].round(2)
    df["nb_medals"] = df["nb_medals"].round(0)
    df["PIB_per_Capita"] = df["PIB_per_Capita"].round(2)
    return df

# Obtenir la plage (min, max) d'une colonne
def get_range(col, df):
    return [df[col].min(), df[col].max()]

# Trier un DataFrame par année et continent
def sort_dy_by_yr_continent(df):
    return df.sort_values(["Year_Group", "continent"])

# Trier un DataFrame par année et climat
def sort_dy_by_yr_climate(df):
    climate_order = ["Hot climate (>25 C)", "Cold climate (<=5 C)", "Moderate climate (5 C-25 C)"]
    df["Climate"] = pd.Categorical(df["Climate"], categories=climate_order, ordered=True)
    return df.sort_values(["Year_Group", "Climate"])

# Exécution principale
if __name__ == "__main__":
    generate_data_medals_vs_pib(1)
    generate_data_medals_vs_pib(2)
