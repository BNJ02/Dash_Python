# Importation des modules Dash et autres modules nécessaires
from dash import Dash, dcc, html, Input, Output, callback
import numpy as np
import pandas as pd
import plotly.express as px

# Définition des feuilles de style externes à utiliser pour le tableau de bord
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Initialisation de l'application Dash
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Génération d'un DataFrame de données aléatoires avec 6 colonnes
np.random.seed(0)  # Seed pour la reproductibilité des données
df = pd.DataFrame({"Col " + str(i + 1): np.random.rand(30) for i in range(6)})

# Définition de la mise en page du tableau de bord
app.layout = html.Div(
    [
        # Trois graphiques disposés en lignes et chacun dans une colonne de largeur quatre
        html.Div(
            dcc.Graph(id="g1", config={"displayModeBar": False}),
            className="four columns",
        ),
        html.Div(
            dcc.Graph(id="g2", config={"displayModeBar": False}),
            className="four columns",
        ),
        html.Div(
            dcc.Graph(id="g3", config={"displayModeBar": False}),
            className="four columns",
        ),
    ],
    className="row",
)

# Définition d'une fonction pour obtenir la figure du graphique en fonction des données sélectionnées
def get_figure(df, x_col, y_col, selectedpoints, selectedpoints_local):

    # Gestion de la sélection des points dans le graphique
    if selectedpoints_local and selectedpoints_local["range"]:
        ranges = selectedpoints_local["range"]
        selection_bounds = {
            "x0": ranges["x"][0],
            "x1": ranges["x"][1],
            "y0": ranges["y"][0],
            "y1": ranges["y"][1],
        }
    else:
        selection_bounds = {
            "x0": np.min(df[x_col]),
            "x1": np.max(df[x_col]),
            "y0": np.min(df[y_col]),
            "y1": np.max(df[y_col]),
        }

    # Création du graphique avec Plotly Express
    fig = px.scatter(df, x=df[x_col], y=df[y_col], text=df.index)

    # Mise à jour du style des points sélectionnés et non sélectionnés
    fig.update_traces(
        selectedpoints=selectedpoints,
        customdata=df.index,
        mode="markers+text",
        marker={"color": "rgba(0, 116, 217, 0.7)", "size": 20},
        unselected={
            "marker": {"opacity": 0.3},
            "textfont": {"color": "rgba(0, 0, 0, 0)"},
        },
    )

    # Mise à jour du layout du graphique
    fig.update_layout(
        margin={"l": 20, "r": 0, "b": 15, "t": 5},
        dragmode="select",
        hovermode=False,
        newselection_mode="gradual",
    )

    # Ajout d'une zone de sélection sur le graphique
    fig.add_shape(
        dict(
            {"type": "rect", "line": {"width": 1, "dash": "dot", "color": "darkgrey"}},
            **selection_bounds
        )
    )
    return fig

# Définition de la fonction de callback pour mettre à jour les graphiques en fonction des sélections
@callback(
    Output("g1", "figure"),
    Output("g2", "figure"),
    Output("g3", "figure"),
    Input("g1", "selectedData"),
    Input("g2", "selectedData"),
    Input("g3", "selectedData"),
)
def callback(selection1, selection2, selection3):
    selectedpoints = df.index
    for selected_data in [selection1, selection2, selection3]:
        if selected_data and selected_data["points"]:
            selectedpoints = np.intersect1d(
                selectedpoints, [p["customdata"] for p in selected_data["points"]]
            )

    # Renvoi des figures mises à jour
    return [
        get_figure(df, "Col 1", "Col 2", selectedpoints, selection1),
        get_figure(df, "Col 3", "Col 4", selectedpoints, selection2),
        get_figure(df, "Col 5", "Col 6", selectedpoints, selection3),
    ]

# Démarrage de l'application en mode débogage si ce script est exécuté en tant que programme principal
if __name__ == "__main__":
    app.run(debug=True)
