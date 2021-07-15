from utils import Header, parse_contents, getPositions, getPortfolioStatistics
from pages import (
    upload,
    overview,
    pricePerformance,
    portfolioManagement,
    feesMins,
    distributions
)
import base64
import datetime
from datetime import date

import io
import pathlib

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
import plotly.graph_objs as go



PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data/Input").resolve()


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([dcc.Location(id="url", refresh=False),
                       html.Div(id="page-content"),
                       # html.Div(id="hidden_div_for_redirect_callback"),

    dcc.Upload(
        id='upload-data',
        children=html.Div([]),
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    # html.Button(id='analyze-button', n_clicks=0),
    # html.Button(id='container-button-basic', n_clicks=0),
    html.Button(id='container-button-basic', style = dict(display='none')),
                       ],
    className="twelve columns")

# Upload excel files.
@app.callback(
    Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified')
              )
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# Update page layout.
@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/dash-financial-report/price-performance":
        return pricePerformance.create_layout(app)
    elif pathname == "/dash-financial-report/portfolio-management":
        return portfolioManagement.create_layout(app)
    elif pathname == "/dash-financial-report/overview":
        return overview.create_layout(app)
    elif pathname == "/dash-financial-report/fees":
        return feesMins.create_layout(app)
    elif pathname == "/dash-financial-report/distributions":
        return distributions.create_layout(app)
    elif pathname == "/dash-financial-report/full-view":
        return (
            overview.create_layout(app),
            upload.create_layout(app),
            pricePerformance.create_layout(app),
            portfolioManagement.create_layout(app),
            feesMins.create_layout(app),
            distributions.create_layout(app),
        )
    else:
        return upload.create_layout(app)

@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('analyze-button', 'n_clicks')],)
def update_output(n_clicks):
    if n_clicks is not None :
        print('Button clicked')
        path = r"C:\Users\Norbert\PycharmProjects\portfolio\data\Input\transactions.txt"
        data = pd.read_csv(path, delimiter = ",")
        getPositions(data=data)

        # Rename relevant columns.
        cols = ['Datum', 'Product', 'ISIN', 'Omschrijving', 'Unnamed: 8', 'Unnamed: 10']
        data = data[cols]
        data.columns = ['date', 'product', 'isin', 'desc', 'transaction', 'saldo']
        data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y')

        # Obtain period of portfolio.
        start_date = min(data['date'])
        end_date = pd.to_datetime(date.today(), format="%Y-%m-%d")

        # getPositions(data=data)
        getPortfolioStatistics(data=data, start_date=start_date, end_date=end_date)
        return dcc.Location(pathname="/dash-financial-report/overview", id="someid_doesnt_matter")

if __name__ == "__main__":
    app.run_server(debug=True, port=1896)
