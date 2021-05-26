import math
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd


millnames = ['',' Thousand',' Million',' Billion',' Trillion']
currency = "€"

def round_nb(n):
    return round(n)

def show_nb(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def show_nb_with_currency(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])+" "+currency

def show_percent(n):
    if n > 0:
        return "+"+str(round(n))+"%"
    return str(round(n))+"%"

def create_table(df, label_X, label_Y, label_year=None, label_percent=None):
    if label_year is None and label_percent is None:
        df.columns = [label_X,label_Y]
    elif label_percent is not None:
        df.columns = [label_X, label_Y, label_percent]
    else:
        df.columns = [label_year, label_X,label_Y]

    table = html.Div([
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
            ],
            style_cell={'textAlign': 'left'},
            data=df.to_dict('records'),
            #editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            #column_selectable="single",
            #row_selectable="multi",
            #row_deletable=True,
            #selected_columns=[],
            #selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 10,
        ),
        html.Div(id='datatable-interactivity-container')
    ])
    return table

def feedback_table(df):
    table = html.Div([
        dash_table.DataTable(
            id='datatable-feedback',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
            ],
            style_cell={'minWidth': '80px', 'textAlign': 'left', 'padding': '5px', 'whiteSpace': 'normal',
        'height': 'auto'},
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            data=df.to_dict('records'),
            #editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            #column_selectable="single",
            #row_selectable="multi",
            #row_deletable=True,
            #selected_columns=[],
            #selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 5,
        ),
        html.Div(id='datatable-feedback-container')
    ])
    return table

def terminology():
    terms = [
        html.Span(
            "ordinary buget",
            id="term1",
            style={"cursor": "pointer"},
            className="tag"
        ),
        dbc.Tooltip(
            "revenues and expenses that occur at least once per fiscal year and provide for regular revenues and operations.",
            target="term1",
        ),
        html.Span(
            "service revenue",
            id="term3",
            style={"cursor": "pointer"},
            className="tag"
        ),
        dbc.Tooltip(
            "revenues for which the municipality provides a work, supply or service in return.",
            target="term3",
        ),
        html.Span(
            "transfer revenue",
            id="term4",
            style={"cursor": "pointer"},
            className="tag"
        ),
        dbc.Tooltip(
            "revenues for which the municipalities do not contribute directly.",
            target="term4",
        ),
        html.Span(
            "debt revenue",
            id="term5",
            style={"cursor": "pointer"},
            className="tag"
        ),
        dbc.Tooltip(
            "revenues from the Commune's receivables and assets.",
            target="term5",
        ),
        html.Span(
            "staff expense",
            id="term6",
            style={"cursor": "pointer"},
            className="tag"
        ),
        dbc.Tooltip(
            "salaries of the municipal staff (statutory and contractual) as well as the agents.",
            target="term6",
        ),
        html.Span(
            "operating expense",
            id="term7",
            style={"cursor": "pointer"},
            className="tag"
        ),
        dbc.Tooltip(
            "expenses essential to the proper functioning of the Commune, with the exception of personnel expenses.",
            target="term7",
        ),
        html.Span(
            "transfer expense",
            id="term8",
            style={"cursor": "pointer"},
            className="tag"
        ),
        dbc.Tooltip(
            "the legally obligatory financial interventions (e.g., hospital and public utilities deficits, police zones) and optional subsidies to various sports, cultural and philanthropic associations.",
            target="term8",
        ),
        html.Span(
            "debt expense",
            id="term9",
            style={"cursor": "pointer"},
            className="tag"
        ),
        dbc.Tooltip(
            "the repayment of the debt (capital and interest), whether it is borne by the municipality, a third party or the higher authority.",
            target="term9",
        ),
        html.Br(),
        html.Hr(),
        html.Span(
            "extraordinary buget",
            id="term2",
            style={"cursor": "pointer"},
            className="tag"
        ),
        dbc.Tooltip(
            "exceptional revenues and expenses relating to investments: major repairs to buildings or roads, purchases of buildings, etc.",
            target="term2",
        ),
        html.Span(
            "investment revenue",
            id="term10",
            style={"cursor": "pointer"},
            className="tag"
        ),
        dbc.Tooltip(
            "revenues from the municipality's own funds, e.g., from the sale of property, from planning charges",
            target="term10",
        ),
        html.P(
            [
            dcc.Link([
                "More details",
            ], href='http://www.ixelles.be/site/270-Budget-communal', target="_blank", className="spansm text-right no-decor sm-font text-blue"),
            ], className="text-right"),
    ]
    return terms
