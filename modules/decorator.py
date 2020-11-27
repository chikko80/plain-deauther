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
            clean_output()
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
                band_color = 'red'
                channel_color = 'red'
                band_color = 'red'
                target_color = 'red'
                seperator = colored("|",menu_color)
                si_label = colored('Selected interface:',menu_color)
                si = colored(f'{self.manager.chosen_interface.interface}',interface_color)
                mode_label = colored('Mode:',menu_color)
                mode = colored(f'{self.manager.chosen_interface.mode}',mode_color)
                mac_label = colored('MAC:',menu_color)
                mac = colored(f'{self.manager.chosen_interface.mac_address}',mac_color)
                state_label = colored('State:',menu_color)
                state = colored(f'{self.manager.chosen_interface.state}',state_color)
                band_label = colored('Supported Bands:',menu_color)
                supported_bands = ", ".join(self.manager.chosen_interface.bands)
                bands = colored(f'{supported_bands}',band_color)
                channel_label = colored('Channel:',menu_color)
                if self.manager.chosen_interface.chosen_channel:
                    ichannel = colored(f'{self.manager.chosen_interface.chosen_channel}',channel_color)
                if self.manager.chosen_interface.chosen_band:
                    cband_label = colored('Selected Band:',menu_color)
                    if self.manager.chosen_interface.chosen_band == 'a':
                        cband = colored('5GHz',band_color)
                    else:
                        cband = colored('2.4GHz',band_color)
                if self.manager.chosen_target:
                    target_label = colored('Target AP:',menu_color)
                    target = colored(f'{self.manager.chosen_target.essid if self.manager.chosen_target.essid else self.manager.chosen_target.bssid}',target_color)
                    target_channel = colored(f'{self.manager.chosen_target.channel}',target_color)
                if settings.mobile:
                    interface = f"{si_label} {si}" 
                    mode = f"{mode_label} {mode}"
                    mac = f"{mac_label} {mac}"
                    state = f"{state_label} {state}"
                    bands = f'{band_label} {bands}'
                    print("{: <50} {: <20} {: <20} ".format(interface,seperator,mode))
                    print("{: <50} {: <20} {: <20} ".format(mac,seperator,state))
                    print ("\033[A                                                                                      \033[A")
                    print("{: <50}".format(bands))
                else:
                    header_string = f"{si_label} {si} {seperator} {mode_label} {mode} {seperator} {mac_label} {mac} {seperator} {state_label} {state}{band_label} {bands}"
                    if self.manager.chosen_interface.chosen_channel:
                        chosen_channel_string = f' {seperator} {channel_label} {ichannel}' 
                        header_string += chosen_channel_string
                    if self.manager.chosen_interface.chosen_band:
                        chosen_band_string = f' {seperator} {cband_label} {cband}' 
                        header_string += chosen_band_string
                    if self.manager.chosen_target:
                        target_string = f'{seperator} {target_label} {target} {seperator} {channel_label} {target_channel}'
                        header_string += target_string
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
    [print() for _ in range(2)]
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


def print_default_colored_line(color):  
    cprint("--------------------------------------------------------------------------------------",color)

def print_mobile_colored_line(color):  
    cprint("-----------------------------------------------------------------",color)

def clean_output():
    os.system('cls' if os.name == 'nt' else 'clear')