# Import des modules nécessaires
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback
from skimage import data

# Chargement de l'image de test (une image de caméra)
img = data.camera()

# Création de la figure Plotly avec l'image en utilisant le mode de chaîne binaire
fig = px.imshow(img, binary_string=True)
fig.update_layout(dragmode="drawrect")  # Activation du mode de dessin de rectangle

# Création de l'histogramme de l'image
fig_hist = px.histogram(img.ravel())

# Initialisation de l'application Dash
app = Dash(__name__)

# Définition de la mise en page de l'application
app.layout = html.Div(
    [
        html.H3("Faites glisser un rectangle pour afficher l'histogramme de la zone d'intérêt (ROI)"),
        html.Div(
            [dcc.Graph(id="graph-pic-camera", figure=fig),],  # Affichage de la figure avec l'image
            style={"width": "60%", "display": "inline-block", "padding": "0 0"},
        ),
        html.Div(
            [dcc.Graph(id="histogram", figure=fig_hist),],  # Affichage de l'histogramme initial
            style={"width": "40%", "display": "inline-block", "padding": "0 0"},
        ),
    ]
)

# Définition de la fonction de rappel pour mettre à jour l'histogramme en fonction de la zone d'intérêt sélectionnée
@callback(
    Output("histogram", "figure"),   # Sortie : l'histogramme de la zone d'intérêt (ROI)
    Input("graph-pic-camera", "relayoutData"),   # Entrée : les données de réorganisation de la figure
    prevent_initial_call=True,       # Ne pas appeler la fonction lors du démarrage initial
)
def on_new_annotation(relayout_data):
    if "shapes" in relayout_data:   # Vérifie si des formes ont été ajoutées à la figure
        last_shape = relayout_data["shapes"][-1]   # Récupère la dernière forme ajoutée (le dernier rectangle dessiné)
        # Les coordonnées de la forme sont des flottants, nous devons les convertir en entiers pour découper l'image
        x0, y0 = int(last_shape["x0"]), int(last_shape["y0"])   # Coordonnées du coin supérieur gauche
        x1, y1 = int(last_shape["x1"]), int(last_shape["y1"])   # Coordonnées du coin inférieur droit
        roi_img = img[y0:y1, x0:x1]   # Sélectionne la zone d'intérêt (ROI) de l'image
        return px.histogram(roi_img.ravel())   # Crée un nouvel histogramme pour la zone d'intérêt
    else:
        return no_update   # Aucune mise à jour nécessaire si aucune nouvelle annotation n'est présente

# Point d'entrée principal de l'application
if __name__ == "__main__":
    app.run(debug=True)   # Exécute l'application en mode débogage
