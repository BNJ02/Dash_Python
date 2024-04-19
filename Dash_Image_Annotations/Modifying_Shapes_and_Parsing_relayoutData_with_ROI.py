# Import des modules nécessaires
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, no_update, callback
from skimage import data, exposure
import json

# Chargement de l'image de test (une image de caméra)
img = data.camera()

# Création de la figure Plotly avec l'image en utilisant le mode de chaîne binaire
fig = px.imshow(img, binary_string=True)

# Mise à jour de la disposition de la figure pour activer le mode de dessin de rectangle
fig.update_layout(dragmode="drawrect")

# Création de l'histogramme de l'image
fig_hist = px.histogram(img.ravel())

# Configuration des boutons de la barre de mode
config = {
    "modeBarButtonsToAdd": [
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
        html.H3("Dessinez une forme, puis modifiez-la."),
        html.Div(
            [dcc.Graph(id="fig-pic", figure=fig, config=config),],  # Affichage de la figure avec l'image
            style={"width": "60%", "display": "inline-block", "padding": "0 0"},
        ),
        html.Div(
            [dcc.Graph(id="graph-hist", figure=fig_hist, config=config),],  # Affichage de l'histogramme initial
            style={"width": "40%", "display": "inline-block", "padding": "0 0"},
        ),
        html.Pre(id="annotations"),  # Affichage préformaté pour les données d'annotation
    ]
)

# Définition de la fonction de rappel pour mettre à jour l'histogramme en fonction du rectangle dessiné
@callback(
    Output("graph-hist", "figure"),     # Sortie : l'histogramme de la zone d'intérêt (ROI)
    Output("annotations", "children"),  # Sortie : les données d'annotation préformatées
    Input("fig-pic", "relayoutData"),   # Entrée : les données de réorganisation de la figure
    prevent_initial_call=True,          # Ne pas appeler la fonction lors du démarrage initial
)
def on_relayout(relayout_data):
    x0, y0, x1, y1 = (None,) * 4
    if "shapes" in relayout_data:   # Vérifie si des formes ont été ajoutées à la figure
        last_shape = relayout_data["shapes"][-1]   # Récupère la dernière forme ajoutée (le dernier rectangle dessiné)
        x0, y0 = int(last_shape["x0"]), int(last_shape["y0"])   # Coordonnées du coin supérieur gauche
        x1, y1 = int(last_shape["x1"]), int(last_shape["y1"])   # Coordonnées du coin inférieur droit
        if x0 > x1:   # Assure que x0 est inférieur à x1
            x0, x1 = x1, x0
        if y0 > y1:   # Assure que y0 est inférieur à y1
            y0, y1 = y1, y0
    elif any(["shapes" in key for key in relayout_data]):   # Si plusieurs formes ont été ajoutées à la figure
        x0 = int([relayout_data[key] for key in relayout_data if "x0" in key][0])   # Coordonnée x0 du dernier rectangle
        x1 = int([relayout_data[key] for key in relayout_data if "x1" in key][0])   # Coordonnée x1 du dernier rectangle
        y0 = int([relayout_data[key] for key in relayout_data if "y0" in key][0])   # Coordonnée y0 du dernier rectangle
        y1 = int([relayout_data[key] for key in relayout_data if "y1" in key][0])   # Coordonnée y1 du dernier rectangle
    if all((x0, y0, x1, y1)):   # Vérifie si toutes les coordonnées sont non nulles
        roi_img = img[y0:y1, x0:x1]   # Sélectionne la zone d'intérêt (ROI) de l'image
        return (px.histogram(roi_img.ravel()), json.dumps(relayout_data, indent=2))   # Renvoie l'histogramme et les données d'annotation
    else:
        return (no_update,) * 2   # Aucune mise à jour nécessaire si aucune nouvelle annotation n'est présente

# Point d'entrée principal de l'application
if __name__ == "__main__":
    app.run(jupyter_mode="inline", port=8057)   # Exécute l'application en mode intégré (inline)
