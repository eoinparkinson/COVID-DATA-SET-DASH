import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

#external stylesheet for plotly dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#opening mapbox token
token = "pk.eyJ1IjoiZW9pbnBhcmtpbnNvbiIsImEiOiJja2Zzb213MHAwanU0MnFwZGthZjZ1cHljIn0.qX9tz-O9KSxxws35X6LY4Q"

# initialising/defining the flask/dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, height=device-height, initial-scale=1, maximum-scale=1.0, user-scalable=no"}
    ])

# defining some proppa shwanky colours
colors = {
    "background": "#1a1a1a",
    "text": "#FFD23F",
    "sub-text": "#ffffff"
}

#reading and ingesting datafile
df = pd.read_csv("https://raw.githubusercontent.com/eoinparkinson/covid-19-data-raw/master/covid-stats.csv", index_col=0)

# i cleaning df
df_clean = df.groupby("CountyName", as_index=False).agg({"ConfirmedCovidCases": "mean", "Lat": "mean", "Long": "mean"})
print(df_clean)

# i description of dataframe
print(df_clean.describe())


# setting map temp variable

tempGraph = map_fig

# setting up map_fig
map_fig = px.scatter_mapbox(df_clean.round({"ConfirmedCovidCases":0}), lat="Lat", lon="Long", color="CountyName", size="ConfirmedCovidCases", color_continuous_scale=px.colors.cyclical.IceFire, size_max=40, zoom=5.5)
#updating map mapbox_style
map_fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token, paper_bgcolor="#1a1a1a", font=dict(color="white"), showlegend=False, margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=1
    ))


bar_fig = px.bar(df_clean.round({"ConfirmedCovidCases":0}), x="CountyName", y="ConfirmedCovidCases", color="CountyName")



#init the dash app @/
app.layout = html.Div(style={
    #setting style of header div
    "backgroundColor": "#1a1a1a",
    "display": "flex",
    "flex-direction": "column",
    "padding": "0px",
    "margin": "-8px",
    "height": "calc( 100vh - 8px )",
    },
    # visual header div & title
    children=[


    html.H2(children="Ireland Covid-19 Stats",
    style={
        "textAlign": "center",
        "color": colors["text"],
        "font-weight": "bold",
        "padding-top": "12px",
    }),

    html.H6(children="by Eoin Parkinson",style={
        "textAlign": "right",
        "color": "#ffffff",
        "padding-right": "7px",
    }),




    html.Div(children=[


        html.Div(children=[
            html.Label('Data Type',style={"color":"#ffffff"}),
            dcc.Dropdown(
                options=[
                    {'label': 'Average Covid Cases', 'value': 'mean'},
                    {'label': 'Total Covid Cases', 'value': 'total'}
                ],
                value='mean'
            ),
        ], className="six columns"),



        html.Div(children=[
            html.Label('Graph Type', style={"color":"#ffffff"}),
            dcc.Dropdown(
                id="graph-type",
                options=[
                    {'label': 'Country Map', 'value': 'country-map'},
                    {'label': 'Bar Chart', 'value': 'bar-chart'},
                    {"label": "Line Graph", "value": "line-graph"}
                ],
                value='country-map'
            ),
        ], className="six columns"),



    ], className="row", style={

        "padding-bottom": "25px",
        "padding-left": "7px",
        "padding-right": "7px",

    }),





# implementing the graph
    html.Div(style={"backgroundColor":"#1a1a1a", "height":"100%"},children=
        dcc.Graph(
            id='example-graph',
            figure=mtempGraph,
            style={
            "backgroundColor": "#1a1a1a",
            "height": "100%",
            })
        )
])


@app.callback(
    Output(component_id="example-graph", component_property="figure"),
    [Input(component_id="graph-type", component_property="value")]
)


def changeGraphType(graphType):
    if graphType == "country-map":
        tempGraph=map_fig
    elif graphType == "bar-chart":
        tempGraph=bar_fig



if __name__ == '__main__':
    app.run_server(host="0.0.0.0",debug=True)
