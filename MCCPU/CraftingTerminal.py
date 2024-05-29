#import the required libraries
import tkinter as tk

from tkinter import ttk

import CPUfile.CPU as CPU 

class CraftingTerminal:

    def __init__(self, root):
        """The Crafting Terminal is where the user will select the items they want to craft and how many of them to be crafted"""
        self.root = root

        #name of the GUI
        if __name__ == "__main__":
            self.root.title("Crafting Terminal")

        #Create the Item Selection Panel Frame
        self.item_selection_frame = tk.LabelFrame(self.root, text="Item Selection Panel", padx=10, pady=10)
        #Create a list for the 10 memory address buttons to be placed inside
        self.item_buttons = []
        #Fill the list of 10 memory addresses with default values of zero
        for i in range(10):
            #set the button to toggle itself from 0 to 1 and from 1 to 0
            btn = tk.Button(self.item_selection_frame, text="0", width=3, command=lambda i=i: self.toggle_item(i))
            #Grid the buttons to the right of the last one
            btn.grid(row=0, column=i)
            #append the button to the list of 10 buttons
            self.item_buttons.append(btn)
        
        #Grid the Items Selection panel To be the first frame in the column of frames
        self.item_selection_frame.grid(row=0, column=0, padx=10, pady=10)

        #---- 

        #Create Number of Items Wanted Frame
        self.number_panel_frame = tk.LabelFrame(self.root, text="Number of Items Wanted", padx=10, pady=10)
        #Create the 4 seven segments
        self.seven_segments = [tk.Label(self.number_panel_frame, text="0", font=("Courier", 24), width=2, anchor="e") for _ in range(4)]

        #For each of the seven segments place one two the right of the last
        for i, segment in enumerate(self.seven_segments):

            segment.grid(row=0, column=i)

        #I am not fully shure what this line does, but my guess is attach the segment displays to the number buttons frame
        self.number_buttons_frame = tk.Frame(self.number_panel_frame)
        
        #This array holds the information needed to construct the number pad
        numberpad_layout = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0]]

        #for each row 
        for row_index, row in enumerate(numberpad_layout):
            #for each colum
            for col_index, num in enumerate(row):
                #make a button 
                btn = tk.Button(self.number_buttons_frame, text=str(num), width=3, command=lambda num=num: self.update_number(num))
                #if the button value is 0 it needs to be in the center of the column
                #else grid then side by side
                if num == 0:
                    btn.grid(row=row_index + 1, column=col_index+1)
                else:
                    btn.grid(row=row_index + 1, column=col_index)

        #places the number panel frame under the first items selection panel
        self.number_panel_frame.grid(row=1, column=0, padx=10, pady=10)
        #places the number pad under the segments
        self.number_buttons_frame.grid(row=1, columnspan=4)

        #---- 

        #Create the Craft Button
        self.craft_button = tk.Button(self.root, text="Craft", width=10, command=self.craft_item)
        #Grid the craft button under the nubmer of items wanted screen
        self.craft_button.grid(row=2, column=0, pady=5)

        #---- 

        #Create the Clear Button
        self.clear_button = tk.Button(self.root, text="Clear", width=10, command=self.clear_all)
        #grid the clear button under the craft button
        self.clear_button.grid(row=3, column=0, pady=5)

        #----

        #Create the Output Display frame
        self.output_frame = tk.LabelFrame(self.root, text="Output", padx=10, pady=10)

        #Create the labels and set them to their default values
        self.in_storage_label = ttk.Label(self.output_frame, text="0")
        self.able_to_craft_label = ttk.Label(self.output_frame, text="0")
        self.crafting_label = ttk.Label(self.output_frame, text="No")
        self.remaining_label = ttk.Label(self.output_frame, text="0")

        #Grid the Output frame the be the final frame
        self.output_frame.grid(row=4, column=0, padx=10, pady=10)

        #grid the lables and their lables acordingly
        ttk.Label(self.output_frame, text="In Storage:").grid(row=0, column=0)
        self.in_storage_label.grid(row=0, column=1)
        ttk.Label(self.output_frame, text="Able to Craft:").grid(row=1, column=0)
        self.able_to_craft_label.grid(row=1, column=1)
        ttk.Label(self.output_frame, text="Crafting?").grid(row=2, column=0)
        self.crafting_label.grid(row=2, column=1)
        ttk.Label(self.output_frame, text="Remaining:").grid(row=3, column=0)
        self.remaining_label.grid(row=3, column=1)



    def toggle_item(self, idx):
        """Toggles the text on the Item selection panel"""
        current_text = self.item_buttons[idx].cget("text")
        self.item_buttons[idx].config(text="1" if current_text == "0" else "0")



    def craft_item(self):
        """When the craft button is pressed this function execute and send the data over to the CPU"""
        # Collect item selection states
        selected_items = [btn.cget("text") for btn in self.item_buttons]

        # Collect number of items wanted
        number_of_items = int("".join(segment.cget("text") for segment in self.seven_segments))

        Cpu = CPU.CraftingProcessingUnit()
        Cpu.RetrieveDataFromMemory(selected_items)
        

        """# Placeholder for crafting logic
        print(f"Craft button pressed with items: {selected_items} and number: {number_of_items}")"""



    def update_number(self, num):
        """
        this button is called from one of the number pad's number buttons
        it takes the value of the button clicked adds it to a place shifted version of the last number
        """
        #Get the current number baised off of the values of the seven segment displays 
        current_number = int("".join(segment.cget("text") for segment in self.seven_segments))
        #Shift the current number left a digit and add the current number to it
        #Works like a microwave display
        new_number = current_number * 10 + num
        #if the new number is larger than 9999 take take the largest num off so that it fits inside the 4 displays again
        if new_number > 9999:

            new_number = new_number % 10000
        #takes the number and makes it a string 
        new_str_num = "{:04}".format(new_number)
        #for each segment in the seven segment display make the text the value of the current char in the number
        for i, segment in enumerate(self.seven_segments):
            segment.config(text=new_str_num[i])



    def clear_all(self):
        """Clear all the inputs and reset them to their default values"""

        #Clears the values in the Item selection panel
        for btn in self.item_buttons:
            btn.config(text="0")
        #Cleras the values in the Number of Items wanted
        for segment in self.seven_segments:
            segment.config(text="0")
        
        #set the outputs to default
        self.in_storage_label.config(text="0")
        self.able_to_craft_label.config(text="0")
        self.crafting_label.config(text="No")
        self.remaining_label.config(text="0")



if __name__ == "__main__":

    root = tk.Tk()

    app = CraftingTerminal(root)

    root.mainloop()