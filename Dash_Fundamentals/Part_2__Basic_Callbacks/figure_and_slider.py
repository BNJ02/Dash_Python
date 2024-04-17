from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

import pandas as pd

# Importer le dataset Gapminder
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# Créer l'application Dash
app = Dash(__name__)

# Définir le layout de l'application
app.layout = html.Div([
    # Ajouter un graphique avec un identifiant 'graph-with-slider'
    dcc.Graph(id='graph-with-slider'),
    # Ajouter un curseur avec un identifiant 'year-slider'
    dcc.Slider(
        # Définir la plage de valeurs du curseur en utilisant les années minimales et maximales du dataset
        df['year'].min(),
        df['year'].max(),
        # Définir le pas du curseur sur None pour autoriser toutes les valeurs entières dans la plage
        step=None,
        # Définir la valeur initiale du curseur sur la première année du dataset
        value=df['year'].min(),
        # Définir les repères du curseur en utilisant les années uniques du dataset
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    )
])

# Définir la fonction de rappel pour mettre à jour le graphique en fonction de la valeur sélectionnée dans le curseur
@callback(
    # Définir la sortie de la fonction de rappel sur le graphique avec l'identifiant 'graph-with-slider'
    Output('graph-with-slider', 'figure'),
    # Définir l'entrée de la fonction de rappel sur la valeur sélectionnée dans le curseur avec l'identifiant 'year-slider'
    Input('year-slider', 'value'))
def update_figure(selected_year):
    # Filtrer le dataset pour ne conserver que les lignes correspondant à l'année sélectionnée
    filtered_df = df[df.year == selected_year]

    # Créer un graphique scatter en utilisant le dataset filtré
    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     # Définir la taille des points en fonction de la population
                     size="pop",
                     # Définir la couleur des points en fonction du continent
                     color="continent",
                     # Définir le nom des points en fonction du nom du pays
                     hover_name="country",
                     # Utiliser une échelle logarithmique pour l'axe des x
                     log_x=True,
                     # Définir la taille maximale des points
                     size_max=55)

    # Mettre à jour le layout du graphique pour ajouter une durée de transition de 500 millisecondes
    fig.update_layout(transition_duration=500)

    # Retourner le graphique mis à jour
    return fig

# Démarrer l'application Dash
if __name__ == '__main__':
    app.run(debug=True)