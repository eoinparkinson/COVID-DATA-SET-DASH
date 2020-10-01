import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


colors = {
    "background": "#EE4266",
    "text": "#FFD23F",
    "sub-text": "#ffffff"
}




#fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(style={
    "backgroundColor": colors["background"]
    }, children=[
    html.H1(children='Porki Pie',
    style={
        "textAlign": "center",
        "color": colors["text"]
    }),


    html.Div(children='''
        Covid-19 stats for Ireland.
    ''',
    style={
    "textAlign": "center",
    "color": colors["sub-text"]
    }),

    """
    dcc.Graph(
        id='example-graph',
        figure=fig
    ) """
])

if __name__ == '__main__':
    app.run_server(debug=True)
