import math
import dash_table
import dash_core_components as dcc
import dash_html_components as html
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

def create_table(df, label_X, label_Y, label_year=None):
    if label_year is None:
        df.columns = [label_X,label_Y]
    else:
        df.columns = [label_year, label_X,label_Y]

    table = html.Div([
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
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
            page_size= 10,
        ),
        html.Div(id='datatable-interactivity-container')
    ])
    return table
