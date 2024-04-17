# Importer les bibliothèques nécessaires
from dash import Dash, dcc, html, Input, Output, State, callback

# Importer les feuilles de style externes
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Créer une instance de l'application Dash
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Définir le layout de l'application
app.layout = html.Div([
    # Créer un champ de texte avec l'identifiant "input-1-state" et une valeur initiale de "Montréal"
    dcc.Input(id='input-1-state', type='text', value='Montréal'),
    # Créer un deuxième champ de texte avec l'identifiant "input-2-state" et une valeur initiale de "Canada"
    dcc.Input(id='input-2-state', type='text', value='Canada'),
    # Créer un bouton de soumission avec l'identifiant "submit-button-state"
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    # Créer une zone de sortie avec l'identifiant "output-state"
    html.Div(id='output-state')
])

# Définir la fonction de rappel qui est déclenchée lorsqu'on clique sur le bouton de soumission
@callback(
    # Sortie: la zone de sortie avec l'identifiant "output-state"
    Output('output-state', 'children'),
    # Entrée: le nombre de clics sur le bouton avec l'identifiant "submit-button-state"
    Input('submit-button-state', 'n_clicks'),
    # Entrée: la valeur du premier champ de texte avec l'identifiant "input-1-state"
    State('input-1-state', 'value'),
    # Entrée: la valeur du deuxième champ de texte avec l'identifiant "input-2-state"
    State('input-2-state', 'value'),
)
def update_output(n_clicks, input1, input2):
    # Retourner une chaîne de caractères formatée qui affiche le nombre de fois que le bouton a été pressé,
    # ainsi que les valeurs des deux champs de texte
    return f'''
        The Button has been pressed {n_clicks} times,
        Input 1 is "{input1}",
        and Input 2 is "{input2}"
    '''

# Démarrer l'application Dash
if __name__ == '__main__':
    app.run(debug=True)