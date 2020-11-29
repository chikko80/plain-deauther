import subprocess
import shlex
import os
import time
import os.path

from modules.models.client import Client
from modules.models.target import Target
from modules.menu_helper import MenuHelper
print_targets = MenuHelper.print_targets

class Scanner:

    def __init__(self,interface):
        self.interface = interface
        self.filepath = 'scan-01.csv'
        self.targets = None


    def start_scan(self):
        command = [
            'airodump-ng',
            self.interface.interface,
            '-a', # Only show associated clients
            '-w', "scan", # Output file prefix
            '--output-format' ,'csv',
            '--write-interval', '1' # Write every second
        ]

        if self.interface.chosen_channel:
            command.extend(["-c",str(self.interface.chosen_channel)])
        elif self.interface.chosen_band:
            command.extend(["--band",str(self.interface.chosen_band)])
        else:
            command.extend(["--band",str("abg")])

        joined = " ".join(command) 
        process = subprocess.Popen(shlex.split(joined),shell=False,stdout=subprocess.PIPE)
        # Poll procVess.stdout to show stdout live
        try:
            while True:
                #TODO run in thread while deauth attack
                if process.poll() is not None:
                    break
                if not self.file_exists():
                    continue
                self.targets = get_targets_from_csv('scan-01.csv')
                print_targets(self.targets)

                time.sleep(1)
        except KeyboardInterrupt:
            pass
            # return self.targets

    def file_exists(self):
        return os.path.isfile(self.filepath) 

    def delete_old_file(self):
        #TODO execute without output
        os.system('rm scan-01.csv')


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
        for target in targets:
            if len(target.clients) > 0:
                for client in target.clients:
                    client.associated_essid = target.essid

        return targets
