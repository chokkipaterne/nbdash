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
                "Améliorer l'engagement des citoyens grâce aux tableaux de bord"
            ],
            className='msgtop mb-4'),
            html.H5(
            [
                "Utilisation des données du portail",
                html.Span(
                    " Open Data Namur ",
                    className='bold',
                ),
                "pour créer des",
                html.Span(
                    " tableaux de bord ",
                    className='bold',
                ),
                "qui peuvent aider les",
                html.Span(
                    " citoyens ",
                    className='bold',
                ),
                "à comprendre leur",

                html.Span(
                    " utilité ",
                    className='bold',
                ),
                "et donc",
                html.Span(
                    " améliorer l'engagement des citoyens. ",
                    className='bold',
                ),
            ],
            className='msgtop mb-4'),
            html.Br(),
            html.Br(),
            html.H6("Vos commentaires sont les bienvenus :).",
                        className='subtop mb-2'),
            html.Div([
                html.A("Nous contacter", href='mailto:abiola-paterne.chokki@unamur.be', className="btn bglarge no-decor btn-success"),
            ], className="mb-4"),
            html.Br(),
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
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        [
                            dbc.CardImg(
                                src="assets/dash1.PNG",
                                bottom=True),
                            dbc.CardBody([
                                    html.H4(
                                        dcc.Link("NBDash (Namur Budget Dashboard)", href='/apps/budget', className="card-link"),
                                        className="card-title"),
                                    html.P(
                                        "Ce tableau de bord présente les informations relatives au budget ordinaire et extra-ordinaire de la commune de Namur.",
                                        className="card-text")
                                ]
                            ),
                        ], className="shadow mb-4"
                    ),
                    dbc.Card(
                        [
                            dbc.CardImg(
                                src="assets/dash2.PNG",
                                bottom=True),
                            dbc.CardBody([
                                    html.H4(
                                        html.A("STI (Système Transport Intelligent)", href='https://sti.namur.be/map', target="_blank", className="card-link"),
                                        className="card-title"),
                                    html.P(
                                        ["Ce tableau de bord présente les informations sur les parkings et le stationnements des vélos dans la commune de Namur.",
                                        html.Br(),
                                        html.B("Author: Ville de Namur", className="author")],
                                        className="card-text")
                                ]
                            ),
                        ], className="shadow mb-4"
                    )
                ], xs=12, sm=12, md=6, lg=6, xl=6),
                dbc.Col([
                    dbc.Card(
                        [
                            dbc.CardImg(
                                src="assets/dash3.PNG",
                                bottom=True),
                            dbc.CardBody([
                                    html.H4(
                                        html.A("COVID 19 Hospitalisations en Belgique", href='https://data.namur.be/explore/dataset/covid19be_hosp/custom/?disjunctive.province&disjunctive.region', target="_blank", className="card-link"),
                                        className="card-title"),
                                    html.P(
                                        ["Ce tableau de bord présente les informations relatives aux hospitalisations covid19 en Belgique.",
                                        html.Br(),
                                        html.B("Author: Ville de Namur", className="author")
                                        ],
                                        className="card-text")
                                ]
                            ),
                        ], className="shadow mb-4"
                    )
                ], xs=12, sm=12, md=6, lg=6, xl=6),
                ], align="start")
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
