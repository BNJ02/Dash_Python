# Import necessary libraries
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# Initialize the Dash application
app = Dash(__name__)

# Define the layout of the Dash application
app.layout = html.Div([
    # Add a title to the application
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    # Add a dropdown menu for selecting a country
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    # Add a graph component for displaying the population data
    dcc.Graph(id='graph-content')
])

# Define the callback function for updating the graph component
@callback(
    # Specify the output component and property to update
    Output('graph-content', 'figure'),
    # Specify the input component and property to use as the trigger
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    # Filter the dataframe to only include the selected country
    dff = df[df.country==value]
    # Create a line graph of the population data for the selected country
    fig = px.line(dff, x='year', y='pop')
    # Return the figure to update the graph component
    return fig

# Run the Dash application
if __name__ == '__main__':
    app.run(debug=True)
    # With custom host and port
    # app.run_server(debug=True, host='192.168.1.100', port=8080)