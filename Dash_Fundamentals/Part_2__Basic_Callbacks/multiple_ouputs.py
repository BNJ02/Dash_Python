# Importer les bibliothèques nécessaires
from dash import Dash, dcc, html, Input, Output, callback

# Importer le style externe à partir d'une URL
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Créer l'application Dash et lui passer les feuilles de style externes
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Définir le layout de l'application
app.layout = html.Div([
    # Créer une entrée de type "number" avec l'ID 'num-multi' et une valeur initiale de 5
    dcc.Input(
        id='num-multi',
        type='number',
        value=5
    ),
    # Créer une table avec cinq lignes et deux colonnes par ligne
    html.Table([
        html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]), # Première ligne : afficher x² dans la deuxième colonne
        html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),   # Deuxième ligne : afficher x³ dans la deuxième colonne
        html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),    # Troisième ligne : afficher 2^x dans la deuxième colonne
        html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),   # Quatrième ligne : afficher 3^x dans la deuxième colonne
        html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),  # Cinquième ligne : afficher x^x dans la deuxième colonne
    ]),
])

# Définir la fonction de rappel qui met à jour les cellules de la table en fonction de la valeur de l'entrée
@callback(
    # Définir les sorties de la fonction de rappel : les enfants des cellules avec les IDs 'square', 'cube', 'twos', 'threes' et 'x^x'
    Output('square', 'children'),
    Output('cube', 'children'),
    Output('twos', 'children'),
    Output('threes', 'children'),
    Output('x^x', 'children'),
    # Définir l'entrée de la fonction de rappel : la valeur de l'entrée avec l'ID 'num-multi'
    Input('num-multi', 'value')
)
def callback_a(x):
    # Retourner les résultats des cinq opérations mathématiques impliquant la valeur entrée par l'utilisateur
    return x**2, x**3, 2**x, 3**x, x**x

# Exécuter l'application Dash
if __name__ == '__main__':
    app.run(debug=True)