from termcolor import colored,cprint
from .decorator import base_menu,device_menu,scanner_menu
import time
import re
from settings import settings

class MenuHelper:

    def __init__(self,manager):
        self.manager = manager
        self.device_menu = [
            "Desktop",
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
        self.deauther_menu = [
            "Scan Networks",
            "Set Channel (default channel-hopping)",
            "Set band (default 2.4GHz + 5GHz)",
            "Attack Networks",
        ]

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
                if option == 'target_menu':
                    if selected_option < 1 or selected_option > len(self.manager.targets):
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
    
    @device_menu
    def print_device_menu(self):
        self.print_menu_options(self.device_menu)

    @base_menu("cyan")
    def print_interfaces(self,interfaces):
        self.print_table_row(["",'PHY',"Interface","Driver","Chipset"])
        print()
        for interface in interfaces:
            self.print_table_row(interface.return_as_list())

    @base_menu("yellow")
    def print_main_menu_options(self):
        self.print_menu_options(self.main_menu)

    @base_menu("magenta")
    def print_mac_changer_menu(self):
        self.print_menu_options(self.mac_changer_menu)
    
    @base_menu("blue")
    def print_deauther_menu(self):
        self.print_menu_options(self.deauther_menu)

    def print_menu_options(self,option_list,color="green"):
        print()
        for index,option in enumerate(option_list):
            cprint("{: <5} {: <10} ".format(f"{index+1}.",f"{option}"),color)
        print()
    
    @staticmethod
    @scanner_menu
    def print_targets(targets):
        if targets:
            for index,target in enumerate(targets,start=1):
                print(colored(str(index).rjust(5)),target.to_str())
            cprint("   --------------------------------------------------------")
            total_count = colored(str(len(targets)),'yellow')
            total_string = colored(f'Total: {total_count}','blue')
            info_string = colored('If you found your target exit with Ctrl+C','red')
            print(f'    {total_string} {info_string}')
        
    def print_table_row(self,row_as_list):
        if settings.mobile:

            print("{: <5} {: <5} {: <10} {: <10} {: <20}".format(*row_as_list))
        else:
            print("{: <5} {: <10} {: <15} {: <15} {: <20}".format(*row_as_list))

    def yes_no_question(self,message,option="Yes/y - No/n"):
        cprint(message,'yellow')
        print(colored(f"{option}:\t",'red'),end="")
        while True:
            try:
                selected_option = str(input()).lower()
                if not (selected_option == "y" or selected_option =="n"):
                    raise ValueError
                if selected_option == 'y':
                    return True
                else:
                    return False
                return selected_option
            except ValueError:
                clean_last_line()
                print(colored(f"{option}:\t",'red'),end="")


def clean_last_line():
    print ("\033[A                                                                                      \033[A")