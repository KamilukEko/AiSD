import tkinter as tk
from tkinter import ttk, simpledialog, messagebox 
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

        self.sortable_array = [SortableRecord(record) for record in self.db.get_all()]

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

        self.add_user_button = tk.Button(self.add_frame, text="Add User", command=self.add_user)
        self.add_user_button.pack(side=tk.LEFT, padx=10)

        self.del_user_button = tk.Button(self.add_frame, text="Delete User", command=self.delete_user)
        self.del_user_button.pack(side=tk.LEFT, padx=10)

        self.sort_by_id_button = tk.Button(self.add_frame, text="Sort by ID", command=lambda: self.sort_data("ID"))
        self.sort_by_id_button.pack(side=tk.RIGHT, padx=10)

        self.sort_by_timestamp_button = tk.Button(self.add_frame, text="Sort by Timestamp", command=lambda: self.sort_data("Timestamp"))
        self.sort_by_timestamp_button.pack(side=tk.RIGHT, padx=10)

        self.sort_by_timestamp_button = tk.Button(self.add_frame, text="Sort by Name", command=lambda: self.sort_data("Name"))
        self.sort_by_timestamp_button.pack(side=tk.RIGHT, padx=10)

    def add_striped_rows(self):

        for i, record in enumerate(self.sortable_array):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=record.to_tuple(), tags=(tag,))

        self.tree.tag_configure("evenrow", background="#F5F5F5")  
        self.tree.tag_configure("oddrow", background="#E8E8E8")   

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.add_striped_rows()

    def sort_data(self, column):

        if column == "Timestamp":
            radix_sort(self.sortable_array)
        elif column == "ID":
            self.sortable_array.sort(key=lambda record: record.id)
        else:
            self.sortable_array.sort(key=lambda record: record.user_name)

        self.load_data()

    def add_user(self):

        while True:  
            user_name = simpledialog.askstring("Input", "Enter Name:")
            if user_name.strip():
                break
            else:
                messagebox.showerror("Error", "Name cannot be empty.")
        
        def is_valid(timestamp):
            val = timestamp.split("/")
        
            if 1900<= int(val[0]) <= 2025 and 1<= int(val[1]) <= 12 and 1<= int(val[2]) <= 31 and  0<= int(val[3]) <= 23 and 0<=int(val[4]) <= 59 and 0<=int(val[5])<= 59:
                return True
            return False

        while True:
            timestamp = simpledialog.askstring("Input", "Enter Timestamp: (YYYY/MM/DD/Hour/Minute/Second)")
            if is_valid(timestamp):
                break
            else:
                messagebox.showerror("Error", "Please, follow the pattern.")

        self.db.add_user(user_name, timestamp)
        self.sortable_array = [SortableRecord(record) for record in self.db.get_all()] 
        self.load_data()

    def delete_user(self):
        user_id = simpledialog.askstring("Input", "Enter ID of user You want to delete:")

        if user_id is not None:
            try:
                user_id = int(user_id)
            
                self.db.del_user(user_id)  

                self.sortable_array = [SortableRecord(record) for record in self.db.get_all()] 
                self.load_data() 
                
                messagebox.showinfo("Success", f"User with ID {user_id} has been deleted.")
            
            except ValueError:
                messagebox.showerror("Error", "Invalid ID. Please enter a valid integer.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecordSortingApp(root)
    root.geometry("600x400")
    root.mainloop()
