class Interface:

    def __init__(self,index,phy,interface,driver,chipset):
        self.index = index
        self.phy = phy
        self.interface = interface
        self.driver = driver
        self.chipset = chipset
        self.mode = "Monitor" if "mon" in self.interface else "Managed"
        self.mac_address = None
        self.state = None
        self.bands = []

    def __str__(self):
        return "Index: " + self.index + "\n" + "PHY: " + self.phy + "\n" +"Interface: " + self.interface + "\n" + "Driver: " + self.driver + "\n" +"Chipset: " + self.chipset + "\n" 

    def return_as_list(self):
        return [str(self.index + " : "),str(self.phy),str(self.interface),str(self.driver),str(self.chipset)]