import os
from termcolor import cprint
from .interface import Interface
from .menu import clean_last_line
class Manager:

    def __init__(self):
        self.interfaces = []
        self.choosen_interface = None

    def read_interfaces(self):
        output = os.popen("airmon-ng").read()
        output = output.split("\n")
        index = 1
        for counter,line in enumerate(output):
            if counter > 2 and line.startswith("phy"):
                splitted_line = line.split("\t")
                remove_empty = [word for word in splitted_line if word]
                interface = Interface(str(index),remove_empty[0],remove_empty[1],remove_empty[2],remove_empty[3])
                self.interfaces.append(interface)
                index +=1
        self.assign_mac_address()

    def assign_mac_address(self):
        for interface in self.interfaces:
            output = os.popen("").read()


    def select_interface(self,option):
        index = option - 1 
        self.choosen_interface = self.interfaces[index]
        clean_last_line()
        cprint(f'Selected interface: {self.choosen_interface.interface}\t|\tMode: {self.choosen_interface.mode}','yellow')
            
    
    