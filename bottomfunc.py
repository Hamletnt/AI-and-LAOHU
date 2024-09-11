import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from tkinter import ttk

# Define global variables for the DataFrame and current data index
df = None
current_row = 0
batch_size = 100  # Number of rows to load in each batch

# Function to import the Excel file and start lazy loading in batches
def import_file():
    global df, current_row
    file_path = filedialog.askopenfilename(
        title="Select an Excel file to import",
        filetypes=[("Excel files", "*.xlsx")]
    )
    
    if file_path:
        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(file_path)
            
            # Replace NaN or NaT with empty strings
            df = df.fillna("")

            # Reset current row index for lazy loading
            current_row = 0

            # Clear the Treeview before displaying new data
            for i in tree.get_children():
                tree.delete(i)

            # Set the columns in the Treeview based on DataFrame columns
            tree["columns"] = list(df.columns)
            tree["show"] = "headings"

            # Add column headings
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)  # Set width for each column

            # Load the first batch of rows
            load_more_rows()

            messagebox.showinfo("File Imported", f"File imported: {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {str(e)}")

# Function to load more rows in batches
def load_more_rows():
    global current_row
    if df is None:
        return
    
    # Calculate the rows to load in this batch
    next_row = current_row + batch_size
    for index, row in df.iloc[current_row:next_row].iterrows():
        # Insert each row into the Treeview
        tree.insert("", "end", values=list(row))
    
    current_row = next_row

    # Hide the "Load More" button if all rows have been loaded
    if current_row >= len(df):
        load_more_button.pack_forget()

# Function to set the size of the display based on screen resolution
def set_display_size():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the size of the Treeview relative to the screen resolution
    tree_frame.config(width=int(screen_width * 0.9), height=int(screen_height * 0.7))

# Function to handle file selection (if needed for further functionality)
def select_file():
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        messagebox.showinfo("File Selected", f"Selected file: {file_path}")

# Create the main window
root = tk.Tk()
root.title("Excel File Viewer")

# Create a frame for buttons
frame = tk.Frame(root)
frame.pack(pady=20)

# Create the "Import File" button
import_button = tk.Button(frame, text="Import Excel File", command=import_file)
import_button.pack(side="left", padx=10)

# Create the "Select File" button but don't display it yet
select_button = tk.Button(frame, text="Select File", command=select_file)

# Create a frame for the Treeview (spreadsheet-like display)
tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True)

# Create a Treeview widget to display the Excel file content
tree = ttk.Treeview(tree_frame)
tree.pack(side="left", fill=tk.BOTH, expand=True)

# Add a scrollbar to the Treeview
scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Create a "Load More" button to load additional rows
load_more_button = tk.Button(root, text="Load More Rows", command=load_more_rows)
load_more_button.pack(pady=10)

# Set the display size based on screen resolution
set_display_size()

# Run the Tkinter event loop
root.mainloop()
