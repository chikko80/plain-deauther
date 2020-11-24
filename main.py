import os
from termcolor import cprint,colored
from modules.menu import MenuHelper
from modules.manager import Manager

manager = Manager()
menu_helper = MenuHelper(manager)


def main():
    start()
    select_interface()
    main_menu()
    

def start():    
    menu_helper.print_banner()
    manager.read_interfaces()
    
    
def select_interface():
    menu_helper.print_interfaces(manager.interfaces)
    option = menu_helper.read_option(option="interface")
    manager.select_interface(option)


def main_menu():
    menu_helper.print_interface_options()
    option = menu_helper.read_option(option="main_menu")

    if option == 0:
        select_interface()
        main_menu()
    elif option == 1:
        pass
    elif option == 2:
        pass
    elif option == 3:
        pass
    elif option == 4:
        pass






if __name__ == "__main__":
    main()