from termcolor import cprint,colored
from .decorator import banner_decorator,base_menu
import time
import re


class MenuHelper:

    def __init__(self,manager):
        self.manager = manager

    @banner_decorator
    @base_menu("blue")
    def print_interfaces(self,interfaces):
        table_prettifier(["",'PHY',"Interface","Driver","Chipset"])
        print()
        for interface in interfaces:
            table_prettifier(interface.return_as_list())


    def read_option(self,option='option'):
        print(f"\nSelect {option}:\t",end="")
        while True:
            try:
                selected_option = int(input())
                if option == "interface":
                    if selected_option > len(self.manager.interfaces) or selected_option < 1:
                        raise ValueError
                if option == "main_menu":
                    if selected_option < 0 or selected_option > 4:
                        raise ValueError
                return selected_option
            except ValueError:
                clean_last_line()
                clean_last_line()
                cprint(f"No valid input. Please select a valid {option}","red")
                print(f"Select {option}:\t",end="")

    def read_mac_address(self):
        valid_mac = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        regex = re.compile(valid_mac)
        print(f"Custom MAC:\t",end="")
        while True:
            try:
                selected_option = str(input())
                if selected_option == "0":
                    return False
                if not regex.match(selected_option):
                    raise ValueError
                return selected_option
            except ValueError:
                clean_last_line()
                clean_last_line()
                cprint(f"No valid input. Please enter a valid mac address","red")
                print(f"Custom MAC:\t",end="")
    

    @banner_decorator
    @base_menu("yellow")
    def print_main_menu_options(self):
        print()
        cprint("{: <5} {: <10} ".format("0.","Change interface"),'green')
        cprint("{: <5} {: <10} ".format("1.","Change mac-address"),'green')
        cprint("{: <5} {: <10} ".format("2.","Put in monitor mode"),'green')
        cprint("{: <5} {: <10} ".format("3.","Put in managed mode"),'green')
        cprint("{: <5} {: <10} ".format("4.","Scan Networks"),'green')
        print()

    @banner_decorator
    @base_menu("magenta")
    def print_mac_changer_menu(self):
        print()
        cprint("{: <5} {: <10} ".format("0.","Back to main menu"),'green')
        cprint("{: <5} {: <10} ".format("1.","Set random address"),'green')
        cprint("{: <5} {: <10} ".format("2.","Set custom address"),'green')
        cprint("{: <5} {: <10} ".format("3.","Reset to original"),'green')
        print()


def table_prettifier(row_as_list):
    print("{: <5} {: <10} {: <15} {: <15} {: <20}".format(*row_as_list))



def clean_last_line():
    print ("\033[A                                                                                      \033[A")