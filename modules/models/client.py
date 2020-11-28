'''
    Source Code of this model:
    https://github.com/derv82/wifite2
'''

class Client(object):
    '''
        Holds details for a 'Client' - a wireless device (e.g. computer)
        that is associated with an Access Point (e.g. router)
    '''

    def __init__(self, fields):
        '''
            Initializes & stores client info based on fields.
            Args:
                Fields - List of strings
                INDEX KEY
                    0 Station MAC (client's MAC address)
                    1 First time seen,
                    2 Last time seen,
                    3 Power,
                    4 # packets,
                    5 BSSID, (Access Point's MAC address)
                    6 Probed ESSIDs
        '''
        self.station =     fields[0].strip()
        self.power   = int(fields[3].strip())
        self.packets = int(fields[4].strip())
        self.bssid   =     fields[5].strip()
        self.associated_essid = None

    def __str__(self):
        ''' String representation of a Client '''
        return f'Station: {self.station}  |  Connected AP: {self.associated_essid}'