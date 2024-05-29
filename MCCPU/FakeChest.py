import tkinter as tk
from tkinter import messagebox
import os
import sqlite3

class FakeChest:

    def __init__(self, root):
        self.root = root
        if __name__ == "__main__":
            self.root.title("Fake Chest")

        self.memory_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Storage.db")

        self.conn = sqlite3.connect(self.memory_db_path)

        self.cursor = self.conn.cursor()

        self.create_gui()

    def create_gui(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Frame for the original crafting and recipe terminals (existing content)
        self.existing_frame = tk.Frame(self.root)
        self.existing_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame for the new chest buttons with scrollbars
        self.chest_frame = tk.Frame(self.root)
        self.chest_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Configure grid weights to allow proper expansion
        self.chest_frame.grid_rowconfigure(0, weight=1)
        self.chest_frame.grid_columnconfigure(0, weight=1)
        self.chest_frame.grid_rowconfigure(2, weight=0)
        
        # Canvas setup
        self.canvas = tk.Canvas(self.chest_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_x = tk.Scrollbar(self.chest_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.scrollbar_y = tk.Scrollbar(self.chest_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.grid_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        # Create control frame inside chest_frame
        self.control_frame = tk.Frame(self.chest_frame)
        self.control_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Entry and buttons in the control frame
        tk.Label(self.control_frame, text="Address (10-bit binary):").grid(row=0, column=0, padx=5, pady=5)
        self.address_entry = tk.Entry(self.control_frame)
        self.address_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.control_frame, text="Item:").grid(row=1, column=0, padx=5, pady=5)
        self.item_entry = tk.Entry(self.control_frame)
        self.item_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.control_frame, text="Add/Update", command=self.add_update_button).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.control_frame, text="Delete", command=self.delete_button).grid(row=2, column=1, padx=5, pady=5)

        self.buttons = {}

        # Initialize 32x32 grid buttons with scrollbars
        for i in range(32):
            for j in range(32):
                address_str = format(i, '05b') + format(j, '05b')
                btn = tk.Button(self.grid_frame, text=address_str, width=10, command=lambda addr=address_str: self.show_message(addr))
                btn.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
                self.grid_frame.grid_rowconfigure(i, weight=1)  # Allow rows to expand
                self.grid_frame.grid_columnconfigure(j, weight=1)  # Allow columns to expand
                self.buttons[address_str] = btn

        # Load initial state from the database
        self.load_initial_state()

    def load_initial_state(self):
        self.cursor.execute("SELECT address, item FROM button_states")
        rows = self.cursor.fetchall()
        for row in rows:
            address, item = row
            if address in self.buttons:
                self.buttons[address].config(text=item)

    def show_message(self, address):
        messagebox.showinfo("Button Clicked", f"Address: {address}")

    def add_update_button(self):
        address = self.address_entry.get()
        item = self.item_entry.get()

        if len(address) != 10 or not all(bit in '01' for bit in address):
            messagebox.showerror("Invalid Address", "Address must be a 10-bit binary string.")
            return

        if address not in self.buttons:
            messagebox.showerror("Invalid Address", "Address is not within valid range.")
            return

        self.buttons[address].config(text=item)

        self.cursor.execute("REPLACE INTO button_states (address, item) VALUES (?, ?)", (address, item))

        self.conn.commit()

    def delete_button(self):
        address = self.address_entry.get()

        if len(address) != 10 or not all(bit in '01' for bit in address):
            messagebox.showerror("Invalid Address", "Address must be a 10-bit binary string.")
            return

        if address not in self.buttons:
            messagebox.showerror("Invalid Address", "Address is not within valid range.")
            return

        self.buttons[address].config(text=address)

        self.cursor.execute("DELETE FROM button_states WHERE address = ?", (address,))

        self.conn.commit()

    def close(self):
        self.conn.close()

# Database initialization
def init_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS button_states (
            address TEXT PRIMARY KEY,
            item TEXT
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":

    init_database(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Storage.db"))

    root = tk.Tk()

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    app = FakeChest(root)

    root.protocol("WM_DELETE_WINDOW", app.close)

    root.mainloop()