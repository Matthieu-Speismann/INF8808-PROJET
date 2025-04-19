# Importation des bibliothèques nécessaires
import pandas as pd  # Pour manipuler les données sous forme de DataFrame
import matplotlib.pyplot as plt  # Pour créer des visualisations (non utilisé dans ce code)
import os  # Pour manipuler les chemins de fichiers

# Fonction pour charger un fichier CSV depuis le dossier 'data'
def load_csv(filename):
    """
    Charge un fichier CSV depuis le dossier 'data'.
    """
    path = os.path.join("data", filename)  # Construit le chemin complet du fichier
    return pd.read_csv(path)  # Charge le fichier CSV dans un DataFrame

# Chargement des données depuis le fichier CSV
data = load_csv("all_athlete_games.csv")

# Liste des sports d'été
summer_sports = [
    "Athletics", "Badminton", "Basketball", "Boxing",
    "Canoeing", "Cycling", "Fencing", "Football", "Gymnastics",
    "Handball", "Judo", "Rowing", "Sailing", "Swimming", "Weightlifting", "Wrestling"
]

# Liste des sports d'hiver
winter_sports = [
    "Alpine Skiing", "Biathlon", "Bobsleigh", "Cross Country Skiing", "Curling", 
    "Figure Skating", "Ice Hockey", "Luge", "Nordic Combined", "Ski Jumping", "Skeleton", "Snowboarding"
]

# Dictionnaire associant les villes hôtes des Jeux Olympiques à leurs pays respectifs
organaizing_countries = {
    "Albertville": "FRA",
    "Amsterdam": "NED",
    "Antwerpen": "BEL",
    "Athina": "GRE",
    "Atlanta": "USA",
    "Barcelona": "ESP",
    "Beijing": "CHN",
    "Berlin": "GER",
    "Calgary": "CAN",
    "Chamonix": "FRA",
    "Cortina d'Ampezzo": "ITA",
    "Garmisch-Partenkirchen": "GER",
    "Grenoble": "FRA",
    "Helsinki": "FIN",
    "Innsbruck": "AUT",
    "Lake Placid": "USA",
    "Lillehammer": "NOR",
    "London": "GBR",
    "Los Angeles": "USA",
    "Melbourne": "AUS",
    "Mexico City": "MEX",
    "Montreal": "CAN",
    "Moskva": "RUS",
    "Munich": "GER",
    "Nagano": "JPN",
    "Oslo": "NOR",
    "Paris": "FRA",
    "Rio de Janeiro": "BRA",
    "Roma": "ITA",
    "Salt Lake City": "USA",
    "Sankt Moritz": "SUI",
    "Sapporo": "JPN",
    "Sarajevo": "BIH",
    "Seoul": "KOR",
    "Sochi": "RUS",
    "Squaw Valley": "USA",
    "St. Louis": "USA",
    "Stockholm": "SWE",
    "Sydney": "AUS",
    "Tokyo": "JPN",
    "Torino": "ITA",
    "Vancouver": "CAN"
}

# Fonction pour convertir les données et calculer les médailles par sport et par pays
def convert_data(season):
    """
    Convertit les données pour obtenir les médailles par sport et par pays.
    Filtre les données entre 1991 et 2020, puis calcule les médailles pour les
    10 meilleurs pays par sport, en regroupant les autres pays sous 'Others'.
    """

    # Détermine les sports et filtre les données en fonction de la saison
    if season == 'Summer':
        sports = summer_sports  # Sports d'été
        filtered_data = data[(data['Year'] >= 1992) & (data['Year'] <= 2020)]  # Filtre les années pour les JO d'été
    else:
        sports = winter_sports  # Sports d'hiver
        filtered_data = data[(data['Year'] >= 1994) & (data['Year'] <= 2020)]  # Filtre les années pour les JO d'hiver

    medal_counts = {}  # Dictionnaire pour stocker les médailles par sport

    # Parcourt chaque sport pour calculer les médailles
    for sport in sports:
        # Filtre les données pour un sport spécifique
        sport_data = filtered_data[filtered_data['Sport'] == sport]
        if not sport_data.empty:  # Vérifie si les données pour ce sport ne sont pas vides
            # Groupe par pays (NOC) et année, puis compte les médailles
            medals_by_country_year = sport_data.groupby(['NOC', 'Year'])['Medal'].count().unstack(fill_value=0)
            
            # Trie les pays par le total des médailles (somme sur toutes les années)
            sorted_medals = medals_by_country_year.sum(axis=1).sort_values(ascending=False)

            # Trie par total des médailles en ordre décroissant, puis par NOC en ordre alphabétique
            sorted_medals = sorted_medals.sort_index(ascending=True).sort_values(ascending=False, kind='mergesort')
            
            # Sélectionne les 10 meilleurs pays
            top_countries = sorted_medals.head(10).index
            
            # Extrait les données pour les 10 meilleurs pays
            top_countries_data = medals_by_country_year.loc[top_countries]

            # Calcule les médailles pour les pays hors du top 10
            others_data = medals_by_country_year.drop(top_countries).sum()
            
            # Ajoute une ligne 'Others' pour les autres pays
            top_countries_data.loc['Others'] = others_data

            # Ajoute les données au dictionnaire pour le sport actuel
            medal_counts[sport] = top_countries_data

    # Ajoute une colonne pour le code du pays organisateur
    filtered_data['Host_Country'] = filtered_data['City'].map(organaizing_countries)

    # Crée un dictionnaire avec les années comme clés et les codes des pays organisateurs comme valeurs
    host_countries_by_year = filtered_data[filtered_data['Season'] == season][['Year', 'Host_Country']].drop_duplicates().sort_values('Year')
    host_countries_dict = dict(zip(host_countries_by_year['Year'], host_countries_by_year['Host_Country']))

    # Ajoute les données des pays organisateurs dans medal_counts
    medal_counts['Host_Countries'] = host_countries_dict
    
    return medal_counts  # Retourne le dictionnaire contenant les médailles par sport et les pays organisateurs
