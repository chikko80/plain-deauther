import os
import time
from termcolor import cprint,colored
from settings import settings

def base_menu(color):
    """
    base menu decorator function that draws a menu for desktop or mobile version
    """
    def function_wrapper(func):
        def draw_outlines(*args):
            if settings.mobile:
                print_banner = print_mobile_banner
                print_colored_line = print_mobile_colored_line
            else:
                print_banner = print_default_banner
                print_colored_line = print_default_colored_line

            self = args[0]
            clean_output()
            print_banner()
            print_colored_line(color)
            if not self.manager.chosen_interface:
                cprint('Please select an interface:','yellow')
            else:
                def colorize_menu_part(s):
                    return colored(s,'cyan')
                def colorize_vars_part(s):
                    return colored(s,'red')
                seperator = colorize_menu_part("|")
                se_interface = colorize_menu_part('Selected interface: ') + colorize_vars_part(self.manager.chosen_interface.interface)
                mode = colorize_menu_part("Mode: ") + colorize_vars_part(self.manager.chosen_interface.mode)
                mac = colorize_menu_part('MAC: ') + colorize_vars_part(self.manager.chosen_interface.mac_address)
                state = colorize_menu_part("State: ") + colorize_vars_part(self.manager.chosen_interface.state)
                bands  = colorize_menu_part("Supported Bands: ") + colorize_vars_part(", ".join(self.manager.chosen_interface.bands))
                attack_type = self.manager.get_attack_type()
                if settings.mobile:
                    if attack_type == 'Each sep. ex.':
                        attack_type = attack_type.replace("Each sep. ex.",'Each s.ex.')
                    elif attack_type == "Specific cl.":
                        attack_type = attack_type.replace("Specific cl.",'Spec. cl.')
                attack_type = colorize_menu_part("Attack Type: ") + colorize_vars_part(attack_type)
                if self.manager.chosen_interface.chosen_channel:
                    interface_channel = colorize_menu_part("Channel: ") + colorize_vars_part(self.manager.chosen_interface.chosen_channel)
                if self.manager.chosen_interface.chosen_band:
                    if self.manager.chosen_interface.chosen_band == 'a':
                        cband = colorize_vars_part('5GHz')
                    else:
                        cband = colorize_vars_part('2.4GHz')
                    se_band = colorize_menu_part("Selected Band: ") + cband
                if self.manager.chosen_target:
                    target = colorize_menu_part("Target AP: ") + colorize_vars_part(f'{self.manager.chosen_target.essid if self.manager.chosen_target.essid else self.manager.chosen_target.bssid}')
                    target_channel = colorize_menu_part("APChannel: ") + colorize_vars_part(self.manager.chosen_target.channel if self.manager.chosen_target.channel else "")
                if self.manager.target_client:
                    target_client = colorize_menu_part("Target Client: ") + colorize_vars_part(self.manager.target_client)
                if self.manager.ignore_mac:
                    ignore_mac = colorize_menu_part("Ignore Client: ") + colorize_vars_part(self.manager.ignore_mac)
                if settings.mobile:
                    print("{: <50} {: <17} {: <20} ".format(se_interface,seperator,mode))
                    print("{: <50} {: <17} {: <20} ".format(mac,seperator,state))
                    print("{: <50} {: <17} {: <20}".format(bands,seperator,attack_type))
                    if self.manager.chosen_interface.chosen_channel:
                        print("{: <50} {: <17}".format(interface_channel,seperator))
                    if self.manager.chosen_interface.chosen_band:
                        print("{: <50} {: <17}".format(se_band,seperator))
                    if self.manager.chosen_target:
                        print("{: <50} {: <17} {: <20} ".format(target,seperator,target_channel))
                    if self.manager.target_client:
                        print("{: <50} {: <17}".format(target_client,seperator))
                    if self.manager.ignore_mac:
                        print("{: <50} {: <17}".format(ignore_mac,seperator))
                else:
                    print("{: <50} {: <13} {: <34} {: <13} {: <43}".format(se_interface,seperator,mode,seperator,mac))
                    print("{: <50} {: <13} {: <34} {: <13} {: <43}".format(bands,seperator,state,seperator,attack_type))
                    if self.manager.chosen_target:
                        print("{: <50} {: <13} {: <34}".format(target,seperator,target_channel))
                    if self.manager.chosen_interface.chosen_channel:
                        print(interface_channel)
                    if self.manager.chosen_interface.chosen_band:
                        print(se_band)
                    if self.manager.target_client:
                        print(target_client)
                    if self.manager.ignore_mac:
                        print(ignore_mac)
                        
                    # clean line,otherwise their will be a new line because string is at line limit
                # print ("\033[A                                                                                      \033[A")
            print_colored_line(color)
            func(*args)
            print_colored_line(color)
        return draw_outlines
    return function_wrapper


def print_default_banner():
    """
    banner for desktop version
    """
    [print() for _ in range(5)]
    print_default_colored_line('green')
    print_default_colored_line('green')
    cprint(
    """
'########::'########::::'###::::'##::::'##:'########:'##::::'##:'########:'########::
 ##.... ##: ##.....::::'## ##::: ##:::: ##:... ##..:: ##:::: ##: ##.....:: ##.... ##:
 ##:::: ##: ##::::::::'##:. ##:: ##:::: ##:::: ##:::: ##:::: ##: ##::::::: ##:::: ##:
 ########:: ######:::'##:::. ##: ##:::: ##:::: ##:::: #########: ######::: ########::
 ##.....::: ##...:::: #########: ##:::: ##:::: ##:::: ##.... ##: ##...:::: ##.. ##:::
 ##:::::::: ##::::::: ##.... ##: ##:::: ##:::: ##:::: ##:::: ##: ##::::::: ##::. ##::
 ##:::::::: ########: ##:::: ##:. #######::::: ##:::: ##:::: ##: ########: ##:::. ##:
..:::::::::........::..:::::..:::.......::::::..:::::..:::::..::........::..:::::..::
    """
    ,'red')
    print_default_colored_line('green')
    print(colored("--------------------------------- ",'green'),end='')
    print(colored("coded by chikko80",'red'),end="")
    cprint(" ----------------------------------",'green')
    print_default_colored_line('green')
    print()
    print()


def print_mobile_banner():
    """
    banner for mobile version
    """
    [print() for _ in range(2)]
    print_mobile_colored_line("green")
    print_mobile_colored_line("green")
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

def os_menu(func):
    """
    start menu - platform selection 
    """
    def draw_start_banner(*args):
        clean_output()
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


def scanner_menu(func):
    """
    draws the outer menu while scanning
    """
    def header(*args,**kwargs):
        clean_output()
        #! for testing
        show_bssids = False
        # First row: columns
        cprint("   --------------------------------------------------------")
        num = colored('   NUM')
        essid = colored('                      ESSID')
        if show_bssids:
            bssid = colored('              BSSID')
        else:
            bssid = ""
        #removed wps
        rest = colored('   CH  ENCR  POWER  CLIENT')

        # Second row: separator
        sep = colored('   ---')
        sep2 = colored('  -------------------------')
        if show_bssids:
            sep3 = colored('  -----------------')
        else:
            sep3 = ""
        rest2 =  colored('  ---  ----  -----  ------')
        print(f'{num}{essid}{bssid}{rest}')
        print(f'{sep}{sep2}{sep3}{rest2}')
        func(*args,**kwargs)
        cprint("   --------------------------------------------------------")
    return header

def abort_information(two_times=False):
    """
    shows the abort information how to exit the scanner
    """
    def funcwrapper(func):
        #TODO maybe clear
        def inner(*args):
            cprint('Starting attack...','green')
            time.sleep(1)
            if two_times:
                cprint('Stop attack with DOUBLE Ctrl+C...','red')
                time.sleep(3)
            else:
                cprint('Stop attack with Ctrl+C...','red')
                time.sleep(2)
            func(*args)
        return inner
    return funcwrapper

def print_default_colored_line(color):  
    cprint("--------------------------------------------------------------------------------------",color)

def print_mobile_colored_line(color):  
    cprint("-----------------------------------------------------------------",color)

def clean_output():
    os.system('cls' if os.name == 'nt' else 'clear')