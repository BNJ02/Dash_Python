# Importer les bibliothèques nécessaires
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import json
import pandas as pd

# Définir les feuilles de style externes à utiliser
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Créer une instance de l'application Dash
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Définir les styles à utiliser pour les prévisualisations de texte
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# Créer un DataFrame pandas avec des données de démonstration
df = pd.DataFrame({
    "x": [1,2,1,2],
    "y": [1,2,3,4],
    "customdata": [1,2,3,4],
    "fruit": ["apple", "apple", "orange", "orange"]
})

# Créer un graphique avec Plotly Express en utilisant les données du DataFrame
fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])

# Mettre à jour le layout du graphique pour activer le mode click+event
fig.update_layout(clickmode='event+select')

# Mettre à jour les traces du graphique pour définir la taille des marqueurs
fig.update_traces(marker_size=20)

# Définir le layout de l'application Dash
app.layout = html.Div([
    # Ajouter un graphique interactif à l'application
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),

    # Ajouter des prévisualisations de texte pour afficher les données de hover, click, sélection et reconfiguration
    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')
    ])
])

# Définir une fonction de rappel pour afficher les données de hover
@callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

# Définir une fonction de rappel pour afficher les données de click
@callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

# Définir une fonction de rappel pour afficher les données de sélection
@callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)

# Définir une fonction de rappel pour afficher les données de reconfiguration
@callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)

# Exécuter l'application si ce fichier est le script principal
if __name__ == '__main__':
    app.run(debug=True)