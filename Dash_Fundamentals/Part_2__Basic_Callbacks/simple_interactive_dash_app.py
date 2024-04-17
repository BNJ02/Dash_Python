# Importer les bibliothèques nécessaires
from dash import Dash, dcc, html, Input, Output, callback

# Créer l'application Dash
app = Dash(__name__)

# Définir le layout de l'application
app.layout = html.Div([
    # Ajouter un titre de niveau 6
    html.H6("Change the value in the text box to see callbacks in action!"),
    # Ajouter une div contenant le texte "Input: " et une boîte de saisie de texte
    html.Div([
        "Input: ",
        # Créer une boîte de saisie de texte avec un identifiant 'my-input' et une valeur initiale 'initial value'
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    # Ajouter une balise de ligne vide
    html.Br(),
    # Ajouter une div avec un identifiant 'my-output' qui contiendra la sortie de texte
    html.Div(id='my-output'),

])

# Définir la fonction de rappel qui met à jour la sortie de texte en fonction de la valeur saisie dans la boîte de saisie
@callback(
    # Définir la sortie de la fonction de rappel sur la div avec l'identifiant 'my-output'
    Output(component_id='my-output', component_property='children'),
    # Définir l'entrée de la fonction de rappel sur la valeur de la boîte de saisie avec l'identifiant 'my-input'
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    # Retourner la chaîne de caractères 'Output: ' suivie de la valeur saisie dans la boîte de saisie
    return f'Output: {input_value}'

# Démarrer l'application Dash
if __name__ == '__main__':
    app.run(debug=True)