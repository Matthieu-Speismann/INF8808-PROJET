import pandas as pd
import os

def load_csv(filename):
    """
    Loads a CSV file from the 'data' folder.
    """
    # Construit le chemin complet vers le fichier CSV dans le dossier 'data'
    path = os.path.join("data", filename)
    # Charge le fichier CSV en tant que DataFrame pandas
    return pd.read_csv(path)

def preprocess_data(df, season=None):
    """
    Prepares the data for the lollipop charts.
    """
    # 1. Filtrer les données pour la période 1945–2020 et éventuellement par saison
    df = df[(df['Year'] >= 1945) & (df['Year'] <= 2020)].copy()
    if season:
        # Filtrer les données pour une saison spécifique (été ou hiver)
        df = df[df['Season'] == season].copy()

    # 2. Associer les villes hôtes aux pays hôtes
    city_country_map = {
        # Été
        "London": "United Kingdom", "Helsinki": "Finland", "Melbourne": "Australia",
        "Rome": "Italy", "Tokyo": "Japan", "Mexico City": "Mexico",
        "Munich": "Germany", "Montreal": "Canada", "Moscow": "Russia",
        "Los Angeles": "United States", "Seoul": "South Korea", "Barcelona": "Spain",
        "Atlanta": "United States", "Sydney": "Australia", "Athens": "Greece",
        "Beijing": "China", "Rio de Janeiro": "Brazil",
        # Hiver
        "St. Moritz": "Switzerland", "Oslo": "Norway", "Cortina d'Ampezzo": "Italy",
        "Squaw Valley": "United States", "Innsbruck": "Austria", "Grenoble": "France",
        "Sapporo": "Japan", "Lake Placid": "United States", "Sarajevo": "Bosnia and Herzegovina",
        "Calgary": "Canada", "Albertville": "France", "Lillehammer": "Norway",
        "Nagano": "Japan", "Salt Lake City": "United States", "Turin": "Italy",
        "Vancouver": "Canada", "Sochi": "Russia", "Pyeongchang": "South Korea"
    }

    # 3. Ajouter des colonnes nécessaires
    # Associer chaque ville hôte à son pays hôte
    df['HostCountry'] = df['City'].map(city_country_map)
    # Indiquer si une équipe est le pays hôte
    df['IsHost'] = df['Team'] == df['HostCountry']
    # Indiquer si un athlète a gagné une médaille
    df['HasMedal'] = df['Medal'].notna()

    # Fonction pour déterminer la période (1945-1991 ou 1992-2020)
    def get_period(year):
        return "1945-1991" if year <= 1991 else "1992-2020"

    # Ajouter une colonne pour la période
    df['Period'] = df['Year'].apply(get_period)

    # 4. Calculer le nombre moyen d'athlètes par pays / période / IsHost (moyenne par édition)
    athlete_counts = (
        df.groupby(['Team', 'Year', 'Period', 'IsHost'])['Name']
        .nunique()  # Compter le nombre d'athlètes uniques
        .reset_index(name='NumAthletesPerEdition')
    )
    athletes_per_group = (
        athlete_counts.groupby(['Team', 'Period', 'IsHost'])['NumAthletesPerEdition']
        .mean()  # Calculer la moyenne par groupe
        .reset_index(name='NumAthletes')
    )

    # 5. Calculer le nombre moyen de médailles par pays / période / IsHost (moyenne par édition)
    medal_counts = (
        df[df['HasMedal']]  # Filtrer uniquement les athlètes ayant gagné une médaille
        .groupby(['Team', 'Year', 'Period', 'IsHost'])['Medal']
        .count()  # Compter le nombre de médailles
        .reset_index(name='NumMedalsPerEdition')
    )
    medals_per_group = (
        medal_counts.groupby(['Team', 'Period', 'IsHost'])['NumMedalsPerEdition']
        .mean()  # Calculer la moyenne par groupe
        .reset_index(name='NumMedals')
    )

    # 6. Joindre les données et calculer le ratio médailles/athlètes
    summary = pd.merge(athletes_per_group, medals_per_group,
                       on=['Team', 'Period', 'IsHost'], how='left')
    # Remplacer les valeurs NaN dans 'NumMedals' par 0
    summary['NumMedals'] = summary['NumMedals'].fillna(0)
    # Calculer le ratio médailles/athlètes
    summary['Ratio'] = summary['NumMedals'] / summary['NumAthletes']

    # Arrondir les colonnes à 0 décimales, sauf 'Ratio' à 2 décimales
    summary['NumAthletes'] = summary['NumAthletes'].round(0)
    summary['NumMedals'] = summary['NumMedals'].round(0)
    summary['Ratio'] = summary['Ratio'].round(2)

    # 7. Transformer les données en une structure pivotée
    pivot = summary.pivot_table(
        index=['Team', 'Period'],  # Index de la table pivot
        columns='IsHost',  # Colonnes basées sur la valeur de 'IsHost'
        values=['NumAthletes', 'NumMedals', 'Ratio']  # Valeurs à inclure
    )

    # Renommer les colonnes pour plus de clarté
    pivot.columns = [
        'Athletes_Away', 'Athletes_Host',
        'Medals_Away', 'Medals_Host',
        'Ratio_Away', 'Ratio_Host'
    ]

    # Réinitialiser l'index pour obtenir un DataFrame classique
    pivot = pivot.reset_index()

    return pivot
