# Importer les bibliothèques nécessaires
from dash import Dash, dcc, html, Input, Output, callback

# Importer les feuilles de style externes
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Créer une instance de l'application Dash
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Définir le layout de l'application
app.layout = html.Div([
    # Créer un champ de texte avec l'identifiant "input-1" et une valeur initiale de "Montréal"
    dcc.Input(id="input-1", type="text", value="Montréal"),
    # Créer un deuxième champ de texte avec l'identifiant "input-2" et une valeur initiale de "Canada"
    dcc.Input(id="input-2", type="text", value="Canada"),
    # Créer une zone de sortie avec l'identifiant "number-output"
    html.Div(id="number-output"),
])

# Définir la fonction de rappel qui est déclenchée lorsqu'une valeur est saisie dans l'un des deux champs de texte
@callback(
    # Sortie: la zone de sortie avec l'identifiant "number-output"
    Output("number-output", "children"),
    # Entrée: la valeur du premier champ de texte avec l'identifiant "input-1"
    Input("input-1", "value"),
    # Entrée: la valeur du deuxième champ de texte avec l'identifiant "input-2"
    Input("input-2", "value"),
)
def update_output(input1, input2):
    # Retourner une chaîne de caractères formatée qui affiche les valeurs des deux entrées
    return f'Input 1 is "{input1}" and Input 2 is "{input2}"'

# Démarrer l'application Dash
if __name__ == "__main__":
    app.run(debug=True)