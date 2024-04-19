# Importation des modules nécessaires
from dash import Dash, dcc, html, Input, Output, no_update, callback

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from skimage import data
from PIL import Image

import json, re, base64, io

# Chargement d'une image à partir du module scikit-image
img_default = data.chelsea()

# Création d'une figure Plotly Express à partir de l'image chargée
fig = px.imshow(img_default)

# Conversion de l'image en tableau NumPy
img_array = np.array(img_default)

# Séparer les canaux de couleur
red_channel = img_array[:, :, 0]
green_channel = img_array[:, :, 1]
blue_channel = img_array[:, :, 2]

fig_hist = go.Figure()
fig_hist.add_trace(go.Histogram(
    x=red_channel.ravel(),
    name='Red', # name used in legend and hover labels
    marker_color='#FF0000' # Red color
))
fig_hist.add_trace(go.Histogram(
    x=green_channel.ravel(),
    name='Green',
    marker_color='#00FF00' # Green color
))
fig_hist.add_trace(go.Histogram(
    x=blue_channel.ravel(),
    name='Blue',
    marker_color='#0000FF' # Blue color
))

# Mise en forme de la figure
fig_hist.update_layout(
    title='Number of pixels as a function of channel intensity value',
    xaxis_title='8bit pixel values',
    yaxis_title='count in ROI'
)

# Mise à jour de la configuration de la figure pour permettre le dessin de rectangles
fig.update_layout(dragmode="drawrect", title='Matrix image with annotations')

# Configuration des boutons d'annotations à ajouter à la barre d'outils
config = {
    "modeBarButtonsToAdd": [
        # "drawcircle",        # Cercle
        "drawrect",          # Rectangle
        "eraseshape",        # Effacer la forme
    ]
}

# Initialisation de l'application Dash
app = Dash(__name__)

# Définition de la mise en page du tableau de bord
app.layout = html.Div(
    [
        dcc.Store(id='image-store', data=img_default.tolist()),  # Stockage de l'image téléchargée
        html.H1(children="Drag and draw annotations", style={"textAlign": "center"}),  # Titre du tableau de bord
        dcc.Upload(
            id='upload-image',
            children=html.Div(['Drag and Drop or Select a picture']),
            style={
                'width': '15%',
                'height': '30px',
                'lineHeight': '30px',
                'borderWidsth': '1px',
                'borderRadius': '15px',
                'borderStyle': 'dashed',
                'textAlign': 'center',
                'backgroundColor': 'grey',
                "margin": "auto", 
                "display": "block",
            },
        ),
        html.Div(
            [dcc.Graph(id='graph', figure=fig, config=config),],  # Graphique interactif avec la figure et la configuration     
            style={"width": "60%", "display": "inline-block", "padding": "0 0"},
        ),
        html.Div(
            [dcc.Graph(id="histogram", figure=fig_hist),],
            style={"width": "40%", "display": "inline-block", "padding": "0 0"},
        ),
        html.Hr(),  # Ligne horizontale pour séparer le graphique des données JSON
        html.Div(children="JSON Output:", style={"margin-bottom": "20px", "margin-top": "20px"}),  # Titre pour les données JSON des annotations
        html.Div(       # Div pour afficher les données JSON des annotations
            id='output-json',
            style={"border": "1px solid black", "padding": "10px", "width": "95%", "height": "200px", "overflowY": "scroll", "margin": "auto", "display": "block"}  # Ajout de bordures et de marges pour le conteneur du texte
        )
    ]
)

# Fonction callback pour mettre à jour l'image affichée en fonction de l'image téléchargée
@callback(
    Output('graph', 'figure'),
    Output('image-store', 'data'), 
    Input('upload-image', 'contents')
)
def update_output(contents):
    if contents is not None:
        # Convertir les données de l'image en base64
        img_data = contents.split(",")[1]
        # Décoder les données base64 en tant qu'objet image
        decoded_img = base64.b64decode(img_data)
        img_obj = Image.open(io.BytesIO(decoded_img))
        img_array = np.array(img_obj)
        print(img_array.shape)
        # Créer une nouvelle figure Plotly Express avec l'objet image
        new_fig = px.imshow(np.array(img_obj))
        new_fig.update_layout(dragmode="drawrect")
        # Supprimer les annotations précédentes
        with open('annotations.json', 'w') as f:  # Ouvre un fichier JSON en écriture
            json.dump('', f)  # Écrit les annotations dans le fichier JSON
        return (new_fig, img_array.tolist())
    else:
        return (no_update,) *2
    

# Fonction callback pour capturer les annotations dessinées && mettre à jour l'histogramme de l'image en fonction de la région d'intérêt (ROI) sélectionnée
@app.callback(
    Output('output-json', 'children'),  # Mise à jour d'un élément HTML pour afficher les données JSON
    Output("histogram", "figure"), # Mise à jour de l'histogramme de l'image
    Input('graph', 'relayoutData'),  # Déclenchement de la fonction à chaque fois qu'une annotation est dessinée
    Input('image-store', 'data')  # Déclenchement de la fonction à chaque fois qu'une annotation est dessinée
)
def save_annotations(relayout_data, img_data):
    print(relayout_data)

    if img_data is not None:
        img = np.array(img_data)
        if relayout_data is not None and 'shapes' in relayout_data and len(relayout_data["shapes"]) > 0: # Vérifie si des annotations ont été trouvées
                last_shape = relayout_data["shapes"][-1]
                # shape coordinates are floats, we need to convert to ints for slicing
                x0, y0 = int(last_shape["x0"]), int(last_shape["y0"])
                x1, y1 = int(last_shape["x1"]), int(last_shape["y1"])
                roi_img = img[y0:y1, x0:x1]  # Récupère la région d'intérêt (ROI) de l'image
        else:
            roi_img = img  # Récupère l'image entière si aucune annotation n'est trouvée

        # Séparer les canaux de couleur
        red_channel = roi_img[:, :, 0]
        green_channel = roi_img[:, :, 1]
        blue_channel = roi_img[:, :, 2]

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=red_channel.ravel(),
            name='Red', # name used in legend and hover labels
            marker_color='#FF0000' # Red color
        ))
        fig_hist.add_trace(go.Histogram(
            x=green_channel.ravel(),
            name='Green',
            marker_color='#00FF00' # Green color
        ))
        fig_hist.add_trace(go.Histogram(
            x=blue_channel.ravel(),
            name='Blue',
            marker_color='#0000FF' # Blue color
        ))

        # Mise en forme de la figure
        fig_hist.update_layout(
            title='Number of pixels as a function of channel intensity value',
            xaxis_title='8bit pixel values',
            yaxis_title='count in ROI'
        )

    if relayout_data is not None and 'shapes' in relayout_data:  # Vérifie si des formes ont été dessinées
        annotations = relayout_data['shapes']  # Récupère les annotations dessinées
        with open('annotations.json', 'w') as f:  # Ouvre un fichier JSON en écriture
            json.dump(annotations, f, indent=4)  # Écrit les annotations dans le fichier JSON avec un formatage indenté
        
        return (json.dumps(relayout_data), fig_hist)

    elif relayout_data is not None and any(key.startswith('shapes[') for key in relayout_data.keys()):
        # Expression régulière pour trouver le chiffre entre crochets de relayout_data.keys()
        pattern = r'\[(\d+)\]'

        # Utilisation de re.search pour trouver le motif dans la chaîne
        match = re.search(pattern, next(iter(relayout_data.keys())))
        shape_index = int(match.group(1)) # Trouve et convertie en entier pour avoir l'index de notre figure

        # Étape 1 : Charger les données existantes du fichier JSON
        with open("annotations.json", "r") as f:    # Ouvre un fichier JSON en lecture
            annotations = json.load(f)              # Charge le json dans annotations

        # Étape 2 : Modifier les données
        for key in ['x0', 'x1', 'y0', 'y1']:
            annotations[shape_index][key] = relayout_data[f"shapes[{shape_index}].{key}"]

        # Étape 3 : Écrire les données modifiées dans le même fichier JSON
        with open('annotations.json', 'w') as f:  # Ouvre un fichier JSON en écriture
            json.dump(annotations, f, indent=4)  # Écrit les annotations dans le fichier JSON avec un formatage indenté

        return (json.dumps(annotations), fig_hist)  # Retourne un message de succès si les annotations sont sauvegardées
    else:
        return (json.dumps(obj=''), fig_hist)  # Retourne une chaîne vide si aucune annotation n'a été trouvée

# Démarrage de l'application en mode débogage si ce script est exécuté en tant que programme principal
if __name__ == "__main__":
    app.run(debug=True, port=8057)  # Exécute l'application en mode débogage (debug=True) sur le port 8057 (par défaut)
