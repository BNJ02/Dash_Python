from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# On crée une application Dash qui s'appelle "country_indicators"
app = Dash(__name__)

# On lit le fichier CSV des indicateurs de pays
df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

# On définit le layout de l'application Dash, qui contient :
# - Deux menus déroulants pour sélectionner les indicateurs à afficher
# - Deux boutons radio pour choisir le type d'axe (linéaire ou logarithmique)
# - Un graphique pour afficher les données
# - Un curseur pour sélectionner l'année
app.layout = html.Div([
    html.Div([
        # Premier menu déroulant pour sélectionner l'indicateur à afficher sur l'axe X
        html.Div([
            dcc.Dropdown(
                df['Indicator Name'].unique(),  # Liste des indicateurs disponibles
                'Fertility rate, total (births per woman)',  # Valeur par défaut
                id='xaxis-column'  # ID du composant
            ),
            # Boutons radio pour choisir le type d'axe X
            dcc.RadioItems(
                ['Linear', 'Log'],  # Options disponibles
                'Linear',  # Valeur par défaut
                id='xaxis-type',  # ID du composant
                inline=True  # Afficher les boutons côte à côte
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        # Deuxième menu déroulant pour sélectionner l'indicateur à afficher sur l'axe Y
        html.Div([
            dcc.Dropdown(
                df['Indicator Name'].unique(),  # Liste des indicateurs disponibles
                'Life expectancy at birth, total (years)',  # Valeur par défaut
                id='yaxis-column'  # ID du composant
            ),
            # Boutons radio pour choisir le type d'axe Y
            dcc.RadioItems(
                ['Linear', 'Log'],  # Options disponibles
                'Linear',  # Valeur par défaut
                id='yaxis-type',  # ID du composant
                inline=True  # Afficher les boutons côte à côte
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    # Graphique pour afficher les données
    dcc.Graph(id='indicator-graphic'),

    # Curseur pour sélectionner l'année
    dcc.Slider(
        df['Year'].min(),  # Valeur minimale
        df['Year'].max(),  # Valeur maximale
        step=None,  # Pas de valeurs intermédiaires
        id='year--slider',  # ID du composant
        value=df['Year'].max(),  # Valeur par défaut (année la plus récente)
        marks={str(year): str(year) for year in df['Year'].unique()},  # Étiquettes pour chaque année
    )
])

# Fonction de rappel pour mettre à jour le graphique en fonction des sélections de l'utilisateur
@callback(
    Output('indicator-graphic', 'figure'),  # Sortie : le graphique
    Input('xaxis-column', 'value'),  # Entrée : la valeur sélectionnée dans le premier menu déroulant
    Input('yaxis-column', 'value'),  # Entrée : la valeur sélectionnée dans le deuxième menu déroulant
    Input('xaxis-type', 'value'),  # Entrée : le type d'axe X sélectionné
    Input('yaxis-type', 'value'),  # Entrée : le type d'axe Y sélectionné
    Input('year--slider', 'value')  # Entrée : l'année sélectionnée
)
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    # On filtre le DataFrame pour ne garder que les lignes correspondant à l'année sélectionnée
    dff = df[df['Year'] == year_value]

    # On crée un graphique avec Plotly Express
    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],  # Données pour l'axe X
                     y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],  # Données pour l'axe Y
                     hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])  # Nom des pays affiché dans le hovertext

    # On ajoute des marges autour du graphique
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    # On définit le titre et le type d'axe X
    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    # On définit le titre et le type d'axe Y
    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    # On renvoie le graphique mis à jour
    return fig

# On lance l'application Dash
if __name__ == '__main__':
    app.run(debug=True)