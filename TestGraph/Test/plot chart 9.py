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

    # ใช้สี default จาก matplotlib
    colors = plt.get_cmap('tab20').colors  # ใช้ color map ที่มีสีให้เลือกมากมาย

    # ถ้ามี 'ไม่เกี่ยว' ใน labels ให้ทำให้เป็นสีขาว
    if 'ไม่เกี่ยว' in labels:
        idx = labels.index('ไม่เกี่ยว')
        colors = list(colors)  # แปลงเป็น list เพื่อปรับแต่งสี
        colors[idx] = '#ffffff'  # เปลี่ยนสี 'ไม่เกี่ยว' เป็นสีขาว
        

    # สร้าง Donut Chart โดยใช้ width=0.5 เพื่อทำให้เป็น donut chart
    wedges, texts, autotexts = ax.pie(data, wedgeprops=dict(width=1), startangle=-40, colors=colors[:len(labels)],
                                      radius=1,autopct='', pctdistance=0.75)

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]  # จัดการข้อความทางซ้าย/ขวา
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)  # สไตล์การเชื่อมต่อเส้นชี้
        percent = (data[i] / sum(data)) * 100

        if labels[i] == 'ไม่เกี่ยว':
            continue  # ไม่ต้องแสดงเปอร์เซ็นต์สำหรับ 'ไม่เกี่ยว'

        if percent < 1.5:
            # กรณีเปอร์เซ็นต์น้อยกว่า 1.5% ให้มีการแสดงเส้นชี้และข้อความปกติ
            ax.annotate(f'{percent:.1f}%', xy=(x, y), xytext=(1.2 * x, 1.2 * y),
                        horizontalalignment=horizontalalignment,
                        arrowprops=dict(arrowstyle="-", connectionstyle=connectionstyle))
        else:
            # แสดงเปอร์เซ็นต์ที่กึ่งกลาง wedge
            ax.text(x * 0.85, y * 0.85, '{:.1f}%'.format(percent), ha='center', va='center', fontsize=8)

    # เพิ่ม legend สำหรับ labels และแสดง title
    ax.legend(wedges, labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),fontsize = 8) #(x,y,)
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
    if value != 0:  # ถ้า value ไม่เท่ากับ 0
        filtered_percent_material.append(value)  # เก็บค่าใน filtered_data1
        filtered_Category.append(Category[i])  # เก็บ labels ที่สอดคล้องกับค่าใน filtered_labels1

for i, value in enumerate(price_material_values):
    if value != 0:  # ถ้า value ไม่เท่ากับ 0
        filtered_price_material_values.append(value)

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


# ฟังก์ชันเปิดหน้าต่างใหม่แสดงกราฟและสัดส่วนในรูปแบบตาราง
def open_new_window(data, labels, title):
    new_window = Toplevel(root)
    new_window.title(f"รายละเอียด {title}")

    # สร้าง Pie Chart ในหน้าต่างใหม่
    fig = create_pie_chart(data, labels, title)
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # ตรวจสอบว่าถ้า title เป็น "Material Cost"
    if title == "Material Cost":
        # สร้าง Treeview สำหรับตารางที่มี 3 คอลัมน์
        table = ttk.Treeview(new_window, columns=('Category', 'Value(baht)', 'Value(%)'), show='headings', height=len(data))
        table.pack(pady=10)  # เพิ่มช่องว่างด้านบนของตาราง

        # กำหนดหัวตาราง
        table.heading('Category', text='Category')
        table.heading('Value(baht)', text='Value (baht)')
        table.heading('Value(%)', text='Value (%)')

        # กำหนดขนาดของแต่ละคอลัมน์
        table.column('Category', width=200, anchor='w')
        table.column('Value(baht)', width=150, anchor='e')
        table.column('Value(%)', width=100, anchor='e')

        # เพิ่มข้อมูลลงในตาราง
        for label, value, price_material in zip(labels, data, filtered_price_material_values):
            table.insert('', 'end', values=(label, f'{price_material:.2f} baht', f'{value:.2f} %'))

    else:
        # สร้าง Treeview สำหรับตารางที่มี 2 คอลัมน์ปกติ
        table = ttk.Treeview(new_window, columns=('Category', 'Value'), show='headings', height=len(data))
        table.pack(pady=10)  # เพิ่มช่องว่างด้านบนของตาราง

        # กำหนดหัวตาราง
        table.heading('Category', text='Category')
        table.heading('Value', text='Value (%)')

        # กำหนดขนาดของแต่ละคอลัมน์
        table.column('Category', width=200, anchor='w')
        table.column('Value', width=100, anchor='e')

        # เพิ่มข้อมูลลงในตาราง
        for label, value in zip(labels, data):
            table.insert('', 'end', values=(label, f'{value:.2f}'))

    # เพิ่มสไตล์ของเส้นตารางให้เหมือน Excel
    style = ttk.Style()
    style.configure("Treeview", rowheight=25)
    style.configure("Treeview.Heading", font=('Arial', 13, 'bold'))
    style.configure("Treeview", font=('Arial', 13), borderwidth=1)
    style.map('Treeview', background=[('selected', '#d9d9d9')])


def create_table_profit(root, data, labels, title):
    # สร้าง Treeview สำหรับตาราง profit
    table = ttk.Treeview(root, columns=('Category', 'Value'), show='headings', height=len(data))
    table.grid(row=1, column=1, padx=10, pady=(50, 10), sticky='n')  # กำหนด pady ให้มีระยะห่างด้านล่าง 50px
    
    # กำหนดหัวตาราง
    table.heading('Category', text=title)
    table.heading('Value', text='Value')

    # กำหนดขนาดของแต่ละคอลัมน์
    table.column('Category', width=450, anchor='w')
    table.column('Value', width=150, anchor='e')

    # เพิ่มข้อมูลลงในตาราง
    for i, (label, value) in enumerate(zip(labels, data)):
        if i < 5:
            table.insert('', 'end', values=(label, f'{value:.2f} baht'))
        elif i == 5:
            table.insert('', 'end', values=(label, f'{value:.2f} %'))
        else:
            table.insert('', 'end', values=(label, f'{value:.2f}'))

    # เพิ่มสไตล์ของเส้นตาราง
    style = ttk.Style()
    style.configure("Treeview", rowheight=30)
    style.configure("Treeview.Heading", font=('Arial', 13, 'bold'))
    style.configure("Treeview", font=('Arial', 13), borderwidth=1)
    style.map('Treeview', background=[('selected', '#d9d9d9')])

def create_table_sell(root, data, labels, title):
    # สร้าง Treeview สำหรับตาราง sell
    table = ttk.Treeview(root, columns=('Category', 'Value'), show='headings', height=len(data))
    table.grid(row=1, column=1, padx=10, pady=(280, 5), sticky='n')  # วางไว้ใต้ตาราง profit และกำหนด pady ด้านบน 50px
    
    # กำหนดหัวตาราง
    table.heading('Category', text=title)
    table.heading('Value', text='Value')

    # กำหนดขนาดของแต่ละคอลัมน์
    table.column('Category', width=450, anchor='w')
    table.column('Value', width=150, anchor='e')

    # เพิ่มข้อมูลลงในตาราง
    for i, (label, value) in enumerate(zip(labels, data)):
        if i == 0:
            table.insert('', 'end', values=(label, f'{value:.2f} day'))
        elif i > 0 and i <= 2:
            table.insert('', 'end', values=(label, f'{value:.2f} baht'))
        elif i == 3:
            table.insert('', 'end', values=(label, f'{value:.2f} คน'))
        else:
            table.insert('', 'end', values=(label, f'{value:.2f}'))

    # เพิ่มสไตล์ของเส้นตาราง
    style = ttk.Style()
    style.configure("Treeview", rowheight=30)
    style.configure("Treeview.Heading", font=('Arial', 13, 'bold'))
    style.configure("Treeview", font=('Arial', 13), borderwidth=1)
    style.map('Treeview', background=[('selected', '#d9d9d9')])

# สร้างหน้าต่าง Tkinter
root = tk.Tk()
root.title("หน้ารวม Donut Chart")

# ทำให้หน้าต่างขยายเต็มหน้าจอแบบ maximized
root.state('zoomed')

# ฟังก์ชันในการปรับความกว้างและความสูงของแต่ละกราฟให้เป็น 1/3 ของความกว้าง และครึ่งหนึ่งของความสูงหน้าจอ
def resize_canvases(root, canvas_list):
    root.update_idletasks()  # อัพเดตข้อมูลขนาดหน้าจอ
    screen_width = root.winfo_width()  # ดึงความกว้างของหน้าต่าง root
    screen_height = root.winfo_height()  # ดึงความสูงของหน้าต่าง root
    canvas_width = screen_width // 3  # กำหนดความกว้างให้เท่ากับ 1/3 ของหน้าต่าง root
    canvas_height = screen_height // 2  # กำหนดความสูงให้เท่ากับครึ่งหนึ่งของหน้าต่าง root

    for canvas in canvas_list:
        canvas.get_tk_widget().config(width=canvas_width, height=canvas_height)

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

# ตาราง profit ที่ row 1 column 1 (ใต้ Donut Chart ที่ 4)
create_table_profit(root, list(data.profit.values()), list(data.profit.keys()), f"Profit {data.month.year}{data.month.strftime("%b")}")

# ตาราง sell ใต้ ตาราง profit
create_table_sell(root, list(data.sell.values()), list(data.sell.keys()), f"Sell {data.month.year}{data.month.strftime("%b")}")

# รันฟังก์ชันปรับขนาดเมื่อหน้าต่าง root ถูกปรับขนาด (รวมตารางในรายการ)
root.bind("<Configure>", lambda event: resize_canvases(root, [canvas1, canvas2, canvas3, canvas4]))


# รันหน้าต่าง Tkinter
root.mainloop()
