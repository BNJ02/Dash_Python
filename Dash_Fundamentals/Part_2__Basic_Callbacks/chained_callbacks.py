# Importer les bibliothèques nécessaires pour créer l'application Dash
from dash import Dash, dcc, html, Input, Output, callback

# Importer le style externe à partir d'une URL
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Créer l'application Dash et lui passer les feuilles de style externes
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Définir un dictionnaire contenant les options pour les pays et les villes
all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': ['Montréal', 'Toronto', 'Ottawa']
}

# Définir le layout de l'application Dash
app.layout = html.Div([
    # Créer un groupe de boutons radio pour les pays avec l'ID 'countries-radio'
    dcc.RadioItems(
        list(all_options.keys()),  # Liste des pays à afficher
        'America',  # Valeur sélectionnée par défaut
        id='countries-radio',  # ID du groupe de boutons radio
    ),

    # Ajouter une ligne horizontale
    html.Hr(),

    # Créer un groupe de boutons radio pour les villes avec l'ID 'cities-radio'
    dcc.RadioItems(id='cities-radio'),

    # Ajouter une ligne horizontale
    html.Hr(),

    # Créer un Div qui affichera les valeurs sélectionnées
    html.Div(id='display-selected-values')
])

# Définir la fonction de rappel pour mettre à jour les options des boutons radio des villes
@callback(
    # Sortie : les options des boutons radio des villes
    Output('cities-radio', 'options'),
    # Entrée : la valeur sélectionnée pour le pays
    Input('countries-radio', 'value'))
def set_cities_options(selected_country):
    # Retourner une liste de dictionnaires contenant les labels et les valeurs pour les villes
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

# Définir la fonction de rappel pour mettre à jour la valeur sélectionnée pour les boutons radio des villes
@callback(
    # Sortie : la valeur sélectionnée pour les boutons radio des villes
    Output('cities-radio', 'value'),
    # Entrée : les options disponibles pour les boutons radio des villes
    Input('cities-radio', 'options'))
def set_cities_value(available_options):
    # Retourner la première valeur disponible dans la liste d'options
    return available_options[0]['value']

# Définir la fonction de rappel pour afficher les valeurs sélectionnées pour les pays et les villes
@callback(
    # Sortie : le texte à afficher dans le Div
    Output('display-selected-values', 'children'),
    # Entrée : la valeur sélectionnée pour le pays
    Input('countries-radio', 'value'),
    # Entrée : la valeur sélectionnée pour les villes
    Input('cities-radio', 'value'))
def set_display_children(selected_country, selected_city):
    # Retourner une chaîne de caractères formatée contenant les valeurs sélectionnées
    return f'{selected_city} is a city in {selected_country}'

# Exécuter l'application Dash
if __name__ == '__main__':
    app.run(debug=True)