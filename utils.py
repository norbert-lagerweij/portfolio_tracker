import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import numpy as np
import base64
import datetime
import csv
import os
from datetime import date
import io
import pathlib
import yfinance as yf

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

# mapping = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))


mapping = pd.read_csv(r"C:\Users\Norbert\PycharmProjects\portfolio\data\tickers.txt")


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])

def Header_landing_page(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])

def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("Norb_DS_logo.png"),
                        className="logo",
                    ),
                    html.A(
                        html.Button("Contact us", id="learn-more-button"),
                        href="https://www.linkedin.com/in/nflagerweij/",
                        className="logo",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Portfolio overview")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/dash-financial-report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Upload",
                href="/dash-financial-report/upload",
                className="tab first",
            ),
            dcc.Link(
                "Overview",
                href="/dash-financial-report/overview",
                className="tab",
            ),
            dcc.Link(
                "Price Performance",
                href="/dash-financial-report/price-performance",
                className="tab",
            ),
            dcc.Link(
                "Portfolio & Management",
                href="/dash-financial-report/portfolio-management",
                className="tab",
            ),
            dcc.Link(
                "Fees & Minimums", href="/dash-financial-report/fees", className="tab"
            ),
            dcc.Link(
                "Distributions",
                href="/dash-financial-report/distributions",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns]) ] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))

            data = contents.encode("utf8").split(b";base64,")[1]
            # with open(os.path.join(r'Files/Output/input/', filename), "wb") as fp:

            path = r"C:\Users\Norbert\PycharmProjects\portfolio\data\Input\transactions.txt"
            assert os.path.isfile(path)

            try:
                with open(path, 'wb') as fp:
                    fp.write(base64.decodebytes(data))
            except Exception as e:
                print(e)

        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.Div([
            html.Div([
                html.H6("Filename: "+ str(filename), className="subtitle padded")
            ],
                className="nine columns"),

            html.Div([
                html.Button("Analyze now", id='analyze-button', disabled=False)
            ],
                className="three columns",
            )
        ],
            className="row",
            style={'marginTop': 10}
        ),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_table={'overflowY': 'scroll',
                         'maxHeight': '400'},
        ),
    ],
        className="twelve columns")

def getPositions(data):
    ''' Obtains historical and current positions of all shares

    Args:
        data = Pandas dataframe containing all transactions incl. date and ISIN.
    Returns:
        Positions over time of all current and previous shares.
    '''
    # Omit copy warning
    pd.options.mode.chained_assignment = None

    # Rename relevant columns.
    cols = ['Datum', 'Product', 'ISIN', 'Omschrijving', 'Unnamed: 8', 'Unnamed: 10']
    data = data[cols]
    data.columns = ['date', 'product', 'isin', 'desc', 'transaction', 'saldo']
    data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y')

    # Obtain period of portfolio.
    start_date = min(data['date'])
    end_date = pd.to_datetime(date.today(), format="%Y-%m-%d")


    # Create buy/sell variables
    data['buy'] = 0
    data.loc[data['desc'].str.startswith('Koop'), 'buy'] = (data['desc'].str.extract(r'(\d+)')
        .loc[data['desc'].str.startswith('Koop')]).values.astype(int)

    data['sell'] = 0
    data.loc[data['desc'].str.startswith('Verkoop'), 'sell'] = (data['desc'].str.extract(r'(\d+)')
        .loc[data['desc'].str.startswith('Verkoop')]).values.astype(int)

    tickers = data.loc[(data['buy'] > 0) | (data['sell'] > 0), 'isin'].dropna().astype(str).unique()

    positions = pd.DataFrame({'date': pd.date_range(start=start_date, end=end_date, freq='D')[::-1]})
    for tick in tickers:
        trade = data.loc[(data['isin'] == tick) &
                         ((data['buy'] > 0) | (data['sell'] > 0))]

        trade['delta'] = trade.apply(lambda row: row['buy'] - row['sell'], axis=1)

        trade_daily = trade[['date', 'delta']].groupby(['date']).agg('sum')
        pos_daily = pd.merge(positions, trade_daily, how='left', on='date').fillna(0)

        # Append position to portfolio.
        positions[tick] = np.flipud(np.flipud(pos_daily['delta']).cumsum())

    path = r"C:\Users\Norbert\PycharmProjects\portfolio\data\database\positions.txt"
    assert os.path.isfile(path)

    positions.to_csv(path, index=None)
    return positions

def getPortfolioStatistics(data, start_date, end_date):
    ''' Obtains historical and current positions of all shares

    Args:
        data = Pandas dataframe containing all transactions incl. date and ISIN.
        start_date = start date of portfolio
        end_date = end date / today
    Returns:
        Positions over time of all current and previous shares.
    '''

    # Omit copy warning
    pd.options.mode.chained_assignment = None

    # cash
    data['cash'] = data['saldo'].apply(lambda x: float(x.replace(",", ".")))
    cash_pos = data.loc[data['cash'] > 0.01,]
    cash = cash_pos[['date', 'cash']].groupby('date').agg('min').reset_index()

    # Create buy/sell variables
    data['buy'] = 0
    data.loc[data['desc'].str.startswith('Koop'), 'buy'] = (data['desc'].str.extract(r'(\d+)')
        .loc[data['desc'].str.startswith('Koop')]).values.astype(int)

    data['sell'] = 0
    data.loc[data['desc'].str.startswith('Verkoop'), 'sell'] = (data['desc'].str.extract(r'(\d+)')
        .loc[data['desc'].str.startswith('Verkoop')]).values.astype(int)

    tickers = data.loc[(data['buy'] > 0) | (data['sell'] > 0), 'isin'].dropna().astype(str).unique()

    positions = pd.DataFrame({'date': pd.date_range(start=start_date, end=end_date, freq='D')[::-1]})
    for tick in tickers:
        trade = data.loc[(data['isin'] == tick) &
                         ((data['buy'] > 0) | (data['sell'] > 0))]

        trade['delta'] = trade.apply(lambda row: row['buy'] - row['sell'], axis=1)

        trade_daily = trade[['date', 'delta']].groupby(['date']).agg('sum')
        pos_daily = pd.merge(positions, trade_daily, how='left', on='date').fillna(0)

        # Append position to portfolio.
        positions[tick] = np.flipud(np.flipud(pos_daily['delta']).cumsum())

    # Obtain daily prices of purchased assets.
    prices_dly = pd.DataFrame({'date': pd.date_range(start=start_date, end=end_date, freq='D')[::-1]})
    ISIN_codes = positions.columns[1:]

    # mapping = pd.read_csv("data/tickers.txt")

    # Loop through ISIN codes.
    for ISIN in ISIN_codes:
        # Obtain dates with positive positions
        pos_pos = positions[positions[ISIN] > 0]

        # Download data for positive positions
        if len(pos_pos) > 0:
            start = min(pos_pos['date'])
            end = max(pos_pos['date'])
            print(ISIN)

            # Transform ISIN code to ticker for yahoo finance api
            ticker = mapping.loc[mapping['ISIN'] == str(ISIN), 'Ticker'].values[0]
            ticker_prices = yf.download(tickers=ticker, start=start, end=end).reset_index()[['Date', 'Close']]
            ticker_prices.columns = ['date', ISIN]
            prices_dly = pd.merge(prices_dly, ticker_prices, how='left', on='date').fillna(0)
        else:
            prices_dly[ISIN] = 0

    # Compute deposit amounts
    savings = pd.DataFrame({'date': pd.date_range(start=start_date, end=end_date, freq='D')[::-1]})

    deposit = data.loc[data['desc'].str.startswith('iDEAL', na=False), ['date', 'transaction']]
    deposit['transaction'] = deposit['transaction'].apply(lambda x: x.replace(',', '.')).astype(float)

    deposit_daily = pd.merge(savings, deposit, how='left', on='date').fillna(0)

    deposit_daily['deposit_cum'] = np.flipud(np.flipud(deposit_daily['transaction'].astype(int)).cumsum())

    data = pd.DataFrame({'date': pd.date_range(start=start_date, end=end_date, freq='D')[::-1]})
    for col in positions.columns[1:]:
        data[col] = positions[col] * prices_dly[col]

    data['portfolio'] = data[1:].sum(axis=1)
    data = data.loc[data['portfolio'] > 0]
    data = pd.merge(data, deposit_daily[['date', 'deposit_cum']], how='left', on='date')
    data = pd.merge(data, cash, how='left', on='date')
    data['cash'] = data['cash'][::-1].fillna(method='ffill')

    # Compute portfolio value and returns
    data['total_portfolio'] = data[['portfolio', 'cash']].apply(lambda row: row['portfolio'] + row['cash'], axis=1)
    data['returns_abs'] = data[['total_portfolio', 'deposit_cum']].apply(lambda row: row['total_portfolio'] - row['deposit_cum'], axis=1)

    # Define path and write csv
    path = r"C:\Users\Norbert\PycharmProjects\portfolio\data\portfolio.txt"
    data.to_csv(path, index=False)

    # Get current portfolio
    df_tickers = data.drop(columns=['date', 'portfolio', 'deposit_cum', 'cash', 'total_portfolio', 'returns_abs'], index=1)

    df = pd.DataFrame(data=df_tickers.iloc[1, df_tickers.values[0] > 0]).reset_index().rename(
        columns={'index': 'ISIN', 2: 'total_value'})
    df['portfolio_share'] = (df['total_value'] / df['total_value'].sum()) * 100

    df.sort_values(by='total_value', ascending=False, inplace=True)
    current_portfolio = pd.merge(df, mapping, on='ISIN').round(2)
    current_portfolio = current_portfolio[['Name', 'total_value', 'portfolio_share', 'ISIN', 'Ticker']]
    current_portfolio.columns = ['Asset', 'Total value (€)', 'Share', 'ISIN', 'Ticker']
    print(current_portfolio)

    # Define path and write csv
    path2 = r"C:\Users\Norbert\PycharmProjects\portfolio\data\current_portfolio.txt"
    current_portfolio.to_csv(path2, index=False)

    return data