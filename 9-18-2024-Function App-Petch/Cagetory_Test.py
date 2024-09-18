import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox, ttk 
import xlsxwriter

window = tk.Tk()
window.title("LuoHu")
window.geometry("1250x750")

file_Cagetory = 'Cagetory_Test.xlsx'
# Dictionary สำหรับเก็บหมวดหมู่ที่ผู้ใช้เพิ่ม
categories = {}

def location_tv2():
    df = pd.read_excel(file_Cagetory, usecols=['สถานที่'])
    df = df.fillna('')
    df_rows = df.to_numpy().tolist()  # แปลงData ให้อยู่ในรูปแบบ List
    for row in df_rows: #ทำทุกแถว
        if any(row):
            tv2.insert("","end", values=(row,"")) 

def ingredients_tv3():
    df = pd.read_excel(file_Cagetory, usecols=['วัตถุดิบ'])
    df = df.fillna('')
    df_rows = df.to_numpy().tolist()  # แปลงData ให้อยู่ในรูปแบบ List
    for row in df_rows: #ทำทุกแถว
        if any(row):
            tv3.insert("","end", values=(row,"")) 

def Manage_tv4():
    df = pd.read_excel(file_Cagetory, usecols=['การดำเนินการ'])
    df = df.fillna('')
    df_rows = df.to_numpy().tolist()  # แปลงData ให้อยู่ในรูปแบบ List
    for row in df_rows: #ทำทุกแถว
        if any(row):
            tv4.insert("","end", values=(row,"")) 

def add_category_popup():
    def add_category():
        category_name = category_entry.get()
        keyword_list = keyword_text.get("1.0", "end-1c").split(",")  # รับข้อมูลจาก Text widget และแยกคำด้วยจุลภาค
        category_types = type_menu.get()  # ดึงประเภทหมวดหมู่จาก Combobox

        if category_name and keyword_list:
            # อัปเดตไฟล์ Excel
            try:
                df = pd.read_excel(file_Cagetory)

                # ตรวจสอบว่าประเภทหมวดหมู่คืออะไร และอัปเดตในคอลัมน์ที่เกี่ยวข้อง
                if category_types == "สถานที่":
                    new_row = pd.DataFrame({'สถานที่': [category_name], 'keyword 1': [', '.join(keyword_list)]})
                    df = pd.concat([df, new_row], ignore_index=True)  # เพิ่มแถวใหม่
                    tv2.insert("", "end", values=(category_name, "", ""))  # เพิ่มข้อมูลใน Treeview สถานที่
                elif category_types == "วัตถุดิบ":
                    new_row = pd.DataFrame({'วัตถุดิบ': [category_name], 'keyword 3': [', '.join(keyword_list)]})
                    df = pd.concat([df, new_row], ignore_index=True)  # เพิ่มแถวใหม่
                    tv3.insert("", "end", values=(category_name, "", ""))  # เพิ่มข้อมูลใน Treeview วัตถุดิบ
                elif category_types == "การดำเนินการ":
                    new_row = pd.DataFrame({'การดำเนินการ': [category_name], 'keyword 2': [', '.join(keyword_list)]})
                    df = pd.concat([df, new_row], ignore_index=True)  # เพิ่มแถวใหม่
                    tv4.insert("", "end", values=(category_name, "", ""))  # เพิ่มข้อมูลใน Treeview การดำเนินการ

                # บันทึกการเปลี่ยนแปลงลงในไฟล์ Excel
                df.to_excel(file_Cagetory, index=False)
                messagebox.showinfo("Success", "หมวดหมู่และคำสำคัญถูกเพิ่มลงใน Excel และแสดงใน Treeview แล้ว.")
            except Exception as e:
             messagebox.showerror("Error", f"เกิดข้อผิดพลาดในการอัปเดต Excel: {e}")

            popup.destroy()  # ปิดหน้าต่าง popup หลังจากเพิ่มหมวดหมู่
        else:
            messagebox.showwarning("Warning", "กรุณาใส่ชื่อหมวดหมู่และคำสำคัญ.")

    # สร้าง popup window
    popup = Toplevel()
    popup.title("Add Category")
    popup.geometry("360x250")

    category_types = ["วัตถุดิบ", "สถานที่", "การดำเนินการ"]  # ตัวอย่างประเภทหมวดหมู่

    # อินพุตสำหรับเลือกประเภทหมวดหมู่
    category_label = Label(popup, text="การเพิ่มหมวดหมู่")
    category_label.place(x=30, y=15)
    category_label1 = Label(popup, text="ประเภทของหมวดหมู่ :")
    category_label1.place(x=30, y=50)
    type_menu = ttk.Combobox(popup,values=category_types,width=12, state="readonly")
    #type_menu.set(category_types[0])  # ตั้งค่าเริ่มต้น
    type_menu.place(x=138, y=48)

    # อินพุตสำหรับชื่อหมวดหมู่
    category_label2 = Label(popup, text="ชื่อหมวดหมู่ :")
    category_label2.place(x=30, y=85)
    category_entry = Entry(popup, width=35)
    category_entry.place(x=100, y=85)

    # อินพุตสำหรับคำสำคัญ
    keyword_label = Label(popup, text="Keyword (คั่นด้วย ',') :")
    keyword_label.place(x=30, y=120)
    keyword_text = Text(popup, height=4, width=20)  # Text widget รองรับหลายบรรทัด
    keyword_text.place(x=150, y=120)

    # ปุ่มเพิ่มหมวดหมู่
    add_button = Button(popup, text="เพิ่มหมวดหมู่", command=add_category)
    add_button.place(x=245, y=200)

excel_data_frame2 = LabelFrame(window, text='สถานที่')
excel_data_frame2.place(x=850, y=100, height=250, width=300)
tv2 = ttk.Treeview(excel_data_frame2)
tv2.place(relheight=1, relwidth=1)
treescrolly2 = tk.Scrollbar(excel_data_frame2, orient="vertical", command=tv2.yview)
treescrollx2 = tk.Scrollbar(excel_data_frame2, orient="horizontal", command=tv2.xview)
tv2.configure(xscrollcommand=treescrollx2.set, yscrollcommand=treescrolly2.set)
treescrolly2.pack(side="right", fill="y")
treescrollx2.pack(side="bottom", fill="x")

excel_data_frame3 = LabelFrame(window, text='วัตถุดิบ')
excel_data_frame3.place(x=1170, y=100, height=350, width=300)
tv3 = ttk.Treeview(excel_data_frame3)
tv3.place(relheight=1, relwidth=1)
treescrolly3 = tk.Scrollbar(excel_data_frame3, orient="vertical", command=tv3.yview)
treescrollx3 = tk.Scrollbar(excel_data_frame3, orient="horizontal", command=tv3.xview)
tv3.configure(xscrollcommand=treescrollx3.set, yscrollcommand=treescrolly3.set)
treescrolly3.pack(side="right", fill="y")
treescrollx3.pack(side="bottom", fill="x")

excel_data_frame4 = LabelFrame(window, text='การดำเนินการ')
excel_data_frame4.place(x=850, y=370, height=270, width=300)
tv4 = ttk.Treeview(excel_data_frame4)
tv4.place(relheight=1, relwidth=1)
treescrolly4 = tk.Scrollbar(excel_data_frame4, orient="vertical", command=tv4.yview)
treescrollx4 = tk.Scrollbar(excel_data_frame4, orient="horizontal", command=tv4.xview)
tv4.configure(xscrollcommand=treescrollx4.set, yscrollcommand=treescrolly4.set)
treescrolly4.pack(side="right", fill="y")
treescrollx4.pack(side="bottom", fill="x")

add_button = tk.Button(window, text ='Add Category ', width=12, command=add_category_popup).place(x=800, y=40)

for tv in [tv2, tv3, tv4]:
    tv["column"] = ("รายการ", "Coat", "%")
    tv["show"] = "headings"
    for column in tv["column"]:
        tv.heading(column, text=column)
        tv.column(column, width=100)

ingredients_tv3()
location_tv2()
Manage_tv4()

window.mainloop()






