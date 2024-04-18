# Import des modules nécessaires
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback
from skimage import data
import json

# Chargement de l'image de test (une image de chat)
img = data.chelsea()

# Création de la figure Plotly avec l'image
fig = px.imshow(img)
fig.update_layout(dragmode="drawclosedpath")  # Activation du mode de dessin de formes fermées

# Configuration des boutons de la barre de mode
config = {
    "modeBarButtonsToAdd": [
        "drawline",         # Dessiner une ligne
        "drawopenpath",     # Dessiner un chemin ouvert
        "drawclosedpath",   # Dessiner une forme fermée
        "drawcircle",       # Dessiner un cercle
        "drawrect",         # Dessiner un rectangle
        "eraseshape",       # Effacer une forme
    ]
}

# Construction de l'application Dash
app = Dash(__name__)

# Définition de la mise en page de l'application
app.layout = html.Div(
    [
        html.H4(
            "Faites glisser et dessinez des annotations - utilisez la barre de mode pour choisir un outil de dessin différent"
        ),
        dcc.Graph(id="graph-pic", figure=fig, config=config),  # Affichage de la figure avec l'image
        dcc.Markdown("Caractéristiques des formes"),            # Affichage du titre pour les caractéristiques des formes
        html.Pre(id="annotations-data-pre"),                    # Affichage préformaté pour les données d'annotation
    ]
)

# Définition de la fonction de rappel pour mettre à jour les données d'annotation
@callback(
    Output("annotations-data-pre", "children"),   # Sortie : les données d'annotation
    Input("graph-pic", "relayoutData"),          # Entrée : les données de réorganisation de la figure
    prevent_initial_call=True,                   # Ne pas appeler la fonction lors du démarrage initial
)
def on_new_annotation(relayout_data):
    if "shapes" in relayout_data:  # Vérifie si des formes ont été ajoutées à la figure
        return json.dumps(relayout_data["shapes"], indent=2)  # Renvoie les données d'annotation sous forme JSON
    else:
        return no_update  # Aucune mise à jour nécessaire si aucune nouvelle annotation n'est présente

# Point d'entrée principal de l'application
if __name__ == "__main__":
    # app.run(mode="inline")  # Exécute l'application en mode intégré (inline)
    app.run(debug=True)
