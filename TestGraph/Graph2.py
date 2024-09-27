import plotly.express as px

data = {'Labels': ['กหฟกห', 'B', 'C', 'D'], 'Values': [15, 30, 45, 10]}
fig = px.pie(data, values='Values', names='Labels')
fig.show()