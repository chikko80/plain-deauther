import os
from termcolor import cprint
from .interface import Interface
from .menu import clean_last_line
import re
class Manager:

    def __init__(self):
        self.interfaces = []
        self.chosen_interface = None
              
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
        self.read_mac_addresses()

    def read_mac_addresses(self,update_current=False):    
        if update_current:
            output = os.popen(f"ip link show {self.chosen_interface.interface}").read()
            addr = re.search(r"([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})",output).group(0)
            self.chosen_interface.mac_address = addr.upper()
        else:
            for interface in self.interfaces:
                output = os.popen(f"ip link show {interface.interface}").read()
                addr = re.search(r"([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})",output).group(0)
                interface.mac_address = addr.upper()

    def select_interface(self,option):
        index = option - 1 
        self.chosen_interface = self.interfaces[index]
    
    def set_random_mac_address(self):
        os.popen(f"ifconfig {self.chosen_interface.interface} down").read()
        os.popen(f"macchanger -r {self.chosen_interface.interface} ").read()
        os.popen(f"ifconfig {self.chosen_interface.interface} up").read()
        self.read_mac_addresses(update_current=True)

    
    def set_custom_mac_address(self, custom_address):
        os.popen(f"ifconfig {self.chosen_interface.interface} down").read()
        os.popen(f"macchanger -m {custom_address} {self.chosen_interface.interface} ").read()
        os.popen(f"ifconfig {self.chosen_interface.interface} up").read()
        self.read_mac_addresses(update_current=True)

    def reset_mac_address(self):
        os.popen(f"ifconfig {self.chosen_interface.interface} down").read()
        os.popen(f"macchanger -p {self.chosen_interface.interface} ").read()
        os.popen(f"ifconfig {self.chosen_interface.interface} up").read()
        self.read_mac_addresses(update_current=True)
    
    def get_interface_state(self):
        output = os.popen(f"cat /sys/class/net/{self.chosen_interface.interface}/operstate").read()
        return output




            

        
    