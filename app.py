import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# defining some colours
colors = {
    "background": "#EE4266",
    "text": "#FFD23F",
    "sub-text": "#ffffff"
}

#reading and ingesting datafile
df = pd.read_csv("https://raw.githubusercontent.com/eoinparkinson/covid-19-data-raw/master/covid-stats.csv", index_col=0)
print(df)

#opening mapbox token
token = "pk.eyJ1IjoiZW9pbnBhcmtpbnNvbiIsImEiOiJja2Zzb213MHAwanU0MnFwZGthZjZ1cHljIn0.qX9tz-O9KSxxws35X6LY4Q"

# setting up map_graph
fig = px.scatter_mapbox(df, lat="Lat", lon="Long", color="CountyName", size="ConfirmedCovidCases",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=40, zoom=5.5)


#updating map mapbox_style
fig.update_layout(mapbox_style="light", mapbox_accesstoken=token)

#init layout at /
app.layout = html.Div(style={
    #setting style of header div
    "backgroundColor": colors["background"],
    "display": "flex",
    "flex-direction": "column",
    },
    # visual header div & title
    children=[
    html.H1(children="Ireland Covid-19 Stats",
    style={
        "textAlign": "center",
        "color": colors["text"]
    }),

    #main content-div (not the header)
    html.Div(children='''
        by Eoin P.
    ''',
    style={    # style
    "textAlign": "center",
    "color": colors["sub-text"],
    }),

# implementing the graph
    html.Div(style={"height":"cover"},children=
        dcc.Graph(
            id='example-graph',
            figure=fig,
            style={
            "height": "800px"
            })
        )
])



if __name__ == '__main__':
    app.run_server(debug=True)
