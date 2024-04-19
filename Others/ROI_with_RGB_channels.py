import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output, callback, no_update
import numpy as np
from skimage import data

# Chargement d'une image à partir du module scikit-image
img_default = data.chelsea()

# Conversion de l'image en tableau NumPy
img_array = np.array(img_default)

# Séparer les canaux de couleur
red_channel = img_array[:, :, 0]
green_channel = img_array[:, :, 1]
blue_channel = img_array[:, :, 2]

fig_hist = go.Figure()
fig_hist.add_trace(go.Histogram(
    x=red_channel.ravel(),
    histnorm='',
    name='Red', # name used in legend and hover labels
    marker_color='#FF0000', # Red color
    opacity=0.75
))
fig_hist.add_trace(go.Histogram(
    x=green_channel.ravel(),
    histnorm='',
    name='Green',
    marker_color='#00FF00', # Green color
    opacity=0.75
))

fig_hist.add_trace(go.Histogram(
    x=blue_channel.ravel(),
    histnorm='',
    name='Blue',
    marker_color='#0000FF', # Blue color
    opacity=0.75
))

# Mise en forme de la figure
fig_hist.update_layout(
    title='Superposition de plusieurs fonctions sur un histogramme',
    xaxis_title='Valeurs 8bits des pixels',
    yaxis_title='Apparition dans le ROI',
)

# Initialisation de l'application Dash
app = Dash(__name__)

# Définition de la mise en page de l'application
app.layout = html.Div(
    [
        html.H3("Faites glisser un rectangle pour afficher l'histogramme de la zone d'intérêt (ROI)"),
        html.Div(
            [dcc.Graph(id="graph", figure=px.imshow(img_default)),],  # Affichage de la figure avec l'image
            style={"width": "60%", "display": "inline-block", "padding": "0 0"},
        ),
        html.Div(
            [dcc.Graph(id="histogram", figure=fig_hist),],  # Affichage de l'histogramme initial
            style={"width": "40%", "display": "inline-block", "padding": "0 0"},
        ),
    ]
)

# Point d'entrée principal de l'application
if __name__ == "__main__":
    app.run_server(debug=True)   # Exécute l'application en mode débogage
