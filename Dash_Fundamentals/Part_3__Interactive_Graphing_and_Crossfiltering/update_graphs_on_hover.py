# Importation des modules Dash et autres modules nécessaires
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

# Définition des feuilles de style externes à utiliser pour le tableau de bord
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialisation de l'application Dash
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Chargement des données à partir d'un fichier CSV en ligne
df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

# Définition de la mise en page du tableau de bord
app.layout = html.Div([
    # Sélecteurs pour les colonnes x et y ainsi que le type d'échelle pour chaque axe
    html.Div([
        html.Div([
            # Sélecteur de colonne x
            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in df['Indicator Name'].unique()],
                value='Fertility rate, total (births per woman)',
                id='crossfilter-xaxis-column',
            ),
            # Sélecteur de type d'échelle pour l'axe x
            dcc.RadioItems(
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                id='crossfilter-xaxis-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            # Sélecteur de colonne y
            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in df['Indicator Name'].unique()],
                value='Life expectancy at birth, total (years)',
                id='crossfilter-yaxis-column'
            ),
            # Sélecteur de type d'échelle pour l'axe y
            dcc.RadioItems(
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                id='crossfilter-yaxis-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={'padding': '10px 5px'}),
    # Graphique principal
    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    # Graphiques de séries temporelles
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    # Curseur pour sélectionner l'année
    html.Div(dcc.Slider(
        min=df['Year'].min(),
        max=df['Year'].max(),
        step=None,
        id='crossfilter-year--slider',
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])

# Fonction de callback pour mettre à jour le graphique principal en fonction des sélections
@callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'),
    Input('crossfilter-yaxis-type', 'value'),
    Input('crossfilter-year--slider', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    # Filtrage des données en fonction de l'année sélectionnée
    dff = df[df['Year'] == year_value]

    # Création du graphique à partir de Plotly Express
    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                     y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                     hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name']
                     )

    # Mise à jour des traces avec les données personnalisées
    fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    # Mise à jour des axes x et y
    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    # Mise à jour du layout du graphique
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig

# Fonction pour créer les graphiques de séries temporelles
def create_time_series(dff, axis_type, title):
    fig = px.scatter(dff, x='Year', y='Value')
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')
    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return fig

# Callback pour mettre à jour la série temporelle sur l'axe x en fonction de la sélection
@callback(
    Output('x-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-xaxis-column', 'value'),
    Input('crossfilter-xaxis-type', 'value'))
def update_x_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)

# Callback pour mettre à jour la série temporelle sur l'axe y en fonction de la sélection
@callback(
    Output('y-time-series', 'figure'),
    Input('crossfilter-indicator-scatter', 'hoverData'),
    Input('crossfilter-yaxis-column', 'value'),
    Input('crossfilter-yaxis-type', 'value'))
def update_y_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

# Démarrage de l'application en mode débogage si ce script est exécuté en tant que programme principal
if __name__ == '__main__':
    app.run(debug=True)
