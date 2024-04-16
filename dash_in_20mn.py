#Initialize a Dash app and create a layout with a single HTML element that displays the text "Hello World".

# Import the Dash library and the html module
from dash import Dash, html

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the Dash app
app.layout = html.Div([
    html.Div(children='Hello World')
])

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
