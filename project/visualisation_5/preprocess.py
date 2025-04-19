import pandas as pd
import numpy as np
import os

def load_csv(filename):
    """
    Charge un fichier CSV depuis le dossier 'data'.
    """
    path = os.path.join("data", filename)  # Construit le chemin complet vers le fichier CSV
    return pd.read_csv(path)  # Charge le fichier CSV dans un DataFrame

data = load_csv("all_athlete_games.csv")  # Charge les données du fichier CSV spécifié


def rejet_annees(data, annee_inf, ete=True):
    """
    Rejette les lignes dont la valeur de la colonne "Year" est inférieure à `annee_inf`.
    ---
    Arguments:
        -`data`: DataFrame
        -`annee_inf`: int: Année minimale à conserver
        -`ete`: bool: Filtrer pour les Jeux d'été ou d'hiver
    
    Returns:
        -`data`: DataFrame sans les lignes rejetées
    """
    data["Year"] = data["Year"].astype("Int64")  # Convertit la colonne "Year" en entier nullable

    if ete:
        data = data[data["Season"] == "Summer"]  # Filtre pour les Jeux d'été
    else:
        data = data[data["Season"] == "Winter"]  # Filtre pour les Jeux d'hiver

    return data[data["Year"] >= annee_inf]  # Garde uniquement les années >= annee_inf


def points(data):
    """
    Ajoute une colonne "Medals" et une colonne "Points" au dataframe.
    ---
    Arguments:
        -`data`: DataFrame
    
    Returns:
        -`data`: DataFrame avec les nouvelles colonnes
    """
    # Ajoute une colonne "Medals" avec 1 pour les médailles et 0 sinon
    data.loc[data["Medal"].isin(["Gold", "Silver", "Bronze"]), "Medals"] = 1
    data["Medals"] = data["Medals"].fillna(0).astype(int)  # Remplit les valeurs manquantes avec 0

    # Ajoute une colonne "Points" avec des scores basés sur le type de médaille
    data["Points"] = np.nan  # Initialise la colonne avec des valeurs NaN
    data.loc[data["Medal"] == "Gold", "Points"] = 3  # 3 points pour l'or
    data.loc[data["Medal"] == "Silver", "Points"] = 2  # 2 points pour l'argent
    data.loc[data["Medal"] == "Bronze", "Points"] = 1  # 1 point pour le bronze
    data["Points"] = data["Points"].fillna(0).astype(int)  # Remplit les NaN avec 0 et convertit en entier

    return data


def data_without(data):
    """
    Filtre les athlètes ayant gagné moins de 2 médailles par année.
    ---
    Arguments:
        -`data`: DataFrame
    
    Returns:
        -`data_without`: DataFrame filtré
    """
    # Compte le nombre de médailles par athlète et par année
    df_medals_count = data.groupby(["Name", "Year"])["Medals"].sum().reset_index()
    # Sélectionne les athlètes ayant gagné moins de 2 médailles
    athletes_to_keep = df_medals_count[df_medals_count["Medals"] < 2]["Name"]
    # Filtre les données pour ne garder que ces athlètes
    data_without = data[data["Name"].isin(athletes_to_keep)]

    return data_without


def pays_points(data_with, data_without):
    """
    Retourne le nombre de points par pays et par année.
    ---
    Arguments:
        -`data_with`: DataFrame avec tous les athlètes
        -`data_without`: DataFrame sans les athlètes ayant gagné plusieurs médailles
    
    Returns:
        -`df_merged`: DataFrame avec les points par pays et par année
    """
    # Supprime les doublons pour les événements par équipe
    data_with_unique = data_with.drop_duplicates(subset=["Event", "Team", "Year", "Medal"])
    data_without_unique = data_without.drop_duplicates(subset=["Event", "Team", "Year", "Medal"])

    # Calcule les points et médailles par pays et par année pour les deux ensembles de données
    df_points_with = data_with_unique.groupby(['NOC', 'Year'])[['Points', "Medals"]].sum().reset_index()
    df_points_with.columns = ['Country', 'Year', 'Points with', "Medals with"]

    df_points_without = data_without_unique.groupby(['NOC', 'Year'])[['Points', "Medals"]].sum().reset_index()
    df_points_without.columns = ['Country', 'Year', 'Points without', "Medals without"]

    # Fusionne les deux DataFrames sur les colonnes 'Country' et 'Year'
    df_merged = pd.merge(df_points_with, df_points_without, on=['Country', 'Year'], how='outer')

    return df_merged


def get_usefull_dataframe(df_final, pays, years):
    """
    Crée un DataFrame structuré pour visualiser les points d'un pays donné.
    ---
    Arguments:
        -`df_final`: DataFrame contenant les points par pays et par année
        -`pays`: str: Code du pays (NOC)
        -`years`: list: Liste des années
    
    Returns:
        -`df`: DataFrame structuré pour la visualisation
    """
    # Récupère les points "avec" et "sans" pour le pays spécifié
    points_with = df_final[df_final["Country"] == pays]["Points with"].values
    points_without = df_final[df_final["Country"] == pays]["Points without"].values

    # Crée un DataFrame structuré pour la visualisation
    df = pd.DataFrame({
        "Year": years + years,  # Duplique les années pour les deux types de points
        "Type": ["With" for _ in years] + ["Without" for _ in years],  # Ajoute les types "With" et "Without"
        "Points": list(points_with) + list(points_without)  # Combine les points "avec" et "sans"
    })
    return df


# Liste des pays disponibles avec leur code NOC et leur nom complet
pays_dispo = [("USA", "United States"),
              ("CAN", "Canada"),
              ("FRA", "France"),
              ("GBR", "Great Britain"),
              ("GER", "Germany"),
              ("ITA", "Italy"),
              ("JPN", "Japan"),
              ("NED", "Netherlands"),
              ("NZL", "New-Zeland"),
              ("CHN", "China"),
              ("IND", "India"),
              ("AUS", "Australia"),
              ("BRA", "Brazil"),
              ("ESP", "Spain"),
              ("NOR", "Norway"),
              ("SWE", "Sweden"),
              ("FIN", "Finland")]

# Trie la liste des pays par leur nom complet
pays_dispo = sorted(pays_dispo, key=lambda x: x[1])


def is_value_in_tuples(value, tuples_list):
    """
    Vérifie si une valeur est présente dans une liste de tuples.
    ---
    Arguments:
        -`value`: str: Valeur à rechercher
        -`tuples_list`: list: Liste de tuples
    
    Returns:
        -`tpl`: tuple ou None: Le tuple contenant la valeur ou None si non trouvé
    """
    for tpl in tuples_list:  # Parcourt chaque tuple de la liste
        if value in tpl:  # Vérifie si la valeur est dans le tuple
            return tpl  # Retourne le tuple correspondant
    return None  # Retourne None si la valeur n'est pas trouvée