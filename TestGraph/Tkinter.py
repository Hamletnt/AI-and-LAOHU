#tkinter

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# สร้าง GUI
root = tk.Tk()
root.title("หน้ารวม Pie Chart")

# ข้อมูลตัวอย่าง
labels = ['หมวด A', 'หมวด B', 'หมวด C', 'หมวด D']
sizes = [15, 30, 45, 10]

# สร้าง Pie Chart
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%')
ax.set_title('กราฟวงกลม')

# แสดงกราฟใน GUI
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

root.mainloop()