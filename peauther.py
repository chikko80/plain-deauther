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
                #!TESTING
    # attack_menu()
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
        inner_option = menu_helper.read_option(option='target_menu')
        manager.select_target(inner_option) 
        return attack_menu()
    elif option == 3:
        inner_option = menu_helper.read_option(option='channel (0 for channel-hopping)')
        manager.select_channel(inner_option) 
        return deauther_menu()
    elif option == 4:
        inner_option = menu_helper.yes_no_question("Select a band (0 for default) ",option=["2.4GHz/2","5GHz/5"])
        manager.select_band(inner_option)
        return deauther_menu()
    elif option == 5:
        if not manager.chosen_target:
            print_message("Please select a target first..",'red')
            return deauther_menu()
        return attack_menu()

def attack_menu():
    menu_helper.print_attack_menu()
    option = menu_helper.read_option(option="attack_menu")
    if option == 1:
        return deauther_menu()
    elif option == 2:
        if not manager.clients_exists():
            return deauther_menu()
        menu_helper.print_associated_clients()
        inner_option = menu_helper.read_option(option="client")
        manager.spoof_mac_address_of_client(inner_option)
        return attack_menu()
    elif option == 3:
        menu_helper.print_attack_type_menu()
        attack_type_option = menu_helper.read_option(option="attack_type_menu")
        if attack_type_option == 3:
            print_message("MAC-Address to ignore (abort with 1): \n",'yellow',instant=True)
            mac = menu_helper.read_mac_address()
            if not mac:
                return attack_menu()
            manager.ignore_mac = mac
        if attack_type_option == 4:
            custom = menu_helper.yes_no_question('Target client: Specify custom mac or choose one from scan results (abort with 1)',option=['Custom/c','Scanned/s'])
            if custom:
                mac = menu_helper.read_mac_address()
                if not mac:
                    return attack_menu()
                manager.target_client = mac
            else:
                menu_helper.print_associated_clients()
                inner_option = menu_helper.read_option(option="client")
                manager.select_target_client(inner_option)
        manager.select_attack_type(attack_type_option)
        return attack_menu()
    elif option == 4:
        manager.start_deauth_attack()
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
        check_trouble()
        print_message("Putting into monitor mode..",'yellow')
        manager.set_monitor_mode()
        return main_menu()
    elif option == 4:
        manager.set_managed_mode()
        return main_menu()
    elif option == 5:
        return deauther_menu()

def check_trouble():
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