# Import des modules nécessaires
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import dash_daq as daq
from skimage import data

# Chargement de l'image de test (une image de chat)
img = data.chelsea()

# Création de la figure Plotly avec l'image et configuration du style des annotations
fig = px.imshow(img)
fig.update_layout(
    dragmode="drawrect",  # Mode de dessin : rectangle
    newshape=dict(
        fillcolor="cyan",   # Couleur de remplissage des annotations : cyan
        opacity=0.3,        # Opacité des annotations : 0.3 (30%)
        line=dict(
            color="darkblue",   # Couleur de la ligne de contour des annotations : bleu foncé
            width=8             # Épaisseur de la ligne de contour des annotations : 8 pixels
        )
    )
)

# Initialisation de l'application Dash
app = Dash(__name__)

# Définition de la mise en page de l'application
app.layout = html.Div(
    [
        html.H3("Faites glisser et dessinez des annotations"),
        dcc.Graph(id="graph-styled-annotations", figure=fig),  # Affichage de la figure avec l'image et les annotations
        html.Pre('Opacité des annotations'),
        dcc.Slider(
            id="opacity-slider",    # Identifiant du curseur d'opacité
            min=0, max=1, value=0.5, step=0.1,  # Valeurs minimale, maximale, par défaut et incréments du curseur
            tooltip={'always_visible': True}    # Affichage de la valeur du curseur en permanence
        ),
        daq.ColorPicker(
            id="annotation-color-picker",          # Identifiant du sélecteur de couleur
            label="Sélecteur de couleur",         # Étiquette du sélecteur de couleur
            value=dict(hex="#119DFF")             # Valeur initiale de la couleur sélectionnée en format hexadécimal
        ),
    ]
)

# Définition de la fonction de rappel pour changer le style des annotations en fonction des valeurs des widgets interactifs
@callback(
    Output("graph-styled-annotations", "figure"),   # Sortie : la figure mise à jour avec le nouveau style des annotations
    Input("opacity-slider", "value"),              # Entrée : la valeur d'opacité sélectionnée par l'utilisateur
    Input("annotation-color-picker", "value"),     # Entrée : la couleur sélectionnée par l'utilisateur
    prevent_initial_call=True,                     # Ne pas appeler la fonction lors du démarrage initial
)
def on_style_change(slider_value, color_value):
    # Création d'une nouvelle figure avec l'image et mise à jour du style des annotations
    fig = px.imshow(img)
    fig.update_layout(
        dragmode="drawrect",                        # Mode de dessin : rectangle
        newshape=dict(
            opacity=slider_value,                   # Mise à jour de l'opacité des annotations
            fillcolor=color_value["hex"],           # Mise à jour de la couleur de remplissage des annotations
        )
    )
    return fig

# Point d'entrée principal de l'application
if __name__ == "__main__":
    app.run(debug=True)  # Exécute l'application en mode débogage
