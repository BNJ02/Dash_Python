# Import des modules nécessaires
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, no_update, callback
from skimage import data, draw
from scipy import ndimage

# Fonction pour convertir le chemin SVG en tableau numpy de coordonnées, chaque ligne étant un point (ligne, colonne)
def path_to_indices(path):
    indices_str = [
        el.replace("M", "").replace("Z", "").split(",") for el in path.split("L")
    ]
    return np.rint(np.array(indices_str, dtype=float)).astype(int)

# Fonction pour convertir le chemin SVG en un masque binaire où tous les pixels enfermés par le chemin sont True, et les autres pixels sont False.
def path_to_mask(path, shape):
    cols, rows = path_to_indices(path).T
    rr, cc = draw.polygon(rows, cols)
    mask = np.zeros(shape, dtype=bool)
    mask[rr, cc] = True
    mask = ndimage.binary_fill_holes(mask)
    return mask

# Chargement de l'image de test (une image de caméra)
img = data.camera()

# Création de la figure Plotly avec l'image en utilisant le mode de chaîne binaire
fig = px.imshow(img, binary_string=True)
fig.update_layout(dragmode="drawclosedpath")  # Activation du mode de dessin de chemin fermé

# Création de l'histogramme de l'image
fig_hist = px.histogram(img.ravel())

# Initialisation de l'application Dash
app = Dash(__name__)

# Définition de la mise en page de l'application
app.layout = html.Div(
    [
        html.H3("Dessinez un chemin pour afficher l'histogramme de la zone d'intérêt (ROI)"),
        html.Div(
            [dcc.Graph(id="graph-camera", figure=fig),],  # Affichage de la figure avec l'image
            style={"width": "60%", "display": "inline-block", "padding": "0 0"},
        ),
        html.Div(
            [dcc.Graph(id="graph-histogram", figure=fig_hist),],  # Affichage de l'histogramme initial
            style={"width": "40%", "display": "inline-block", "padding": "0 0"},
        ),
    ]
)

# Définition de la fonction de rappel pour mettre à jour l'histogramme en fonction du chemin dessiné
@callback(
    Output("graph-histogram", "figure"),   # Sortie : l'histogramme de la zone d'intérêt (ROI)
    Input("graph-camera", "relayoutData"),   # Entrée : les données de réorganisation de la figure
    prevent_initial_call=True,       # Ne pas appeler la fonction lors du démarrage initial
)
def on_new_annotation(relayout_data):
    if "shapes" in relayout_data:   # Vérifie si des formes ont été ajoutées à la figure
        last_shape = relayout_data["shapes"][-1]   # Récupère la dernière forme ajoutée (le dernier chemin dessiné)
        mask = path_to_mask(last_shape["path"], img.shape)   # Convertit le chemin en masque binaire
        return px.histogram(img[mask])   # Crée un nouvel histogramme pour la zone d'intérêt
    else:
        return no_update   # Aucune mise à jour nécessaire si aucune nouvelle annotation n'est présente

# Point d'entrée principal de l'application
if __name__ == "__main__":
    app.run(debug=True)   # Exécute l'application en mode débogage
