# Import des modules nécessaires
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback
from skimage import data
import json

# Chargement de l'image de test (une image de chat)
img = data.chelsea()

# Création de la figure Plotly avec l'image
fig = px.imshow(img)

# Mise à jour de la disposition de la figure pour activer le mode de dessin de chemin fermé
fig.update_layout(dragmode="drawclosedpath")

# Configuration des boutons de la barre de mode
config = {
    "modeBarButtonsToAdd": [
        "drawline",         # Bouton pour dessiner une ligne
        "drawopenpath",     # Bouton pour dessiner un chemin ouvert
        "drawclosedpath",   # Bouton pour dessiner un chemin fermé
        "drawcircle",       # Bouton pour dessiner un cercle
        "drawrect",         # Bouton pour dessiner un rectangle
        "eraseshape",       # Bouton pour effacer une forme
    ]
}

# Initialisation de l'application Dash
app = Dash(__name__)

# Définition de la mise en page de l'application
app.layout = html.Div(
    [
        html.H4("Dessinez une forme, puis modifiez-la"),
        dcc.Graph(id="fig-image", figure=fig, config=config),  # Affichage de la figure avec l'image et les outils de dessin
        dcc.Markdown("Caractéristiques des formes"),           # Affichage du titre pour les caractéristiques des formes
        html.Pre(id="annotations-pre"),                        # Affichage préformaté pour les données d'annotation
    ]
)

# Définition de la fonction de rappel pour afficher les caractéristiques des formes dessinées
@callback(
    Output("annotations-pre", "children"),   # Sortie : les données d'annotation préformatées
    Input("fig-image", "relayoutData"),     # Entrée : les données de réorganisation de la figure
    prevent_initial_call=True,              # Ne pas appeler la fonction lors du démarrage initial
)
def on_new_annotation(relayout_data):
    for key in relayout_data:   # Parcourir les clés des données de réorganisation
        if "shapes" in key:     # Vérifier si la clé correspond aux formes dessinées
            return json.dumps(f'{key}: {relayout_data[key]}', indent=2)  # Renvoyer les données d'annotation formatées
    return no_update   # Aucune mise à jour nécessaire si aucune nouvelle annotation n'est présente

# Point d'entrée principal de l'application
if __name__ == "__main__":
    app.run(debug=True)   # Exécute l'application en mode débogage
