import os
from termcolor import cprint,colored

def main():
    print_banner()
    menu = Menu()
    menu.show_interfaces()
    menu.select_interface()
    print(menu.choosen_interface)


class Menu:

    def __init__(self,interfaces=[]):
        self.interfaces = interfaces
        self.choosen_interface = None

    def show_interfaces(self):
        output = os.popen("airmon-ng").read()
        self.assign_interfaces(output)
        self.print_interfaces()

    def assign_interfaces(self,output):
        output = output.split("\n")
        index = 1
        for counter,line in enumerate(output):
            if counter > 2 and line.startswith("phy"):
                splitted_line = line.split("\t")
                remove_empty = [word for word in splitted_line if word]
                self.interfaces.append(Interface(str(index),remove_empty[0],remove_empty[1],remove_empty[2],remove_empty[3]))
                index +=1

    def print_interfaces(self):
        self.table_prettifier(["",'PHY',"Interface","Driver","Chipset"])
        print()
        for interface in self.interfaces:
            self.table_prettifier(interface.return_as_list())

    def select_interface(self):
        print("\nSelect Interface:\t",end="")
        while True:
            try:
                index = int(input())
                if index < 1 or index > len(self.interfaces):
                    raise ValueError
                else: 
                    self.choosen_interface = self.interfaces[index-1]
                    break
            except ValueError:
                cprint("No valid input. Select a valid index","red")
                print("Select Interface:\t",end="")
    
    def table_prettifier(self,row_as_list):
        print("{: <5} {: <10} {: <15} {: <15} {: <20}".format(*row_as_list))

    def clean_last_line():
        print ("\033[A                             \033[A")

class Interface:

    def __init__(self,index,phy,interface,driver,chipset):
        self.index = index
        self.phy = phy
        self.interface = interface
        self.driver = driver
        self.chipset = chipset

    def __str__(self):
        return "Index: " + self.index + "\n" + "PHY: " + self.phy + "\n" +"Interface: " + self.interface + "\n" + "Driver: " + self.driver + "\n" +"Chipset: " + self.chipset + "\n" 

    def return_as_list(self):
        return [str(self.index + " : "),str(self.phy),str(self.interface),str(self.driver),str(self.chipset)]




def print_banner():
    cprint("--------------------------------------------------------------------------------","green")
    cprint(" __        __  _    __   _   ____                                               ","red")
    cprint(" \ \      / / (_)  / _| (_) / ___|    ___    __ _   _ __    _ __     ___   _ __ ",'red')
    cprint("  \ \ /\ / /  | | | |_  | | \___ \   / __|  / _` | | '_ \  | '_ \   / _ \ | '__|",'red')
    cprint("   \ V  V /   | | |  _| | |  ___) | | (__  | (_| | | | | | | | | | |  __/ | |   ",'red')
    cprint("    \_/\_/    |_| |_|   |_| |____/   \___|  \__,_| |_| |_| |_| |_|  \___| |_|   ",'red')
    cprint("--------------------------------------------------------------------------------",'green')
    print(colored("------------------------------- ",'green'),end='')
    print(colored("coded by chikko80",'red'),end="")
    cprint(" -------------------------------",'green')
    cprint("--------------------------------------------------------------------------------",'green')
    print()
    print()



if __name__ == "__main__":
    main()