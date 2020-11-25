#!/usr/bin/python3
import os
from termcolor import cprint,colored
from modules.menu_helper import MenuHelper
from modules.manager import Manager

manager = Manager()
menu_helper = MenuHelper(manager)


def menu():
    select_interface()
    main_menu()
    


def select_interface():
    manager.read_interfaces()
    menu_helper.print_interfaces(manager.interfaces)
    option = menu_helper.read_option(option="interface")
    manager.select_interface(option)

def mac_changer_menu():
    menu_helper.print_mac_changer_menu() 
    option = menu_helper.read_option(option="mac_changer")
    if option == 0:
        main_menu()
    elif option == 1:
        manager.set_random_mac_address()
        main_menu()
    elif option == 2:
        input_address = menu_helper.read_mac_address()
        if not input_address:
            return main_menu()
        manager.set_custom_mac_address(input_address)
        main_menu()
    elif option == 3:
        manager.reset_mac_address()
        main_menu()

def main_menu():
    menu_helper.print_main_menu_options()
    option = menu_helper.read_option(option="main_menu")

    if option == 0:
        select_interface()
        main_menu()
    elif option == 1:
        mac_changer_menu()        
    elif option == 2:
        manager.set_monitor_mode()
        main_menu()
    elif option == 3:
        manager.set_managed_mode()
        main_menu()
    elif option == 4:
        pass

if __name__ == "__main__":
    menu()