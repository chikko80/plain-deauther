import os
from termcolor import cprint,colored
from settings import settings

def base_menu(color):
    def function_wrapper(func):
        def draw_outlines(*args):
            if settings.mobile:
                print_banner = print_mobile_banner
                print_colored_line = print_mobile_colored_line
            else:
                print_banner = print_default_banner
                print_colored_line = print_default_colored_line

            self = args[0]
            print_banner()
            print_colored_line(color)
            if not self.manager.chosen_interface:
                cprint('Please select an interface:','yellow')
            else:
                menu_color = 'cyan'
                interface_color = 'red'
                mode_color = 'red'
                mac_color = 'red'
                state_color = 'red'
                seperator = colored("|",menu_color)
                si_label = colored('Selected interface:',menu_color)
                si = colored(f'{self.manager.chosen_interface.interface}',interface_color)
                mode_label = colored('Mode:',menu_color)
                mode = colored(f'{self.manager.chosen_interface.mode}',mode_color)
                mac_label = colored('MAC:',menu_color)
                mac = colored(f'{self.manager.chosen_interface.mac_address}',mac_color)
                state_label = colored('State:',menu_color)
                state = colored(f'{self.manager.chosen_interface.state}',state_color)
                if settings.mobile:
                    interface = f"{si_label} {si}" 
                    mode = f"{mode_label} {mode}"
                    mac = f"{mac_label} {mac}"
                    state = f"{state_label} {state}"
                    print("{: <50} {: <20} {: <20} ".format(interface,seperator,mode))
                    print("{: <50} {: <20} {: <20} ".format(mac,seperator,state))
                else:
                    print(f"{si_label} {si} {seperator} {mode_label} {mode} {seperator} {mac_label} {mac} {seperator} {state_label} {state}")
                    # clean line,otherwise their will be a new line because string is at line limit
                print ("\033[A                                                                                      \033[A")
            print_colored_line(color)
            func(*args)
            print_colored_line(color)
        return draw_outlines
    return function_wrapper


def print_default_banner():
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


def print_mobile_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    [print() for _ in range(5)]
    cprint("-----------------------------------------------------------------","green")
    cprint("-----------------------------------------------------------------","green")
    cprint(
        """
,------.,------. ,---. ,--. ,--,--------,--.  ,--,------,------.  
|  .--. |  .---'/  O  \|  | |  '--.  .--|  '--'  |  .---|  .--. ' 
|  '--' |  `--,|  .-.  |  | |  |  |  |  |  .--.  |  `--,|  '--'.' 
|  | --'|  `---|  | |  '  '-'  '  |  |  |  |  |  |  `---|  |\  \  
`--'    `------`--' `--'`-----'   `--'  `--'  `--`------`--' '--' 
        """
    ,"red")
    print_mobile_colored_line("green")
    print(colored("----------------------- ",'green'),end='')
    print(colored("coded by chikko80",'red'),end="")
    cprint(" -----------------------",'green')
    print_mobile_colored_line("green")

def device_menu(func):
    def draw_start_banner(*args):
        print_mobile_colored_line('green')
        print_mobile_colored_line('green')
        cprint(
        """
██████╗ ███████╗ █████╗ ██╗   ██╗████████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔════╝██╔══██╗██║   ██║╚══██╔══╝██║  ██║██╔════╝██╔══██╗
██████╔╝█████╗  ███████║██║   ██║   ██║   ███████║█████╗  ██████╔╝
██╔═══╝ ██╔══╝  ██╔══██║██║   ██║   ██║   ██╔══██║██╔══╝  ██╔══██╗
██║     ███████╗██║  ██║╚██████╔╝   ██║   ██║  ██║███████╗██║  ██║
╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    ""","red",attrs=['blink']
        )
        print_mobile_colored_line("green")
        print(colored("----------------------- ",'green'),end='')
        print(colored("coded by chikko80",'red'),end="")
        cprint(" -----------------------",'green')
        print_mobile_colored_line("green")
        print_mobile_colored_line('yellow')
        cprint("Choose Version: ","blue")
        print_mobile_colored_line('yellow')

        func(*args)
    return draw_start_banner


def print_default_colored_line(color):  
    cprint("--------------------------------------------------------------------------------------",color)

def print_mobile_colored_line(color):  
    cprint("-----------------------------------------------------------------",color)

# def menu_outline_decorator(color):
#     def function_wrapper(func):
#         def draw_outlines(*args):
#             print_colored_line(color)
#             func(*args)
#             print_colored_line(color)
#         return draw_outlines
#     return function_wrapper