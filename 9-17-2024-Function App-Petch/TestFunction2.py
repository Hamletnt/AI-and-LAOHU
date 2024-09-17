import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox, ttk

window = tk.Tk()
window.title("LuoHu")
window.geometry("1250x750")

# Dictionary สำหรับเก็บหมวดหมู่ที่ผู้ใช้เพิ่ม
categories = {}

# ฟังก์ชันสำหรับอัปโหลดไฟล์
def upload_file():
    filename = filedialog.askopenfilename(initialdir="/", 
                                          title="Select A File",
                                          filetypes=[("Excel file", '*.xlsx')])
    if filename:
        label_file2["text"] = filename
    else:
        tk.messagebox.showwarning("Warning", "No file selected")
    return None   

# ฟังก์ชันโหลดไฟล์และแสดงข้อมูลใน Treeview
def load_file():
    clear_data()  # ลบข้อมูลเก่าก่อนกรณีกด loadfile หลายรอบ
    file_path = label_file2["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if not file_path.endswith('.xlsx'):
            raise ValueError("Invalid file format")
        df = pd.read_excel(file_path, usecols=[0, 1, 2, 3, 4, 5])  # กำหนดคอลัมน์ที่จะให้อ่าน
    except ValueError:
        tk.messagebox.showerror("Error", "Your file is invalid. Please select an Excel (.xlsx) file.")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Error", f"No such file as {file_path}")
        return None
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {e}")
        return None

    # แปลงคอลัมน์ ลำดับที่ ให้ไม่มีทศนิยม
    if "ลำดับที่" in df.columns:
        df["ลำดับที่"] = pd.to_numeric(df["ลำดับที่"], errors='coerce').round(0)
        df["ลำดับที่"] = df["ลำดับที่"].apply(lambda x: "" if pd.isna(x) or x == 0 else int(x))

    # แปลงคอลัมน์ รายรับ รายจ่าย คงเหลือ ให้มีทศนิยม 2 ตำแหน่ง
    numeric_cols = ["รายรับ", "รายจ่าย", "คงเหลือ"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
            df[col] = df[col].fillna("")  # แทน NaN ในคอลัมน์ให้เป็นค่าว่าง

    # แทนที่ NaT ในคอลัมน์วันที่ด้วยข้อความ ""
    if "วันที่" in df.columns:
        df["วันที่"] = pd.to_datetime(df["วันที่"], errors='coerce').dt.strftime('%Y-%m-%d')
        df["วันที่"] = df["วันที่"].replace("NaT", "")  # แทนที่ NaT ด้วยค่าว่าง

    # คำสั่งแทนที่ NaN ด้วยค่าว่าง
    df = df.fillna("")

    # เพิ่มคอลัมน์ "หมวดหมู่" โดยใช้ฟังก์ชัน categorize
    df['หมวดหมู่'] = df['รายการ'].apply(categorize)

    # แทรกคอลัมน์ "หมวดหมู่" ก่อน "รายรับ"
    df = df[['ลำดับที่', 'วันที่', 'รายการ', 'หมวดหมู่', 'รายรับ', 'รายจ่าย', 'คงเหลือ']]

    # แสดงข้อมูลใน Treeview
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"  # แสดงคอลัมน์แรก
    for column in tv1["column"]:
        tv1.heading(column, text=column)
        # ตั้งค่าความกว้างของแต่ละคอลัมน์
        if column == "ลำดับที่":
            tv1.column(column, width=45)
        elif column == "วันที่":
            tv1.column(column, width=100)
        elif column == "รายการ":
            tv1.column(column, width=250)
        elif column == "หมวดหมู่":
            tv1.column(column, width=90)
        elif column == "รายรับ":
            tv1.column(column, width=90)
        elif column == "รายจ่าย":
            tv1.column(column, width=90)
        elif column == "คงเหลือ":
            tv1.column(column, width=90)
    df_rows = df.to_numpy().tolist()  # แปลงData ให้อยู่ในรูปแบบ List
    for row in df_rows:
        tv1.insert("", "end", values=row)  # แทรกdataเข้าไปใน Treeview1
    return None

# ฟังก์ชันเคลียร์ข้อมูลใน Treeview
def clear_data():
    tv1.delete(*tv1.get_children()) 

# ฟังก์ชันเคลียร์ข้อมูลทั้งหมด
def clear_file():
    if label_file2["text"] == "No file Selected":
        tk.messagebox.showinfo("Warning", "No file to clear.")
    else:
        clear_data()
        label_file2["text"] = "No file Selected"
        global df
        df = pd.DataFrame()

# ฟังก์ชันสำหรับการเพิ่มหมวดหมู่ใหม่ใน popup window
def add_category_popup():
    def add_category():
        category_name = category_entry.get()
        keyword_list = keyword_text.get("1.0", "end-1c").split(",")  # รับข้อมูลจาก Text widget และแยกคำด้วยจุลภาค
        if category_name and keyword_list:
            categories[category_name] = keyword_list  # เพิ่มหมวดหมู่และคำสำคัญใน dictionary
            
            category_types = type_menu.get()  # ดึงประเภทหมวดหมู่จาก Combobox
            if category_types == "วัตถุดิบ":
                tv3.insert("", "end", values=(category_name, "N/A", "N/A"))  # เพิ่มข้อมูลใน Treeview วัตถุดิบ
            elif category_types == "สถานที่":
                tv2.insert("", "end", values=(category_name, "N/A", "N/A"))  # เพิ่มข้อมูลใน Treeview สถานที่
            elif category_types == "การดำเนินการ":
                tv4.insert("", "end", values=(category_name, "N/A", "N/A"))  # เพิ่มข้อมูลใน Treeview การดำเนินการ

            popup.destroy()  # ปิดหน้าต่าง popup หลังจากเพิ่มหมวดหมู่
        else:
            messagebox.showwarning("Warning", "Please enter both category name and keywords.")

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

# ฟังก์ชันแยกหมวดหมู่ตามคำสำคัญที่ผู้ใช้ป้อน
def categorize(item):
    for category, items in categories.items():
        if any(keyword.strip() in item for keyword in items):
            return category
    return 'อื่น ๆ'

# ฟังก์ชัน Auto Filter สำหรับใช้หมวดหมู่กับรายการ
def auto_filter():
    df['หมวดหมู่'] = df['รายการ'].apply(categorize)
    clear_data()  # ลบข้อมูลเก่าออกก่อนแสดงใหม่
    df_rows = df.to_numpy().tolist()  # แปลง DataFrame เป็น list
    for row in df_rows:
        tv1.insert("", "end", values=row)
    messagebox.showinfo("Info", "Categories have been applied successfully.")

# ส่วน UI ของโปรแกรม
title_label = tk.Label(window, text='Import File', font = '15').pack()
browse_button = tk.Button(window, text ='Browse File', width = 10, command=upload_file).place(x=500, y=40)
load_button = tk.Button(window, text ='Load File', width = 10, command=load_file).place(x=600, y=40)
clear_button = tk.Button(window, text ='Clear File', width = 10, command=clear_file).place(x=700, y=40)
add_button = tk.Button(window, text ='Add Category ', width=12, command=add_category_popup).place(x=800, y=40)
auto_button = tk.Button(window, text ='Auto Filter', width=10, command=auto_filter).place(x=600, y=660)
submit_button = tk.Button(window, text ='Submit', width=10).place(x=700, y=660)

label_file1= tk.Label(window, text = "File Name --> ")
label_file1.place(x=500, y=80)
label_file2= tk.Label(window, text = "No file Selected")
label_file2.place(x=600, y=80)

# Create LabelFrame and place it
excel_data_frame1 = LabelFrame(window, text='Excel Data')
excel_data_frame1.place(x=50, y=100, height=540, width=760)
# Create Treeview and pack it into the frame
tv1 = ttk.Treeview(excel_data_frame1)
tv1.place(relheight=1, relwidth=1)
# Add Scrollbars for Treeview
treescrolly1 = tk.Scrollbar(excel_data_frame1, orient="vertical", command=tv1.yview)
treescrollx1 = tk.Scrollbar(excel_data_frame1, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx1.set, yscrollcommand=treescrolly1.set)
#กำหนดตำแหน่ง Scrollbars
treescrolly1.pack(side="right", fill="y")
treescrollx1.pack(side="bottom", fill="x")

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

for tv in [tv2, tv3, tv4]:
    tv["column"] = ("รายการ", "Coat", "%")
    tv["show"] = "headings"
    for column in tv["column"]:
        tv.heading(column, text=column)
        tv.column(column, width=100)

window.mainloop()
