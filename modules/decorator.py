import os
from termcolor import cprint,colored

def banner_decorator(function):
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
    def banner(*args):
        clear()
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
        function(*args)
    return banner

# def menu_outline_decorator(color):
#     def function_wrapper(func):
#         def draw_outlines(*args):
#             print_colored_line(color)
#             func(*args)
#             print_colored_line(color)
#         return draw_outlines
#     return function_wrapper

def base_menu(color):
    def function_wrapper(func):
        def draw_outlines(*args):
            self = args[0]
            print_colored_line(color)
            if not self.manager.chosen_interface:
                cprint('Please select an interface:','yellow')
            else:
                cprint(f'Selected interface: {self.manager.chosen_interface.interface}   |   Mode: {self.manager.chosen_interface.mode}   |   MAC: {self.manager.chosen_interface.mac_address}',color)
            print_colored_line(color)
            func(*args)
            print_colored_line(color)
        return draw_outlines
    return function_wrapper

def print_colored_line(color):  
    cprint("--------------------------------------------------------------------------------------",color)