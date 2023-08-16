import sqlite3
import pandas as pd

cnx = sqlite3.connect("./data/sensor_data.db")
# cur = con.cursor()

# res = cur.execute("SELECT * FROM air_quality")

aq_df = pd.read_sql_query("SELECT * FROM air_quality", cnx)

print(aq_df['timestamp'].head())

aq_df['timestamp'] = pd.to_datetime(list(map(lambda x: int(x * 10**9), aq_df['timestamp'])))
print(aq_df['timestamp'].head())

print("-" * 80)

# dash setup stuff
import dash
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(children='show data'),
    dash_table.DataTable(data=aq_df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.scatter(aq_df, x='timestamp', y='co2', animation_frame="timestamp")),
    dcc.Graph(figure=px.scatter(aq_df, x='timestamp', y='ethanol')),
    # dcc.Graph(id="scatter-plot"),
    # dcc.RangeSlider(
    #     id='range-slider',
    #     min=aq_df["timestamp"].min(), max=aq_df["timestamp"].max(),
    #     marks={0: '0', 2.5: '2.5'},
    #     value=[aq_df.iloc[-101]["timestamp"], aq_df.iloc[-1]["timestamp"]]
    # )
])

# @app.callback(
#     Output("scatter-plot", "figure"), 
#     Input("range-slider", "value"))
# def update_bar_chart(slider_range):
#     df = aq_df # replace with your own data source
#     low, high = slider_range
#     mask = (df['timestamp'] > low) & (df['timestamp'] < high)
#     fig = px.scatter(
#         df[mask], x="timestamp", y="co2", 
# )
#     return fig

if __name__ == '__main__':
    app.run()