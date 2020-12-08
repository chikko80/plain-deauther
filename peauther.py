#!/usr/bin/python3
import os
import sys
import time
from modules.menu_helper import MenuHelper, print_message
from modules.manager import Manager
from modules.decorator import clean_output
from settings import settings

manager = Manager()
menu_helper = MenuHelper(manager)


def menu():
    select_device()
    select_interface()
    main_menu()

def select_device():
    """ 
    Select your Platform PC or Mobile
    """ 
    menu_helper.print_device_menu()
    option = menu_helper.read_option(option='device_menu')
    if option == 1:
        settings.mobile = False
    else:
        settings.mobile = True

    
def select_interface():
    """ 
    Select your monitor- and injectionmode compatible interface (adapter, wifi-card)
    """ 
    manager.read_interfaces()
    menu_helper.print_interfaces(manager.interfaces)
    option = menu_helper.read_option(option="interface")
    manager.select_interface(option)


def main_menu():
    """ 
    Go to macchanger menu, set interface in monitor or managed mode, go to deauther menu
    """ 
    menu_helper.print_main_menu_options()
    option = menu_helper.read_option(option="main_menu")
    # back to interface selection
    if option == 1:
        select_interface()
        return main_menu()

    # go to macchanger menu 
    elif option == 2:
        return mac_changer_menu()        
    
    # set interface in monitor mode
    elif option == 3:
        if manager.in_monitor_mode():
            return main_menu()
        check_trouble()
        print_message("Putting into monitor mode..",'yellow')
        manager.set_monitor_mode()
        return main_menu()

    # set interface in managed mode
    elif option == 4:
        manager.set_managed_mode()
        return main_menu()

    # go to deather menu
    elif option == 5:
        return deauther_menu()


def mac_changer_menu():
    """ 
    Change your mac address to a random, custom mac or reset to hardware mac
    """ 
    menu_helper.print_mac_changer_menu() 
    option = menu_helper.read_option(option="mac_changer")
    # back to main menu
    if option == 1:
        return main_menu()

    # set random mac
    elif option == 2:
        manager.set_random_mac_address()
        return main_menu()

    # enter custom mac address
    elif option == 3:
        input_address = menu_helper.read_mac_address()
        if not input_address:
            return main_menu()
        manager.set_custom_mac_address(input_address)
        return main_menu()

    # reset mac to hardwareaddress
    elif option == 4:
        manager.reset_mac_address()
        return main_menu()

def deauther_menu():
    """ 
    Start target scan, set your target channel or band, go to attack menu
    """ 
    menu_helper.print_deauther_menu()
    option = menu_helper.read_option(option="deauther_menu")
    # back to main menu
    if option == 1:
        return main_menu()

    # start scan
    elif option == 2:
        success = manager.start_scan()
        if not success:
            return deauther_menu()
        menu_helper.print_targets(manager.targets,final=True)
        inner_option = menu_helper.read_option(option='target_menu')
        manager.select_target(inner_option) 
        return attack_menu()

    # change channel
    elif option == 3:
        inner_option = menu_helper.read_option(option='channel (0 for channel-hopping)')
        manager.select_channel(inner_option) 
        return deauther_menu()

    # change band
    elif option == 4:
        inner_option = menu_helper.yes_no_question("Select a band (0 for default) ",option=["2.4GHz/2","5GHz/5"])
        manager.select_band(inner_option)
        return deauther_menu()

    #go to attack menu
    elif option == 5:
        if not manager.chosen_target:
            print_message("Please select a target first..",'red')
            return deauther_menu()
        return attack_menu()

def attack_menu():
    """
    Spoof mac address of a scanned client, set attack type, start deauthentication
    """
    menu_helper.print_attack_menu()
    option = menu_helper.read_option(option="attack_menu")
    # back to deauther menu
    if option == 1:
        return deauther_menu()

    # Spoof mac address 
    elif option == 2:
        if not manager.clients_exists():
            return deauther_menu()
        menu_helper.print_associated_clients()
        inner_option = menu_helper.read_option(option="client")
        manager.spoof_mac_address_of_client(inner_option)
        return attack_menu()
    
    # Set attack type
    elif option == 3:
        menu_helper.print_attack_type_menu()
        attack_type_option = menu_helper.read_option(option="attack_type_menu")

        # attack type: deauth all except one client
        if attack_type_option == 3:
            # choose mac from interfaces (for example your wlan0 that have a connection to target ap) or enter custom mac
            custom = menu_helper.yes_no_question('Target client: Specify custom mac or choose one interfaces',option=['Custom/c','Interfaces/i'])
            if custom:
                print_message("MAC-Address to ignore (abort with 1): \n",'yellow',instant=True)
                mac = menu_helper.read_mac_address()
                if not mac:
                    return attack_menu()
                manager.ignore_mac = mac
            else:
                #choose interface
                menu_helper.print_interfaces(manager.interfaces)
                option = menu_helper.read_option(option="interface_exception")
                manager.ignore_mac = manager.interfaces[option-1].mac_address

        # attack type: deauth specific client
        if attack_type_option == 4:
            # choose mac from scanned clients results or enter custom mac
            custom = menu_helper.yes_no_question('Target client: Specify custom mac or choose one from scan results (abort with 1)',option=['Custom/c','Scanned/s'])
            if custom:
                # enter custom mac
                mac = menu_helper.read_mac_address()
                if not mac:
                    return attack_menu()
                manager.target_client = mac
            else:
                # choose interface
                menu_helper.print_associated_clients()
                inner_option = menu_helper.read_option(option="client")
                manager.select_target_client(inner_option)
        manager.select_attack_type(attack_type_option)
        return attack_menu()

    # Start deauth attack with provided options
    elif option == 4:
        manager.start_deauth_attack()
        return attack_menu()


def check_trouble():
    """
    check for processes that could cause trouble with "airmon-ng check kill"
    """
    trouble,output = manager.check_trouble()
    if trouble and output:
        output = output + "Your other interfaces will probably lose their internet connection.."
        yes = menu_helper.yes_no_question(output)
        if yes:
            manager.check_kill()


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        # clean_output()
        print()
        sys.exit(0)