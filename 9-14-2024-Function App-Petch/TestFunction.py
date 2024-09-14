import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox, ttk

window = tk.Tk()
window.title("LuoHu")
window.geometry("1250x720")

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
    clear_data() #ลบข้อมูลเก่าก่อนกรณีกด loadfile หลายรอบ
    file_path = label_file2["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if not file_path.endswith('.xlsx'):
            raise ValueError("Invalid file format")
        df = pd.read_excel(file_path, usecols=['ลำดับที่', 'วันที่', 'รายการ', 'รายรับ', 'รายจ่าย', 'คงเหลือ']) #กำหนดคอลัมน์ที่จะให้อ่าน
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

    # เพิ่มคอลัมน์ "หมวดหมู่" ระหว่าง "รายการ" และ "รายรับ"
    keyword = {
        #วัตถุดิบ
        'วัตถุดิบอื่นๆ': ['ข้าวญี่ปุ่น','ฟาร์มเฟรช','แมคโคร','อาซัน','พริกผัด','กลิ่นทรัฟเฟิล','น้ำมันทรัฟเฟิล','asan','ฉั่วฮะเส็ง'],
        'หมู': ['หมูเบทราโกร','หมูหัวไหล่'],
        'ไก่,ไข่': ['ไข่','อกไก่เบทราโกร'],
        'เนื้อ': ['เนื้อนัยนา','เนื้อโชคอาลี'],
        'FarmF+สุรพล': [],
        'ลูกชิ้น': ['ลูกชิ้น'],
        'กุ้ง': ['กุ้ง'],
        'ผัก': ['ผัก'],
        'น้ำ': ['pepsi'],
        'ไอติม': ['ete'],
        'ขนมจีบซาลาเปา': ['ซาลาเปา','seatech','ขนมจีบ'],
        'ของหวาน': ['น้ำดอกไม้สุก','ข้าวเหนียวมูล'],
        'ผลไม้': ['แก้วขมิ้น','ลูกชิด'],

        #สถาที่
        'ปรับปรุง': ['ปรับปรุง'],
        'ไฟฟ้า': ['ไฟฟ้า'],
        'ประปา': ['ประปา'],
        'Air': ['Air'],
        'ปลวก': ['ปลวก'],
        'สถาบัน': ['สถาบัน','ค่าเช่า'],
        'Fur': ['Fur'],
        'อุปกรณ์': ['อุปกรณ์','ค่ามือถือเครื่องใหม่','Deep fryer'],

        #การดำเนินการ
        'อุปกรณ์ใช้สอย': ['อุปกรณ์ใช้สอย'],
        'วัสดุสิ้นเปลือง': ['วัสดุสิ้นเปลือง',],
        'ค่าใช้สอย': ['ค่าใช้สอย','ค่าเช่าเครื่องล้างจาน'],
        'PR': ['PR'],
        'ค่าไฟ': ['ค่าไฟ'],
        'ค่าแรง': ['ค่าแรง'],
        'Part time': ['Part time'],
        'สวัสดิการ': ['สวัสดิการ','เสื้อตรุษจีน','Deep fryer'],
        'Manage': ['Manage','tax'],
    }

    # ฟังก์ชันแยกหมวดหมู่ โดยตรวจสอบเฉพาะช่องที่เป็น "รายจ่าย"
    def categorize_item(item, expense, income, keyword):
        if pd.notna(expense) and expense != 0:
            for category, items in keyword.items():
                if any(i in item for i in items):
                    return category
        elif pd.notna(income) and income != 0:
            for category, items in keyword.items():
                if any(i in item for i in items):
                    return "รายรับอื่นๆ"
        return ""  # ถ้าไม่มีค่าในรายจ่ายหรือไม่พบหมวดหมู่ ให้คืนค่าว่าง

    # การเรียกใช้งานฟังก์ชัน categorize_item
    df['หมวดหมู่'] = df.apply(lambda row: categorize_item(row['รายการ'], row['รายจ่าย'], row['รายรับ'], keyword), axis=1)
    
    # แทรกคอลัมน์ "หมวดหมู่" ก่อน "รายรับ"
    df = df[['ลำดับที่', 'วันที่', 'รายการ', 'หมวดหมู่', 'รายรับ', 'รายจ่าย', 'คงเหลือ']]

    tv1["column"] = list(df.columns)
    tv1["show"] = "headings" #แสดงคอลัมน์แรก
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

    df_rows = df.to_numpy().tolist() #แปลงData ให้อยู่ในรูปแบบ List (แปลงเป็นArray แล้วแปลงเป็น Listต่อ)
    for row in df_rows: #ทำทุกแถว
        tv1.insert("","end", values=row) #แทรกdataเข้าไปใน Treeview1
    return None
    
def clear_data():#ลบข้อมูลใน Treeview1
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

def category2_frame():
    category2 = ["ปรับปรุง","ไฟฟ้า","ประปา","Air","ปลวก","สถาบัน","Fur","อุปกรณ์","รวม"]
    tv2["column"]=('column1','column2','column3')
    tv2["show"] = "headings"
    tv2.heading('column1',text = 'รายการ')
    tv2.heading('column2',text = 'Coat')
    tv2.heading('column3',text = '%')
    tv2.column('column1', width=90)  
    tv2.column('column2', width=100)
    tv2.column('column3', width=100)

    #tv2.insert("","end", values=location_category)    
    for row in category2: #ทำทุกแถว
        tv2.insert("","end", values=(row,""))

def category3_frame():
    category3 = ["วัตถุดิบอื่นๆ","หมู","ไก่,ไข่","เนื้อ","FarmF+สุรพล","ลูกชิ้น","กุ้ง","ผัก","น้ำ","ไอติม","ขนมจีบซาลาเปา","ของหวาน","ผลไม้","รวม"]
    tv3["column"]=('column1','column2','column3')
    tv3["show"] = "headings"
    tv3.heading('column1',text = 'รายการ')
    tv3.heading('column2',text = 'Coat')
    tv3.heading('column3',text = '%')
    tv3.column('column1', width=90)  
    tv3.column('column2', width=100)
    tv3.column('column3', width=100)

    #tv2.insert("","end", values=location_category)    
    for row in category3: #ทำทุกแถว
        tv3.insert("","end", values=(row,"")) 

def category4_frame():
    category4 = ["อุปกรณ์ใช้สอย","วัสดุสิ้นเปลือง","ค่าใช้สอย","PR","ค่าไฟ","ค่าแรง","Part time","สวัสดิการ","Manage","รวม"]
    tv4["column"]=('column1','column2','column3')
    tv4["show"] = "headings"
    tv4.heading('column1',text = 'รายการ')
    tv4.heading('column2',text = 'Coat')
    tv4.heading('column3',text = '%')
    tv4.column('column1', width=90)  
    tv4.column('column2', width=100)
    tv4.column('column3', width=100)

    #tv2.insert("","end", values=location_category)    
    for row in category4: #ทำทุกแถว
        tv4.insert("","end", values=(row,""))  
    
    

title_label = tk.Label(window, text='Import File', font = '15').pack()
browse_button = tk.Button(window, text ='Browse File',width = 10, command=lambda:upload_file()).place(x=500, y=40)
load_button = tk.Button(window, text ='Load File',width = 10, command=lambda:load_file()).place(x=600, y=40)
clear_button = tk.Button(window, text ='Clear File',width = 10, command=lambda:clear_file()).place(x=700, y=40)
auto_button = tk.Button(window, text ='Auto Filter',width = 10).place(x=600, y=660)
submit_button = tk.Button(window, text ='Submit',width = 10).place(x=700, y=660)

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

excel_data_frame2 = LabelFrame(window, text='หมวดหมู่สถานที่')
excel_data_frame2.place(x=850, y=100, height=250, width=300)
tv2 = ttk.Treeview(excel_data_frame2)
tv2.place(relheight=1, relwidth=1)
treescrolly2 = tk.Scrollbar(excel_data_frame2, orient="vertical", command=tv2.yview)
treescrollx2 = tk.Scrollbar(excel_data_frame2, orient="horizontal", command=tv2.xview)
tv2.configure(xscrollcommand=treescrollx2.set, yscrollcommand=treescrolly2.set)
treescrolly2.pack(side="right", fill="y")
treescrollx2.pack(side="bottom", fill="x")
category2_frame()

excel_data_frame3 = LabelFrame(window, text='หมวดหมู่วัตถุดิบ')
excel_data_frame3.place(x=1170, y=100, height=350, width=300)
tv3 = ttk.Treeview(excel_data_frame3)
tv3.place(relheight=1, relwidth=1)
treescrolly3 = tk.Scrollbar(excel_data_frame3, orient="vertical", command=tv3.yview)
treescrollx3 = tk.Scrollbar(excel_data_frame3, orient="horizontal", command=tv3.xview)
tv3.configure(xscrollcommand=treescrollx3.set, yscrollcommand=treescrolly3.set)
treescrolly3.pack(side="right", fill="y")
treescrollx3.pack(side="bottom", fill="x")
category3_frame()

excel_data_frame4 = LabelFrame(window, text='หมวดหมู่การดำเนินการ')
excel_data_frame4.place(x=850, y=370, height=270, width=300)
tv4 = ttk.Treeview(excel_data_frame4)
tv4.place(relheight=1, relwidth=1)
treescrolly4 = tk.Scrollbar(excel_data_frame4, orient="vertical", command=tv4.yview)
treescrollx4 = tk.Scrollbar(excel_data_frame4, orient="horizontal", command=tv4.xview)
tv4.configure(xscrollcommand=treescrollx4.set, yscrollcommand=treescrolly4.set)
treescrolly4.pack(side="right", fill="y")
treescrollx4.pack(side="bottom", fill="x")
category4_frame()

window.mainloop()
