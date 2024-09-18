import tkinter as tk
from tkinter import ttk

def open_filtered_data_window(filtered_df):
    print(f"Filtered DataFrame in filtered_view:\n{filtered_df}")
    
    filtered_window = tk.Toplevel()
    filtered_window.title("Filtered View")

    frame = tk.Frame(filtered_window)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, show="headings")
    
    scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")
    tree.pack(fill=tk.BOTH, expand=True)

    columns = list(filtered_df.columns)
    tree["columns"] = columns
    tree["show"] = "headings"

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center", stretch=tk.NO)

    for i, row in filtered_df.iterrows():
        tree.insert("", "end", values=list(row))
    
    filtered_window.update_idletasks()
    filtered_window.geometry(f"{filtered_window.winfo_reqwidth()}x{filtered_window.winfo_reqheight()}")


def main():
    import main_app
    main_app.main()

if __name__ == "__main__":
    main()