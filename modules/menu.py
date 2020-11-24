from termcolor import cprint,colored
import time
import re
class MenuHelper:

    def __init__(self,manager):
        self.manager = manager
        self.error_line = False
        self.last_print = 0

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
                if self.error_line:
                    clean_last_line()
                    self.error_line = False
                clean_last_line()
                return selected_option
            except ValueError:
                clean_last_line()
                clean_last_line()
                cprint(f"No valid input. Please select a valid {option}","red")
                print(f"Select {option}:\t",end="")
                self.error_line = True

    def read_mac_address(self):
        valid_mac = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        regex = re.compile(valid_mac)
        print(f"Custom MAC:\t",end="")
        while True:
            try:
                selected_option = str(input())
                if not regex.match(selected_option):
                    raise ValueError
                if self.error_line:
                    clean_last_line()
                    self.error_line = False
                clean_last_line()
                return selected_option
            except ValueError:
                clean_last_line()
                clean_last_line()
                cprint(f"No valid input. Please enter a valid mac address","red")
                print(f"Custom MAC:\t",end="")
                self.error_line = True

    def print_interfaces(self,interfaces):
        self.print_colored_line("blue")
        self.table_prettifier(["",'PHY',"Interface","Driver","Chipset"])
        print()
        for interface in interfaces:
            self.table_prettifier(interface.return_as_list())
        self.print_colored_line("blue")
    
    def table_prettifier(self,row_as_list):
        print("{: <5} {: <10} {: <15} {: <15} {: <20}".format(*row_as_list))

    def print_main_menu_options(self):
        self.print_colored_line('yellow')
        cprint(f'Selected interface: {self.manager.chosen_interface.interface}   |   Mode: {self.manager.chosen_interface.mode}   |   MAC: {self.manager.chosen_interface.mac_address}','yellow')
        self.print_colored_line('yellow')
        print()
        cprint("{: <5} {: <10} ".format("0.","Change interface"),'green')
        cprint("{: <5} {: <10} ".format("1.","Change mac-address"),'green')
        cprint("{: <5} {: <10} ".format("2.","Put in monitor mode"),'green')
        cprint("{: <5} {: <10} ".format("3.","Put in managed mode"),'green')
        cprint("{: <5} {: <10} ".format("4.","Scan Networks"),'green')
        print()
        self.print_colored_line('yellow')

    def print_mac_changer_menu(self):
        self.print_colored_line('magenta')
        cprint(f'Selected interface: {self.manager.chosen_interface.interface}   |   Mode: {self.manager.chosen_interface.mode}   |   MAC: {self.manager.chosen_interface.mac_address}','magenta')
        self.print_colored_line('magenta')
        print()
        cprint("{: <5} {: <10} ".format("0.","Back to main menu"),'green')
        cprint("{: <5} {: <10} ".format("1.","Set random address"),'green')
        cprint("{: <5} {: <10} ".format("2.","Set custom address"),'green')
        cprint("{: <5} {: <10} ".format("3.","Reset to original"),'green')
        # cprint("{: <5} {: <10} ".format("4.","xxxxxxxx"),'green')
        print()
        self.print_colored_line('magenta')

    def print_banner(self):
        print()
        print()
        self.print_colored_line("green")
        cprint("'########::'########::::'###::::'##::::'##:'########:'##::::'##:'########:'########::","red")
        cprint(" ##.... ##: ##.....::::'## ##::: ##:::: ##:... ##..:: ##:::: ##: ##.....:: ##.... ##:","red")
        cprint(" ##:::: ##: ##::::::::'##:. ##:: ##:::: ##:::: ##:::: ##:::: ##: ##::::::: ##:::: ##:",'red')
        cprint(" ########:: ######:::'##:::. ##: ##:::: ##:::: ##:::: #########: ######::: ########::",'red')
        cprint(" ##.....::: ##...:::: #########: ##:::: ##:::: ##:::: ##.... ##: ##...:::: ##.. ##:::",'red')
        cprint(" ##:::::::: ##::::::: ##.... ##: ##:::: ##:::: ##:::: ##:::: ##: ##::::::: ##::. ##::",'red')
        cprint(" ##:::::::: ########: ##:::: ##:. #######::::: ##:::: ##:::: ##: ########: ##:::. ##:",'red')
        cprint("..:::::::::........::..:::::..:::.......::::::..:::::..:::::..::........::..:::::..::",'red')
        cprint("--------------------------------------------------------------------------------------",'green')
        print(colored("--------------------------------- ",'green'),end='')
        print(colored("coded by chikko80",'red'),end="")
        cprint(" ----------------------------------",'green')
        self.print_colored_line("green")
        print()
        print()

    def print_colored_line(self,color):  
        cprint("--------------------------------------------------------------------------------------",color)

def clean_last_line():
    print ("\033[A                                                                                      \033[A")