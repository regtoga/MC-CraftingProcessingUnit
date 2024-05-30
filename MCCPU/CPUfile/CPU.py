import sqlite3

import os



class CraftingProcessingUnit:

    def __init__(self):
        """Initialize the CPU and connect to the SQLite database"""
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Memory.db")
        self.address_bits_list = [[]]
        self.recipe_type_amount_per_craft_bits = []

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()



    def AddNewItemToMemory(self, address_bits: list[list[bool]], crafted_address_bits: list[bool], recipe_type_amount_per_craft: list[bool]):
        """This function takes the information from the RecipeTerminal and stores it in memory"""
        print(f"Submit button pressed with, address_bits: {address_bits}, crafted_address_bits: {crafted_address_bits}, recipe_type_amount_per_craft: {recipe_type_amount_per_craft}")

        # Convert crafted_address_bits to a string to use as table name
        crafted_address_bits_str = ''.join(map(str, map(int, crafted_address_bits)))

        # Check if the table for the crafted_address_bits already exists
        self.cursor.execute(f"""
            SELECT name FROM sqlite_master WHERE type='table' AND name='table_{crafted_address_bits_str}'
        """)

        table_exists = self.cursor.fetchone()

        # If the table exists, drop it first to replace with the new recipe
        if table_exists:
            self.cursor.execute(f"DROP TABLE IF EXISTS table_{crafted_address_bits_str}")
            self.conn.commit()

        # Create a new table for the crafted_address_bits
        self.cursor.execute(f"""
            CREATE TABLE table_{crafted_address_bits_str} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bit_list TEXT
            )
        """)

        self.conn.commit()

        # Insert the address bits and recipe type and amount per craft into the table
        # Convert the lists to strings for storage in the database
        for bit_list in address_bits + [recipe_type_amount_per_craft]:
            bit_list_str = ''.join(map(str, map(int, bit_list)))
            self.cursor.execute(f"""
                INSERT INTO table_{crafted_address_bits_str} (bit_list)
                VALUES (?)
            """, (bit_list_str,))

        self.conn.commit()

    def RetrieveDataFromMemory(self, crafted_address_bits: list[bool]):
        """This function takes the crafted_address_bits, retrieves data from the corresponding table, and sets the data to global variables"""
        # Convert crafted_address_bits to a string to use as table name
        crafted_address_bits_str = ''.join(map(str, map(int, crafted_address_bits)))

        # Check if the table for the crafted_address_bits exists
        self.cursor.execute(f"""
            SELECT name FROM sqlite_master WHERE type='table' AND name='table_{crafted_address_bits_str}'
        """)

        table_exists = self.cursor.fetchone()

        if not table_exists:
            print(f"No table found for the crafted address bits: {crafted_address_bits}")
            return

        # Retrieve data from the table
        self.cursor.execute(f"SELECT bit_list FROM table_{crafted_address_bits_str}")
        rows = self.cursor.fetchall()

        if len(rows) != 10:
            print(f"Expected 10 rows of data, but found {len(rows)}")
            return

        # Set variables
        self.address_bits_list = [list(map(int, row[0])) for row in rows[:9]]  # First 9 rows
        self.recipe_type_amount_per_craft_bits = list(map(int, rows[9][0]))    # 10th row

        print("------------------------------------")
        print("   recipe type / amount per craft  ")
        print(self.recipe_type_amount_per_craft_bits)
        print("               ------               ")
        counter = 1
        for i in self.address_bits_list:
            print(f"{counter}: {i}")
            counter += 1
        print("------------------------------------")

    def close(self):
        """Close the database connection"""
        self.conn.close()

    # CPU object Main Object in program
    def CPU(self):
        """Run the algorithm to craft an item, this may need to be recursive 
        each time its called do stuff with the info you have to route it to the crafters"""
        pass

    # Object takes a memory address and locates all the necessary information related to it.
    # Items are stored in the same address as it is stored in memory so we just need to count the amount of each item we need and send it to the proper place
    def Storage_MemoryController(self):
        pass

    # This is the Cache of the CPU; it stores temporary data needed per item; I am planning on having enough cache to store about 6 recipes that are queued up for crafting at any given moment
    def CacheController(self):
        pass

    # The CPU will send items/orders/amounts to the crafters, and the crafters will send the result back
    def Crafters(self):
        pass

    # The CPU will send items to be smelted to the furnaces, and the furnaces will send the result back
    def Smelters(self):
        pass