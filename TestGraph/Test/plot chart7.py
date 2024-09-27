import sys
from openpyxl import Workbook, load_workbook
import tkinter as tk
from tkinter import Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pulldataRowColumn as data

# ตั้งค่า encoding ให้เป็น utf-8
sys.stdout.reconfigure(encoding='utf-8')

# โหลดไฟล์ workbook และ worksheet
wb = load_workbook('Test/LProfitLoss24-Feb-.xlsx')
ws = wb.active

# ตั้งค่าฟอนต์ที่รองรับภาษาไทย เช่น Tahoma
rcParams['font.family'] = 'Tahoma'

# ฟังก์ชันในการสร้าง Pie Chart แบบ Donut Chart
def create_pie_chart(data, labels, title):
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    # ใช้สี default จาก matplotlib
    colors = plt.get_cmap('tab20').colors  # ใช้ color map ที่มีสีให้เลือกมากมาย

    # ถ้ามี 'ไม่เกี่ยว' ใน labels ให้ทำให้เป็นสีขาว
    if 'ไม่เกี่ยว' in labels:
        idx = labels.index('ไม่เกี่ยว')
        colors = list(colors)  # แปลงเป็น list เพื่อปรับแต่งสี
        colors[idx] = '#ffffff'  # เปลี่ยนสี 'ไม่เกี่ยว' เป็นสีขาว

    # สร้าง Donut Chart โดยใช้ width=0.5 เพื่อทำให้เป็น donut chart
    wedges, texts, autotexts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40, colors=colors[:len(labels)],
                                      autopct='', pctdistance=0.75)

    # ดึงข้อมูลสำหรับแต่ละ wedge และเพิ่มเส้นชี้และข้อความสำหรับส่วนที่มีค่าต่ำกว่า 1.5%
    base_offset_x = 2.0  # ตัวคูณสำหรับแกน x
    base_offset_y = 1.6  # ตัวคูณสำหรับแกน y

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        percent = (data[i] / sum(data)) * 100

        if percent < 1.5:
            # เพิ่มระดับการขยับของเส้นและข้อความตามลำดับ wedge (เพิ่มทีละขั้น)
            offset_x = base_offset_x + (i * 0.3)  # คูณตัวเพิ่มให้ความยาวเพิ่มขึ้นตามลำดับ wedge
            offset_y = base_offset_y + (i * 0.3)
            ax.annotate('{:.1f}%'.format(percent), xy=(x, y), xytext=(offset_x * x, offset_y * y), 
                        horizontalalignment=horizontalalignment, 
                        arrowprops=dict(arrowstyle="->", connectionstyle=connectionstyle))
        else:
            # แสดงเปอร์เซ็นต์ในกราฟปกติถ้ามากกว่า 1.5%
            ax.text(x * 0.6, y * 0.6, '{:.1f}%'.format(percent), ha=horizontalalignment, va='center', fontsize=8)
    
    # เพิ่ม legend สำหรับ labels และแสดง title
    ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title(title)
    
    return fig




# ฟังก์ชันในการเพิ่มข้อมูลส่วนที่ขาด
def adjust_for_missing_percentage(data, labels):
    total = sum(data)
    if total < 98:
        missing_percentage = 100 - total
        data.append(missing_percentage)
        labels.append('ไม่เกี่ยว')
    return data, labels

# ข้อมูลตัวอย่างสำหรับ Pie Charts
percent_price_material = list(data.percent_price_material.values())
Category = list(data.percent_price_material.keys())

percent_invest = list(data.percent_invest.values())
invest = list(data.percent_invest.keys())

percent_total_cost = list(data.percent_total_cost.values())
cost = list(data.percent_total_cost.keys())

percent_sell = list(data.percent_sell.values())
sell = list(data.percent_sell.keys())

# กรอง data1 และ labels1 ให้ไม่รวมค่าที่เป็น 0
filtered_percent_material = []
filtered_Category = []

for i, value in enumerate(percent_price_material):
    if value != 0:  # ถ้า value ไม่เท่ากับ 0
        filtered_percent_material.append(value)  # เก็บค่าใน filtered_data1
        filtered_Category.append(Category[i])  # เก็บ labels ที่สอดคล้องกับค่าใน filtered_labels1

filtered_percent_invest = []
filtered_invest = []

for i, value in enumerate(percent_invest):
    if value != 0:  # ถ้า value ไม่เท่ากับ 0
        filtered_percent_invest.append(value)  # เก็บค่าใน filtered_data1
        filtered_invest.append(invest[i])  # เก็บ labels ที่สอดคล้องกับค่าใน filtered_labels1

filtered_percent_total_cost = []
filtered_cost = []
for i, value in enumerate(percent_total_cost):
    if value != 0:
        filtered_percent_total_cost.append(value)
        filtered_cost.append(cost[i])

filtered_percent_sell = []
filtered_sell = []

for i, value in enumerate(percent_sell):
    if value != 0:
        filtered_percent_sell.append(value)
        filtered_sell.append(sell[i])


# ปรับข้อมูลสำหรับ Pie Chart
adjusted_percent_material, adjusted_Category = adjust_for_missing_percentage(filtered_percent_material, filtered_Category)
adjusted_percent_invest, adjusted_invest = adjust_for_missing_percentage(filtered_percent_invest, filtered_invest)
adjusted_percent_total_cost, adjusted_cost = adjust_for_missing_percentage(filtered_percent_total_cost, filtered_cost)
adjusted_percent_sell, adjusted_sell = adjust_for_missing_percentage(filtered_percent_sell, filtered_sell)

# ฟังก์ชันเปิดหน้าต่างใหม่แสดงกราฟและสัดส่วน
def open_new_window(data, labels, title):
    new_window = Toplevel(root)
    new_window.title(f"รายละเอียด {title}")

    # สร้าง Pie Chart ในหน้าต่างใหม่
    fig = create_pie_chart(data, labels, title)
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # แสดงสัดส่วนในหน้าต่างใหม่
    for label, value in zip(labels, data):
        tk.Label(new_window, text=f'{label}: {value}').pack()

# สร้างหน้าต่าง Tkinter
root = tk.Tk()
root.title("หน้ารวม Donut Chart")
root.geometry("1920x1080")

# Donut Chart ที่ 1
fig1 = create_pie_chart(adjusted_percent_material, adjusted_Category, "Material Cost")
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.draw()
canvas1.get_tk_widget().grid(row=0, column=0)
canvas1.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(adjusted_percent_material, adjusted_Category, "Material Cost"))

# Donut Chart ที่ 2
fig2 = create_pie_chart(adjusted_percent_invest, adjusted_invest, "Invest Cost")
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.draw()
canvas2.get_tk_widget().grid(row=0, column=1)
canvas2.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(adjusted_percent_invest, adjusted_invest, "Invest Cost"))

# Donut Chart ที่ 3
fig3 = create_pie_chart(adjusted_percent_total_cost, adjusted_cost, "Cost Portion")
canvas3 = FigureCanvasTkAgg(fig3, master=root)
canvas3.draw()
canvas3.get_tk_widget().grid(row=0, column=2)
canvas3.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(adjusted_percent_total_cost, adjusted_cost, "Cost Portion"))

# Donut Chart ที่ 4
fig4 = create_pie_chart(adjusted_percent_sell, adjusted_sell, "Sell Portion")
canvas4 = FigureCanvasTkAgg(fig4, master=root)
canvas4.draw()
canvas4.get_tk_widget().grid(row=1, column=0)
canvas4.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(adjusted_percent_sell, adjusted_sell, "Sell Portion"))

# รันหน้าต่าง Tkinter
root.mainloop()
