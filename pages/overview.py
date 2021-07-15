import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px


from utils import Header, make_dash_table, generate_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))
df_portfolio = pd.read_csv(DATA_PATH.joinpath("portfolio.txt"))
df_current_portfolio = pd.read_csv(DATA_PATH.joinpath("current_portfolio.txt"))

df_graph = pd.read_csv(DATA_PATH.joinpath("df_graph.csv"))

def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Investment Strategy"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    The strategy of this portfolio is 1) asset growth for the purchase of a house, \
                                    and 2) a more risky long horizon component for early retirement purposes. \
                                    The Emerging Markets component will be held for lifetime, whereas the remaining assets \
                                    can be sold on short or medium term. The portfolio is enlarged with monthly deposits \
                                    distributed as follows: ",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                    html.Li("19% Asia Pacific ETF (dividend) ",style={"color": "#ffffff"}),
                                    html.Li("27% S&P 500 (dividend)", style={"color": "#ffffff"}),
                                    html.Li("27% World ETF ",style={"color": "#ffffff"}),
                                    html.Li("27% Emerging Markets ETF", style={"color": "#ffffff"}),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Current Portfolio Facts"], className="subtitle padded"
                                    ),
                                    generate_table(df_current_portfolio[['Asset', 'Total value (€)']])
                                    # html.Table(make_dash_table(df_fund_facts)),
                                    # df =
                                    # html.Table(make_dash_table(
                                    #     df_current_portfolio[['Name', 'total_value', 'portfolio_share']])),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        ["Current Portfolio Distribution"],
                                    className="subtitle padded"
                                    ),
                                    dcc.Graph(
                                        figure=go.Figure(
                                            data=[go.Pie(labels=df_current_portfolio['Asset'],
                                                         values=df_current_portfolio['Share'],
                                                         showlegend=False,
                                                         marker={'colors':px.colors.sequential.RdBu},

                                                         )],
                                            layout=go.Layout(height=250,
                                                          margin=go.layout.Margin(
                                                                l=10, #left margin
                                                                r=10, #right margin
                                                                b=10, #bottom margin
                                                                t=10, #top margin
    )
)
                                                ),
                                        config={'displayModeBar': False}
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Fund Facts"], className="subtitle padded"
                                    ),
                                    # html.Table(make_dash_table(df_fund_facts)),
                                    # df =
                                    html.Table(make_dash_table(df_current_portfolio[['Asset','Total value (€)','Share']])),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Average annual performance",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-1",
                                        figure={
                                            "data": [
                                                go.Bar(
                                                    x=[
                                                        "1 Year",
                                                        "3 Year",
                                                        "5 Year",
                                                        "10 Year",
                                                        "41 Year",
                                                    ],
                                                    y=[
                                                        "21.67",
                                                        "11.26",
                                                        "15.62",
                                                        "8.37",
                                                        "11.11",
                                                    ],
                                                    marker={
                                                        "color": "#97151c",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="Calibre Index Fund",
                                                ),
                                                go.Bar(
                                                    x=[
                                                        "1 Year",
                                                        "3 Year",
                                                        "5 Year",
                                                        "10 Year",
                                                        "41 Year",
                                                    ],
                                                    y=[
                                                        "21.83",
                                                        "11.41",
                                                        "15.79",
                                                        "8.50",
                                                    ],
                                                    marker={
                                                        "color": "#dddddd",
                                                        "line": {
                                                            "color": "rgb(255, 255, 255)",
                                                            "width": 2,
                                                        },
                                                    },
                                                    name="S&P 500 Index",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=False,
                                                bargap=0.35,
                                                font={"family": "Raleway", "size": 10},
                                                height=200,
                                                hovermode="closest",
                                                legend={
                                                    "x": -0.0228945952895,
                                                    "y": -0.189563896463,
                                                    "orientation": "h",
                                                    "yanchor": "top",
                                                },
                                                margin={
                                                    "r": 0,
                                                    "t": 20,
                                                    "b": 10,
                                                    "l": 10,
                                                },
                                                showlegend=True,
                                                title="",
                                                width=330,
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [-0.5, 4.5],
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "category",
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [0, 22.9789473684],
                                                    "showgrid": True,
                                                    "showline": True,
                                                    "title": "",
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Portfolio return",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-2",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=df_portfolio["date"],
                                                    y=df_portfolio["returns_abs"],
                                                    line={"color": "#97151c"},
                                                    mode="lines",
                                                    name="Portfolio return",

                                                )
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                width=700,
                                                height=200,
                                                font={"family": "Raleway", "size": 10},
                                                margin={
                                                    "r": 30,
                                                    "t": 30,
                                                    "b": 30,
                                                    "l": 30,
                                                },
                                                titlefont={
                                                    "family": "Raleway",
                                                    "size": 10,
                                                },
                                                showlegend=True,
                                                xaxis={
                                                    "autorange": True,
                                                    "linewidth": 1,
                                                    "showline": True,

                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    # "gridcolor": "rgba(127, 127, 127, 0.2)",
                                                    # "mirror": False,
                                                    # "nticks": 4,
                                                    # # "range": [0, 30000],
                                                    # "showgrid": True,
                                                    "showline": True,
                                                    # "ticklen": 10,
                                                    # "ticks": "outside",
                                                    "title": "€",
                                                    # "type": "linear",
                                                    # "zeroline": False,
                                                    # "zerolinewidth": 4,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            ),
                        ],
                        className="row ",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Portfolio development ", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-self",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=df_portfolio["date"],
                                                    y=df_portfolio["total_portfolio"],
                                                    line={"color": "#BC4639"},
                                                    mode="lines",
                                                    name="Portfolio value",
                                                ),
                                                go.Scatter(
                                                    x=df_portfolio["date"],
                                                    y=df_portfolio[
                                                        "deposit_cum"
                                                    ],
                                                    line={"color": "#b5b5b5"},
                                                    mode="lines",
                                                    name="Total cash deposited",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                width=700,
                                                height=200,
                                                font={"family": "Raleway", "size": 10},
                                                margin={
                                                    "r": 30,
                                                    "t": 30,
                                                    "b": 30,
                                                    "l": 30,
                                                },
                                                showlegend=True,
                                                titlefont={
                                                    "family": "Raleway",
                                                    "size": 10,
                                                },
                                                xaxis={
                                                    "autorange": True,
                                                    "rangeselector": {
                                                        "buttons": [
                                                            {
                                                                "count": 1,
                                                                "label": "1M",
                                                                "step": "month",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "count": 3,
                                                                "label": "3M",
                                                                "step": "month",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "label": "All",
                                                                "step": "all",
                                                            },
                                                        ]
                                                    },
                                                    "showline": True,
                                                    "type": "date",
                                                    "zeroline": False,
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [
                                                        18.6880162434,
                                                        278.431996757,
                                                    ],
                                                    "showline": True,
                                                    "type": "linear",
                                                    "zeroline": False,
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                    )

                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
