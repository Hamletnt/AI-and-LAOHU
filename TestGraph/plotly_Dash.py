import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

# ข้อมูลตัวอย่าง
data = {'Labels': ['A', 'B', 'C', 'D'], 'Values': [15, 30, 45, 10]}
fig = px.pie(data, values='Values', names='Labels')

app.layout = html.Div([
    html.H1("หน้ารวม Pie Chart"),
    dcc.Graph(id='pie_chart', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)