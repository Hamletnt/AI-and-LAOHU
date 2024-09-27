import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# สร้างแอปพลิเคชัน Dash
app = dash.Dash(__name__)

# ข้อมูลตัวอย่างสำหรับ 3 กราฟ
data1 = pd.DataFrame({'Labels': ['A', 'B', 'C', 'D'], 'Values': [15, 30, 45, 10]})
data2 = pd.DataFrame({'Labels': ['E', 'F', 'G', 'H'], 'Values': [25, 35, 20, 20]})
data3 = pd.DataFrame({'Labels': ['I', 'J', 'K', 'L'], 'Values': [10, 40, 30, 20]})

# สร้าง Pie Charts 3 อัน
fig1 = px.pie(data1, values='Values', names='Labels', title="กราฟที่ 1")
fig2 = px.pie(data2, values='Values', names='Labels', title="กราฟที่ 2")
fig3 = px.pie(data3, values='Values', names='Labels', title="กราฟที่ 3")

# Layout ของหน้าแอป
app.layout = html.Div([
    html.H1("หน้ารวม Pie Chart"),
    
    # แสดง Pie Chart ที่ 1
    html.Div([
        dcc.Graph(id='pie_chart_1', figure=fig1),
    ], style={'width': '30%', 'display': 'inline-block'}),
    
    # แสดง Pie Chart ที่ 2
    html.Div([
        dcc.Graph(id='pie_chart_2', figure=fig2),
    ], style={'width': '30%', 'display': 'inline-block'}),

    # แสดง Pie Chart ที่ 3
    html.Div([
        dcc.Graph(id='pie_chart_3', figure=fig3),
    ], style={'width': '30%', 'display': 'inline-block'}),
])

# รันเซิร์ฟเวอร์
if __name__ == '__main__':
    app.run_server(debug=True)