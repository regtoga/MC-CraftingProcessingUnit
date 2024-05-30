import tkinter as tk
from tkinter import messagebox
import os
import sqlite3

class FakeChest:

    def __init__(self, root):
        self.root = root
        #if the program is standalone use this title
        if __name__ == "__main__":
            self.root.title("Fake Chest")
        else:
            #Creates a database if none exist
            init_database(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Storage.db"))

        #find the database and write down the path, finally connect to the database
        self.memory_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Storage.db")
        self.conn = sqlite3.connect(self.memory_db_path)
        self.cursor = self.conn.cursor()

        #keeps track if there is more than one pop up
        self.current_popup = None

        #Create the GUI
        self.create_gui()

    def create_gui(self):
        #give the GUI an ammount of space to exist
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        #Frame for the original crafting and recipe terminals
        self.existing_frame = tk.Frame(self.root)
        self.existing_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #Frame for the new chest buttons with scrollbars
        self.chest_frame = tk.Frame(self.root)
        self.chest_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        #Configure grid weights to allow proper expansion
        self.chest_frame.grid_rowconfigure(0, weight=1)
        self.chest_frame.grid_columnconfigure(0, weight=1)
        self.chest_frame.grid_rowconfigure(2, weight=0)
        
        #Setup the canvas for the chest frame
        self.canvas = tk.Canvas(self.chest_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        #Create X scrollbars for the main canvas
        self.scrollbar_x = tk.Scrollbar(self.chest_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        #Create Y scrollbars for the main canvas
        self.scrollbar_y = tk.Scrollbar(self.chest_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        #bind the two scrollbars to the canvas
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        #Create the frame for the canvas controls
        self.grid_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        #Create control frame inside chest_frame
        self.control_frame = tk.Frame(self.chest_frame)
        self.control_frame.grid(row=2, column=0, columnspan=2, pady=10)

        #Entry and buttons in the control frame
        tk.Label(self.control_frame, text="Address (10-bit binary):").grid(row=0, column=0, padx=5, pady=5)
        self.address_entry = tk.Entry(self.control_frame)
        self.address_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.control_frame, text="Item:").grid(row=1, column=0, padx=5, pady=5)
        self.item_entry = tk.Entry(self.control_frame)
        self.item_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.control_frame, text="Ammount in Storage:").grid(row=2, column=0, padx=5, pady=5)
        self.ammount_entry = tk.Entry(self.control_frame)
        self.ammount_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.control_frame, text="Add/Update", command=self.add_update_button).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.control_frame, text="Delete", command=self.delete_button).grid(row=3, column=1, padx=5, pady=5)

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
        """Function goes to the database and loads all the data from that datbase onto the buttons"""
        self.cursor.execute("SELECT address, item FROM button_states")
        rows = self.cursor.fetchall()
        for row in rows:
            address, item = row
            if address in self.buttons:
                self.buttons[address].config(text=item)

    def non_modal_messagebox(self, title, message):
        # Close the current popup if it exists
        if self.current_popup is not None:
            self.current_popup.destroy()
        
        popup = tk.Toplevel()
        self.current_popup = popup
        popup.title(title)
        
        # Remove resizability
        popup.resizable(False, False)
        
        # Disable minimize and maximize buttons, keeping only the close button
        popup.attributes('-toolwindow', True)
        
        # Create the message label and OK button
        label = tk.Label(popup, text=message)
        label.pack(pady=10, padx=10)
        button = tk.Button(popup, text="OK", command=popup.destroy)
        button.pack(pady=5)
        
        # Calculate position to center the popup
        popup.update_idletasks()  # Ensure the geometry is updated
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        popup_width = popup.winfo_width()
        popup_height = popup.winfo_height()
        
        x = (screen_width // 2) - (popup_width // 2)
        y = (screen_height // 2) - (popup_height // 2)
        
        popup.geometry(f'{popup_width}x{popup_height}+{x}+{y}')
        
        # Reset the current popup reference when it is closed
        popup.protocol("WM_DELETE_WINDOW", self.on_popup_close)

    def on_popup_close(self):
        self.current_popup.destroy()
        self.current_popup = None

    def show_message(self, address):
        """When a button is clicked we will show its address"""
        self.non_modal_messagebox("Button Clicked", f"Address: {address}")
        #messagebox.showinfo("Button Clicked", f"Address: {address}")

    def add_update_button(self):
        """this function checks if an input is valid before appending it to the database and updating the text on a button"""
        #Get the inputs from the user
        address = self.address_entry.get()
        item = self.item_entry.get()
        ammount = self.ammount_entry.get()

        #Check if the address is the right lenght and only consisting of ones and zeros
        if len(address) != 10 or not all(bit in '01' for bit in address):
            messagebox.showerror("Invalid Address", "Address must be a 10-bit binary string.")
            return

        #checks if the address actually corelates with a button
        if address not in self.buttons:
            messagebox.showerror("Invalid Address", "Address is not within valid range.")
            return
        
        #checks if the ammount is a real integer value if its not the default is zero         
        try:
            ammount = int(ammount)
        except:
            ammount = 0

        #Change the text on a button
        self.buttons[address].config(text=item)

        #Update the database
        self.cursor.execute("REPLACE INTO button_states (address, item, ammount) VALUES (?, ?, ?)", (address, item, ammount))
        #Save the changes
        self.conn.commit()

    def delete_button(self):
        """Deletes an item from the database then resets the text of the button to the address after validating the input"""
        address = self.address_entry.get()

        if len(address) != 10 or not all(bit in '01' for bit in address):
            messagebox.showerror("Invalid Address", "Address must be a 10-bit binary string.")
            return

        if address not in self.buttons:
            messagebox.showerror("Invalid Address", "Address is not within valid range.")
            return

        #Change the text on a button
        self.buttons[address].config(text=address)
        #Update the database
        self.cursor.execute("DELETE FROM button_states WHERE address = ?", (address,))
        #Save the changes
        self.conn.commit()

    def close(self):
        """Close the connection to the database"""
        self.conn.close()

# Database initialization
def init_database(db_path):
    """initiate the connection to the database, also create the database if it doesnt exist"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS button_states (
            address TEXT PRIMARY KEY,
            item TEXT,
            ammount INTEGER
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    #make the database at the correct location for local running
    init_database(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Storage.db"))

    root = tk.Tk()
    #give the GUI an ammount of space to exist
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    app = FakeChest(root)
    #Run the GUI
    root.mainloop()