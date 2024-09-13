import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox, ttk

window = tk.Tk()
window.title("LuoHu")
window.geometry("1200x700")

def upload_file():
    filename = filedialog.askopenfilename(initialdir="/", 
                                          title="Select A File",
                                          filetypes=[("Excel file", '*.xlsx')])
    if filename:
        label_file2["text"] = filename
    else:
        tk.messagebox.showwarning("Warning", "No file selected")
    return None   

def load_file():
    file_path = label_file2["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if not file_path.endswith('.xlsx'):
            raise ValueError("Invalid file format")
        df = pd.read_excel(file_path, usecols=[0,1,2,3,4,5]) #กำหนดคอลัมน์ที่จะให้อ่าน
    except ValueError:
        tk.messagebox.showerror("Error", "Your file is invalid. Please select an Excel (.xlsx) file.")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Error", f"No such file as {file_path}")
        return None
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {e}")
        return None

    #แปลงคอลัมน์ ลำดับที่ ให้ไม่มีทศนิยม
    if "ลำดับที่" in df.columns:
        df["ลำดับที่"] = pd.to_numeric(df["ลำดับที่"], errors='coerce').round(0) # แปลงคอลัมน์เป็นตัวเลข และปัดเศษทศนิยม
        df["ลำดับที่"] = df["ลำดับที่"].apply(lambda x: "" if pd.isna(x) or x == 0 else int(x)) # แทนค่าที่เป็น 0 ด้วยค่าว่าง
        
    # แปลงคอลัมน์ รายรับ รายจ่าย คงเหลือ ให้มีทศนิยม 2 ตำแหน่ง
    numeric_cols = ["รายรับ", "รายจ่าย", "คงเหลือ"]  # ระบุคอลัมน์ตัวเลข
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

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings" #แสดงเฉพาะส่วนของหัวคอลัมน์
    for column in tv1["column"]:
        tv1.heading(column, text=column)
        # ตั้งค่าความกว้างของแต่ละคอลัมน์
        if column == "ลำดับที่":
            tv1.column(column, width=50)
        elif column == "วันที่":
            tv1.column(column, width=100)
        elif column == "รายการ":
            tv1.column(column, width=250)
        elif column == "รายรับ":
            tv1.column(column, width=100)
        elif column == "รายจ่าย":
            tv1.column(column, width=100)
        elif column == "คงเหลือ":
            tv1.column(column, width=100)

    df_rows = df.to_numpy().tolist() #แปลงData ให้อยู่ในรูปแบบ List (แปลงเป็นArray แล้วแปลงเป็น Listต่อ)
    for row in df_rows: #ทำทุกแถว
        tv1.insert("","end", values=row) #แทรกdataเข้าไปใน Treeview
    return None
    
def clear_data():#ลบข้อมูลใน Treeview
    tv1.delete(*tv1.get_children()) 

def clear_file(): #ลบข้อมูลทั้งหมด
    if label_file2["text"] == "No file Selected" :
        tk.messagebox.showinfo("Warning", "No file to clear.")
    else :
        clear_data()
        label_file2["text"] = "No file Selected" #Reset ชื่อfile
        global df
        df = pd.DataFrame()
        #tk.messagebox.showinfo("Info", "File and data have been cleared.")

title_label = tk.Label(window, text='Import File', font = '15').pack()
browse_button = tk.Button(window, text ='Browse File',width = 10, command=lambda:upload_file()).place(x=500, y=40)
load_button = tk.Button(window, text ='Load File',width = 10, command=lambda:load_file()).place(x=600, y=40)
clear_button = tk.Button(window, text ='Clear File',width = 10, command=lambda:clear_file()).place(x=700, y=40)
auto_button = tk.Button(window, text ='Auto Filter',width = 10).place(x=700, y=620)

label_file1= tk.Label(window, text = "File Name --> ")
label_file1.place(x=500, y=80)
label_file2= tk.Label(window, text = "No file Selected")
label_file2.place(x=600, y=80)

# Create LabelFrame and place it
excel_data_frame1 = LabelFrame(window, text='Excel Data')
excel_data_frame1.place(x=50, y=100, height=500, width=730)
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

excel_data_frame2 = LabelFrame(window, text='การแยกหมวดหมู่')
excel_data_frame2.place(x=820, y=100, height=500, width=330)
tv2 = ttk.Treeview(excel_data_frame2)
tv2.place(relheight=1, relwidth=1)
# Add Scrollbars for Treeview
treescrolly2 = tk.Scrollbar(excel_data_frame2, orient="vertical", command=tv1.yview)
treescrollx2 = tk.Scrollbar(excel_data_frame2, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx1.set, yscrollcommand=treescrolly1.set)
#กำหนดตำแหน่ง Scrollbars
treescrolly2.pack(side="right", fill="y")
treescrollx2.pack(side="bottom", fill="x")

window.mainloop()
