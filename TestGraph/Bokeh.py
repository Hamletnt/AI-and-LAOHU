from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc
from bokeh.layouts import column

# ข้อมูลตัวอย่าง
labels = ['หมวด A', 'หมวด B', 'หมวด C', 'หมวด D']
sizes = [15, 30, 45, 10]

# สร้าง Pie Chart
p = figure(title="กราฟวงกลม", tools="hover", tooltips="@labels: @sizes")
p.wedge(x=0, y=1, radius=0.4,
        start_angle=0, end_angle=1.5, fill_color="navy")

# จัดการเลย์เอาต์
layout = column(p)

curdoc().add_root(layout)
show(layout)