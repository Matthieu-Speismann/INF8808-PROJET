import project.visualisation_5.preprocess as preprocess
# Importation du module `preprocess` depuis le fichier `preprocess.py` situé dans le même dossier.
# Ce module est utilisé pour accéder à des fonctions et données nécessaires au traitement.

pays_disponibles = preprocess.pays_dispo
# Récupération de la liste des pays disponibles depuis le module `preprocess`.

def get_hovertemplate(pays):
    # Définition d'une fonction qui génère un modèle d'infobulle (hover template) pour un pays donné.

    _, full_pays = preprocess.is_value_in_tuples(pays, pays_disponibles)
    # Vérifie si le pays donné est présent dans la liste des pays disponibles.
    # Renvoie le nom complet du pays correspondant.

    hovertemplate = (f"<extra></extra><br>" +
                     # Ajout d'une section vide pour éviter l'affichage d'informations supplémentaires par défaut.
                     "<b style='font-family:Inter;'>Year:</b> %{customdata[0]}<br>" + 
                     # Ajout de l'année (provenant des données personnalisées `customdata[0]`) dans l'infobulle.
                     "<b style='font-family:Inter;'>Country:</b> " + str(full_pays) + "<br>" +
                     # Ajout du nom complet du pays dans l'infobulle.
                     "<b style='font-family:Inter;'>%{y} points</b> <br>") 
                     # Ajout de la valeur associée à l'axe Y (par exemple, des points ou une mesure) dans l'infobulle.

    return hovertemplate
    # Retourne le modèle d'infobulle généré.