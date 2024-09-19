import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from TestFunction2 as data

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

def load_keywords():
    global categories
    categories = {}  # รีเซ็ตดิกชันนารีก่อน
    try:
        df = pd.read_excel(file_Cagetory)
        
        # อ่านคีย์เวิร์ดจากแต่ละประเภทหมวดหมู่
        for category, keyword_col in [('สถานที่', 'keyword 1'), 
                                      ('วัตถุดิบ', 'keyword 3'), 
                                      ('การดำเนินการ', 'keyword 2')]:
            if category in df.columns and keyword_col in df.columns: #เช็คว่าcategory และ keyword_col มีในexcel ที่จะอ่านไหม
                keyword_data = df[[category, keyword_col]].dropna() #ดึงค่าว่างออก
                for _, row in keyword_data.iterrows():
                    if pd.notna(row[keyword_col]):
                        keywords = [keyword.strip() for keyword in row[keyword_col].split(',')] #แยกkeyword ด้วย ,
                        categories[row[category]] = keywords #เพิ่มในdictionalry
    except Exception as e:
        tk.messagebox.showerror("Error", f"เกิดข้อผิดพลาดในการโหลดคีย์เวิร์ด: {e}")    
                
# ฟังก์ชัน Auto Filter สำหรับอัปเดตเฉพาะคอลัมน์หมวดหมู่
def auto_filter():
    load_keywords()  # โหลดคีย์เวิร์ดก่อน
    clear_data()
    file_path = label_file2["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if not file_path.endswith('.xlsx'):
            raise ValueError("Invalid file format")
        df = pd.read_excel(file_path, usecols=['ลำดับที่', 'วันที่', 'รายการ', 'รายรับ', 'รายจ่าย', 'คงเหลือ'])
    except FileNotFoundError:
        tk.messagebox.showerror("Error", f"No such file as {file_path}")
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
            df[col] = df[col].fillna("")

    # แทนที่ NaT ในคอลัมน์วันที่ด้วยข้อความ ""
    if "วันที่" in df.columns:
        df["วันที่"] = pd.to_datetime(df["วันที่"], errors='coerce').dt.strftime('%Y-%m-%d')
        df["วันที่"] = df["วันที่"].replace("NaT", "")

    # คำสั่งแทนที่ NaN ด้วยค่าว่าง
    df = df.fillna("")

    # เพิ่มคอลัมน์ "หมวดหมู่" โดยใช้ฟังก์ชัน categorize
    df['หมวดหมู่'] = df['รายการ'].apply(categorize)

    # แทรกคอลัมน์ "หมวดหมู่" ก่อน "รายรับ"
    df = df[['ลำดับที่', 'วันที่', 'รายการ', 'หมวดหมู่', 'รายรับ', 'รายจ่าย', 'คงเหลือ']]

    # แสดงข้อมูลใน Treeview
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["column"]:
        tv1.heading(column, text=column)
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
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("", "end", values=row)
    messagebox.showinfo("Info", "Auto Filter applied successfully.")    

# ฟังก์ชันเคลียร์ข้อมูลใน Treeview
def clear_data():
    tv1.delete(*tv1.get_children())   

# Create LabelFrame and place it
excel_data_frame1 = LabelFrame(window, text='Excel Data')
excel_data_frame1.place(x=50, y=100, height=540, width=760)
# Create Treeview and pack it into the frame
tv1 = ttk.Treeview(excel_data_frame1)
tv1.place(relheight=1, relwidth=1)                  