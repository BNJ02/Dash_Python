from dash import Dash, dcc, html, Input, Output, callback, no_update
import plotly.express as px
import numpy as np
from skimage import data

import base64, io

from PIL import Image

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__) # , external_stylesheets=external_stylesheets

# Chargement d'une image à partir du module scikit-image
img_default = data.chelsea()

# Création d'une figure Plotly Express à partir de l'image chargée
fig = px.imshow(img_default)

# Mise à jour de la configuration de la figure pour permettre le dessin de rectangles
fig.update_layout(dragmode="drawrect")

# Configuration des boutons d'annotations à ajouter à la barre d'outils
config = {
    "modeBarButtonsToAdd": [
        "drawcircle",        # Cercle
        "drawrect",          # Rectangle
        "eraseshape",        # Effacer la forme
    ]
}

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidsth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
    dcc.Graph(id='graph', figure=fig, config=config)  # Graphique interactif avec la figure et la configuration
])

@callback(
    Output('graph', 'figure'),
    Input('upload-image', 'contents')
)
def update_output(contents):
    if contents is not None:
        # Convertir les données de l'image en base64
        img_data = contents[0].split(",")[1]
        # Décoder les données base64 en tant qu'objet image
        decoded_img = base64.b64decode(img_data)
        img_obj = Image.open(io.BytesIO(decoded_img))
        # Créer une nouvelle figure Plotly Express avec l'objet image
        new_fig = px.imshow(np.array(img_obj))
        new_fig.update_layout(dragmode="drawrect")
        return new_fig
    else:
        return no_update

if __name__ == '__main__':
    app.run(debug=True)
