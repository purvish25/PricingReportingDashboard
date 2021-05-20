import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from MainClass import MainClass

df = pd.read_csv("data/pricing_data.csv")
data = df.copy()
dropdownListItems = [{'label': "Monthly", 'value': "Monthly"},
                     {'label': "Weekly", 'value': "Weekly"},
                     {'label': "Age Groups", 'value': "Age Groups"},
                     {'label': "Credit Groups", 'value': "Credit Groups"},
                     {'label': "Vehicle Value", 'value': "Vehicle Value"},
                     {'label': "Vehicle Mileage", 'value': "Vehicle Mileage"},
                     {'label': "Licence Length", 'value': "Licence Length"}]
stringlist = ["Monthly chart", "Weekly chart", "Age Group wise chart", "Credit Group wise chart",
              "Vehicle Value Group wise chart",
              "Vehicle Milege Group wise chart", "Licence Length Group wise chart"]
# print(df.info)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

df['Credit Score'].fillna((df['Credit Score'].mean()), inplace=True)
df['Vehicle Value'].fillna((df['Vehicle Value'].mean()), inplace=True)
df['Vehicle Mileage'].fillna((df['Vehicle Mileage'].mean()), inplace=True)

cats = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
        'December']
labels = ['18-29', '30-39', '40-49', '50-59', '60-69', '70+']
bins = [18, 30, 40, 50, 60, 70, 120]
crediScoreGroups = ['100-199', '200-299', '300-399', '400-499', '500-599', '600-699', '700-799']
crditbins = [100, 200, 300, 400, 500, 600, 700, 800]
licenceGroups = ['1-2.99', '3-4.99', '5-6.99', '7-8.99', '9-10.99', '11-12.99', '13+']
licenbins = [1, 3, 5, 7, 9, 11, 13, 18]
mileageGroups = ['1-2.9k', '3-4.9k', '5-6.9k', '7-8.9k', '9-10.9k', '11-12.9k', '13k+']
mileagebins = [1000, 3000, 5000, 7000, 9000, 11000, 13000, 20000]
vehiclevalueGroups = ['1-2.9k', '3-4.9k', '5-6.9k', '7-8.9k', '9-10.9k', '11-12.9k', '13-14.99k', '15k+']
vehiclevaluebins = [1000, 3000, 5000, 7000, 9000, 11000, 13000, 15000, 20000]
dropdownListItems = [{'label': "Monthly", 'value': "Monthly"},
                     {'label': "Weekly", 'value': "Weekly"},
                     {'label': "Age Groups", 'value': "Age Groups"},
                     {'label': "Credit Groups", 'value': "Credit Groups"},
                     {'label': "Vehicle Value", 'value': "Vehicle Value"},
                     {'label': "Vehicle Mileage", 'value': "Vehicle Mileage"},
                     {'label': "Licence Length", 'value': "Licence Length"}]

tlist = [{'label': "Conversion Percentage", 'value': "Conversion Percentage"}]
conversionList = dropdownListItems + tlist

mainclass = MainClass()

df['Age Groups'] = pd.cut(df["Customer Age"], bins, labels=labels, include_lowest=True)
df['Credit Groups'] = pd.cut(df["Credit Score"], crditbins, labels=crediScoreGroups, include_lowest=True)
df['Licence Groups'] = pd.cut(df["Licence Length"], licenbins, labels=licenceGroups, include_lowest=True)
df['Mileage Groups'] = pd.cut(df["Vehicle Mileage"], mileagebins, labels=mileageGroups, include_lowest=True)
df['Vehiclevalue Groups'] = pd.cut(df["Vehicle Value"], vehiclevaluebins, labels=vehiclevalueGroups,
                                   include_lowest=True)

df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
df = df.sort_values(by="Transaction Date")
df['months'] = df['Transaction Date'].dt.strftime('%B')
df['weeks'] = df['Transaction Date'].dt.strftime('%V')
df['Gross Profit'] = df['Total Price'] - df['Net Price']
total_revenue_2020 = round(df['Total Price'].sum(), 2)
maskA = (df['Test Group'] == 'A')
maskB = (df['Test Group'] == 'B')

df_with_A = df[maskA]
df_With_B = df[maskB]

total_revenue_A = round(df_with_A['Total Price'].sum(), 2)
total_revenue_B = round(df_With_B['Total Price'].sum(), 2)

# print(df.groupby(df['Transaction Date'].dt.strftime('%B'))['Profit'].sum().sort_values())

counts_in_dfA = df_with_A['months'].value_counts()
counts_in_dfA = mainclass.oreder_series_months(counts_in_dfA)
counts_in_dfB = df_With_B['months'].value_counts()
counts_in_dfB = mainclass.oreder_series_months(counts_in_dfB)

print(df['months'].value_counts())

profitA_and_B_monthly, profitA_and_B_weekly, profitA_and_B_agewise, profitA_B_creditwise, \
profitA_B_vehicle_value, profit_A_B_vehicle_mile, profit_A_B_licence = mainclass.get_dataframe_for_netProfit_chart(
    df_with_A, df_With_B)

conversionA_and_B_monthly, conversionA_and_B_weekly, conversion_percentage_A_B, conversionA_and_B_agewise, \
conversionA_B_Crediwise, conversion_A_B_vv, conversion_A_B_vehicle_mile, conversion_A_B_licence = \
    mainclass.get_dataframes_for_conversion_chart(df_with_A, df_With_B, counts_in_dfA, counts_in_dfB)

revenueA_B_monthly, revenueA_B_weekly, revenue_A_B_agewise, revenueA_B_Crediwise, \
revenue_A_B_vv, revenue_A_B_vehicle_mile, revenue_A_B_licence = mainclass.get_dataframes_for_revenue_charts(df_with_A,
                                                                                                            df_With_B)

gross_profitA_B_monthly, gross_profitA_B_weekly, gross_profit_A_B_agewise, \
gross_profitA_B_Crediwise, gross_profit_A_B_vv, gross_profit_A_B_vehicle_mile, \
gross_profit_A_B_licence = mainclass.get_gross_profit_for_chart(df_with_A, df_With_B)

app.layout = dbc.Container([
    html.A(dbc.Button('Refresh', className="mr-1", color="success"), href='/'),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(id='dd-profit', value="Monthly",
                                             options=dropdownListItems, multi=False, clearable=False)
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='profit-bar-chart', figure={},
                                          config={'displayModeBar': True,
                                                  'displaylogo': False,
                                                  'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian',
                                                                             'hoverClosestCartesian',
                                                                             'toggleSpikelines']})
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dash_table.DataTable(
                                    id='datatable-interactivity',
                                    # columns=[{'name': i, 'id': i, } for i in profitA_and_B_monthly.columns],
                                    columns=[],
                                    data=[],  # the contents of the table
                                    editable=False,  # allow editing of data inside all cells
                                    sort_action="native",
                                    # enables data to be sorted per-column by user or not ('none')
                                    sort_mode="single",  # sort across 'multi' or 'single' columns
                                    page_action="native",  # all data is passed to the table up-front or not ('none')
                                    page_current=0,  # page number that user is on
                                    page_size=6,  # number of rows visible per page
                                    style_cell={  # ensure adequate header width when text is shorter than cell's text
                                        'width': 'auto',
                                        'textAlign': 'center'
                                    },

                                    style_data={  # overflow cells' content into multiple lines
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                    }
                                ),
                            ])
                        ]),

                    ]),
                ],
                style={"width": "36rem"},
                className="mt-3"
            )
        ], width=6),
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(id='dd-conversion', value="Monthly",
                                             options=conversionList, multi=False, clearable=False)
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='conversion-bar-chart', figure={},
                                          config={'displayModeBar': True,
                                                  'displaylogo': False,
                                                  'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian',
                                                                             'hoverClosestCartesian',
                                                                             'toggleSpikelines']})
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dash_table.DataTable(
                                    id='conversion-datatable',
                                    # columns=[{'name': i, 'id': i, } for i in profitA_and_B_monthly.columns],
                                    columns=[],
                                    data=[],  # the contents of the table
                                    editable=False,  # allow editing of data inside all cells
                                    sort_action="native",
                                    # enables data to be sorted per-column by user or not ('none')
                                    sort_mode="single",  # sort across 'multi' or 'single' columns
                                    page_action="native",  # all data is passed to the table up-front or not ('none')
                                    page_current=0,  # page number that user is on
                                    page_size=6,  # number of rows visible per page
                                    style_cell={  # ensure adequate header width when text is shorter than cell's text
                                        'width': 'auto',
                                        'textAlign': 'center'
                                    },

                                    style_data={  # overflow cells' content into multiple lines
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                    }
                                ),
                            ])
                        ]),

                    ]),
                ],
                style={"width": "36rem"},
                className="mt-3"
            )
        ], width=6),
    ], justify='center'),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(id='dd-revenue', value="Monthly",
                                             options=dropdownListItems, multi=False, clearable=False)
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='revenue-bar-chart', figure={},
                                          config={'displayModeBar': True,
                                                  'displaylogo': False,
                                                  'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian',
                                                                             'hoverClosestCartesian',
                                                                             'toggleSpikelines']})
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dash_table.DataTable(
                                    id='revenue-datatable',
                                    # columns=[{'name': i, 'id': i, } for i in profitA_and_B_monthly.columns],
                                    columns=[],
                                    data=[],  # the contents of the table
                                    editable=False,  # allow editing of data inside all cells
                                    sort_action="native",
                                    # enables data to be sorted per-column by user or not ('none')
                                    sort_mode="single",  # sort across 'multi' or 'single' columns
                                    page_action="native",  # all data is passed to the table up-front or not ('none')
                                    page_current=0,  # page number that user is on
                                    page_size=6,  # number of rows visible per page
                                    style_cell={  # ensure adequate header width when text is shorter than cell's text
                                        'width': 'auto',
                                        'textAlign': 'center'
                                    },

                                    style_data={  # overflow cells' content into multiple lines
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                    }
                                ),
                            ])
                        ]),

                    ]),
                ],
                style={"width": "36rem"},
                className="mt-3"
            )
        ], width=6),
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(id='dd-gross-profit', value="Monthly",
                                             options=dropdownListItems, multi=False, clearable=False)
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='gross-profit-bar-chart', figure={},
                                          config={'displayModeBar': True,
                                                  'displaylogo': False,
                                                  'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian',
                                                                             'hoverClosestCartesian',
                                                                             'toggleSpikelines']})
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dash_table.DataTable(
                                    id='gross-profit-datatable',
                                    # columns=[{'name': i, 'id': i, } for i in profitA_and_B_monthly.columns],
                                    columns=[],
                                    data=[],  # the contents of the table
                                    editable=False,  # allow editing of data inside all cells
                                    sort_action="native",
                                    # enables data to be sorted per-column by user or not ('none')
                                    sort_mode="single",  # sort across 'multi' or 'single' columns
                                    page_action="native",  # all data is passed to the table up-front or not ('none')
                                    page_current=0,  # page number that user is on
                                    page_size=6,  # number of rows visible per page
                                    style_cell={  # ensure adequate header width when text is shorter than cell's text
                                        'width': 'auto',
                                        'textAlign': 'center'
                                    },

                                    style_data={  # overflow cells' content into multiple lines
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                    }
                                ),
                            ])
                        ]),

                    ]),
                ],
                style={"width": "36rem"},
                className="mt-3"
            )
        ], width=6),
    ], justify='center'),
])

@app.callback(
    [Output(component_id='profit-bar-chart', component_property='figure'),
     Output('datatable-interactivity', 'data'),
     Output('datatable-interactivity', 'columns')],
    [Input('dd-profit', 'value')])
# [State('datatable-gapminder', 'selected_row_indices')])
def update_bar_chart(value_chsn):
    # mask = df["day"] == day
    datatosend = {}
    colstosend = []
    if value_chsn == "Monthly":
        fig = px.bar(profitA_and_B_monthly, x="months", y="profits",
                     color="group", barmode="group", title="Net Profit " + stringlist[0])
        datatosend = profitA_and_B_monthly.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in profitA_and_B_monthly.columns]
    elif value_chsn == "Weekly":
        fig = px.bar(profitA_and_B_weekly, x="weeks", y="profits",
                     color="group", barmode="group", title="Net Profit " + stringlist[1])
        fig.update_layout(xaxis_tickangle=-45)
        datatosend = profitA_and_B_weekly.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in profitA_and_B_weekly.columns]
    elif value_chsn == "Age Groups":
        fig = px.bar(profitA_and_B_agewise, x="age groups", y="profits",
                     color="group", barmode="group", title="Net Profit " + stringlist[2])
        datatosend = profitA_and_B_agewise.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in profitA_and_B_agewise.columns]
    elif value_chsn == "Credit Groups":
        fig = px.bar(profitA_B_creditwise, x="credit groups", y="profits",
                     color="group", barmode="group", title="Net Profit " + stringlist[3])
        datatosend = profitA_B_creditwise.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in profitA_B_creditwise.columns]
    elif value_chsn == "Vehicle Value":
        fig = px.bar(profitA_B_vehicle_value, x="vehicle value", y="profits",
                     color="group", barmode="group", title="Net Profit " + stringlist[4])
        datatosend = profitA_B_vehicle_value.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in profitA_B_vehicle_value.columns]
    elif value_chsn == "Vehicle Mileage":
        fig = px.bar(profit_A_B_vehicle_mile, x="mileage", y="profits",
                     color="group", barmode="group", title="Net Profit " + stringlist[5])
        datatosend = profit_A_B_vehicle_mile.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in profit_A_B_vehicle_mile.columns]
    else:
        fig = px.bar(profit_A_B_licence, x="licence length", y="profits",
                     color="group", barmode="group", title="Net Profit " + stringlist[6])
        datatosend = profit_A_B_licence.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in profit_A_B_licence.columns]
    return fig, datatosend, colstosend


@app.callback(
    [Output(component_id='conversion-bar-chart', component_property='figure'),
     Output('conversion-datatable', 'data'),
     Output('conversion-datatable', 'columns')],
    [Input('dd-conversion', 'value')])
def update_bar_chart(value_chsn):
    datatosend = {}
    colstosend = []
    if value_chsn == "Monthly":
        fig = px.bar(conversionA_and_B_monthly, x="months", y="conversion",
                     color="group", barmode="group", title="Conversion " + stringlist[0])
        datatosend = conversionA_and_B_monthly.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in conversionA_and_B_monthly.columns]
    elif value_chsn == "Weekly":
        fig = px.bar(conversionA_and_B_weekly, x="weeks", y="conversion",
                     color="group", barmode="group", title="Conversion " + stringlist[1])
        fig.update_layout(xaxis_tickangle=-45)
        datatosend = conversionA_and_B_weekly.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in conversionA_and_B_weekly.columns]
    elif value_chsn == "Age Groups":
        fig = px.bar(conversionA_and_B_agewise, x="age groups", y="conversion",
                     color="group", barmode="group", title="Conversion " + stringlist[2])
        datatosend = conversionA_and_B_agewise.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in conversionA_and_B_agewise.columns]
    elif value_chsn == "Credit Groups":
        fig = px.bar(conversionA_B_Crediwise, x="credit groups", y="conversion",
                     color="group", barmode="group", title="Conversion " + stringlist[3])
        datatosend = conversionA_B_Crediwise.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in conversionA_B_Crediwise.columns]
    elif value_chsn == "Vehicle Value":
        fig = px.bar(conversion_A_B_vv, x="vehicle value", y="conversion",
                     color="group", barmode="group", title="Conversion " + stringlist[4])
        datatosend = conversion_A_B_vv.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in conversion_A_B_vv.columns]
    elif value_chsn == "Vehicle Mileage":
        fig = px.bar(conversion_A_B_vehicle_mile, x="mileage", y="conversion",
                     color="group", barmode="group", title="Conversion " + stringlist[5])
        datatosend = conversion_A_B_vehicle_mile.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in conversion_A_B_vehicle_mile.columns]
    elif value_chsn == "Conversion Percentage":
        fig = px.bar(conversion_percentage_A_B, x="months", y="percentage",
                     color="group", barmode="group", title="Conversion Percentage chart")
        datatosend = conversion_percentage_A_B.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in conversion_percentage_A_B.columns]
    else:
        fig = px.bar(conversion_A_B_licence, x="licence length", y="conversion",
                     color="group", barmode="group", title="Conversion " + stringlist[6])
        datatosend = conversion_A_B_licence.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in conversion_A_B_licence.columns]
    return fig, datatosend, colstosend


@app.callback(
    [Output(component_id='revenue-bar-chart', component_property='figure'),
     Output('revenue-datatable', 'data'),
     Output('revenue-datatable', 'columns')],
    [Input('dd-revenue', 'value')])
def update_bar_chart(value_chsn):
    datatosend = {}
    colstosend = []
    if value_chsn == "Monthly":
        fig = px.bar(revenueA_B_monthly, x="months", y="revenue",
                     color="group", barmode="group", title="Revenue " + stringlist[0])
        datatosend = revenueA_B_monthly.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in revenueA_B_monthly.columns]
    elif value_chsn == "Weekly":
        fig = px.bar(revenueA_B_weekly, x="weeks", y="revenue",
                     color="group", barmode="group", title="Revenue " + stringlist[1])
        fig.update_layout(xaxis_tickangle=-45)
        datatosend = revenueA_B_weekly.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in revenueA_B_weekly.columns]
    elif value_chsn == "Age Groups":
        fig = px.bar(revenue_A_B_agewise, x="age groups", y="revenue",
                     color="group", barmode="group", title="Revenue " + stringlist[2])
        datatosend = revenue_A_B_agewise.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in revenue_A_B_agewise.columns]
    elif value_chsn == "Credit Groups":
        fig = px.bar(revenueA_B_Crediwise, x="credit groups", y="revenue",
                     color="group", barmode="group", title="Revenue " + stringlist[3])
        datatosend = revenueA_B_Crediwise.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in revenueA_B_Crediwise.columns]
    elif value_chsn == "Vehicle Value":
        fig = px.bar(revenue_A_B_vv, x="vehicle value", y="revenue",
                     color="group", barmode="group", title="Revenue " + stringlist[4])
        datatosend = revenue_A_B_vv.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in revenue_A_B_vv.columns]
    elif value_chsn == "Vehicle Mileage":
        fig = px.bar(revenue_A_B_vehicle_mile, x="mileage", y="revenue",
                     color="group", barmode="group", title="Revenue " + stringlist[5])
        datatosend = revenue_A_B_vehicle_mile.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in revenue_A_B_vehicle_mile.columns]
    else:
        fig = px.bar(revenue_A_B_licence, x="licence length", y="revenue",
                     color="group", barmode="group", title="Revenue " + stringlist[6])
        datatosend = revenue_A_B_licence.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in revenue_A_B_licence.columns]
    return fig, datatosend, colstosend


@app.callback(
    [Output(component_id='gross-profit-bar-chart', component_property='figure'),
     Output('gross-profit-datatable', 'data'),
     Output('gross-profit-datatable', 'columns')],
    [Input('dd-gross-profit', 'value')])
def update_bar_chart(value_chsn):
    # datatosend = {}
    # colstosend = []
    if value_chsn == "Monthly":
        fig = px.bar(gross_profitA_B_monthly, x="months", y="gross profit",
                     color="group", barmode="group", title="Gross Profit " + stringlist[0])
        datatosend = gross_profitA_B_monthly.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in gross_profitA_B_monthly.columns]
    elif value_chsn == "Weekly":
        fig = px.bar(gross_profitA_B_weekly, x="weeks", y="gross profit",
                     color="group", barmode="group", title="Gross Profit " + stringlist[1])
        fig.update_layout(xaxis_tickangle=-45)
        datatosend = gross_profitA_B_weekly.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in gross_profitA_B_weekly.columns]
    elif value_chsn == "Age Groups":
        fig = px.bar(gross_profit_A_B_agewise, x="age groups", y="gross profit",
                     color="group", barmode="group", title="Gross Profit " + stringlist[2])
        datatosend = gross_profit_A_B_agewise.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in gross_profit_A_B_agewise.columns]
    elif value_chsn == "Credit Groups":
        fig = px.bar(gross_profitA_B_Crediwise, x="credit groups", y="gross profit",
                     color="group", barmode="group", title="Gross Profit " + stringlist[3])
        datatosend = gross_profitA_B_Crediwise.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in gross_profitA_B_Crediwise.columns]
    elif value_chsn == "Vehicle Value":
        fig = px.bar(gross_profit_A_B_vv, x="vehicle value", y="gross profit",
                     color="group", barmode="group", title="Gross Profit " + stringlist[4])
        datatosend = gross_profit_A_B_vv.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in gross_profit_A_B_vv.columns]
    elif value_chsn == "Vehicle Mileage":
        fig = px.bar(gross_profit_A_B_vehicle_mile, x="mileage", y="gross profit",
                     color="group", barmode="group", title="Gross Profit " + stringlist[5])
        datatosend = gross_profit_A_B_vehicle_mile.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in gross_profit_A_B_vehicle_mile.columns]
    else:
        fig = px.bar(gross_profit_A_B_licence, x="licence length", y="gross profit",
                     color="group", barmode="group", title="Gross Profit " + stringlist[6])
        datatosend = gross_profit_A_B_licence.to_dict('records')
        colstosend = [{"name": i, "id": i} for i in gross_profit_A_B_licence.columns]
    return fig, datatosend, colstosend


if __name__ == '__main__':
    app.run_server(debug=True)
