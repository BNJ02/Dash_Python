import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback, no_update
import plotly.express as px
import numpy as np
from skimage import data

# Chargement d'une image à partir du module scikit-image
img_default = data.chelsea()

# Création d'une figure Plotly Express à partir de l'image chargée
fig = px.imshow(img_default)

# Mise à jour de la configuration de la figure pour permettre le dessin de rectangles
fig.update_layout(dragmode="drawrect")

# Création de l'histogramme de l'image
fig_hist = px.histogram(img_default.ravel())

app = Dash(__name__)

# Définition de la mise en page de l'application
app.layout = html.Div(
    [
        html.H3("Faites glisser un rectangle pour afficher l'histogramme de la zone d'intérêt (ROI)"),
        html.Div(
            [dcc.Graph(id="graph", figure=fig),],  # Affichage de la figure avec l'image
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
    Input("graph", "relayoutData"),   # Entrée : les données de réorganisation de la figure
    prevent_initial_call=True,       # Ne pas appeler la fonction lors du démarrage initial
)
def on_new_annotation(relayout_data):
    if "shapes" in relayout_data:   # Vérifie si des formes ont été ajoutées à la figure
        last_shape = relayout_data["shapes"][-1]   # Récupère la dernière forme ajoutée (le dernier rectangle dessiné)
        # Les coordonnées de la forme sont des flottants, nous devons les convertir en entiers pour découper l'image
        x0, y0 = int(last_shape["x0"]), int(last_shape["y0"])   # Coordonnées du coin supérieur gauche
        x1, y1 = int(last_shape["x1"]), int(last_shape["y1"])   # Coordonnées du coin inférieur droit
        roi_img = img_default[y0:y1, x0:x1]   # Sélectionne la zone d'intérêt (ROI) de l'image
        
        img_array = np.array(roi_img)

        # Séparer les canaux de couleur
        red_channel = img_array[:, :, 0]
        green_channel = img_array[:, :, 1]
        blue_channel = img_array[:, :, 2]

        # Créer un graphique 3D
        fig = go.Figure()

        # Ajouter les surfaces pour chaque canal de couleur
        fig.add_surface(z=red_channel, name='Red', colorscale='Reds', showscale=False)
        fig.add_surface(z=green_channel, name='Green', colorscale='Greens', showscale=False)
        fig.add_surface(z=blue_channel, name='Blue', colorscale='Blues', showscale=False)

        # Mise en forme du titre et des étiquettes
        fig.update_layout(
            title='Décomposition des canaux de couleur',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Intensité',
            )
        )
        
        return fig   # Crée un nouvel histogramme pour la zone d'intérêt
    else:
        return no_update   # Aucune mise à jour nécessaire si aucune nouvelle annotation n'est présente

# Point d'entrée principal de l'application
if __name__ == "__main__":
    app.run(debug=True)   # Exécute l'application en mode débogage
