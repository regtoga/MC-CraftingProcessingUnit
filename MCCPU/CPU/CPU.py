class CraftingProcessingUnit:
    def __init__(self) -> None:
        pass

    def __del__(self) -> None:
        pass

    
    #CPU object Main Object in program:
    def CPU(self):
        """Run the algorithm in a loop
        each time its called do stuff with the info you have to route it to the crafters"""
        pass

    
    #Object takes a memory address and locates all the nessesary information related to it.
    #Items are stored in the same address as it is stored in memory so we just need to count the ammount of each item we need and send it to the proper place
    def Storage_MemoryController(self):
        pass

    #This is the Cashe of the CPU, it stores temporary data needed per item, i am planning on having enough cash to store about 6 recipies that are qued up for crafting an any given moment.
    def CasheController(self):
        pass

    #The CPU will send items/orders/andammounts to the crafters and the crafters will send the result back
    def Crafters(self):
        pass

    #The CPU will send items to be smelted to the furnesses and the furnesses will send the result back
    def Smelters(self):
        pass


