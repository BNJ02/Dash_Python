from dash import Dash, dcc, html

# Initialisation de l'application Dash
app = Dash(__name__)

# Définition du texte avec un contenu long
text_content = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer euis
mod odio at eros feugiat, id condimentum massa tempor. Aenean malesuada 
eros non consequat euismod. Vivamus posuere sollicitudin enim, ac ultrices 
nunc bibendum vel. Pellentesque habitant morbi tristique senectus et 
netus et malesuada fames ac turpis egestas. Donec nec commodo ante. 
Vivamus lacinia ultricies nulla, sit amet interdum neque sagittis vel. 
Nam et diam in massa scelerisque vulputate. Nulla facilisi. Proin sit
amet justo luctus, lacinia justo a, sodales lectus. Aliquam aliquam 
dolor nec mi euismod dictum. Vivamus vel fermentum lorem. Fusce fringilla, 
risus eu suscipit mattis, odio mauris vulputate est, eu pharetra risus 
libero ac magna. Maecenas venenatis quam nulla, at congue velit auctor nec. 
Phasellus vel lectus a dolor pharetra malesuada. In non justo eget odio aliquet consequat.
"""

# Définition du style CSS pour le conteneur du texte
text_style = {
    "maxHeight": "50px",   # Taille maximale du conteneur
    "overflowY": "scroll",  # Ajout d'une barre de défilement verticale si le contenu dépasse la taille maximale
}

# Définition de la mise en page de l'application
app.layout = html.Div(
    children=[
        html.H1("Texte avec barre de défilement"),
        html.Div(
            children=html.Div(text_content, style=text_style),  # Ajout du texte avec le style CSS défini
            style={"border": "1px solid black", "padding": "10px"}  # Ajout de bordures et de marges pour le conteneur du texte
        ),
    ]
)

# Point d'entrée principal de l'application
if __name__ == "__main__":
    app.run_server(debug=True)
