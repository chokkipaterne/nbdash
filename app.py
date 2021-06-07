import dash
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
external_stylesheets = [dbc.themes.BOOTSTRAP, 'assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}], suppress_callback_exceptions=True
                )
server = app.server
