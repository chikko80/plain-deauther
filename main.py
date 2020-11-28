#!/usr/bin/python3
import os
import sys
import time
from modules.menu_helper import MenuHelper
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
    menu_helper.print_device_menu()
    option = menu_helper.read_option(option='device_menu')
    if option == 1:
        settings.mobile = False
    else:
        settings.mobile = True

    
def select_interface():
    manager.read_interfaces()
    menu_helper.print_interfaces(manager.interfaces)
    option = menu_helper.read_option(option="interface")
    manager.select_interface(option)

def mac_changer_menu():
    menu_helper.print_mac_changer_menu() 
    option = menu_helper.read_option(option="mac_changer")
    if option == 1:
        return main_menu()
    elif option == 2:
        manager.set_random_mac_address()
        return main_menu()
    elif option == 3:
        input_address = menu_helper.read_mac_address()
        if not input_address:
            return main_menu()
        manager.set_custom_mac_address(input_address)
        return main_menu()
    elif option == 4:
        manager.reset_mac_address()
        return main_menu()

def deauther_menu():
    menu_helper.print_deauther_menu()
    option = menu_helper.read_option(option="deauther_menu")
    if option == 1:
        return main_menu()
    elif option == 2:
        success = manager.start_scan()
        if not success:
            return deauther_menu()
        menu_helper.print_targets(manager.targets,final=True)
        option = menu_helper.read_option(option='target_menu')
        manager.select_target(option) 
        return attack_menu()
    elif option == 3:
        option = menu_helper.read_option(option='channel (0 for channel-hopping)')
        manager.select_channel(option) 
        return deauther_menu()
    elif option == 4:
        option = menu_helper.yes_no_question("Select a band (0 for default) ",option=["2.4GHz/2","5GHz/5"])
        manager.select_band(option)
        return deauther_menu()
    elif option == 5:
        return attack_menu()

#TODO read options in menuhelper
def attack_menu():
    menu_helper.print_attack_menu()
    option = menu_helper.read_option(option="attack_menu")
    if option == 1:
        return deauther_menu()
    elif option == 2:
        if not manager.clients_exists():
            return deauther_menu()
        menu_helper.print_associated_clients()
        option = menu_helper.read_option(option="client")
        manager.spoof_mac_address_of_client(option)
        #TODO spoof mac of client if exists
        return attack_menu()
    elif option == 3:
        menu_helper.print_attack_type_menu()
        option = menu_helper.read_option(option="attack_menu")
        manager.select_attack_type(option)
        return attack_menu()
    elif option == 4:
        #TODO start deauth 
        return attack_menu()

def main_menu():
    menu_helper.print_main_menu_options()
    option = menu_helper.read_option(option="main_menu")
    if option == 1:
        select_interface()
        return main_menu()
    elif option == 2:
        return mac_changer_menu()        
    elif option == 3:
        if manager.in_monitor_mode():
            return main_menu()
        trouble,output = manager.check_trouble()
        if trouble and output:
            output = output + "Your other interfaces will probably lose their internet connection.."
            yes = menu_helper.yes_no_question(output)
            if yes:
                manager.check_kill()
        manager.set_monitor_mode()
        return main_menu()
    elif option == 4:
        manager.set_managed_mode()
        return main_menu()
    elif option == 5:
        return deauther_menu()


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        # clean_output()
        print()
        sys.exit(0)