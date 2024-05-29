#Import required libraries
import tkinter as tk

class RecipeTerminal:
    def __init__(self, root):
        """The Recipe Terminal is a GUI that programs a recipe into the CraftingProcessingUnit"""
        self.root = root

        #name of the GUI
        if __name__ == "__main__":
            self.root.title("Recipe Terminal")


        #This var is where we are currently editing inside the address bits array
        self.current_index = 1

        #This array stores the nine required memory locations for each spot in the crafting table
        self.address_bits = [[0] * 10 for _ in range(9)]

        #this array stores the memory location of the output item
        self.crafted_address_bits = [0] * 10

        #set up the GUI
        self.setup_gui()



    def setup_gui(self):
        """This Function is used to setup the elements inside the GUI"""

        #Create Crafting/Smelting Toggle frame
        self.crafting_frame = tk.Frame(self.root)
        #Crafting/Smelting Label
        self.crafting_label = tk.Label(self.crafting_frame, text="Crafting/Smelting:")
        #Crafting/Smelting toggle button
        self.toggle_button = tk.Button(self.crafting_frame, text="Crafting", width=10, command=self.toggle_crafting_smelting)

        #Grid the frame that holds all widgets related to the crafting/Smelting toggle
        self.crafting_frame.grid(row=0, column=0, padx=10, pady=10)
        #Grid the label for the toggle button to the left of the button
        self.crafting_label.grid(row=0, column=0)
        #Grid the toggle button to the right of its label
        self.toggle_button.grid(row=0, column=1)

        #----

        #Create the frame that will hold the 10 toggle buttons for the inputs address
        self.address_input_frame = tk.LabelFrame(self.root, text="Address Input", padx=10, pady=10)

        #Create a empty list to hold buttons that will be used to represent the location in memory where that item is located in both memory and storage
        self.address_buttons = []

        #creates 10 buttons to that will toggle themselves between 0 and 1 when clicked
        for i in range(10):

            #place the button into the address_input_frame with a default value of 0, when clicked it will toggle its value 
            btn = tk.Button(self.address_input_frame, text="0", width=3, command=lambda i=i: self.toggle_address_bit(i))

            #Grid each new button to the right of the last button
            btn.grid(row=0, column=i)

            #append the button to the list of buttons so that later when cycling though each of the nine memory addresses we can neatly revalue each of the buttons
            self.address_buttons.append(btn)

        #Create the change Address button that will rotate the addresses above though their nine states
        self.swap_button = tk.Button(self.address_input_frame, text="Change Address", width=15, command=self.swap_address)

        #This label is the stand in for the seven segment display that will exist in the redstone version
        self.current_item_label = tk.Label(self.address_input_frame, text="1", font=("Courier", 24))
        
        #Grid the address input frame below the Crafting/Smelting frame
        self.address_input_frame.grid(row=1, column=0, padx=10, pady=10)
        #Grid the swap button below the address buttons
        self.swap_button.grid(row=1, column=0, columnspan=5)
        #Grid the current item address label (seven segment display) to the right of the swap button
        self.current_item_label.grid(row=1, column=5, columnspan=5)


        #----

        #Creates the frame that holds all the widgets related to the Amount per craft
        self.amount_frame = tk.LabelFrame(self.root, text="Amount Made Per Craft", padx=10, pady=10)
        # creates the two seven segment displays for the output
        self.seven_segments_amount = [tk.Label(self.amount_frame, text="0", font=("Courier", 24), width=2, anchor="e") for _ in range(2)]
        #for each display, grids it to the right of the last
        for i, segment in enumerate(self.seven_segments_amount):
            segment.grid(row=0, column=i)

        #I am not fully shure what this line does, but my guess is attach the segment displays to the amount frame
        self.amount_buttons_frame = tk.Frame(self.amount_frame)

        #This array holds the information needed to construct the number pad
        numberpad_layout = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [0]]

        #for each row 
        for row_index, row in enumerate(numberpad_layout):
            #for each colum
            for col_index, num in enumerate(row):
                #make a button 
                btn = tk.Button(self.amount_buttons_frame, text=str(num), width=3, command=lambda num=num: self.update_amount(num))
                #if the button value is 0 it needs to be in the center of the column
                #else grid then side by side
                if num == 0:
                    btn.grid(row=row_index + 1, column=col_index+1)
                else:
                    btn.grid(row=row_index + 1, column=col_index)

        #Creates the button that clears seven segment displays
        self.clear_amount_button = tk.Button(self.amount_frame, text="Clear Amount", width=15, command=self.clear_amount)

        #Grids the amount frame in the 3rd row below the address input frame
        self.amount_frame.grid(row=2, column=0, padx=10, pady=10)
        #puts the number pad below the two seven segment displays for the ammount crafted displays
        self.amount_buttons_frame.grid(row=1, columnspan=2)
        #grids the button that clears the ammount crafted displays under the number pad
        self.clear_amount_button.grid(row=2, columnspan=2)

        #----        

        #Create a frame to hold things related to "Crafted Resource Address"
        self.crafted_address_frame = tk.LabelFrame(self.root, text="Crafted Resource Address", padx=10, pady=10)

        #Create an empty array to hold the binary address
        self.crafted_address_buttons = []

        #create 10 buttons that when clicked toggle from 0 to 1 and from 1 to 0
        for i in range(10):
            #when clicked button will flip its bit
            btn = tk.Button(self.crafted_address_frame, text="0", width=3, command=lambda i=i: self.toggle_crafted_address_bit(i))
            #grid the button to the right of the last one
            btn.grid(row=0, column=i)
            #append the button to a list of all the buttons so that later we can easily iterate though the list and change thier values
            self.crafted_address_buttons.append(btn)

        #set the location of this frame below the ammount frame
        self.crafted_address_frame.grid(row=3, column=0, padx=10, pady=10)

        #---- 

        #Creates the frame to hold the Submit and Clear Buttons
        self.submit_clear_frame = tk.Frame(self.root)

        #create a submit and clear button
        self.submit_button = tk.Button(self.submit_clear_frame, text="Submit", width=10, command=self.submit)
        self.clear_button = tk.Button(self.submit_clear_frame, text="Clear", width=10, command=self.clear_all)

        #grid the submit/clear frame below the created address frame
        self.submit_clear_frame.grid(row=4, column=0, padx=10, pady=10)
        #grid the submit button to the left of the clear button
        self.submit_button.grid(row=0, column=0)
        self.clear_button.grid(row=0, column=1)

        #---- 

        #Create the outputs frame
        self.output_frame = tk.LabelFrame(self.root, text="Output", padx=10, pady=10)
        #Create the working label, output for the computer to comunicate that it is currently doing something
        self.working_label = tk.Label(self.output_frame, text="No")

        #Grid the output frame below the submit/clear frame
        self.output_frame.grid(row=5, column=0, padx=10, pady=10)
        #create a label to label on the left of the working label
        tk.Label(self.output_frame, text="Working?").grid(row=0, column=0)
        #grid the working label to the right of the label for the working label
        self.working_label.grid(row=0, column=1)



    def toggle_crafting_smelting(self):
        """
        This function set the text on the crafting smelting button to the opposite of what it is right now,
        Then it disables the swap button, and calls the reset to first address function, which just sets the current address in the address input to the first one.
        """
        #check if the text of the crafting/smelting button is == to 'Crafting'
        if self.toggle_button.config('text')[-1] == 'Crafting':
            #if they are set th text to Smelting and disable the swap button
            self.toggle_button.config(text="Smelting")
            self.swap_button.config(state=tk.DISABLED)
        else:
            #if they arn't set the text to Crafting and enable the swap button
            self.toggle_button.config(text="Crafting")
            self.swap_button.config(state=tk.NORMAL)

        # Reset current_index and update the display
        self.reset_to_first_address()



    def toggle_address_bit(self, idx):
        """Takes a address_bit button and flips it's bit"""
        #get the button's value
        current_text = self.address_buttons[idx].cget("text")
        #if the value is 0 set it to 1 
        #else set it to 0
        new_val = "1" if current_text == "0" else "0"
        #set the button's value to the new value
        self.address_buttons[idx].config(text=new_val)
        #updates the value of the bit being changed in the 9x10 array of crafting table inputs
        self.address_bits[self.current_index - 1][idx] = int(new_val)



    def swap_address(self):
        """if the nine accesable addresses in memory are a drum and the nine addresses are on the face of the drum and we can only see one line of text on the drum...
        then we are rotating the drumm to see the next address"""
        #by default the address is 1, so when this function is called we add one to that number to get the 2 and so on
        self.current_index += 1

        #if the current index is greater than the maximum index allowed reset the number to its defalt
        if self.current_index > 9:
            self.current_index = 1

        #set the value of the seven segment display to to current index value
        self.current_item_label.config(text=str(self.current_index))

        #Update the 10 address bits to the values they should be.
        self.update_address_buttons()



    def update_address_buttons(self):
        """Update the 10 address bits to the values they should be baised off the self.address_bits 2d list"""
        #select the array inside the address_bits array baised off the global current index variable
        #this selected array holds the remembered 10 bits for a memory location
        current_bits = self.address_bits[self.current_index - 1]

        #iterate though the list and set each of the buttons text to the corrosponding value inside the list
        for i, bit in enumerate(current_bits):
            self.address_buttons[i].config(text=str(bit))



    def toggle_crafted_address_bit(self, idx):
        """Takes a crafted_address button and flips it's bit"""
        #get the button's value
        current_text = self.crafted_address_buttons[idx].cget("text")
        #if the value is 0 set it to 1 
        #else set it to 0
        new_val = "1" if current_text == "0" else "0"
        #set the button's value to the new value
        self.crafted_address_buttons[idx].config(text=new_val)
        #updates the value of the bit being changed inside the array keeping track of that
        self.crafted_address_bits[idx] = int(new_val)



    def update_amount(self, num):
        """
        this button is called from one of the number pad's number buttons
        it takes the value of the button clicked adds it to a place shifted version of the last number
        """
        #Get the current number baised off of the values of the seven segment displays 
        current_number = int("".join(segment.cget("text") for segment in self.seven_segments_amount))
        #Shift the current number left a digit and add the current number to it
        #Works like a microwave display
        new_number = current_number * 10 + num
        #if the new number is larger than 64 change nothing because minecraft stacks cant be over 64 items large
        if new_number > 64:
            new_number = 64
        #takes the number and makes it a string 
        new_str_num = "{:02}".format(new_number)
        #for each segment in the seven segment display make the text the value of the current char in the number
        for i, segment in enumerate(self.seven_segments_amount):
            segment.config(text=new_str_num[i])



    def clear_amount(self):
        """Clears the ammount inside the ammount per craft displays"""
        #for each seven segment display set the value to 0
        for segment in self.seven_segments_amount:
            segment.config(text="0")



    def clear_all(self):
        """clears the values of everything to program default"""

        #clears the 2d list of all its memory values
        for bit in self.address_bits:
            #for each bit in each of the 9 memory addresses set the value to 0
            for i in range(10):
                bit[i] = 0

        #Update the addressbits visual representation
        self.update_address_buttons()

        #Clears the memory address for the crafted resourse address visual representation
        for btn in self.crafted_address_buttons:
            btn.config(text="0")
        #clear the data attatched to each of the memory bits
        self.crafted_address_bits = [0] * 10

        #Clear the ammount inside the ammount made per craft display
        self.clear_amount()

        #Make shure the Crafting button is on by default
        self.toggle_button.config(text="Crafting")
        self.swap_button.config(state=tk.NORMAL)

        #Reset the nine address wheel to the first address in the wheel 
        self.reset_to_first_address()



    def submit(self):
        """Submit button's function to submit current data to the CraftingProcessingUnit"""
        # Collect the recipe type
        recipe_type = self.toggle_button.cget("text")

        # Collect address bits
        address_bits = self.address_bits
        crafted_address_bits = self.crafted_address_bits

        # Collect amount made per craft
        amount_per_craft = int("".join(segment.cget("text") for segment in self.seven_segments_amount))

        # Placeholder for submit logic
        print(f"Submit button pressed with recipe_type: {recipe_type}, address_bits: {address_bits}, crafted_address_bits: {crafted_address_bits}, amount_per_craft: {amount_per_craft}")

        # After the data has been submitted, clear all the displays
        self.clear_all()



    def reset_to_first_address(self):
        """Resets the current index of the 9 address scroller to 1 and updates the display"""
        #sets the current index to 1
        self.current_index = 1
        #sets the lable's value to 1 to show that we are looking at the first fow in the matrix of addresses
        self.current_item_label.config(text="1")
        #update the display button bits to reflect the values of the maxtrix level we are on
        self.update_address_buttons()



if __name__ == "__main__":

    root = tk.Tk()

    app = RecipeTerminal(root)

    root.mainloop()