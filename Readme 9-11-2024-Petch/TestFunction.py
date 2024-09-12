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
        df = pd.read_excel(excel_filename)
    except ValueError:
        tk.messagebox.showerror("Error", "Your file is invalid. Please select an Excel (.xlsx) file.")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Error", f"No such file as {file_path}")
        return None
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred: {e}")
        return None
    
    # คำสั่งแทนที่ NaN ด้วยค่าว่าง
    df = df.fillna("")

    # แทนที่ NaT ในคอลัมน์วันที่ด้วยข้อความ "ไม่มีข้อมูล"
    df = df.astype({"วันที่": str})  # แปลงคอลัมน์จากdatetime หรือ timestamp เป็น string ก่อน
    df["วันที่"] = df["วันที่"].replace("NaT", "")  # แทนที่ NaT ด้วยค่าว่าง

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["column"]:
        tv1.heading(column, text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("","end", values=row)
    return None
    
def clear_data():
    tv1.delete(*tv1.get_children())

    

title_label = tk.Label(window, text='Import File', font = '15').pack()
browse_button = tk.Button(window, text ='Browse File',width = 10, command=lambda:upload_file()).place(x=500, y=40)
load_button = tk.Button(window, text ='Load File',width = 10, command=lambda:load_file()).place(x=600, y=40)

label_file1= tk.Label(window, text = "File Name --> ")
label_file1.place(x=500, y=80)
label_file2= tk.Label(window, text = "No file Selected")
label_file2.place(x=600, y=80)

# Create LabelFrame and place it
excel_data_frame = LabelFrame(window, text='Excel Data')
excel_data_frame.place(x=100, y=100, height=400, width=1000)

# Create Treeview and pack it into the frame
tv1 = ttk.Treeview(excel_data_frame)
tv1.place(relheight=1, relwidth=1)

# Add Scrollbars for Treeview
treescrolly = tk.Scrollbar(excel_data_frame, orient="vertical", command=tv1.yview)
treescrollx = tk.Scrollbar(excel_data_frame, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

treescrolly.pack(side="right", fill="y")
treescrollx.pack(side="bottom", fill="x")



window.mainloop()