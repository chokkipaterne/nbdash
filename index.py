import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import budget


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div([
        html.H5("© 2021 Copyright UNamur/Precise/NADI", className='bottom')
    ]),
])

index_page = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5(
            [
                "NBDash (Namur Budget Dashboard)"
            ],
            className='msgtop mb-4'),
            html.H5(
            [
                "Understanding the expenses and revenues by function in the municipality of Namur",
            ],
            className='msgtop bold mb-4'),
            html.Br(),
            html.Br(),
            html.Div([
                dcc.Link("Get started", href='/apps/budget', className="btn bglarge no-decor btn-success"),
            ], className="mb-4"),
            html.Br(),
            html.Br(),
            html.Div([
                html.Img(
                    src="assets/unamur.png", className="btImg1 mr-1"),
                html.Img(
                    src="assets/precise.png", className="btImg2"),
            ], className="mb-6"),

            ], xs=12, sm=12, md=5, lg=5, xl=5, className="text-left mb-4"),
        dbc.Col([
                ""
            ], xs=12, sm=12, md=7, lg=7, xl=7, className="bgGray")
        ]
    )
], fluid=True)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/budget':
        return budget.layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=False)
