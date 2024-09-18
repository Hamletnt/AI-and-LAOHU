import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
 
# Define global variable for the DataFrame and checkbox states
df = None
checkbox_states = {}  # To store checkbox states for each row
current_view = "full"  # To keep track of current view (full or filtered)

# Define categories
categories = [
    "ไฟฟ้า", "ประปา", "Air", "ปลวก", "สถาบัน", "Fur", "อุปกรณ์",
    "รายรับอื่นๆ", "ขาย", "วัตถุดิบ", "หมู", "ไก่", "ไข่", "เนื้อ",
    "วัชระ+สุรพล", "ลูกชิ้น", "กุ้ง", "ผัก", "เครื่องดื่ม", "ไอติม",
    "ขนมจีบ", "ของหวาน", "ผลไม้", "อุปกรณ์ใช้สอย", "วัสดุสิ้นเปลือง",
    "ค่าใช้สอย", "PR", "ค่าไฟ", "ค่าแรง", "Ptime", "สวัสดิการ", "Manage"
]

def import_file():
    global df, checkbox_states
    file_path = filedialog.askopenfilename(
        title="เลือกไฟล์ Excel เพื่อโหลด",
        filetypes=[("Excel files", "*.xlsx")]
    )
    
    if file_path:
        try:
            df = pd.read_excel(file_path)

            # Handle missing columns
            if 'Selected' not in df.columns:
                df['Selected'] = ["❌" for _ in range(len(df))]
            if 'Category' not in df.columns:
                df['Category'] = [""] * len(df)

            # Ensure 'Selected' and 'Category' are in the correct positions
            df.insert(3, 'Selected', df.pop('Selected'))  # Move 'Selected' to column D (index 3)
            df.insert(4, 'Category', df.pop('Category'))  # Move 'Category' to column E (index 4)

            # Handle NaT, NaN values and format dates
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].apply(lambda x: "" if pd.isna(x) else x.strftime('%Y-%m-%d'))
                elif pd.api.types.is_float_dtype(df[col]):
                    df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "")
                else:
                    df[col] = df[col].fillna("")

            checkbox_states = {i: False for i in range(len(df))}

            # Display the full data in the Treeview
            update_treeview()  # Ensure this is called here

            messagebox.showinfo("ไฟล์นำเข้า", f"ไฟล์นำเข้า: {file_path}")

        except pd.errors.EmptyDataError:
            messagebox.showwarning("ไฟล์ว่าง", "ไฟล์ที่เลือกว่างเปล่าหรือไม่สามารถอ่านได้.")
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถอ่านไฟล์ได้: {str(e)}")


def update_treeview(filtered_df=None):
    # Clear the Treeview before displaying new data
    tree.delete(*tree.get_children())

    # Determine DataFrame to use
    data_to_display = filtered_df if filtered_df is not None else df
    if data_to_display is None:
        return

    # Set columns in the Treeview
    columns = list(data_to_display.columns)
    tree["columns"] = columns
    tree["show"] = "headings"

    # Configure the column headers
    for col in columns:
        if col == 'Selected':
            tree.heading(col, text="Selected", anchor="w")
            tree.column(col, width=70, anchor="center", stretch=tk.NO)
        elif col == 'Category':
            tree.heading(col, text="Category", anchor="w")
            tree.column(col, width=150, anchor="center", stretch=tk.NO)
        else:
            tree.heading(col, text=col, anchor="w")
            tree.column(col, width=150, anchor="center", stretch=tk.NO)

    # Insert rows into the Treeview
    for i, row in data_to_display.iterrows():
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        tree.insert("", "end", values=list(row), tags=(tag,))

def toggle_checkbox(event):
    item = tree.identify_row(event.y)
    if item:
        row_id = tree.index(item)
        checkbox_states[row_id] = not checkbox_states[row_id]
        new_value = "✅" if checkbox_states[row_id] else "❌"
        tree.set(item, 'Selected', new_value)
        
        # Update the DataFrame directly
        df.at[row_id, 'Selected'] = new_value

        # Assign category from the combobox if selected, else assign default
        if new_value == "✅":
            selected_category = category_combobox.get() or "ไฟฟ้า"  # Default to "ไฟฟ้า"
            tree.set(item, 'Category', selected_category)
            df.at[row_id, 'Category'] = selected_category
        else:
            tree.set(item, 'Category', "")
            df.at[row_id, 'Category'] = ""

def export_selected_rows():
    global df
    if df is None:
        messagebox.showwarning("ไม่มีข้อมูล", "ไม่มีข้อมูลสำหรับการส่งออก กรุณานำเข้าไฟล์ก่อน.")
        return
    
    selected_rows = [i for i, checked in checkbox_states.items() if checked]
    if not selected_rows:
        messagebox.showwarning("ไม่มีการเลือก", "ไม่มีแถวที่เลือกสำหรับการส่งออก.")
        return
    
    # Filter selected rows
    selected_df = df.loc[selected_rows]

    # Drop 'Selected' column from the DataFrame
    selected_df = selected_df.drop(columns=['Selected'])

    # Sum by category
    try:
        sum_by_category()

        # Gather the sum results
        sales_df = selected_df[selected_df['Category'] == 'ขาย']
        other_df = selected_df[selected_df['Category'] != 'ขาย']

        # Sum column 5 for 'ขาย' category (ensure numeric values)
        sales_df.iloc[:, 5] = pd.to_numeric(sales_df.iloc[:, 5], errors='coerce')
        total_sales = sales_df.iloc[:, 5].sum()

        # Sum column 6 for other categories
        other_df.iloc[:, 6] = pd.to_numeric(other_df.iloc[:, 6], errors='coerce')
        other_sums = other_df.groupby('Category')[other_df.columns[6]].sum()

        # Combine the results into a dictionary based on `categories` array
        sum_dict = {category: 0 for category in categories}  # Pre-fill with zeros
        sum_dict['ขาย'] = total_sales  # Assign 'ขาย' sum
        for category, total in other_sums.items():
            if category in sum_dict:
                sum_dict[category] = total

    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการคำนวณยอดรวม: {str(e)}")
        return

    # Prepare the sum as a DataFrame with categories in row 1 and sums in row 2
    sum_df = pd.DataFrame([list(sum_dict.keys()), list(sum_dict.values())])

    # Ask the user where to save the file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="บันทึกเป็น"
    )
    
    if file_path:  # Only proceed if a valid file path is chosen
        try:
            # Write selected rows and sum results to Excel
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                selected_df.to_excel(writer, index=False, sheet_name="Selected Rows")  # Export selected rows
                sum_df.to_excel(writer, index=False, header=False, sheet_name="Sum By Category")  # Export sum results

            messagebox.showinfo("การส่งออกสำเร็จ", f"แถวที่เลือกได้ถูกส่งออกไปที่: {file_path}")
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถส่งออกไฟล์ได้: {str(e)}")



def submit_selection():
    # Filter the DataFrame based on selected rows
    filtered_df = df[df['Selected'] == '✅']  # Select only rows that have been marked as selected

    if filtered_df.empty:
        messagebox.showinfo("ไม่มีข้อมูล", "ไม่มีข้อมูลที่ถูกเลือก.")
        return

    # Display the filtered data in the Treeview on the "Filtered Data" page
    update_filtered_treeview(filtered_df)

    # Automatically calculate and update the sum by category
    sum_by_category()

    # Switch to the "Filtered Data" tab
    notebook.select(filtered_data_frame)

def update_filtered_treeview(filtered_df):
    # Clear the Treeview before displaying new data
    filtered_tree.delete(*filtered_tree.get_children())

    # Set columns with correct headings and widths
    columns = list(filtered_df.columns)
    filtered_tree["columns"] = columns
    filtered_tree["show"] = "headings"

    for col in columns:
        filtered_tree.heading(col, text=col)
        filtered_tree.column(col, width=150, anchor="center", stretch=tk.NO)

    # Insert rows into the filtered Treeview
    for i, row in filtered_df.iterrows():
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        filtered_tree.insert("", "end", values=list(row), tags=(tag,))

    # Switch to the "Filtered Data" tab
    notebook.select(filtered_data_frame)

def calculate_sales_sum():
    global df
    if df is None:
        return

    # Filter for rows where Category is 'ขาย'
    sales_df = df[df['Category'] == 'ขาย']

    # Ensure column index 5 contains numeric values (coerce non-numeric to NaN)
    sales_df.iloc[:, 5] = pd.to_numeric(sales_df.iloc[:, 5], errors='coerce')

    # Sum the values in column 5 (Amount column)
    total_sales = sales_df.iloc[:, 5].sum()

    # Update the sum result in the Filtered Data Treeview
    update_sum_treeview(total_sales)

def sum_by_category():
    global df
    if df is None:
        return  # No data available to sum

    # Filter selected rows (where 'Selected' is "✅")
    selected_df = df[df['Selected'] == '✅']

    if selected_df.empty:
        return  # No selected rows, so nothing to sum

    try:
        # Separate the rows where 'Category' is 'ขาย'
        sales_df = selected_df[selected_df['Category'] == 'ขาย']
        other_df = selected_df[selected_df['Category'] != 'ขาย']

        # Sum column 5 for 'ขาย' category (ensure numeric values)
        sales_df.iloc[:, 5] = pd.to_numeric(sales_df.iloc[:, 5], errors='coerce')
        total_sales = sales_df.iloc[:, 5].sum()

        # Sum column 6 for all other categories
        other_df.iloc[:, 6] = pd.to_numeric(other_df.iloc[:, 6], errors='coerce')
        other_sums = other_df.groupby('Category')[other_df.columns[6]].sum()  # Fixing the sum operation on grouped data

        # Combine the results
        result = pd.concat([pd.Series({"ขาย": total_sales}), other_sums])

        # Update the Sum Treeview on the Filtered Data page
        update_sum_treeview(result)

    except Exception as e:
        messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการคำนวณ: {str(e)}")


def update_sum_treeview(result):
    # Clear the Sum Treeview before displaying new data
    sum_tree.delete(*sum_tree.get_children())

    # Insert the summed values into the Sum Treeview
    for category, total in result.items():
        sum_tree.insert("", "end", values=(category, f"{total:.2f}"))


def display_sum_by_category(result):
    # Create a new window to display the sum results
    result_window = tk.Toplevel()
    result_window.title("Sum by Category")

    frame = tk.Frame(result_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Use a Treeview to display the results
    tree = ttk.Treeview(frame, show="headings")
    tree["columns"] = ("Category", "Sum")
    tree.heading("Category", text="หมวดหมู่")
    tree.heading("Sum", text="ยอดรวม")

    tree.column("Category", width=150, anchor="center")
    tree.column("Sum", width=100, anchor="center")

    # Insert the summed values into the Treeview
    for category, total in result.items():
        tree.insert("", "end", values=(category, f"{total:.2f}"))

    # Add vertical and horizontal scrollbars to the Treeview
    scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    tree.pack(fill=tk.BOTH, expand=True)

    # Adjust the size of the window based on the content
    result_window.geometry(f"{result_window.winfo_reqwidth()}x{result_window.winfo_reqheight()}")

    
# Create main window
root = tk.Tk()
root.title("Laohu")

# Create a Notebook for tabbed interface
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create frames for each tab
full_data_frame = tk.Frame(notebook)
filtered_data_frame = tk.Frame(notebook)

# Add frames to notebook
notebook.add(full_data_frame, text="Full Data")
notebook.add(filtered_data_frame, text="Filtered Data")

# Create "Import File" button
import_button = tk.Button(root, text="นำเข้าไฟล์ Excel", command=import_file)
import_button.pack(side="top", padx=10, pady=5)

# Create "Export Selected" button
export_button = tk.Button(root, text="บันทึกไฟล์", command=export_selected_rows)
export_button.pack(side="top", padx=10, pady=5)

# Create combobox for category selection
category_combobox = ttk.Combobox(root, values=categories, state="readonly")
category_combobox.set("เลือกหมวดหมู่")
category_combobox.pack(side="top", padx=10, pady=5)

# Create "Submit" button
submit_button = tk.Button(root, text="ยืนยัน", command=submit_selection)
submit_button.pack(side="top", padx=10, pady=5)

# Create Treeview widget for Full Data
tree = ttk.Treeview(full_data_frame, show="headings", selectmode="browse")

# Add vertical and horizontal scrollbars to the Full Data Treeview
scrollbar_y = tk.Scrollbar(full_data_frame, orient="vertical", command=tree.yview)
scrollbar_x = tk.Scrollbar(full_data_frame, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

# Pack scrollbars and Treeview into the full_data_frame
scrollbar_y.pack(side="right", fill="y")
scrollbar_x.pack(side="bottom", fill="x")
tree.pack(fill=tk.BOTH, expand=True)

# Configure alternating row colors for the Full Data Treeview
tree.tag_configure("evenrow", background="#F2F2F2")  # Light gray background
tree.tag_configure("oddrow", background="#FFFFFF")   # White background

# Ensure the Treeview expands with the window
full_data_frame.grid_rowconfigure(0, weight=1)
full_data_frame.grid_columnconfigure(0, weight=1)


# Create a Treeview widget for displaying sums in the Filtered Data page
sum_tree = ttk.Treeview(filtered_data_frame, show="headings", columns=("Category", "Total Amount"))
sum_tree.heading("Category", text="Category")
sum_tree.heading("Total Amount", text="Total Amount")
sum_tree.column("Category", width=150, anchor="center")
sum_tree.column("Total Amount", width=150, anchor="center")

# Pack the sum Treeview into the filtered data frame
sum_tree.pack(fill=tk.BOTH, expand=True)


# Add vertical and horizontal scrollbars to the Sum Treeview
sum_scrollbar_y = tk.Scrollbar(filtered_data_frame, orient="vertical", command=sum_tree.yview)
sum_scrollbar_x = tk.Scrollbar(filtered_data_frame, orient="horizontal", command=sum_tree.xview)
sum_tree.configure(yscrollcommand=sum_scrollbar_y.set, xscrollcommand=sum_scrollbar_x.set)

# Pack Sum Treeview and scrollbars
sum_scrollbar_y.pack(side="right", fill="y")
sum_scrollbar_x.pack(side="bottom", fill="x")
sum_tree.pack(fill=tk.BOTH, expand=True)

# Configure alternating row colors (gray and white)
tree.tag_configure("evenrow", background="#F2F2F2")  # Light gray background
tree.tag_configure("oddrow", background="#FFFFFF")  # White background

# Configure column headers to have bold font and darker background
style = ttk.Style()
style.configure("Treeview.Heading", font=('Calibri', 12, 'bold'), background="#D3D3D3", foreground="black")

# Add grid lines effect
style.configure("Treeview", highlightthickness=0, borderwidth=0)
style.map("Treeview", background=[('selected', '#C4E1FF')])

# Adjust grid weights to make the Treeview expand with the frame
full_data_frame.grid_rowconfigure(0, weight=1)
full_data_frame.grid_columnconfigure(0, weight=1)

# Create Treeview widget for Filtered Data
filtered_tree = ttk.Treeview(filtered_data_frame, show="headings", selectmode="browse")

# Add vertical and horizontal scrollbars to the Filtered Treeview
filtered_scrollbar_y = tk.Scrollbar(filtered_data_frame, orient="vertical", command=filtered_tree.yview)
filtered_scrollbar_x = tk.Scrollbar(filtered_data_frame, orient="horizontal", command=filtered_tree.xview)
filtered_tree.configure(yscrollcommand=filtered_scrollbar_y.set, xscrollcommand=filtered_scrollbar_x.set)

# Use pack to place Treeview and scrollbars
filtered_scrollbar_y.pack(side="right", fill="y")
filtered_scrollbar_x.pack(side="bottom", fill="x")
filtered_tree.pack(fill=tk.BOTH, expand=True)

# Configure alternating row colors for Filtered Data Treeview
filtered_tree.tag_configure("evenrow", background="#F2F2F2")  # Light gray background
filtered_tree.tag_configure("oddrow", background="#FFFFFF")  # White background

# Bind the toggle_checkbox function to mouse click events
tree.bind("<Button-1>", toggle_checkbox)


# Set the display size based on screen resolution
def set_display_size():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    full_data_frame.config(width=int(screen_width * 0.8), height=int(screen_height * 0.6))

set_display_size()

# Run the main loop
root.mainloop()
