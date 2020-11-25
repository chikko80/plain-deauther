from termcolor import cprint,colored
from .decorator import base_menu
import time
import re


class MenuHelper:

    def __init__(self,manager):
        self.manager = manager
        self.device_menu = [
            "Desktop"
            "Mobile"
        ]
        self.main_menu = [
            "Change interface",
            "Change mac-address",
            "Put in monitor mode",
            "Put in managed mode",
            "Scan Networks",
        ]
        self.mac_changer_menu = [
            "Back to main menu",
            "Set random address",
            "Set custom address",
            "Reset to original",
        ]
        
    def print_device_menu(self):
        cprint("Desktop or Mobile?","blue")
        self.print_menu_options(self.device_menu)

    @base_menu("blue")
    def print_interfaces(self,interfaces):
        self.print_table_row(["",'PHY',"Interface","Driver","Chipset"])
        print()
        for interface in interfaces:
            self.print_table_row(interface.return_as_list())

    def read_option(self,option='option'):
        print(f"\nSelect {option}:\t",end="")
        while True:
            try:
                selected_option = int(input())
                if option == "interface":
                    if selected_option > len(self.manager.interfaces) or selected_option < 1:
                        raise ValueError
                if option == "main_menu":
                    if selected_option < 1 or selected_option > len(self.main_menu):
                        raise ValueError
                if option == 'mac_changer':
                    if selected_option < 1 or selected_option > len(self.mac_changer_menu):
                        raise ValueError
                if option == 'device_menu':
                    if selected_option < 1 or selected_option > len(self.device_menu):
                        raise ValueError
                return selected_option
            except ValueError:
                clean_last_line()
                clean_last_line()
                cprint(f"No valid input. Please select a valid option","red")
                print(f"Select {option}:\t",end="")

    def read_mac_address(self):
        valid_mac = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        regex = re.compile(valid_mac)
        print(f"Custom MAC:\t",end="")
        while True:
            try:
                selected_option = str(input())
                if selected_option == "1":
                    return False
                if not regex.match(selected_option):
                    raise ValueError
                return selected_option
            except ValueError:
                clean_last_line()
                clean_last_line()
                cprint(f"No valid input. Please enter a valid mac address","red")
                print(f"Custom MAC:\t",end="")
    

    @base_menu("yellow")
    def print_main_menu_options(self):
        self.print_menu_options(self.main_menu)

    @base_menu("magenta")
    def print_mac_changer_menu(self):
        self.print_menu_options(self.mac_changer_menu)

    def print_menu_options(self,option_list,color="green"):
        print()
        for index,option in enumerate(option_list):
            cprint("{: <5} {: <10} ".format(f"{index+1}.",f"{option}"),color)
        print()

    def print_table_row(self,row_as_list):
        print("{: <5} {: <10} {: <15} {: <15} {: <20}".format(*row_as_list))


def clean_last_line():
    print ("\033[A                                                                                      \033[A")