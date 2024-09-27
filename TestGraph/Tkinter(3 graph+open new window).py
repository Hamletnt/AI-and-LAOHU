import tkinter as tk
from tkinter import Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib import rcParams

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
data1 = [15, 30, 45, 10]
labels1 = ['A', 'B', 'C', 'D']
data2 = [25, 35, 20, 20]
labels2 = ['E', 'F', 'G', 'H']
data3 = [10, 40, 30, 20]
labels3 = ['I', 'J', 'K', 'L']

# สร้างหน้าต่าง Tkinter
root = tk.Tk()
root.title("หน้ารวม Pie Chart")
root.geometry("1920x1080")

# Pie Chart ที่ 1
fig1 = create_pie_chart(data1, labels1, "กราฟที่ 1")
canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.draw()
canvas1.get_tk_widget().grid(row=0, column=0)
# เพิ่มการคลิกเพื่อเปิดหน้าต่างใหม่
canvas1.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(data1, labels1, "กราฟที่ 1"))

# Pie Chart ที่ 2
fig2 = create_pie_chart(data2, labels2, "กราฟที่ 2")
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.draw()
canvas2.get_tk_widget().grid(row=0, column=1)
canvas2.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(data2, labels2, "กราฟที่ 2"))

# Pie Chart ที่ 3
fig3 = create_pie_chart(data3, labels3, "กราฟที่ 3")
canvas3 = FigureCanvasTkAgg(fig3, master=root)
canvas3.draw()
canvas3.get_tk_widget().grid(row=0, column=2)
canvas3.get_tk_widget().bind("<Button-1>", lambda event: open_new_window(data3, labels3, "กราฟที่ 3"))

# รันหน้าต่าง Tkinter
root.mainloop()