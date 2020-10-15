import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go


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

#reading and ingesting datafile 1
df = pd.read_csv("https://raw.githubusercontent.com/eoinparkinson/covid-19-data-raw/master/covid-stats.csv", index_col=0)

# i cleaning df to df_clean_mean and df_clean_total
df_clean_mean = df.groupby("CountyName", as_index=False).agg({"ConfirmedCovidCases": "mean", "Lat": "mean", "Long": "mean"})
#df_clean_mean = df_clean_mean.round({"ConfirmedCovidCases":0})
df_clean_mean.rename(columns={"ConfirmedCovidCases": "Average Covid Cases", "CountyName": "County Name"}, inplace = True)


# cleaning to get total
df_clean_total = df.groupby("CountyName", as_index=False).agg({"ConfirmedCovidCases": "max"})
df_clean_total.rename(columns={"ConfirmedCovidCases": "Total Covid Cases"}, inplace = True)


# merging both clean dataframes
clean_df = df_clean_mean
# inserting the column "Total Covid Cases" into clean_df
clean_df.insert(2, "Total Covid Cases", df_clean_total["Total Covid Cases"])
# rounding the decimal values from the math to 0 decimal places
clean_df = clean_df.round({"Average Covid Cases":0, "Total Covid Cases":0})

#printing the clean_df in terminal for testing purposes
print(clean_df)


# setting up fig (map)
fig = px.scatter_mapbox(clean_df.round({"Average Covid Cases":0}), lat="Lat", lon="Long", color="County Name", size="Average Covid Cases", color_continuous_scale=px.colors.cyclical.IceFire, size_max=40, zoom=5.5, hover_name="County Name", hover_data=['Average Covid Cases'])
#updating map mapbox_style
fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token, plot_bgcolor="#1a1a1a",paper_bgcolor="#1a1a1a", font=dict(color="white"), showlegend=False, margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=1
    ))

# setting up barFig
barFig = px.bar(clean_df.round({"Average Covid Cases":0}), x="County Name", y="Average Covid Cases", color="County Name", hover_name="County Name")
#updating barFig style
barFig.update_layout(plot_bgcolor="#1a1a1a",paper_bgcolor="#1a1a1a", font=dict(color="white"), showlegend=False, margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=1
    ))


# setting up lineFig
lineFig = px.line(df, x="TimeStamp", y="ConfirmedCovidCases", color="CountyName", line_group="CountyName", hover_name="CountyName", line_shape="spline", render_mode="svg")
# updating lineFig style
lineFig.update_layout(plot_bgcolor="#1a1a1a", paper_bgcolor="#1a1a1a", font=dict(color="white"), xaxis = {"showgrid": False}, yaxis = {"showgrid": False}, margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=1
    ))


#added tempDf for clean data table at bottom of web page
tempDf = clean_df
# dropping columns "Lat" & "long"
tempDf = tempDf.drop(['Lat', 'Long'], axis=1)



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

    # h2 main title "Ireland Covid-19 Stats"
    html.H2(children="Ireland Covid-19 Stats",
    style={
        "textAlign": "center",
        "color": colors["text"],
        "font-weight": "bold",
        "padding-top": "12px",
    }),
    # h6 subtitle
    html.H6(children="by Eoin Parkinson",style={
        "textAlign": "right",
        "color": "#ffffff",
        "padding-right": "7px",
    }),

    # dropdown parent div
    html.Div(children=[

        html.Div(children=[
            # math dropdown "Calculate Mean, Calculate Total"
            dcc.Dropdown(
            id="math_dropdown",
            options=[
                {"label": "Calculate Mean", "value": "Average Covid Cases"},
                {"label": "Calculate Total", "value": "Total Covid Cases"},
            ],
            value="Average Covid Cases",
            multi=False,
            clearable=False

            )
        ], className="six columns"),


        # empty six column div (right of math dropdown)
        html.Div(children=[

        ], className="six columns"),

    ], className="row", style={

        "padding-bottom": "25px",
        "padding-left": "7px",
        "padding-right": "7px",
        "height": "100%",

    }),



    # Layout for graphs in responsive rows
    html.Div(children=[

        # inserting the bar graph in a responsive div
        html.Div(children=[
            html.Label('Bar Graph',style={"color":"#ffffff"}),
            html.Div(style={"backgroundColor":"#1a1a1a", "height":"100%"},children=
                # implementing the responsive bar graph with dropdown callback (on the left)
                dcc.Graph(
                    id='bar-graph',
                    figure=barFig,
                    style={
                    "backgroundColor": "#1a1a1a",
                    "height": "100%",

                    })
                )
        ], className="six columns"),


        # inserting the map graph in a responsive div
        html.Div(children=[
            html.Label('Country Map', style={"color":"#ffffff"}),
            html.Div(style={"backgroundColor":"#1a1a1a", "height":"100%"},children=
                # implementing the map graph (on the right)
                dcc.Graph(
                    id='map-graph',
                    figure=fig,
                    style={
                    "backgroundColor": "#1a1a1a",
                    "height": "100%",
                    })
                )
        ], className="six columns"),



    ], className="row", style={

        "padding-bottom": "25px",
        "padding-left": "7px",
        "padding-right": "7px",
        "height": "100%",

    }),

    html.Div(children=[
        # basic label saying "Confirmed Covid Cases by Date"
        html.Label("Confirmed Covid Cases by Date", style={
        "color":"#ffffff",
        }),
        # scatter lineFig
        dcc.Graph(
            id="line-graph",
            figure=lineFig,
            style={
            "backgroundColor": "#1a1a1a",
            "height":"700px",
            "padding-bottom": "75px",
            }
        )], style={
        "height":"fit",
        "backgroundColor": "#1a1a1a",
        "padding-left":"7px",
        "padding-right":"7px",
        }
    ),

    # adding the white data table seen at bottom of webpage
    html.Div(children=[
        # basic title "Clean Data"
        html.H3("Clean Data", style = {
        "backgroundColor": "#1a1a1a",
        "textAlign":"center",
        "color": colors["text"],
        "font-weight": "bold",
        }),

        # implementing table at bottom of webpage
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in tempDf.columns],
            data=tempDf.to_dict('records'),
            style_cell = {
                "color":"#ffffff",
                "backgroundColor":"#1a1a1a",
                "textAlign":"left",
                "padding-left":"5px",
                "font-size":"20px",
                "font-weight":"bold",
            },
            style_data = {
                "font-weight":"normal",
                "font-size":"15px",
            }

        )],

        style = {
            "padding-bottom":"150px",
            "padding-left":"7px",
            "padding-right":"7px",
            "backgroundColor":"#1a1a1a",
        }

    ),

])

#----------------------------------------------------------------------------------

# callback to update graph math
@app.callback(
    Output(component_id="bar-graph", component_property="figure"),
    [Input(component_id="math_dropdown", component_property="value")]
)

# function which changes the graph on dropdown change
def update_bar_graph(math_dropdown):
    dff = clean_df
    # defining the bar chart for callback
    barChart=px.bar(
            data_frame=dff,
            y=math_dropdown,
            x= "County Name",
            color="County Name",
        )
    # updating bar layout for callback
    barChart.update_layout(plot_bgcolor="#1a1a1a", paper_bgcolor="#1a1a1a", font=dict(color="white"), showlegend=False, xaxis = {"showgrid": False}, yaxis = {"showgrid": False}, margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=1
        ))


    return(barChart)
# run the development server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0",debug=True)
