from termcolor import colored
from .interface import Interface
from .menu_helper import clean_last_line
import os
import re
import time

class Manager:

    def __init__(self):
        self.interfaces = []
        self.chosen_interface = None
              
    def read_interfaces(self):
        # print("airmon")
        self.read_airmon_information()
        # print("mac")
        self.read_mac_addresses()
        # print("state")
        self.read_interface_state()
        self.read_supported_bands()
    
    def read_airmon_information(self):
        self.interfaces = []
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

    def read_interface_state(self,interface=None):
        if interface:
            interface.state = os.popen(f"cat /sys/class/net/{interface.interface}/operstate").read()
        else:
            for interface in self.interfaces:
                interface.state = os.popen(f"cat /sys/class/net/{interface.interface}/operstate").read()


    def read_supported_bands(self,interface=None):
        def check_supp(output,band):
            for line in output.split("\n"):
                if line.strip().startswith("Channel"):
                    for col in line.split(":"):
                        if col[1].startswith(band):
                            return True
            return False
        def update_supported_bands(interface):
            interface.bands = []
            output = os.popen(f"iwlist {interface.interface} freq").read()
            if check_supp(output,'2'):
                interface.bands.append("2.4GHz")
            if check_supp(output,'5'):
                interface.bands.append("5GHz")

        if interface:
            update_supported_bands(interface)
        else:
            for interface in self.interfaces:
                update_supported_bands(interface)


    def update_device_informations(self,mode):
        self.read_interfaces()
        if mode == "monitor":
            target_mode = self.chosen_interface.interface + "mon"
        else:
            target_mode = self.chosen_interface.interface[:len(self.chosen_interface.interface)-3]

        for interface in self.interfaces:
            if target_mode == interface.interface:
                self.chosen_interface = interface
                return True
        return False 

    def check_trouble(self):
        output = os.popen("airmon-ng check").read()
        if len(output.split("\n")) > 3:
            output = output.replace(r"using 'airmon-ng check kill'","").replace('they will','they will maybe')
            return True,output
        else:
            return False,output

    def check_kill(self):
        output = os.popen("airmon-ng check kill").read()


    def select_interface(self,option):
        index = option - 1 
        self.chosen_interface = self.interfaces[index]
    
    def set_random_mac_address(self):
        self.set_interface_down()
        os.popen(f"macchanger -r {self.chosen_interface.interface} ").read()
        self.set_interface_up()
        self.read_mac_addresses(update_current=True)

    def set_custom_mac_address(self, custom_address):
        self.set_interface_down()
        os.popen(f"macchanger -m {custom_address} {self.chosen_interface.interface} ").read()
        self.set_interface_up()
        self.read_mac_addresses(update_current=True)

    def reset_mac_address(self):
        self.set_interface_down()
        os.popen(f"macchanger -p {self.chosen_interface.interface} ").read()
        self.set_interface_up()
        self.read_mac_addresses(update_current=True)

    #TODO check if up/down automatically
    def set_monitor_mode(self):
        os.popen(f"airmon-ng start {self.chosen_interface.interface}").read()
        return self.update_device_informations("monitor")
        
    def set_managed_mode(self):
        os.popen(f"airmon-ng stop {self.chosen_interface.interface}").read()
        return self.update_device_informations("managed")

    def set_interface_down(self):
        os.popen(f"ifconfig {self.chosen_interface.interface} down").read()

    def set_interface_up(self):
        os.popen(f"ifconfig {self.chosen_interface.interface} up").read()
    