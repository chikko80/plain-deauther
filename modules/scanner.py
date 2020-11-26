import subprocess
import shlex
import os
import time
from termcolor import colored
from deauther_models import Client,Target
from decorator import scanner_menu


class Scanner:

    # def __init__(self,interface):
        # self.interface = interface
        
    def __init__(self):
        pass

    def read_airmon_output(self):
        delete_old_file()
        # command = f"airodump-ng --wps -w scan --output-format csv {self.interface.interface}"
        command = f"airodump-ng --wps -w scan --output-format csv --write-interval 1 wlan0mon"
        process = subprocess.Popen(shlex.split(command),shell=False,stdout=subprocess.PIPE)

        # Poll process.stdout to show stdout live
        try:
            while True:
                process.stdout.readline()
                if process.poll() is not None:
                    break
                if not file_exists('scan-01.csv'):
                    continue
                os.system('cls' if os.name == 'nt' else 'clear')
                print_targets()
                time.sleep(1)
        except KeyboardInterrupt:
            pass


@scanner_menu
def print_targets():
    targets = get_targets_from_csv('scan-01.csv')
    for index,target in enumerate(targets,start=1):
        print(colored(str(index).rjust(5)),target.to_str())

def file_exists(filepath):
    import os.path
    return os.path.isfile(filepath) 

def get_targets_from_csv(csv_filename):
        '''Returns list of Target objects parsed from CSV file.'''
        targets = []
        import csv
        with open(csv_filename, 'r') as csvopen:
            lines = []
            for line in csvopen:
                line = line.replace('\0', '')
                lines.append(line)
            csv_reader = csv.reader(lines,
                    delimiter=',',
                    quoting=csv.QUOTE_ALL,
                    skipinitialspace=True,
                    escapechar='\\')

            client_section = False
            for row in csv_reader:
                # Each 'row' is a list of fields for a target/client
                if len(row) == 0: 
                    continue

                if row[0].strip() == 'BSSID':
                    client_section = False
                    continue

                elif row[0].strip() == 'Station MAC':
                    # This is the 'header' for the list of Clients
                    client_section = True
                    continue

                if client_section:
                    # The current row corresponds to a 'Client' (computer)
                    try:
                        client = Client(row)
                    except (IndexError, ValueError) as e:
                        # Skip if we can't parse the client row
                        continue

                    if 'not associated' in client.bssid:
                        # Ignore unassociated clients
                        continue

                    # Add this client to the appropriate Target
                    for t in targets:
                        if t.bssid == client.bssid:
                            t.clients.append(client)
                            break

                else:
                    # The current row corresponds to a 'Target' (router)
                    try:
                        target = Target(row)
                        targets.append(target)
                    except Exception:
                        continue

        return targets


def delete_old_file():
    output = os.system('rm scan-01.csv')

Scanner().read_airmon_output()







