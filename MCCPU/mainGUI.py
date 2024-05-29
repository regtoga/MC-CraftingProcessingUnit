#import nessesary libraries
import tkinter as tk

from CraftingTerminal import CraftingTerminal
from RecipeTerminal import RecipeTerminal
from FakeChest import FakeChest



class MainApplication:
    def __init__(self, root):
        """The Main application that combines the CraftingTerminal and the RecipeTerminal"""
        self.root = root
        #name the program
        self.root.title("Combined Crafting and Recipe Terminal")

        # Frame for Crafting Terminal
        self.crafting_frame = tk.LabelFrame(self.root, text="Crafting Terminal")
        self.crafting_frame.grid(row=0, column=0, padx=10, pady=10)
        self.crafting_terminal = CraftingTerminal(self.crafting_frame)

        # Frame for Recipe Terminal
        self.recipe_frame = tk.LabelFrame(self.root, text="Recipe Terminal")
        self.recipe_frame.grid(row=0, column=1, padx=10, pady=10)
        self.recipe_terminal = RecipeTerminal(self.recipe_frame)

        # Frame for Fake Chest
        self.fake_chest = tk.LabelFrame(self.root, text="Fake Chest")
        self.fake_chest.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.fake_chest_terminal = FakeChest(self.fake_chest)


if __name__ == "__main__":
    #if standalone run the application!
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()