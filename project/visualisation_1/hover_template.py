def get_hover_template(sport):
    # Crée une chaîne de caractères formatée qui sera utilisée comme modèle de survol (hover template)
    # pour afficher des informations spécifiques dans une visualisation interactive.
    template = (f"<b style='font-family:Inter;'>{sport}</b>" +  # Affiche le nom du sport en gras avec une police spécifique
                "<br><b style='font-family:Inter;'>Country:</b> %{y}" +  # Affiche le pays correspondant à la valeur de l'axe y
                "<br><b style='font-family:Inter;'>Year:</b> %{x}" +  # Affiche l'année correspondant à la valeur de l'axe x
                "<br><b style='font-family:Inter;'>Medals:</b> %{z}<extra></extra>")  # Affiche le nombre de médailles correspondant à la valeur de l'axe z
    # Retourne le modèle de survol formaté pour afficher les informations sur le sport, le pays, l'année et les médailles
    return template