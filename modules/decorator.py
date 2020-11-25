import os
from termcolor import cprint,colored

def __print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    [print() for _ in range(5)]
    cprint("--------------------------------------------------------------------------------------",'green')
    cprint("--------------------------------------------------------------------------------------",'green')
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
    cprint("--------------------------------------------------------------------------------------",'green')
    print()
    print()

def mobile_banner():
    print(
        """
_____ _____ _____ _____ _____ _____ _____ _____ 
|  _  |   __|  _  |  |  |_   _|  |  |   __| __  |
|   __|   __|     |  |  | | | |     |   __|    -|
|__|  |_____|__|__|_____| |_| |__|__|_____|__|__|
        """
    )

def base_menu(color):
    def function_wrapper(func):
        def draw_outlines(*args):
            self = args[0]
            __print_banner()
            __print_colored_line(color)
            if not self.manager.chosen_interface:
                cprint('Please select an interface:','yellow')
            else:
                menu_color = 'cyan'
                interface_color = 'red'
                mode_color = 'red'
                mac_color = 'red'
                state_color = 'red'
                seperator = colored(" | ",menu_color)
                si_label = colored('Selected interface: ',menu_color)
                si = colored(f'{self.manager.chosen_interface.interface}',interface_color)
                mode_label = colored('Mode: ',menu_color)
                mode = colored(f'{self.manager.chosen_interface.mode}',mode_color)
                mac_label = colored('MAC: ',menu_color)
                mac = colored(f'{self.manager.chosen_interface.mac_address}',mac_color)
                state_label = colored('State: ',menu_color)
                state = colored(f'{self.manager.chosen_interface.state}',state_color)
                print(f"{si_label}{si}{seperator}{mode_label}{mode}{seperator}{mac_label}{mac}{seperator}{state_label}{state}")
                # clean line,otherwise their will be a new line because string is at line limit
                print ("\033[A                                                                                      \033[A")
            __print_colored_line(color)
            func(*args)
            __print_colored_line(color)
        return draw_outlines
    return function_wrapper

def __print_colored_line(color):  
    cprint("--------------------------------------------------------------------------------------",color)


# def menu_outline_decorator(color):
#     def function_wrapper(func):
#         def draw_outlines(*args):
#             print_colored_line(color)
#             func(*args)
#             print_colored_line(color)
#         return draw_outlines
#     return function_wrapper