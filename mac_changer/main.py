"""
    USAGE : sudo python3 mac_changer/main.py -i wlo1 -m 00:28:C7:0A:42:A2
    Custom util for changing mac with love =)

"""

import re
import sys
import subprocess
from optparse import OptionParser


def initial_setup():

    parser = OptionParser()
    parser.add_option("-m", "--mac-address", dest="mac-address",
                    help="new mac for changing", metavar="11:22:33:44:55")
    parser.add_option("-i", "--interface", dest="interface",
                    help="select interface for changing mac", metavar="eth0")
    options, args = parser.parse_args()
    return options



def change_mac(options:dict):
    #20:16:d8:ac:fb:8b
    """
        sudo ifconfig wlan0 down
        sudo ifconfig wlan0 hw ether 00:28:C7:0A:42:A2
        sudo ifconfig wlan0 up
    """


    cmd_output = subprocess.check_output(f'ifconfig {options["interface"]}',shell=True)
    old_mac = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',str(cmd_output))[0]

    _ = subprocess.call(f'ifconfig {options["interface"]} down',shell=True)
    _ = subprocess.call(f'ifconfig {options["interface"]} hw ether {options["mac-address"]}',shell=True)
    _ = subprocess.call(f'ifconfig {options["interface"]} up',shell=True)

    cmd_output = subprocess.check_output(f'ifconfig {options["interface"]}',shell=True)
    new_mac = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',str(cmd_output))[0]

    return old_mac,new_mac

if __name__ == "__main__":
    options = initial_setup()
    options = vars(options)

    if not options['interface']:
        sys.exit('[-] ERROR please select interface [-i wlo1]')
    if not options['mac-address']:
        mac , _ = change_mac(options)
        sys.exit(f'[-] Your mac-address is {mac}. For change input [-m 11:22:33:44:55:77]')
    
    mac_is_valid = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',str(options["mac-address"]))
    if mac_is_valid:
        try:
            old_mac,new_mac = change_mac(options)
            sys.exit(f'[+] Your mac address successfully changed from {old_mac} to {new_mac}')
        
        except Exception as e:
            sys.exit(f"[-] Error: {str(e)}")
    else:
        sys.exit(f'[-] Please input correct mac-address')

