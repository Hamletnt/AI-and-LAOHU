import sys
from openpyxl import Workbook,load_workbook
import tkinter as tk
from tkinter import Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pulldataRowColumn as data

# ตั้งค่า encoding ให้เป็น utf-8
sys.stdout.reconfigure(encoding='utf-8')

# โหลดไฟล์ workbook และ worksheet
wb = load_workbook('Test/LProfitLoss24-Feb-.xlsx')
ws = wb.active

# ตั้งค่าฟอนต์ที่รองรับภาษาไทย เช่น Tahoma
rcParams['font.family'] = 'Tahoma'

# ฟังก์ชันในการสร้าง Pie Chart แต่ละอัน
def create_pie_chart(data, labels, title):
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%')
    ax.set_title(title)
    return fig

# ฟังก์ชันเปิดหน้าต่างใหม่แสดงกราฟและสัดส่วน
def open_new_window(data, labels, title):
    # สร้างหน้าต่างใหม่
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

# ข้อมูลตัวอย่างสำหรับ Pie Charts
percent_price_material = list(data.percent_price_material.values())  # ดึงค่าเปอร์เซ็นต์จาก dictionary
Category = list(data.percent_price_material.keys())  # ดึงชื่อคอลัมน์ (key) จาก dictionary

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

print(filtered_percent_total_cost)
# print(filtered_percent_sell)

# สร้างหน้าต่าง Tkinter
root = tk.Tk()
root.title("หน้ารวม Pie Chart")
root.geometry("1920x1080")

# Pie Chart ที่ 1
fig1 = create_pie_chart(filtered_percent_material, filtered_Category, "Material Cost")
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.draw()
canvas1.get_tk_widget().grid(row=0, column=0)
# เพิ่มการคลิกเพื่อเปิดหน้าต่างใหม่
canvas1.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(percent_price_material, Category, "Material Cost"))

# Pie Chart ที่ 2
fig2 = create_pie_chart(filtered_percent_invest, filtered_invest, "Invest Cost")
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.draw()
canvas2.get_tk_widget().grid(row=0, column=1)
canvas2.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(percent_invest, invest, "Invest Cost"))

# Pie Chart ที่ 3
fig3 = create_pie_chart(filtered_percent_total_cost, filtered_cost, "Cost Portion")
canvas3 = FigureCanvasTkAgg(fig3, master=root)
canvas3.draw()
canvas3.get_tk_widget().grid(row=0, column=2)
canvas3.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(percent_total_cost, cost, "Cost Portion"))

# Pie Chart ที่ 4
fig4 = create_pie_chart(filtered_percent_sell, filtered_sell, "Sell Portion")
canvas4 = FigureCanvasTkAgg(fig4, master=root)
canvas4.draw()
canvas4.get_tk_widget().grid(row=1, column=0)  # วางที่แถว 1 คอลัมน์ 0
canvas4.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(percent_sell, sell, "Sell Portion"))

# รันหน้าต่าง Tkinter
root.mainloop()