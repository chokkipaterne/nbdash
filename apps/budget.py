import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_bootstrap_components as dbc
import utils
import dash
import plotly.express as px
from datetime import datetime

#Set two decimals for float format
pd.options.display.float_format = '{:,.2f}'.format

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
BUDGET_TYPES = ["ordinary", "extraordinary"]
GROUP_GRAPH_TYPES = ["function", "type"]
GRAPH_TYPES = ["revenue", "expense"]

#read files
dfbo = pd.read_csv(DATA_PATH.joinpath("namur-budget-ordinaire-par-fonction.csv"), delimiter=";")
dfbe = pd.read_csv(DATA_PATH.joinpath("namur-budget-extraordinaire-par-fonction.csv"), delimiter=";")
dff = pd.read_csv(DATA_PATH.joinpath("feedback-file.csv"), delimiter=";")
table_feedback = [
    utils.feedback_table(dff)
]

dfbo.columns = dfbo.columns.str.strip()
dfbe.columns = dfbe.columns.str.strip()

#get distinct years
years = sorted(dfbo["Exercice"].unique(), reverse=True)

#Define some variables
user_displays = [
    dbc.DropdownMenuItem("Simple (New to visualization)", id="pasdutt", n_clicks_timestamp='0'),
    dbc.DropdownMenuItem("Less advanced (Need more control on data and visualizations displayed)", id="unpeu", n_clicks_timestamp='0'),
    dbc.DropdownMenuItem("Advanced (Need to edit visualizations)", id="biensure", n_clicks_timestamp='0'),
]
current_display = "Simple (New to visualization)"
init_conf = "pasdutt"
init_timestamps = 0


labels_cols_ord = ['fiscal year', 'function', 'service revenue', 'transfer revenue',
       'debt revenue', 'total revenue', 'tax revenue',
       'total revenue with tax', 'staff expense',
       'operating expense', 'transfer expense', 'debt expense',
       'total expense', 'tax expense',
       'total expense with tax']
recette_ord_start = 2
recette_ord_end = 8
depense_ord_start = 8
depense_ord_end = 15

labels_cols_extra = ['fiscal year', 'function', 'transfer revenue',
       'investment revenue', 'debt revenue', 'total revenue',
       'tax revenue', 'total revenue with tax',
       'transfer expense', 'investment expense', 'debt expense',
       'total expense ', 'tax expense',
       'total expense with tax']
recette_extra_start = 2
recette_extra_end = 8
depense_extra_start = 8
depense_extra_end = 14

retrieved_date = "August 19, 2020 (annual update)"

col_ord_recette_total = dfbo.columns[5]
col_ord_depense_total = dfbo.columns[12]
col_extra_recette_total = dfbe.columns[5]
col_extra_depense_total = dfbe.columns[11]
indice_ord_recette_total = 5
indice_ord_depense_total = 12
indice_extra_recette_total = 5
indice_extra_depense_total = 11

label_total_recette_ord = "Total Ordinary Revenue"
label_total_depense_ord = "Total Ordinary Expense"
label_total_recette_extra = "Total Extraordinary Revenue"
label_total_depense_extra = "Total Extraordinary Expense"
label_prev_year = "Comparison with previous year"
label_measure = "What do you want to analyze?"
label_settings_graph = "What to show on the graph?"
label_graph = "Type of graph"
label_sort = "Order by"
list_labels_sort = ['Descending', 'Ascending', 'A-Z', 'Z-A']
col_function = 1
label_function = dfbo.columns[col_function]
label_type = "type"
label_amount = "amount"
label_year = "fiscal year"
label_percent = "%"
label_budget_types = ["ordinary", "extraordinary"]
max_elmts_pie = 7
label_new = "Open"
terms = utils.terminology()

# Customize layout of budget dashboard
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.A("Back", href='/', className="btn bglarge no-decor btn-danger mr-3"),
                #html.A("Partager", href='/', className="btn bglarge no-decor btn-primary mr-1"),
                dbc.DropdownMenu(
                    user_displays, label="Change Display Type", bs_size="sm", color="success", className="btn no-decor round mr-3 dt-button"
                ),
                html.A("Access Source Code", href='https://github.com/chokkipaterne/nbdash', target="_blank", id="sourcecode", style={"display": "none"}, className="btn bglarge no-decor btn-primary"),
            ]),
            ], xs=12, sm=12, md=12, lg=12, xl=12, className="mt-2 mb-2 round center text-center")
        ]
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody([
                            html.H5("NBDash - Namur Budget Dashboard",
                                        className='title-dash mb-2'),
                            html.P("This dashboard presents information on the ordinary and extraordinary expenses/revenues of the commune of Namur.",
                                        className='desc-dash mb-4'),
                            html.H5(["Display Type: ",
                            html.Span(id="display"),],
                                        className='sm-title mb-2'),
                        ]
                    ),
                ], className="shadow"
            ),
            html.Br(),
            dbc.Card(
                [
                    dbc.CardBody([
                            html.H5("Terminology",
                                        className='title-dash mb-2'),
                            html.Div(terms
                            ),
                        ]
                    ),
                ], className="shadow"
            ),
            html.Br(),
            dbc.Card(
                [
                    dbc.CardBody([
                        html.H5(["Data Used",
                        html.Span(["  (Source: Namur Open Data Portal)"
                        ],className="spanmd"),]
                        ,
                                    className='sm-title mb-2'),
                        html.Div(
                            [
                                html.P(
                                    [
                                        dcc.Link([
                                            "1. ",
                                            "Namur-Ordinary budget by function",
                                        ], href='https://translate.google.com/translate?sl=fr&tl=en&u=https://data.namur.be/explore/dataset/namur-budget-ordinaire-par-fonction/information/?disjunctive.fonctions', target="_blank", className="no-decor sm-font text-blue"),
                                        html.Span(
                                            " ?",
                                            id="tooltip-target",
                                            style={"cursor": "pointer"},
                                        ),
                                        html.Br(),
                                        html.Span([
                                            'Last update: '
                                            f'{retrieved_date}',
                                        ],className="spansm"),
                                        html.Br(),
                                        html.B([
                                            'Data Quality: 75%'
                                        ],className="spanmd"),
                                        html.Span(
                                            " ?",
                                            id="tooltipq-target",
                                            style={"cursor": "pointer"},
                                        ),

                                    ], className="sm-font text-black"
                                ),
                                dbc.Tooltip(
                                    "This dataset includes the different revenues and expenses allowing "
                                    "the current operation of the City of Namur excluding investments.",
                                    target="tooltip-target",
                                ),
                                dbc.Tooltip([
                                    "No missing values: 100%",
                                    html.Br(),
                                    "Data Information (title, description, modified data, update frequency): 100%",
                                    html.Br(),
                                    "Column titles: 100%",
                                    html.Br(),
                                    "Column Descriptions: 0%",
                                    html.Br(),
                                    "Average Quality: 75%"],
                                    target="tooltipq-target",
                                ),
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.P(
                                    [
                                        dcc.Link("2. Namur-Extraordinary budget by function", href='https://translate.google.com/translate?sl=fr&tl=en&u=https://data.namur.be/explore/dataset/namur-budget-extraordinaire-par-fonction/information/?disjunctive.fonctions', target="_blank", className="no-decor sm-font text-blue"),
                                        html.Span(
                                            " ?",
                                            id="tooltip-target1",
                                            style={"cursor": "pointer"},
                                        ),
                                        html.Br(),
                                        html.Span([
                                            'Last update: '
                                            f'{retrieved_date}',
                                        ],className="spansm"),
                                        html.Br(),
                                        html.B([
                                            'Data Quality: 75%'
                                        ],className="spanmd"),
                                        html.Span(
                                            " ?",
                                            id="tooltipq-target1",
                                            style={"cursor": "pointer"},
                                        ),

                                    ], className="sm-font text-black"
                                ),
                                dbc.Tooltip(
                                    "This dataset includes the various revenues and expenses of the City of Namur's investments.  "
                                    "The expenses represent the amount of the investment, while the revenues represent the type of financing carried out in order to acquire the corresponding investment.",
                                    target="tooltip-target1",
                                ),
                                dbc.Tooltip([
                                    "No missing values: 100%",
                                    html.Br(),
                                    "Data Information (title, description, modified data, update frequency): 100%",
                                    html.Br(),
                                    "Column titles: 100%",
                                    html.Br(),
                                    "Column Descriptions: 0%",
                                    html.Br(),
                                    "Average Quality: 75%"],
                                    target="tooltipq-target1",
                                ),
                            ]
                        )
                        ]
                    ),
                ], className="shadow"
            ),
            html.Br(),
            dbc.Card(
                [
                    dbc.CardBody([
                            html.H5("Give Feedback",
                                        className='sm-title mb-2'),
                            html.Div([
                                dbc.Textarea(id="comments",className="mb-1", placeholder="Leave your comments to help improve the dashboard"),
                                html.Small([
                                "Please check previous comments below before adding your comment."
                                ], className="spansm"),
                                html.Br(),
                                html.Button('Submit', id='submit-val', className="btn bglarge rounded no-decor btn-primary", n_clicks=0),
                            ], className="mb-4"),
                          html.H5("Previous comments", className='sm-title mb-2'),
                          html.Div(table_feedback, id="feedback"),
                          html.Br(),
                        ]
                    ),
                ], className="shadow"
            ),
        ], xs=12, sm=12, md=3, lg=3, xl=3, className="div-left"),
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.Br(),
                                    dcc.Dropdown(
                                        id='budget-type', value=BUDGET_TYPES[0], clearable=False,
                                        persistence=True, persistence_type='session',
                                        options=[{'label': x, 'value': x} for x in BUDGET_TYPES],
                                        placeholder="Choose the type of budget",
                                    ),
                                    html.Div("budget", style={"display": "inline"},className='title-dash mb-4'),
                                    html.Div(" during the fiscal year ", style={"display": "inline", "marginLeft": "10px"},className='title-dash mb-4'),
                                    dcc.Dropdown(
                                        id='budget-year', value=years[0], clearable=False,
                                        persistence=True, persistence_type='session',searchable=True,
                                        options=[{'label': x, 'value': x} for x in years]
                                    ),
                                ],className="center text-center"),
                            ], xs=12, sm=12, md=12, lg=12, xl=12),
                        ], align="start", id="top-title"),
                        html.Br(),html.Br(),
                        html.Div(id='summary-result', className="center text-center"),
                        html.Div([
                            html.H5("Analysis of ", style={"display": "inline"},
                                        className='sm-title mb-2'),
                            dcc.Dropdown(
                                id='graph-drop', value=GRAPH_TYPES[0], clearable=False,
                                persistence=True, persistence_type='session',searchable=True,
                                options=[{'label': x, 'value': x} for x in GRAPH_TYPES]
                            ),
                            html.H5(" by ", style={"display": "inline"},
                                        className='sm-title mb-2'),
                            dcc.Dropdown(
                                id='group-drop', value=GROUP_GRAPH_TYPES[0], clearable=False,
                                persistence=True, persistence_type='session',searchable=True,
                                options=[{'label': x, 'value': x} for x in GROUP_GRAPH_TYPES]
                            ),
                            ], id="top-graph", className="mb-2 center text-center"
                        ),
                        dbc.Row([
                        	dbc.Col([
                                html.Div(id='graph-result'),
                        	], xs=12, sm=12, md=9, lg=9, xl=9, id="left-graph" , style={'display': 'block', 'flex': '0 0 100%','maxWidth': '100%'}),
                        	dbc.Col([
                                html.Div(id="interpret-graph", style= {'display': 'block'}),
                                html.Div([
                                html.H5(f'{label_graph}',
                                            className='sm-title mb-2'),
                                html.Div([
                                    html.Button([
                                    html.Img(
                                        src="../assets/Bar150.png", className="btGraph mr-2"),
                                    'Bar chart'
                                    ], id='barre', n_clicks_timestamp=0),
                                    html.Button([
                                    html.Img(
                                        src="../assets/Line150.png", className="btGraph mr-2"),
                                    'Line chart'
                                    ], id='line', n_clicks_timestamp=0, style={'display': 'block'}),
                                    html.Button([
                                    html.Img(
                                        src="../assets/Pie150.png", className="btGraph mr-2"),
                                    'Pie chart'
                                    ], id='camembert', n_clicks_timestamp=0),
                                ], id="graph-btns"),
                                ], id="div-graph", style= {'display': 'none'}),
                                html.H5(f'{label_measure}', id="label-meas",
                                            className='sm-title mb-2', style= {'display': 'none'}),
                                html.Div(
                                [
                                    dcc.RadioItems(
                                        id='recette-ord-meas', value=col_ord_recette_total,
                                        #persistence=True, persistence_type='session',
                                        options=[{'label': x, 'value': v} for x,v in zip(labels_cols_ord[recette_ord_start:recette_ord_end],dfbo.columns[recette_ord_start:recette_ord_end])],
                                    )
                                ],
                                id='list-recette-ord-meas',
                                style= {'display': 'none'},className="max_filt_height"),
                                html.Div(
                            	[
                            		dcc.RadioItems(
                            			id='depense-ord-meas', value=col_ord_depense_total,
                            			#persistence=True, persistence_type='session',
                            			options=[{'label': x, 'value': v} for x,v in zip(labels_cols_ord[depense_ord_start:depense_ord_end],dfbo.columns[depense_ord_start:depense_ord_end])],
                            		)
                            	],
                            	id='list-depense-ord-meas',
                            	style= {'display': 'none'},className="max_filt_height"),
                                html.Div(
                            	[
                            		dcc.RadioItems(
                            			id='recette-extra-meas', value=col_extra_recette_total,
                            			#persistence=True, persistence_type='session',
                            			options=[{'label': x, 'value': v} for x,v in zip(labels_cols_extra[recette_extra_start:recette_extra_end],dfbe.columns[recette_extra_start:recette_extra_end])],
                            		)
                            	],
                            	id='list-recette-extra-meas',
                            	style= {'display': 'none'},className="max_filt_height"),
                                html.Div(
                            	[
                            		dcc.RadioItems(
                            			id='depense-extra-meas', value=col_extra_depense_total,
                            			#persistence=True, persistence_type='session',
                            			options=[{'label': x, 'value': v} for x,v in zip(labels_cols_extra[depense_extra_start:depense_extra_end],dfbe.columns[depense_extra_start:depense_extra_end])],
                            		)
                            	],
                            	id='list-depense-extra-meas',
                            	style= {'display': 'none'},className="max_filt_height"),

                                html.H5(f'{label_settings_graph}', id="label-set-graph",
                                            className='sm-title mb-2', style= {'display': 'none'}),
                                html.Div(
                                [
                                    dcc.Checklist(
                                        id="recette-ord-filt",
                                        options=[{'label': x, 'value': v} for x,v in zip(labels_cols_ord[recette_ord_start:recette_ord_end],dfbo.columns[recette_ord_start:recette_ord_end])],
                                        value=dfbo.columns[recette_ord_start:recette_ord_end]
                                    )
                                ],
                                id='list-recette-ord-filt',
                                style= {'display': 'none'},className="max_filt_height"),

                            	html.Div(
                            	[
                            		dcc.Checklist(
                            			id="depense-ord-filt",
                            			options=[{'label': x, 'value': v} for x,v in zip(labels_cols_ord[depense_ord_start:depense_ord_end],dfbo.columns[depense_ord_start:depense_ord_end])],
                            			value=dfbo.columns[depense_ord_start:depense_ord_end]
                            		)
                            	],
                            	id='list-depense-ord-filt',
                            	style= {'display': 'none'},className="max_filt_height"),

                        	html.Div(
                        	[
                        		dcc.Checklist(
                        			id="recette-extra-filt",
                        			options=[{'label': x, 'value': v} for x,v in zip(labels_cols_extra[recette_extra_start:recette_extra_end],dfbe.columns[recette_extra_start:recette_extra_end])],
                        			value=dfbe.columns[recette_extra_start:recette_extra_end]
                        		)
                        	],
                        	id='list-recette-extra-filt',
                        	style= {'display': 'none'},className="max_filt_height"),

                        	html.Div(
                        	[
                        		dcc.Checklist(
                        			id="depense-extra-filt",
                        			options=[{'label': x, 'value': v} for x,v in zip(labels_cols_extra[depense_extra_start:depense_extra_end],dfbe.columns[depense_extra_start:depense_extra_end])],
                        			value=dfbe.columns[depense_extra_start:depense_extra_end]
                        		)
                        	],
                        	id='list-depense-extra-filt',
                        	style= {'display': 'none'},className="max_filt_height"),
                            html.Div(
                            [
                                dcc.Checklist(
                                    id="function-filt",
                                    options=[{'label': x, 'value': x} for x in sorted(dfbo[label_function].unique())],
                                    #value=sorted(dfbo[label_function].unique())
                                )
                            ],
                            id='list-function-filt',
                            style= {'display': 'none'},className="max_filt_big_height"),
                            html.Div([
                            html.H5(f'{label_sort}',
                                        className='sm-title mb-2'),
                            dcc.Dropdown(
                                id='ord-drop', value=list_labels_sort[0], clearable=False,searchable=True,
                                options=[{'label': x, 'value': x} for x in list_labels_sort]
                            ),
                            ], id="div-sort", style= {'display': 'none'}),
                        	], xs=12, sm=12, md=3, lg=3, xl=3, id="right-graph", style= {'display': 'none'}),
                        	],
                        align="start"),
                        ]
                    ),
                ], className="shadow minh"
            ),
            ], xs=12, sm=12, md=9, lg=9, xl=9, className="div-right")
        ]
    )
], fluid=True)

#register user feedback
@app.callback(
    Output(component_id='feedback', component_property='children'),
    Output(component_id='comments', component_property='value'),
    [Input('submit-val', 'n_clicks')],
    [State(component_id='comments', component_property='value')]
)
def user_feedback(n_clicks, comments):
    table_feedback = None
    comments_value = ""
    if n_clicks and comments and len(comments) > 0:
        comments = comments.replace(";", ",")
        feedback = datetime.today().strftime('%Y-%m-%d') + ": "+comments+";"+label_new
        feedback_file = DATA_PATH.joinpath("feedback-file.csv")
        f= open(feedback_file,"a+")
        f.write("%s\r\n" % (feedback))
        f.close()
        dff = pd.read_csv(feedback_file, delimiter=";")
        table = utils.feedback_table(dff)
        table_feedback = [
            table
        ]
    else:
        raise dash.exceptions.PreventUpdate

    return table_feedback, comments_value

# update summary results based on filters
@app.callback(
    Output(component_id='summary-result', component_property='children'),
    Output(component_id='display', component_property='children'),
    Input(component_id='budget-type', component_property='value'),
    Input(component_id='budget-year', component_property='value'),
    Input('pasdutt', 'n_clicks_timestamp'),
    Input('unpeu', 'n_clicks_timestamp'),
    Input('biensure', 'n_clicks_timestamp')
)
def update_summary(budget_type, budget_year, pasdutt, unpeu, biensure):
    df = None
    col_exercise = None
    col_recette_total = None
    col_depense_total = None
    label_recette_total = None
    label_depense_total = None
    display_left = {'display': 'block'}
    display_right = {'display': 'none'}

    if budget_type is None or budget_year is None:
        raise dash.exceptions.PreventUpdate

    if int(pasdutt) > int(unpeu) and int(pasdutt) > int(biensure):
        init_conf = "pasdutt"
        current_display = "Simple (New to visualization)"
    elif int(unpeu) > int(pasdutt) and int(unpeu) > int(biensure):
        init_conf = "unpeu"
        current_display = "Less advanced (Need more control on data and visualizations displayed)"
    elif int(biensure) > int(pasdutt) and int(biensure) > int(unpeu):
        init_conf = "biensure"
        current_display = "Advanced (Need to edit visualizations)"
    else:
        init_conf = "pasdutt"
        current_display = "Simple (New to visualization)"


    if budget_type == BUDGET_TYPES[0]:
        df = dfbo.copy()
        col_exercise = dfbo.columns[0]
        col_recette_total = col_ord_recette_total
        col_depense_total = col_ord_depense_total
        label_recette_total = label_total_recette_ord
        label_depense_total = label_total_depense_ord
    elif budget_type == BUDGET_TYPES[1]:
        df = dfbe.copy()
        col_exercise = dfbe.columns[0]
        col_recette_total = col_extra_recette_total
        col_depense_total = col_extra_depense_total
        label_recette_total = label_total_recette_extra
        label_depense_total = label_total_depense_extra

    if df is None:
        raise dash.exceptions.PreventUpdate

    df_current_year = df.copy()
    df_prev_year = df.copy()
    query_current_year = (df_current_year[col_exercise] == int(budget_year))
    query_prev_year = (df_prev_year[col_exercise] == (int(budget_year)-1))

    df_current_year = df_current_year.loc[query_current_year]
    df_prev_year = df_prev_year.loc[query_prev_year]

    sum_rec_dep_currrent_year = df_current_year[[col_recette_total,col_depense_total]].sum()
    sum_rec_dep_prev_year = df_prev_year[[col_recette_total,col_depense_total]].sum()

    diff_rec = sum_rec_dep_currrent_year[col_recette_total] - sum_rec_dep_prev_year[col_recette_total]
    diff_dep = sum_rec_dep_currrent_year[col_depense_total] - sum_rec_dep_prev_year[col_depense_total]

    class_prev_rec = "none"
    class_prev_dep = "none"

    if diff_rec != 0 and sum_rec_dep_prev_year[col_recette_total] != 0:
        show_diff_rec = utils.show_percent(float(diff_rec)*100.0/float(sum_rec_dep_prev_year[col_recette_total]))
        if diff_rec > 0:
            class_prev_rec = "greenspan"
        if diff_rec < 0:
            class_prev_rec = "redspan"
    else:
        if sum_rec_dep_prev_year[col_recette_total] == 0:
            show_diff_rec = "~"
        else:
            show_diff_rec = utils.show_nb_with_currency(diff_rec)

    if diff_dep != 0 and sum_rec_dep_prev_year[col_depense_total] != 0:
        show_diff_dep = utils.show_percent(float(diff_dep)*100.0/float(sum_rec_dep_prev_year[col_depense_total]))
        if diff_dep > 0:
            class_prev_dep = "greenspan"
        if diff_dep < 0:
            class_prev_dep = "redspan"
    else:
        if sum_rec_dep_prev_year[col_depense_total] == 0:
            show_diff_dep = "~"
        else:
            show_diff_dep = utils.show_nb_with_currency(diff_dep)

    show_rec = utils.show_nb_with_currency(sum_rec_dep_currrent_year[col_recette_total])
    show_dep = utils.show_nb_with_currency(sum_rec_dep_currrent_year[col_depense_total])

    sum_result = dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody([
                            html.H4(
                                f'{label_recette_total}',
                                className="stat-title"),
                            html.H4(
                                f'{show_rec}',
                                className="stat-amt"),
                            html.P(
                                [
                                    f'{label_prev_year} (',
                                    html.Span(
                                        f'{show_diff_rec}',
                                        className=f'{class_prev_rec}',
                                    ),
                                    ")",
                                ]
                                ,
                                className="stat-text")
                        ]
                    ),
                ], className="round"
            )
        ], xs=12, sm=12, md=4, lg=4, xl=4),
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody([
                            html.H4(
                                f'{label_depense_total}',
                                className="stat-title"),
                            html.H4(
                                f'{show_dep}',
                                className="stat-amt"),
                            html.P(
                                [
                                    f'{label_prev_year} (',
                                    html.Span(
                                        f'{show_diff_dep}',
                                        className=f'{class_prev_dep}',
                                    ),
                                    ")",
                                ]
                                ,
                                className="stat-text")
                        ]
                    ),
                ], className="round"
            )
        ], xs=12, sm=12, md=4, lg=4, xl=4),
        ], align="start", style={"justify-content": "center"}),
    return sum_result, current_display

#show or hide filters based on display type
@app.callback(
    Output(component_id='left-graph', component_property='style'),
    Output(component_id='right-graph', component_property='style'),
    Output(component_id='div-graph', component_property='style'),
    Output(component_id='label-meas', component_property='style'),
    Output(component_id='label-set-graph', component_property='style'),
    Output(component_id='list-recette-ord-meas', component_property='style'),
    Output(component_id='list-recette-ord-filt', component_property='style'),
    Output(component_id='list-depense-ord-meas', component_property='style'),
    Output(component_id='list-depense-ord-filt', component_property='style'),
    Output(component_id='list-recette-extra-meas', component_property='style'),
    Output(component_id='list-recette-extra-filt', component_property='style'),
    Output(component_id='list-depense-extra-meas', component_property='style'),
    Output(component_id='list-depense-extra-filt', component_property='style'),
    Output(component_id='list-function-filt', component_property='style'),
    Output(component_id='div-sort', component_property='style'),
    Output(component_id='interpret-graph', component_property='style'),
    Output(component_id='sourcecode', component_property='style'),


    Input(component_id='budget-type', component_property='value'),
    Input(component_id='budget-year', component_property='value'),
    Input('pasdutt', 'n_clicks_timestamp'),
    Input('unpeu', 'n_clicks_timestamp'),
    Input('biensure', 'n_clicks_timestamp'),
    Input(component_id='graph-drop', component_property='value'),
    Input(component_id='group-drop', component_property='value'),
    Input('barre', 'n_clicks_timestamp'),
    Input('line', 'n_clicks_timestamp'),
    Input('camembert', 'n_clicks_timestamp')
)
def update_filters(budget_type, budget_year, pasdutt, unpeu, biensure, graph_drop, group_drop, barre, line, camembert):
    #display_left = {'display': 'block', 'flex': '0 0 100%','maxWidth': '100%'}
    #display_right = {'display': 'none'}
    display_left = {'display': 'block'}
    display_right = {'display': 'block'}
    display_div_graph = {'display': 'none'}
    display_label_meas = {'display': 'none'}
    display_label_set_graph = {'display': 'none'}
    display_list_recette_ord_meas = {'display': 'none'}
    display_list_recette_ord_filt = {'display': 'none'}
    display_list_depense_ord_meas = {'display': 'none'}
    display_list_depense_ord_filt = {'display': 'none'}
    display_list_recette_extra_meas = {'display': 'none'}
    display_list_recette_extra_filt = {'display': 'none'}
    display_list_depense_extra_meas = {'display': 'none'}
    display_list_depense_extra_filt = {'display': 'none'}
    display_list_function_filt = {'display': 'none'}
    display_div_sort = {'display': 'none'}
    display_interpret_graph = {'display': 'none'}
    display_sourcecode = {'display': 'none'}

    if budget_type is None or budget_year is None:
        raise dash.exceptions.PreventUpdate

    if int(pasdutt) > int(unpeu) and int(pasdutt) > int(biensure):
        init_conf = "pasdutt"
    elif int(unpeu) > int(pasdutt) and int(unpeu) > int(biensure):
        init_conf = "unpeu"
    elif int(biensure) > int(pasdutt) and int(biensure) > int(unpeu):
        init_conf = "biensure"
        display_sourcecode = {'display': 'inline-block'}
    else:
        init_conf = "pasdutt"

    if int(barre) > int(line) and int(barre) > int(camembert):
        graph_type = 'barre'
    elif int(line) > int(barre) and int(line) > int(camembert):
        graph_type = 'line'
    elif int(camembert) > int(line) and int(camembert) > int(barre):
        graph_type = 'camembert'
    else:
        graph_type = 'barre'

    if graph_type == 'line' and group_drop == GROUP_GRAPH_TYPES[1]:
        graph_type = 'barre'

    if init_conf == "pasdutt":
        display_interpret_graph = {'display': 'block'}
    if init_conf != "pasdutt":
        #display_left = {'display': 'block'}
        #display_right = {'display': 'block'}
        display_div_graph = {'display': 'block'}
        display_label_set_graph = {'display': 'block'}
        display_div_sort = {'display': 'block'}
        if graph_type == 'line':
            display_div_sort = {'display': 'none'}

        if budget_type == BUDGET_TYPES[0]:
            #budget ordinaire
            if group_drop == GROUP_GRAPH_TYPES[0]:
                #fonction
                display_list_function_filt = {'display': 'block'}
                display_label_meas = {'display': 'block'}
                if graph_drop == GRAPH_TYPES[0]:
                    #recettes
                    display_list_recette_ord_meas = {'display': 'block'}
                elif graph_drop == GRAPH_TYPES[1]:
                    #depenses
                    display_list_depense_ord_meas = {'display': 'block'}
            elif group_drop == GROUP_GRAPH_TYPES[1]:
                #type
                if graph_drop == GRAPH_TYPES[0]:
                    #recettes
                    display_list_recette_ord_filt = {'display': 'block'}
                elif graph_drop == GRAPH_TYPES[1]:
                    #depenses
                    display_list_depense_ord_filt = {'display': 'block'}
        elif budget_type == BUDGET_TYPES[1]:
            #budget extraordinaire
            if group_drop == GROUP_GRAPH_TYPES[0]:
                #fonction
                display_list_function_filt = {'display': 'block'}
                display_label_meas = {'display': 'block'}
                if graph_drop == GRAPH_TYPES[0]:
                    #recettes
                    display_list_recette_extra_meas = {'display': 'block'}
                elif graph_drop == GRAPH_TYPES[1]:
                    #depenses
                    display_list_depense_extra_meas = {'display': 'block'}
            elif group_drop == GROUP_GRAPH_TYPES[1]:
                #type
                if graph_drop == GRAPH_TYPES[0]:
                    #recettes
                    display_list_recette_extra_filt = {'display': 'block'}
                elif graph_drop == GRAPH_TYPES[1]:
                    #depenses
                    display_list_depense_extra_filt = {'display': 'block'}

    return display_left, display_right, display_div_graph, display_label_meas,display_label_set_graph,display_list_recette_ord_meas,display_list_recette_ord_filt,display_list_depense_ord_meas,display_list_depense_ord_filt,display_list_recette_extra_meas,display_list_recette_extra_filt,display_list_depense_extra_meas,display_list_depense_extra_filt,display_list_function_filt,display_div_sort,display_interpret_graph,display_sourcecode

#Update visualizations based on filters and display type
@app.callback(
    Output(component_id='graph-result', component_property='children'),
    Output(component_id='interpret-graph', component_property='children'),
    Output(component_id='line', component_property='style'),

    Input(component_id='budget-type', component_property='value'),
    Input(component_id='budget-year', component_property='value'),
    Input('pasdutt', 'n_clicks_timestamp'),
    Input('unpeu', 'n_clicks_timestamp'),
    Input('biensure', 'n_clicks_timestamp'),
    Input(component_id='graph-drop', component_property='value'),
    Input(component_id='group-drop', component_property='value'),
    Input('barre', 'n_clicks_timestamp'),
    Input('line', 'n_clicks_timestamp'),
    Input('camembert', 'n_clicks_timestamp'),
    Input(component_id='recette-ord-meas', component_property='value'),
    Input(component_id='depense-ord-meas', component_property='value'),
    Input(component_id='recette-extra-meas', component_property='value'),
    Input(component_id='depense-extra-meas', component_property='value'),
    Input(component_id='function-filt', component_property='value'),
    Input(component_id='recette-ord-filt', component_property='value'),
    Input(component_id='depense-ord-filt', component_property='value'),
    Input(component_id='recette-extra-filt', component_property='value'),
    Input(component_id='depense-extra-filt', component_property='value'),
    Input(component_id='ord-drop', component_property='value')
)
def update_graph(budget_type, budget_year, pasdutt, unpeu, biensure, graph_drop, group_drop,barre,line,camembert,
recette_ord_meas,depense_ord_meas,recette_extra_meas,depense_extra_meas,function_filt,recette_ord_filt,
depense_ord_filt,recette_extra_filt,depense_extra_filt,ord_drop):
    df = None
    graph_result = None
    interpret_graph = []
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    graph_type = 'barre'
    col_exercise = None
    col_recette_total = None
    col_depense_total = None
    label_X = None
    label_Y = None
    title_graph = None
    add_suffix = ""
    recette_start = None
    recette_end = None
    depense_start = None
    depense_end = None
    fig = None
    params_fig = {}
    id_graph = "graph"
    config_pasdutt = {
      'displayModeBar': True,
      'displaylogo': False,
      'modeBarButtonsToRemove':['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toggleSpikelines', 'resetViews',
      'hoverCompareCartesian', 'hoverClosestGl2d', 'hoverClosestCartesian', 'hoverCompareCartesian']
    }
    config_unpeu = {
      'displayModeBar': True,
      'displaylogo': False,
      'modeBarButtonsToRemove':['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toggleSpikelines', 'resetViews',
      'hoverCompareCartesian', 'hoverClosestGl2d', 'hoverClosestCartesian', 'hoverCompareCartesian']
    }
    config_biensure = {
      'showLink': True,
      'displayModeBar': True,
      'displaylogo': False,
      'plotlyServerURL': "https://chart-studio.plotly.com",
      'linkText': 'Edit chart',
      'modeBarButtonsToRemove':['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d', 'toggleSpikelines', 'resetViews',
      'hoverCompareCartesian', 'hoverClosestGl2d', 'hoverClosestCartesian', 'hoverCompareCartesian']
    }
    display_line = {'display': 'block'}
    display_sort = {'display': 'block'}

    if int(barre) > int(line) and int(barre) > int(camembert):
        graph_type = 'barre'
    elif int(line) > int(barre) and int(line) > int(camembert):
        graph_type = 'line'
    elif int(camembert) > int(line) and int(camembert) > int(barre):
        graph_type = 'camembert'
    else:
        graph_type = 'barre'

    if graph_type == 'line' and group_drop == GROUP_GRAPH_TYPES[1]:
        graph_type = 'barre'

    if group_drop == GROUP_GRAPH_TYPES[0]:
        #fonction
        display_line = {'display': 'block'}
    elif group_drop == GROUP_GRAPH_TYPES[1]:
        #type
        display_line = {'display': 'none'}

    if graph_type == 'line':
        display_sort = {'display': 'none'}


    if int(pasdutt) > int(unpeu) and int(pasdutt) > int(biensure):
        init_conf = "pasdutt"
    elif int(unpeu) > int(pasdutt) and int(unpeu) > int(biensure):
        init_conf = "unpeu"
    elif int(biensure) > int(pasdutt) and int(biensure) > int(unpeu):
        init_conf = "biensure"
        id_graph = "advgraph"
    else:
        init_conf = "pasdutt"

    if budget_type is None or budget_year is None:
        raise dash.exceptions.PreventUpdate

    if budget_type == BUDGET_TYPES[0]:
        df = dfbo.copy()
        col_exercise = dfbo.columns[0]
        col_recette_total = col_ord_recette_total
        col_depense_total = col_ord_depense_total
        if group_drop == GROUP_GRAPH_TYPES[0]:
            #fonction
            label_X = labels_cols_ord[col_function]
            if graph_drop == GRAPH_TYPES[0]:
                #recettes
                label_Y = labels_cols_ord[indice_ord_recette_total]
            elif graph_drop == GRAPH_TYPES[1]:
                #depenses
                label_Y = labels_cols_ord[indice_ord_depense_total]
        elif group_drop == GROUP_GRAPH_TYPES[1]:
            #type
            label_X = label_type
            label_Y = label_amount
        title_graph = label_budget_types[0] + " " + label_Y + " by "+ label_X + " during the fiscal year "+ str(budget_year)
        interpret_graph.append("This graph presents "+ title_graph+ ". ")
        interpret_graph.append(html.Br())

        recette_start = recette_ord_start
        recette_end = recette_ord_end
        depense_start = depense_ord_start
        depense_end = depense_ord_end
    elif budget_type == BUDGET_TYPES[1]:
        df = dfbe.copy()
        col_exercise = dfbe.columns[0]
        col_recette_total = col_extra_recette_total
        col_depense_total = col_extra_depense_total
        if group_drop == GROUP_GRAPH_TYPES[0]:
            #fonction
            label_X = labels_cols_extra[col_function]
            if graph_drop == GRAPH_TYPES[0]:
                #recettes
                label_Y = labels_cols_extra[indice_extra_recette_total]
            elif graph_drop == GRAPH_TYPES[1]:
                #depenses
                label_Y = labels_cols_extra[indice_extra_depense_total]
        elif group_drop == GROUP_GRAPH_TYPES[1]:
            #type
            label_X = label_type
            label_Y = label_amount

        title_graph = label_budget_types[1] + " " +label_Y + " by "+ label_X + " during the fiscal year "+ str(budget_year)
        interpret_graph.append("This graph presents "+ title_graph+ ". ")
        interpret_graph.append(html.Br())

        recette_start = recette_extra_start
        recette_end = recette_extra_end
        depense_start = depense_extra_start
        depense_end = depense_extra_end

    if df is None:
        raise dash.exceptions.PreventUpdate

    df_filter = df.copy()
    if init_conf == "pasdutt":
        df_group = None
        query_filter = (df_filter[col_exercise] == int(budget_year))
        list_columns = []
        if group_drop == GROUP_GRAPH_TYPES[0]:
            #fonction
            list_columns.append(df.columns[col_function])
            if graph_drop == GRAPH_TYPES[0]:
                #recettes
                list_columns.append(col_recette_total)
                df_filter = df_filter.loc[query_filter][list_columns]
            elif graph_drop == GRAPH_TYPES[1]:
                #depenses
                list_columns.append(col_depense_total)
                df_filter = df_filter.loc[query_filter][list_columns]
            if df_filter is not None:
                df_group = df_filter.groupby([df.columns[col_function]]).agg("sum")
                df_group = df_group.reset_index()
        elif group_drop == GROUP_GRAPH_TYPES[1]:
            #type
            if graph_drop == GRAPH_TYPES[0]:
                #recettes
                for i in range(recette_start,recette_end):
                    list_columns.append(df.columns[i])
                df_filter = df_filter.loc[query_filter][list_columns]
            elif graph_drop == GRAPH_TYPES[1]:
                #depenses
                for i in range(depense_start,depense_end):
                    list_columns.append(df.columns[i])
                df_filter = df_filter.loc[query_filter][list_columns]
            if df_filter is not None:
                df_group = df_filter.agg("sum").to_frame()
                df_group = df_group.reset_index()
                df_group = df_group.rename(columns = {0:'Total'})

        if df_group is not None:
            df_group.sort_values(by=[df_group.columns[1]], inplace=True, ascending=True)
            df_group = df_group.reset_index(drop=True)
            df_group[df_group.columns.tolist()] = df_group[df_group.columns.tolist()].round(2)

            nb_rows = df_group.shape[0]
            interpret_graph.append(html.B(str(df_group.at[nb_rows-1,df_group.columns[0]])))
            interpret_graph.append(" has the highest value ")
            interpret_graph.append(html.B(str(utils.show_nb_with_currency(df_group.at[nb_rows-1,df_group.columns[1]]))))
            interpret_graph.append(html.Br())
            if nb_rows-1 != 0:
                interpret_graph.append(html.B(str(df_group.at[0,df_group.columns[0]])))
                interpret_graph.append(" has the lowest value ")
                interpret_graph.append(html.B(str(utils.show_nb_with_currency(df_group.at[0,df_group.columns[1]]))))

            params_fig["y"] = df_group.columns[0]
            params_fig["x"] = df_group.columns[1]
            params_fig["orientation"] = 'h'
            params_fig["labels"] = {}
            params_fig["labels"][df_group.columns[0]] = label_X
            params_fig["labels"][df_group.columns[1]] = label_Y
            params_fig["data_frame"] = df_group
            params_fig["template"] = 'plotly_white'
            #params_fig["title"] = title_graph
            if group_drop == GROUP_GRAPH_TYPES[0]:
                #fonction
                params_fig["height"] = 700
            elif group_drop == GROUP_GRAPH_TYPES[1]:
                #fonction
                params_fig["height"] = 300
            fig = px.bar(**params_fig)
            fig.update_layout(showlegend=False,
             xaxis=dict(
                side="top"
            ), margin=dict(
                    l=0,
                    r=10,
                    b=5,
                    t=30,
                    pad=4
                )
            )
            #print(fig)
        if df_group is not None and df_group.shape[0] != 0:
            graph_result = [
                html.P(title_graph, style={"textAlign": "center"}),
                dcc.Graph(id=id_graph, figure=fig, config=config_pasdutt)
            ]
        else:
            graph_result = [
                html.P(title_graph, style={"textAlign": "center"}),
                html.P("No data to plot", style={"textAlign": "center", "color": "red"}),
            ]
    else:
        meas_y = None
        if graph_type == 'barre' or graph_type == 'camembert':
            if group_drop == GROUP_GRAPH_TYPES[0]:
                #fonction
                if graph_drop == GRAPH_TYPES[0]:
                    #recettes
                    if budget_type == BUDGET_TYPES[0]:
                        meas_y = recette_ord_meas
                        index = df.columns.tolist().index(recette_ord_meas)
                        label_Y = labels_cols_ord[index]
                        add_suffix = " " + label_budget_types[0]
                    elif budget_type == BUDGET_TYPES[1]:
                        meas_y = recette_extra_meas
                        index = df.columns.tolist().index(recette_extra_meas)
                        label_Y = labels_cols_extra[index]
                        add_suffix = " " + label_budget_types[1]
                elif graph_drop == GRAPH_TYPES[1]:
                    #depenses
                    if budget_type == BUDGET_TYPES[0]:
                        meas_y = depense_ord_meas
                        index = df.columns.tolist().index(depense_ord_meas)
                        label_Y = labels_cols_ord[index]
                        add_suffix = " " + label_budget_types[0]
                    elif budget_type == BUDGET_TYPES[1]:
                        meas_y = depense_extra_meas
                        index = df.columns.tolist().index(depense_extra_meas)
                        label_Y = labels_cols_extra[index]
                        add_suffix = " " + label_budget_types[1]

                title_graph = add_suffix + " "+ label_Y + " by "+ label_X + " during the fiscal year "+ str(budget_year)

            df_group = None
            query_filter = (df_filter[col_exercise] == int(budget_year))
            list_columns = []
            if group_drop == GROUP_GRAPH_TYPES[0]:
                #fonction
                if function_filt and len(function_filt) != 0:
                    query_filter = query_filter & (df_filter[df.columns[col_function]].isin(function_filt))
                list_columns.append(df.columns[col_function])
                if graph_drop == GRAPH_TYPES[0]:
                    #recettes
                    list_columns.append(meas_y)
                    df_filter = df_filter.loc[query_filter][list_columns]
                elif graph_drop == GRAPH_TYPES[1]:
                    #depenses
                    list_columns.append(meas_y)
                    df_filter = df_filter.loc[query_filter][list_columns]
                if df_filter is not None:
                    df_group = df_filter.groupby([df.columns[col_function]]).agg("sum")
                    df_group = df_group.reset_index()
            elif group_drop == GROUP_GRAPH_TYPES[1]:
                #type
                if graph_drop == GRAPH_TYPES[0]:
                    #recettes
                    if budget_type == BUDGET_TYPES[0] and len(recette_ord_filt)>0:
                        #ordinaire
                        for i in recette_ord_filt:
                            list_columns.append(i)
                    elif budget_type == BUDGET_TYPES[1] and len(recette_extra_filt)>0:
                        #extra
                        for i in recette_extra_filt:
                            list_columns.append(i)
                    else:
                        for i in range(recette_start,recette_end):
                            list_columns.append(df.columns[i])
                    df_filter = df_filter.loc[query_filter][list_columns]
                elif graph_drop == GRAPH_TYPES[1]:
                    #depenses
                    if budget_type == BUDGET_TYPES[0] and len(depense_ord_filt)>0:
                        #ordinaire
                        for i in depense_ord_filt:
                            list_columns.append(i)
                    elif budget_type == BUDGET_TYPES[1] and len(depense_extra_filt)>0:
                        #extra
                        for i in depense_extra_filt:
                            list_columns.append(i)
                    else:
                        for i in range(depense_start,depense_end):
                            list_columns.append(df.columns[i])
                    df_filter = df_filter.loc[query_filter][list_columns]
                if df_filter is not None:
                    df_group = df_filter.agg("sum").to_frame()
                    df_group = df_group.reset_index()
                    df_group = df_group.rename(columns = {0:'Total'})

            if df_group is not None:
                df_group[df_group.columns.tolist()] = df_group[df_group.columns.tolist()].round(2)
                if ord_drop:
                    if ord_drop == list_labels_sort[0]:
                        #decrease
                        df_group.sort_values(by=[df_group.columns[1]], inplace=True, ascending=True)
                    elif ord_drop == list_labels_sort[1]:
                        #increase
                        df_group.sort_values(by=[df_group.columns[1]], inplace=True, ascending=False)
                    elif ord_drop == list_labels_sort[2]:
                        #a-z
                        df_group.sort_values(by=[df_group.columns[0]], inplace=True, ascending=False)
                    elif ord_drop == list_labels_sort[3]:
                        #z-a
                        df_group.sort_values(by=[df_group.columns[0]], inplace=True, ascending=True)
                df_group = df_group.reset_index(drop=True)

                #nb_rows = df_group.shape[0]
                #interpret_graph.append(html.B(str(df_group.at[nb_rows-1,df_group.columns[0]])))
                #interpret_graph.append(" has the highest value ")
                #interpret_graph.append(html.B(str(utils.show_nb_with_currency(df_group.at[nb_rows-1,df_group.columns[1]]))))
                #interpret_graph.append(html.Br())
                #if nb_rows-1 != 0:
                #    interpret_graph.append(html.B(str(df_group.at[0,df_group.columns[0]])))
                #    interpret_graph.append(" has the lowest value ")
                #    interpret_graph.append(html.B(str(utils.show_nb_with_currency(df_group.at[0,df_group.columns[1]]))))


                params_fig["labels"] = {}
                params_fig["labels"][df_group.columns[0]] = label_X
                params_fig["labels"][df_group.columns[1]] = label_Y
                params_fig["template"] = 'plotly_white'
                #params_fig["title"] = title_graph

                if graph_type == 'barre':
                    table = utils.create_table(df_group,label_X,label_Y)
                    df_group = df_group.loc[(df_group[df_group.columns[1]] != 0)]
                    params_fig["y"] = df_group.columns[0]
                    params_fig["x"] = df_group.columns[1]
                    params_fig["data_frame"] = df_group
                    params_fig["orientation"] = 'h'
                    if group_drop == GROUP_GRAPH_TYPES[0]:
                        #fonction
                        params_fig["height"] = 500
                    elif group_drop == GROUP_GRAPH_TYPES[1]:
                        #type
                        params_fig["height"] = 500
                    fig = px.bar(**params_fig)

                elif graph_type == 'camembert':
                    total_col = df_group[df_group.columns[1]].sum()
                    if total_col == 0:
                        table = utils.create_table(df_group,label_X,label_Y)
                    else:
                        df_group[label_percent] = (df_group[df_group.columns[1]] / total_col) * 100
                        df_group[label_percent] = df_group[label_percent].round(decimals=2)
                        table = utils.create_table(df_group,label_X,label_Y, None, label_percent)

                    df_group = df_group.loc[(df_group[df_group.columns[1]] != 0)]
                    params_fig["names"] = df_group.columns[0]
                    params_fig["values"] = df_group.columns[1]
                    params_fig["data_frame"] = df_group
                    params_fig["color_discrete_sequence"] = px.colors.sequential.RdBu
                    params_fig["height"] = 500
                    fig = px.pie(**params_fig)
                    if df_group is not None and df_group.shape[0] <= max_elmts_pie:
                        fig.update_traces(textposition='inside', textinfo='label+percent')
                    else:
                        fig.update_traces(textinfo='none')

                fig.update_layout(showlegend=True,
                 xaxis=dict(
                    side="top"
                ), margin=dict(
                        l=0,
                        r=10,
                        b=20,
                        t=30,
                        pad=4
                    )
                )
                #print(fig)
            config = config_pasdutt
            if init_conf == "unpeu":
                config = config_unpeu
            elif init_conf == "biensure":
                config = config_biensure
            if df_group is not None and df_group.shape[0] != 0:
                graph_result = [
                    html.P(title_graph, style={"textAlign": "center"}),
                    dcc.Graph(id=id_graph, figure=fig, config=config),
                    html.Br(),
                    html.P("Data displayed in table format", style={"textAlign": "center"}),
                    table
                ]
            else:
                graph_result = [
                    html.P(title_graph, style={"textAlign": "center"}),
                    html.P("No data to plot", style={"textAlign": "center", "color": "red"}),
                    html.Br(),
                    html.P("Data displayed in table format", style={"textAlign": "center"}),
                    table
                ]
        elif graph_type == 'line':
            if group_drop == GROUP_GRAPH_TYPES[0]:
                #fonction
                if graph_drop == GRAPH_TYPES[0]:
                    #recettes
                    if budget_type == BUDGET_TYPES[0]:
                        meas_y = recette_ord_meas
                        index = df.columns.tolist().index(recette_ord_meas)
                        label_Y = labels_cols_ord[index]
                        add_suffix = " " + label_budget_types[0]
                    elif budget_type == BUDGET_TYPES[1]:
                        meas_y = recette_extra_meas
                        index = df.columns.tolist().index(recette_extra_meas)
                        label_Y = labels_cols_extra[index]
                        add_suffix = " " + label_budget_types[1]
                elif graph_drop == GRAPH_TYPES[1]:
                    #depenses
                    if budget_type == BUDGET_TYPES[0]:
                        meas_y = depense_ord_meas
                        index = df.columns.tolist().index(depense_ord_meas)
                        label_Y = labels_cols_ord[index]
                        add_suffix = " " + label_budget_types[0]
                    elif budget_type == BUDGET_TYPES[1]:
                        meas_y = depense_extra_meas
                        index = df.columns.tolist().index(depense_extra_meas)
                        label_Y = labels_cols_extra[index]
                        add_suffix = " " + label_budget_types[1]
                title_graph = add_suffix + " " + label_Y  + " by "+ label_X + " over time"

            df_group = None
            query_filter = None
            list_columns = []
            if group_drop == GROUP_GRAPH_TYPES[0]:
                #fonction
                if function_filt and len(function_filt) != 0:
                    query_filter = (df_filter[df.columns[col_function]].isin(function_filt))
                list_columns.append(df.columns[0])
                list_columns.append(df.columns[col_function])
                if graph_drop == GRAPH_TYPES[0]:
                    #recettes
                    list_columns.append(meas_y)
                    if query_filter is not None:
                        df_filter = df_filter.loc[query_filter][list_columns]
                    else:
                        df_filter = df_filter[list_columns]
                elif graph_drop == GRAPH_TYPES[1]:
                    #depenses
                    list_columns.append(meas_y)
                    if query_filter is not None:
                        df_filter = df_filter.loc[query_filter][list_columns]
                    else:
                        df_filter = df_filter[list_columns]
                if df_filter is not None:
                    df_group = df_filter.groupby([df.columns[0], df.columns[col_function]]).agg("sum")
                    df_group = df_group.reset_index()

            if df_group is not None:
                df_group[df_group.columns.tolist()] = df_group[df_group.columns.tolist()].round(2)
                df_group.sort_values(by=[df_group.columns[1], df_group.columns[0]], inplace=True, ascending=True)

                df_group = df_group.reset_index(drop=True)


                params_fig["labels"] = {}
                params_fig["labels"][df_group.columns[0]] = label_year
                params_fig["labels"][df_group.columns[1]] = label_X
                params_fig["labels"][df_group.columns[2]] = label_Y
                params_fig["template"] = 'plotly_white'
                #params_fig["title"] = title_graph


                table = utils.create_table(df_group,label_X,label_Y, label_year)
                params_fig["y"] = df_group.columns[2]
                params_fig["x"] = df_group.columns[0]
                params_fig["color"] = df_group.columns[1]
                params_fig["data_frame"] = df_group
                params_fig["height"] = 500

                fig = px.line(**params_fig)

                fig.update_layout(showlegend=True,
                 xaxis=dict(
                    side="top"
                ), margin=dict(
                        l=0,
                        r=10,
                        b=20,
                        t=30,
                        pad=4
                    )
                )
                #print(fig)
            config = config_pasdutt
            if init_conf == "unpeu":
                config = config_unpeu
            elif init_conf == "biensure":
                config = config_biensure
            if df_group is not None and df_group.shape[0] != 0:
                graph_result = [
                    html.P(title_graph, style={"textAlign": "center"}),
                    dcc.Graph(id=id_graph, figure=fig, config=config),
                    html.Br(),
                    html.P("Data displayed in table format", style={"textAlign": "center"}),
                    table
                ]
            else:
                graph_result = [
                    html.P(title_graph, style={"textAlign": "center"}),
                    html.P("No data to plot", style={"textAlign": "center", "color": "red"}),
                    html.Br(),
                    html.P("Data displayed in table format", style={"textAlign": "center"}),
                    table
                ]

    return graph_result, interpret_graph, display_line
