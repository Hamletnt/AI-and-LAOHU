import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ฟังก์ชันในการสร้าง Pie Chart แต่ละอัน
def create_pie_chart(data, labels, title):
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%')
    ax.set_title(title)
    return fig

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

# Pie Chart ที่ 1
fig1 = create_pie_chart(data1, labels1, "กราฟที่ 1")
canvas1 = FigureCanvasTkAgg(fig1, master=root)  # ฝังกราฟใน Tkinter
canvas1.draw()
canvas1.get_tk_widget().grid(row=0, column=0)  # จัดวางตำแหน่งกราฟ

# Pie Chart ที่ 2
fig2 = create_pie_chart(data2, labels2, "กราฟที่ 2")
canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.draw()
canvas2.get_tk_widget().grid(row=0, column=1)

# Pie Chart ที่ 3
fig3 = create_pie_chart(data3, labels3, "กราฟที่ 3")
canvas3 = FigureCanvasTkAgg(fig3, master=root)
canvas3.draw()
canvas3.get_tk_widget().grid(row=0, column=2)

# รันหน้าต่าง Tkinter
root.mainloop()
