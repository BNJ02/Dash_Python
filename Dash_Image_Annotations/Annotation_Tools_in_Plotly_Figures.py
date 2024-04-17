# Importation des modules nécessaires
import plotly.express as px
from dash import Dash, dcc, html
from skimage import data

# Chargement d'une image à partir du module scikit-image
img = data.chelsea()

# Création d'une figure Plotly Express à partir de l'image chargée
fig = px.imshow(img)

# Mise à jour de la configuration de la figure pour permettre le dessin de rectangles
fig.update_layout(dragmode="drawrect")

# Configuration des boutons d'annotations à ajouter à la barre d'outils
config = {
    "modeBarButtonsToAdd": [
        "drawline",          # Ligne
        "drawopenpath",      # Chemin ouvert
        "drawclosedpath",    # Chemin fermé
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
        dcc.Graph(figure=fig, config=config),  # Graphique interactif avec la figure et la configuration
    ]
)

# Démarrage de l'application en mode débogage si ce script est exécuté en tant que programme principal
if __name__ == "__main__":
    app.run(debug=True)
