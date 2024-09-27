import sys
from openpyxl import Workbook, load_workbook
import tkinter as tk
from tkinter import Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pulldataRowColumn as data
import tkinter.ttk as ttk

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
    fig.subplots_adjust(left=0.03, right=0.9)  # ปรับขอบซ้ายและขวา

    colors = plt.get_cmap('tab20').colors  # ใช้ color map ที่มีสีให้เลือกมากมาย

    if 'ไม่เกี่ยว' in labels:
        idx = labels.index('ไม่เกี่ยว')
        colors = list(colors)  # แปลงเป็น list เพื่อปรับแต่งสี
        colors[idx] = '#ffffff'  # เปลี่ยนสี 'ไม่เกี่ยว' เป็นสีขาว

    wedges, texts, autotexts = ax.pie(data, wedgeprops=dict(width=1), startangle=-40, colors=colors[:len(labels)],
                                      radius=1, autopct='', pctdistance=0.75)

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        percent = (data[i] / sum(data)) * 100

        if labels[i] == 'ไม่เกี่ยว':
            continue

        if percent < 1.5:
            ax.annotate(f'{percent:.1f}%', xy=(x, y), xytext=(1.2 * x, 1.2 * y),
                        horizontalalignment=horizontalalignment,
                        arrowprops=dict(arrowstyle="-", connectionstyle=connectionstyle))
        else:
            ax.text(x * 0.85, y * 0.85, '{:.1f}%'.format(percent), ha='center', va='center', fontsize=8)

    ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
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
price_material_values = list(data.price_material.values())

percent_invest = list(data.percent_invest.values())
invest = list(data.percent_invest.keys())

percent_total_cost = list(data.percent_total_cost.values())
cost = list(data.percent_total_cost.keys())

percent_sell = list(data.percent_sell.values())
sell = list(data.percent_sell.keys())

# กรอง data1 และ labels1 ให้ไม่รวมค่าที่เป็น 0
filtered_percent_material = []
filtered_Category = []
filtered_price_material_values = []

for i, value in enumerate(percent_price_material):
    if value != 0:
        filtered_percent_material.append(value)
        filtered_Category.append(Category[i])

for i, value in enumerate(price_material_values):
    if value != 0:
        filtered_price_material_values.append(value)

filtered_percent_invest = []
filtered_invest = []

for i, value in enumerate(percent_invest):
    if value != 0:
        filtered_percent_invest.append(value)
        filtered_invest.append(invest[i])

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

# ฟังก์ชันเปิดหน้าต่างใหม่แสดงกราฟและสัดส่วนในรูปแบบตาราง
def open_new_window(data, labels, title):
    new_window = Toplevel(root)
    new_window.title(f"รายละเอียด {title}")

    fig = create_pie_chart(data, labels, title)
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    if title == "Material Cost":
        table = ttk.Treeview(new_window, columns=('Category', 'Value(baht)', 'Value(%)'), show='headings', height=len(data))
        table.pack(pady=10)

        table.heading('Category', text='Category')
        table.heading('Value(baht)', text='Value (baht)')
        table.heading('Value(%)', text='Value (%)')

        table.column('Category', width=200, anchor='w')
        table.column('Value(baht)', width=150, anchor='e')
        table.column('Value(%)', width=100, anchor='e')

        for label, value, price_material in zip(labels, data, filtered_price_material_values):
            table.insert('', 'end', values=(label, f'{price_material:.2f} baht', f'{value:.2f} %'))

    else:
        table = ttk.Treeview(new_window, columns=('Category', 'Value'), show='headings', height=len(data))
        table.pack(pady=10)

        table.heading('Category', text='Category')
        table.heading('Value', text='Value (%)')

        table.column('Category', width=200, anchor='w')
        table.column('Value', width=100, anchor='e')

        for label, value in zip(labels, data):
            table.insert('', 'end', values=(label, f'{value:.2f}'))

    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.configure("Treeview.Heading", font=('Arial', 13, 'bold'))
    style.configure("Treeview", font=('Arial', 13), borderwidth=1)
    style.map('Treeview', background=[('selected', '#d9d9d9')])

def create_table_profit(root, data, labels, title):
    table = ttk.Treeview(root, columns=('Category', 'Value'), show='headings', height=len(data))
    table.grid(row=1, column=1, padx=10, pady=(50, 10), sticky='n')

    table.heading('Category', text=title)
    table.heading('Value', text='Value')

    table.column('Category', width=450, anchor='w')
    table.column('Value', width=150, anchor='e')

    for i, (label, value) in enumerate(zip(labels, data)):
        if i < 5:
            table.insert('', 'end', values=(label, f'{value:.2f} baht'))
        elif i == 5:
            table.insert('', 'end', values=(label, f'{value:.2f} %'))
        else:
            table.insert('', 'end', values=(label, f'{value:.2f}'))

    style = ttk.Style()
    style.configure("Treeview", rowheight=30)
    style.configure("Treeview.Heading", font=('Arial', 13, 'bold'))
    style.configure("Treeview", font=('Arial', 13), borderwidth=1)
    style.map('Treeview', background=[('selected', '#d9d9d9')])

def create_table_sell(root, data, labels, title):
    table = ttk.Treeview(root, columns=('Category', 'Value'), show='headings', height=len(data))
    table.grid(row=1, column=1, padx=10, pady=(280, 5), sticky='n')

    table.heading('Category', text=title)
    table.heading('Value', text='Value')

    table.column('Category', width=450, anchor='w')
    table.column('Value', width=150, anchor='e')

    for i, (label, value) in enumerate(zip(labels, data)):
        if i == 0:
            table.insert('', 'end', values=(label, f'{value:.2f} day'))
        else:
            table.insert('', 'end', values=(label, f'{value:.2f}'))

    style = ttk.Style()
    style.configure("Treeview", rowheight=30)
    style.configure("Treeview.Heading", font=('Arial', 13, 'bold'))
    style.configure("Treeview", font=('Arial', 13), borderwidth=1)
    style.map('Treeview', background=[('selected', '#d9d9d9')])

# ฟังก์ชันในการสร้างและบันทึก PDF
def save_to_pdf():
    pdf_filename = "report.pdf"
    from matplotlib.backends.backend_pdf import PdfPages

    with PdfPages(pdf_filename) as pdf:
        # สร้าง Pie Charts และตาราง
        charts_and_tables = {
            "Material Cost": (adjusted_percent_material, adjusted_Category, "Material Cost"),
            "Invest Cost": (adjusted_percent_invest, adjusted_invest, "Invest Cost"),
            "Cost Portion": (adjusted_percent_total_cost, adjusted_cost, "Cost Portion"),
            "Sell Portion": (adjusted_percent_sell, adjusted_sell, "Sell Portion")
        }

        for title, (data, labels, chart_title) in charts_and_tables.items():
            fig = create_pie_chart(data, labels, chart_title)
            pdf.savefig(fig)  # บันทึก Pie Chart เป็น PDF

        # เพิ่มตารางลงใน PDF
        from matplotlib.table import Table
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_frame_on(False)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        table = Table(ax, bbox=[0, 0, 1, 1])
        ax.add_artist(table)

        # เพิ่มข้อมูลที่คุณต้องการไปยังตารางที่นี่
        # ...

        pdf.savefig(fig)  # บันทึกตารางเป็น PDF

root = tk.Tk()
root.title("Test Graph")

# ปุ่มเพื่อสร้างและบันทึก PDF
btn_save_pdf = tk.Button(root, text="Save to PDF", command=save_to_pdf)
btn_save_pdf.grid(row=0, column=0, padx=10, pady=10)

# สร้างปุ่มเพื่อเปิดหน้าต่างใหม่ที่มี Pie Chart
btn_open_new_window = tk.Button(root, text="Open Pie Chart", command=lambda: open_new_window(filtered_percent_material, filtered_Category, "Material Cost"))
btn_open_new_window.grid(row=0, column=1, padx=10, pady=10)

# สร้างตารางในหน้าหลัก
create_table_profit(root, filtered_percent_material, filtered_Category, "Material Cost")
create_table_sell(root, filtered_percent_sell, filtered_sell, "Sell Portion")

root.mainloop()
