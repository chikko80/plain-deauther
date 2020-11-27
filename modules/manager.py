from termcolor import colored
from .interface import Interface
from .menu_helper import clean_last_line,print_message
from modules.scanner import Scanner
import os
import re
import time

class Manager:

    def __init__(self):
        self.interfaces = []
        self.chosen_interface = None
        self.targets = []
        self.chosen_target = None
        self.scanner = None

    def read_interfaces(self):
        # print("airmon")
        self.read_airmon_information()
        # print("mac")
        self.read_mac_addresses()
        # print("state")
        self.read_interface_state()
        self.read_supported_bands_and_channels()
    
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


    def read_supported_bands_and_channels(self,interface=None):
        def check_supp(interface): 
            output = os.popen(f"iwlist {interface.interface} freq").read()
            interface.bands = []
            interface.channels = []
            for line in output.split("\n"):
                if line.strip().startswith("Channel"):
                    for col in line.split(":"):
                        channel = col[0].split(' ')[1]
                        if channel.startswith("0"): 
                            channel = channel[1:]
                        interface.channels.append(channel)
                        if col[1].startswith("2") and "2.4GHz" not in interface.bands :
                            interface.bands.append("2.4GHz")
                            continue
                        if col[1].startswith("5") and "5GHz" not in interface.bands:
                            interface.bands.append("5GHz")
                            continue
        if interface:
            check_supp(interface)
        else:
            for interface in self.interfaces:
                check_supp(interface)


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
        success =  self.update_device_informations("monitor")
        if not success:
            print_message(f"Couldn't put '{self.chosen_interface.interface}' into monitor mode..")
            return False
        return True
        
    def set_managed_mode(self):
        os.popen(f"airmon-ng stop {self.chosen_interface.interface}").read()
        return self.update_device_informations("managed")

    def set_interface_down(self):
        os.popen(f"ifconfig {self.chosen_interface.interface} down").read()

    def set_interface_up(self):
        os.popen(f"ifconfig {self.chosen_interface.interface} up").read()
    
    def start_scan(self):
        if self.chosen_interface.mode != "Monitor":
            print_message("Interface not in monitor mode! Putting into monitor mode automatically..",'yellow')
            success =  self.set_monitor_mode()
            if not success:
                return False
        self.scanner = Scanner(self.chosen_interface)
        self.scanner.start_scan()
        if not self.scanner.targets:
            return False
        self.targets = self.scanner.targets
        self.scanner.delete_old_file()
        return True
    
    def select_target(self,option):
        self.chosen_target = self.targets[option-1]

    def select_band(self,option):
        self.chosen_target = None
        self.chosen_interface.chosen_channel = None
        if option == 0:
            self.chosen_interface.chosen_band = None
        if option == True:
            self.chosen_interface.chosen_band = "bg" 
        if option == False:
            self.chosen_interface.chosen_band = "a" 

    def select_channel(self,option):
        self.chosen_target = None
        self.chosen_interface.chosen_band = None
        if option == 0:
            self.chosen_interface.chosen_channel = None
        self.chosen_interface.chosen_channel = str(option)
