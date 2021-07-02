#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help (-h) for info")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help (-h) for info")
    else:
        return options

def change_mac(interface,new_mac):
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)
    
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_s_r = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_s_r:
        return mac_s_r.group(0)
    else:
        print("[-] Could not read MAC address")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC: " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] MAC address has successfully changed to " + options.new_mac)
else:
    print("[-] MAC address did not get changed.")
