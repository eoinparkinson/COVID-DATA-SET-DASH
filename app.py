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

#calculate the mean
df_mean = df[["CountyName","ConfirmedCovidCases"]].mean()

fig = px.scatter_mapbox(df, x="CountyName", y="ConfirmedCovidCases", color="CountyName") #,barmode="group"



app.layout = html.Div(style={
    "backgroundColor": colors["background"]
    }, children=[
    html.H1(children="Ireland Covid-19 Stats",
    style={
        "textAlign": "center",
        "color": colors["text"]
    }),


    html.Div(children='''
        by Eoin P.
    ''',
    style={
    "textAlign": "center",
    "color": colors["sub-text"]
    }),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
