import os
from termcolor import cprint,colored
from settings import settings
from modules.menu_helper import print_message

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
            clean_output()
            print_banner()
            print_colored_line(color)
            if not self.manager.chosen_interface:
                cprint('Please select an interface:','yellow')
            else:
                def colorize_menu_part(s):
                    return colored(s,'cyan')
                interface_color = mode_color = mac_color = state_color = band_color = channel_color = target_color = 'red'
                seperator = colorize_menu_part("|")
                si_label = colorize_menu_part('Selected interface:')
                si = colored(self.manager.chosen_interface.interface,interface_color)
                mode_label = colorize_menu_part("Mode:")
                mode = colored(self.manager.chosen_interface.mode,mode_color)
                mac_label = colorize_menu_part('MAC:')
                mac = colored(self.manager.chosen_interface.mac_address,mac_color)
                state_label = colorize_menu_part("State:")
                state = colored(self.manager.chosen_interface.state,state_color)
                band_label = colorize_menu_part("Supported Bands:")
                supported_bands = ", ".join(self.manager.chosen_interface.bands)
                bands = colored(supported_bands,band_color)
                #TODO for mobile
                at_label = colorize_menu_part("Attack Type:")
                attack_type = colored(self.manager.get_attack_type(),'red')
                if self.manager.chosen_interface.chosen_channel:
                    channel_label = colorize_menu_part("Channel:")
                    ichannel = colored(self.manager.chosen_interface.chosen_channel,channel_color)
                if self.manager.chosen_interface.chosen_band:
                    cband_label = colorize_menu_part("Selected Band:")
                    if self.manager.chosen_interface.chosen_band == 'a':
                        cband = colored('5GHz',band_color)
                    else:
                        cband = colored('2.4GHz',band_color)
                if self.manager.chosen_target:
                    target_label = colorize_menu_part("Target AP:")
                    target = colored(f'{self.manager.chosen_target.essid if self.manager.chosen_target.essid else self.manager.chosen_target.bssid}',target_color)
                    tchannel_label = colorize_menu_part("APChannel:")
                    target_channel = colored(self.manager.chosen_target.channel,target_color)
                if self.manager.target_client:
                    #TODO for mobile
                    tc_label = colorize_menu_part("Target Client:")
                    target_client = colored(self.manager.target_client,'red')
                if self.manager.ignore_mac:
                    #TODO for mobile
                    ic_label = colorize_menu_part("Ignore Client:")
                    ignore_mac = colored(self.manager.ignore_mac,'red')
                if settings.mobile:
                    interface = f"{si_label} {si}" 
                    mode = f"{mode_label} {mode}"
                    mac = f"{mac_label} {mac}"
                    state = f"{state_label} {state}"
                    bands = f'{band_label} {bands}'
                    if self.manager.chosen_interface.chosen_channel:
                        ichannel = f'{channel_label} {ichannel}'
                    else: ichannel = ''
                    if self.manager.chosen_interface.chosen_band:
                        cband = f'{cband_label} {cband}'
                    else: cband = ''
                    if self.manager.chosen_target:
                        target = f'{target_label} {target}'
                        tchannel = f'{tchannel_label} {target_channel}'
                    else:
                        target = ''
                        tchannel = ''
                    print("{: <50} {: <20} {: <20} ".format(interface,seperator,mode))
                    print("{: <50} {: <20} {: <20} ".format(mac,seperator,state))
                    print ("\033[A                                                                                     \033[A")
                    print("{: <50} {: <20}".format(bands,seperator))
                    if ichannel:
                        print("{: <50} {: <20}".format(ichannel,seperator))
                    if cband:
                        print("{: <50} {: <20}".format(cband,seperator))
                    if target or tchannel:
                        print("{: <50} {: <20} {: <20} ".format(target,seperator,tchannel))
                else:
                    header_string = f"{si_label} {si} {seperator} {mode_label} {mode} {seperator} {mac_label} {mac} {seperator} {state_label} {state}{band_label} {bands} {seperator} {at_label} {attack_type}\n"
                    if self.manager.chosen_interface.chosen_channel:
                        chosen_channel_string = f' {seperator} {channel_label} {ichannel}' 
                        header_string += chosen_channel_string
                    if self.manager.chosen_interface.chosen_band:
                        chosen_band_string = f' {seperator} {cband_label} {cband}' 
                        header_string += chosen_band_string
                    if self.manager.chosen_target:
                        target_string = f' {seperator} {target_label} {target} {seperator} {tchannel_label} {target_channel}'
                        header_string += target_string
                    if self.manager.target_client:
                        target_client_string = f' {seperator} {tc_label} {target_client}' 
                        header_string += target_client_string
                    if self.manager.ignore_mac:
                        ignore_mac = f' {seperator} {ic_label} {ignore_mac}' 
                        header_string += ignore_mac
                    print(header_string)
                        
                    # clean line,otherwise their will be a new line because string is at line limit
                # print ("\033[A                                                                                      \033[A")
            print_colored_line(color)
            func(*args)
            print_colored_line(color)
        return draw_outlines
    return function_wrapper


def print_default_banner():
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

def start_decorator(func):
    #TODO maybe clear
    def inner(*args):
        print_message('Starting attack...','green',time_delay=1)
        print_message('Stop attack with Ctrl+C...','red',time_delay=2)
        func(*args)
    return inner

def print_default_colored_line(color):  
    cprint("--------------------------------------------------------------------------------------",color)

def print_mobile_colored_line(color):  
    cprint("-----------------------------------------------------------------",color)

def clean_output():
    os.system('cls' if os.name == 'nt' else 'clear')