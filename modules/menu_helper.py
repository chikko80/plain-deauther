from termcolor import colored,cprint
from .decorator import base_menu,os_menu,scanner_menu
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
            "Deauther",
        ]
        self.mac_changer_menu = [
            "Back to main menu",
            "Set random address",
            "Set custom address",
            "Reset to original",
        ]
        self.deauther_menu = [
            "Back to main menu",
            "Scan Networks",
            "Set Channel (default channel-hopping)",
            "Set band (default 2.4GHz + 5GHz)",
            "Attack Network",
        ]
        self.attack_menu = [
            "Back to deauther menu",
            "Spoof MAC of a associated client",
            "Set Attack Type (default flood-all)",
            "Start Deauthentication :)",
        ]
        self.attack_type_menu = [
            "Deauth all clients (default,broadcast)",
            "Deauth each client separately (sometimes more efficient than broadcast)",
            "Deauth all clients except one (f.i yourself) ",
            "Deauth specific client",
        ]

    def read_option(self,option='option'):
        print(f"\nSelect {option}:\t",end="")
        while True:
            try:
                selected_option = int(input())
                if option == "interface":
                    if selected_option > len(self.manager.interfaces) or selected_option < 1:
                        raise ValueError
                elif option == "main_menu":
                    if selected_option < 1 or selected_option > len(self.main_menu):
                        raise ValueError
                elif option == 'mac_changer':
                    if selected_option < 1 or selected_option > len(self.mac_changer_menu):
                        raise ValueError
                elif option == 'device_menu':
                    if selected_option < 1 or selected_option > len(self.device_menu):
                        raise ValueError
                elif option == 'target_menu':
                    if selected_option < 1 or selected_option > len(self.manager.targets):
                        raise ValueError
                elif option == 'channel (0 for channel-hopping)':
                    if selected_option < 0 or selected_option > len(self.manager.chosen_interface.channels):
                        raise ValueError
                elif option == 'attack_menu':
                    if selected_option < 1 or selected_option > len(self.attack_menu):
                        raise ValueError
                elif option == 'attack_type_menu':
                    if selected_option < 1 or selected_option > len(self.attack_type_menu):
                        raise ValueError
                elif option == 'client':
                    if selected_option < 1 or selected_option > len(self.manager.chosen_target.clients):
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
    
    @os_menu
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

    @base_menu("red")
    def print_attack_menu(self):
        self.print_menu_options(self.attack_menu)

    @base_menu("red")
    def print_attack_type_menu(self):
        self.print_menu_options(self.attack_type_menu)

    @base_menu("blue")
    def print_associated_clients(self):
        self.print_menu_options(self.manager.chosen_target.return_clients_as_list())

    def print_menu_options(self,option_list,color="green"):
        print()
        for index,option in enumerate(option_list):
            cprint("{: <5} {: <10} ".format(f"{index+1}.",f"{option}"),color)
        print()
    
    @staticmethod
    @scanner_menu
    def print_targets(targets,final=False):
        if targets:
            for index,target in enumerate(targets,start=1):
                print(colored(str(index).rjust(5)),target.to_str())
            cprint("   --------------------------------------------------------")
            total_count = colored(str(len(targets)),'yellow')
            total_string = colored(f'Total: {total_count}','blue')
            pipe = colored(" | ",'red')
            if final:
                info_string = colored('Please select your target device by number','green')
            else:
                info_string = colored('If you found your target exit with Ctrl+C','red')
            print(f'    {total_string}{pipe}{info_string}')
        
    def print_table_row(self,row_as_list):
        if settings.mobile:
            print("{: <5} {: <5} {: <10} {: <10} {: <20}".format(*row_as_list))
        else:
            print("{: <5} {: <10} {: <15} {: <15} {: <20}".format(*row_as_list))

    def yes_no_question(self,message,option=["Yes/y","No/n"]):
        cprint(message,'yellow')
        printed_option = " - ".join(option)
        print(colored(f"{printed_option}:\t",'red'),end="")
        def get_options(option):
            yes = option[0].split('/')[1]
            no = option[1].split('/')[1]
            return yes,no
        yes,no = get_options(option)

        while True:
            try:
                selected_option = str(input()).lower()
                if selected_option == 0:
                    return selected_option
                if not (selected_option == yes or selected_option ==no):
                    raise ValueError
                if selected_option == yes:
                    return True
                else:
                    return False
                return selected_option
            except ValueError:
                clean_last_line()
                print(colored(f"{option}:\t",'red'),end="")

def print_message(message,color,time_delay=2,instant=False):
    cprint(message,color)
    if instant:
        return
    time.sleep(time_delay)


def clean_last_line():
    print ("\033[A                                                                                      \033[A")