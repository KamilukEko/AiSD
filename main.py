import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from db_manager import DatabaseManager
from radix_sort import radix_sort
from sortable_record import SortableRecord

class RecordSortingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sortable Record Manager")

        self.db = DatabaseManager()

        style = ThemedStyle(self.root)
        style.set_theme("blue")  

        self.create_ui()
        self.load_data()

        style = ttk.Style()

        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    def create_ui(self):
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Name", "Timestamp")  
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, width=150, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(fill=tk.X, padx=10, pady=5)

    def add_striped_rows(self):
        for i, record in enumerate(self.sortable_array):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=record.to_tuple(), tags=(tag,))
        
        self.tree.tag_configure("evenrow", background="#F5F5F5")  
        self.tree.tag_configure("oddrow", background="#E8E8E8")   
    

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        db_data = self.db.get_all()

        self.sortable_array = [SortableRecord(record) for record in db_data]

        radix_sort(self.sortable_array)

        self.add_striped_rows()

if __name__ == "__main__":
    root = tk.Tk()
    app = RecordSortingApp(root)
    root.geometry("600x400")
    root.mainloop()
