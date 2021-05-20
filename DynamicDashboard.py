import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
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

profit = [profitA_and_B_monthly, profitA_and_B_weekly, profitA_and_B_agewise, profitA_B_creditwise, \
          profitA_B_vehicle_value, profit_A_B_vehicle_mile, profit_A_B_licence]

conversionA_and_B_monthly, conversionA_and_B_weekly, percentage_A_B, conversionA_and_B_agewise, \
conversionA_B_Crediwise, conversion_A_B_vv, conversion_A_B_vehicle_mile, conversion_A_B_licence = \
    mainclass.get_dataframes_for_conversion_chart(df_with_A, df_With_B, counts_in_dfA, counts_in_dfB)

conversion = [conversionA_and_B_monthly, conversionA_and_B_weekly, conversionA_and_B_agewise, \
              conversionA_B_Crediwise, conversion_A_B_vv, conversion_A_B_vehicle_mile, conversion_A_B_licence,
              percentage_A_B]

revenueA_B_monthly, revenueA_B_weekly, revenue_A_B_agewise, revenueA_B_Crediwise, \
revenue_A_B_vv, revenue_A_B_vehicle_mile, revenue_A_B_licence = mainclass.get_dataframes_for_revenue_charts(df_with_A,
                                                                                                            df_With_B)
revenue = [revenueA_B_monthly, revenueA_B_weekly, revenue_A_B_agewise, revenueA_B_Crediwise, \
           revenue_A_B_vv, revenue_A_B_vehicle_mile, revenue_A_B_licence]

gross_profitA_B_monthly, gross_profitA_B_weekly, gross_profit_A_B_agewise, \
gross_profitA_B_Crediwise, gross_profit_A_B_vv, gross_profit_A_B_vehicle_mile, \
gross_profit_A_B_licence = mainclass.get_gross_profit_for_chart(df_with_A, df_With_B)

gross_profit = [gross_profitA_B_monthly, gross_profitA_B_weekly, gross_profit_A_B_agewise, \
                gross_profitA_B_Crediwise, gross_profit_A_B_vv, gross_profit_A_B_vehicle_mile, \
                gross_profit_A_B_licence]

all_values = [profit, conversion, revenue, gross_profit]
list_y_axis = ["profits", "conversion", "revenue", "gross profit"]

app.layout = html.Div([
    html.Div(children=[
        dbc.Button('Add Chart', id='add-chart', n_clicks=0),
        html.A(dbc.Button('Refresh', className="mr-1", color="success"), href='/')
    ]),
    html.Div(id='container', children=[])
])


@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks')],
    [State('container', 'children')]
)
def display_graphs(n_clicks, div_children):
    if n_clicks > 3:
        html.P("You have reached maximum limit")
        # return div_children
    else:
        new_child = html.Div(
            style={'width': '45%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
            children=[
                dcc.Dropdown(
                    id={
                        'type': 'dynamic-dropdown',
                        'index': n_clicks
                    },
                    options=dropdownListItems,
                    value='Monthly',
                    clearable=False,
                    multi=False
                ),
                dcc.Graph(
                    id={
                        'type': 'dynamic-graph',
                        'index': n_clicks
                    },
                    config={'displayModeBar': True},
                    figure={}
                ),
                dash_table.DataTable(
                    id={
                        'type': 'dynamic-table',
                        'index': n_clicks
                    },
                    columns=[],
                    data=[],  # the contents of the table
                    editable=True,  # allow editing of data inside all cells
                    sort_action="native",
                    sort_mode="single",  # sort across 'multi' or 'single' columns
                    page_action="native",  # all data is passed to the table up-front or not ('none')
                    page_current=0,  # page number that user is on
                    page_size=6,  # number of rows visible per page
                    style_cell={  # ensure adequate header width when text is shorter than cell's text
                        'width': 'auto',
                        'textAlign': 'left'
                    },
                    style_data={  # overflow cells' content into multiple lines
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    }
                ),

            ]
        )
    div_children.append(new_child)
    return div_children


@app.callback(
    [Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
     Output({'type': 'dynamic-table', 'index': MATCH}, 'columns'),
     Output({'type': 'dynamic-table', 'index': MATCH}, 'data')],
    Input(component_id={'type': 'dynamic-dropdown', 'index': MATCH}, component_property='value'),
    State({'type': 'dynamic-dropdown', 'index': MATCH}, 'id'),
)
def update_graph(value_chsn, id):
    print(value_chsn)
    print(id['index'])
    # datatosend = {}
    # colstosend = []
    if value_chsn == "Monthly":
        fig = px.bar(all_values[id['index']][0], x="months", y=list_y_axis[id['index']],
                     color="group", barmode="group", title="Net Profit ")
        datatosend = all_values[id['index']][0].to_dict('records')
        colstosend = [{"name": i, "id": i} for i in all_values[id['index']][0].columns]
    elif value_chsn == "Weekly":
        fig = px.bar(all_values[id['index']][1], x="weeks", y=list_y_axis[id['index']],
                     color="group", barmode="group", title="Net Profit ")
        fig.update_layout(xaxis_tickangle=-45)
        datatosend = all_values[id['index']][1].to_dict('records')
        colstosend = [{"name": i, "id": i} for i in all_values[id['index']][1].columns]
    elif value_chsn == "Age Groups":
        fig = px.bar(all_values[id['index']][2], x="age groups", y=list_y_axis[id['index']],
                     color="group", barmode="group", title="Net Profit " + stringlist[2])
        datatosend = all_values[id['index']][2].to_dict('records')
        colstosend = [{"name": i, "id": i} for i in all_values[id['index']][2].columns]
    elif value_chsn == "Credit Groups":
        fig = px.bar(all_values[id['index']][3], x="credit groups", y=list_y_axis[id['index']],
                     color="group", barmode="group", title="Net Profit " + stringlist[3])
        datatosend = all_values[id['index']][3].to_dict('records')
        colstosend = [{"name": i, "id": i} for i in all_values[id['index']][3].columns]
    elif value_chsn == "Vehicle Value":
        fig = px.bar(all_values[id['index']][4], x="vehicle value", y=list_y_axis[id['index']],
                     color="group", barmode="group", title="Net Profit " + stringlist[4])
        datatosend = all_values[id['index']][4].to_dict('records')
        colstosend = [{"name": i, "id": i} for i in all_values[id['index']][4].columns]
    elif value_chsn == "Vehicle Mileage":
        fig = px.bar(all_values[id['index']][5], x="mileage", y=list_y_axis[id['index']],
                     color="group", barmode="group", title="Net Profit " + stringlist[5])
        datatosend = all_values[id['index']][5].to_dict('records')
        colstosend = [{"name": i, "id": i} for i in all_values[id['index']][5].columns]
    else:
        fig = px.bar(all_values[id['index']][6], x="licence length", y=list_y_axis[id['index']],
                     color="group", barmode="group", title="Net Profit ")
        datatosend = all_values[id['index']][6].to_dict('records')
        colstosend = [{"name": i, "id": i} for i in all_values[id['index']][6].columns]
    return fig, colstosend, datatosend


if __name__ == '__main__':
    app.run_server(debug=True)
