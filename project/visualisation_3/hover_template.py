'''
    Provides the templates for the tooltips in the lollipop charts.
'''

# Fonction pour obtenir les années où chaque pays a accueilli les Jeux Olympiques
def get_host_years_by_country(season):
    # Dictionnaire pour les Jeux Olympiques d'été
    summer_map = {
        '1945-1991': {  # Période de la Guerre froide
            "United Kingdom": [1948],  # Année où le Royaume-Uni a accueilli
            "Finland": [1952],
            "Australia": [1956],
            "Italy": [1960],
            "Japan": [1964],
            "Mexico": [1968],
            "Germany": [1972],
            "Canada": [1976],
            "Russia": [1980],
            "United States": [1984],
            "South Korea": [1988]
        },
        '1992-2020': {  # Période post-Guerre froide
            "Spain": [1992],
            "United States": [1996],
            "Australia": [2000],
            "Greece": [2004],
            "China": [2008],
            "United Kingdom": [2012],
            "Brazil": [2016],
            "Japan": [2020]
        }
    }

    # Dictionnaire pour les Jeux Olympiques d'hiver
    winter_map = {
        '1945-1991': {  # Période de la Guerre froide
            "Switzerland": [1948],
            "Norway": [1952],
            "Italy": [1956],
            "United States": [1960, 1980],  # Deux éditions accueillies par les États-Unis
            "Austria": [1964, 1976],  # Deux éditions accueillies par l'Autriche
            "France": [1968],
            "Japan": [1972],
            "Bosnia and Herzegovina": [1984],
            "Canada": [1988]
        },
        '1992-2020': {  # Période post-Guerre froide
            "France": [1992],
            "Norway": [1994],
            "Japan": [1998],
            "United States": [2002],
            "Italy": [2006],
            "Canada": [2010],
            "Russia": [2014],
            "South Korea": [2018]
        }
    }

    # Retourne le dictionnaire correspondant à la saison (été ou hiver)
    return summer_map if season == "Summer" else winter_map


# Fonction pour générer un modèle de tooltip (info-bulle) pour les graphiques
def get_hover_template(metric_label, is_host):
    """
    Retourne une chaîne de caractères pour un modèle de tooltip.

    Args:
        metric_label (str): Libellé de la métrique (par ex., 'athletes', 'medals')
        is_host (bool): True si le point correspond à un pays hôte, False sinon

    Returns:
        str: Un modèle de tooltip valide pour Plotly
    """
    if is_host:  # Si le pays est un hôte
        template = (
            # Début du modèle avec un style spécifique
            "<span style='font-family:Roboto Slab'><extra></extra><br>"
            # Affiche le nom du pays
            "<b>Country</b>: %{customdata[0]}<br>"
            # Affiche la valeur de la métrique
            "<b>" + metric_label.capitalize() + "</b>: %{x}<br>"
            # Affiche les éditions accueillies par le pays
            "<b>Home editions</b>: %{customdata[1]}"
        )
    else:  # Si le pays n'est pas un hôte
        template = (
            # Début du modèle avec un style spécifique
            "<span style='font-family:Roboto Slab'><extra></extra><br>"
            # Affiche le nom du pays
            "<b>Country</b>: %{customdata[0]}<br>"
            # Affiche la valeur de la métrique
            "<b>" + metric_label.capitalize() + "</b>: %{x}<br>"
        )
    return template  # Retourne le modèle de tooltip
