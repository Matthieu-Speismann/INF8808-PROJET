# preprocess.py
import pandas as pd  # Importation de la bibliothèque pandas pour la manipulation des données.
import os  # Importation du module os pour interagir avec le système de fichiers.

def load_csv(filename):
    """
    Charge un fichier CSV depuis le dossier 'data'.
    :param filename: Nom du fichier CSV à charger.
    :return: Un DataFrame pandas contenant les données du fichier CSV.
    """
    # Construction du chemin complet vers le fichier en combinant le dossier 'data' et le nom du fichier.
    path = os.path.join("data", filename)
    
    # Lecture du fichier CSV à l'aide de pandas et retour du DataFrame résultant.
    return pd.read_csv(path)
