# Importation des modules nécessaires
import plotly.express as px
from dash import Dash, dcc, html
from skimage import data

import json, re
from dash.dependencies import Input, Output

# Chargement d'une image à partir du module scikit-image
img = data.chelsea()

# Création d'une figure Plotly Express à partir de l'image chargée
fig = px.imshow(img)

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

# Initialisation de l'application Dash
app = Dash(__name__)

# Définition de la mise en page du tableau de bord
app.layout = html.Div(
    [
        html.H3("Drag and draw annotations"),  # Titre du tableau de bord
        dcc.Graph(id='graph', figure=fig, config=config),  # Graphique interactif avec la figure et la configuration
        html.Div(id='output-json')  # Div pour afficher le message de confirmation et les données JSON
    ]
)

# Fonction callback pour capturer les annotations dessinées
@app.callback(
    Output('output-json', 'children'),  # Mise à jour d'un élément HTML pour afficher les données JSON
    Input('graph', 'relayoutData')  # Déclenchement de la fonction à chaque fois qu'une annotation est dessinée
)
def save_annotations(relayout_data):
    print(relayout_data)
    if 'shapes' in relayout_data:  # Vérifie si des formes ont été dessinées
        annotations = relayout_data['shapes']  # Récupère les annotations dessinées
        with open('annotations.json', 'w') as f:  # Ouvre un fichier JSON en écriture
            json.dump(annotations, f, indent=4)  # Écrit les annotations dans le fichier JSON avec un formatage indenté
        return 'Annotations saved successfully!'  # Retourne un message de succès si les annotations sont sauvegardées
    elif any(key.startswith('shapes[') for key in relayout_data.keys()):
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
        return 'Annotations modified saved successfully!'  # Retourne un message de succès si les annotations sont sauvegardées
    else:
        return ''  # Retourne une chaîne vide si aucune annotation n'a été trouvée

# Démarrage de l'application en mode débogage si ce script est exécuté en tant que programme principal
if __name__ == "__main__":
    app.run(debug=True)
