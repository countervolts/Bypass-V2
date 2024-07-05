import time
from scapy.all import ARP, send
import colorama
from colorama import Fore, Style
import socket
import netifaces
import threading
import os
import winreg

colorama.init()

class ArpSpoofer:
    def __init__(self, interface):
        self.spoofing = False
        self.interface = self.get_interface_name(interface)
        self.ip_address = self.get_ip_address()
        self.gateway_ip = self.get_gateway_ip()
        self.new_mac = self.get_mac_address()

    def get_mac_address(self):
        mac_address = input("Enter your changed MAC address (e.g., DE:AD:BE:EF:CA:FE): ")
        formatted_mac_address = ":".join(mac_address[i:i+2] for i in range(0, len(mac_address), 2))
        return formatted_mac_address

    def get_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def get_gateway_ip(self):
        gws = netifaces.gateways()
        return gws['default'][netifaces.AF_INET][0]

    def get_interface_name(self, interface_guid):
        for iface in netifaces.interfaces():
            addresses = netifaces.ifaddresses(iface)
            if netifaces.AF_LINK in addresses:
                for link in addresses[netifaces.AF_LINK]:
                    if 'addr' in link and link['addr'].replace(':', '').upper() == interface_guid.replace('-', '').upper():
                        return iface
        return interface_guid

    def toggle_network_adapters(self, enable):
        adapters = ["Ethernet", "Wi-Fi"]
        for adapter in adapters:
            os.system(f"netsh interface set interface \"{adapter}\" {'enable' if enable else 'disable'}")
        print(Fore.GREEN + f"[-] {'Enabled' if enable else 'Disabled'} network adapters successfully." + Style.RESET_ALL)

    def arp_spoof(self):
        arp_response = ARP(pdst=self.gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=self.ip_address, hwsrc=self.new_mac)
    
        print(f"\n{Fore.YELLOW}Using interface: {self.interface}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Gateway IP: {self.gateway_ip}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}IP Address: {self.ip_address}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}MAC Address: {self.new_mac}{Style.RESET_ALL}")

    def start(self):
        print(Fore.RED + "\n[*] Turning off internet..." + Style.RESET_ALL)
        self.toggle_network_adapters(enable=False)
        time.sleep(5)
        
        print(Fore.YELLOW + "[*] Re-enabling internet connection..." + Style.RESET_ALL)
        self.spoofing = True
        
        print(Fore.GREEN + "[-] Internet connection re-enabled successfully. ARP spoofing is active." + Style.RESET_ALL)
        arp_thread = threading.Thread(target=self.arp_spoof)
        arp_thread.start()
        self.toggle_network_adapters(enable=True)
        time.sleep(2)
        input("\nBypass running. Press enter to stop the bypass.")

if __name__ == "__main__":
    from utils.utils import title, has_perms, permission_giver, clear_console
    from network.net import transport_names, neftcfg_search, search, init_bypass, mac_saver

    title()

    if not has_perms():
        permission_giver()
    clear_console()
    user_input = input("Would you like to save your current mac address? (y/n): ").lower()
    if user_input == 'y':
        mac_saver()
        print("Mac address saved to appdata/bypasser.txt\n")
    transport_names, mp_transport = transport_names()
    if transport_names:
        print("\nAvailable transport names (the first one is usually the correct one):")
        for idx, name in enumerate(transport_names[:5]):
            if name == mp_transport:
                print(f"{idx + 1}. {name} <-- the code detects this is the most likely one")
            else:
                print(f"{idx + 1}. {name}")
        selected_index = int(input("Enter the index of the transport name you want to search: ")) - 1
        if 0 <= selected_index < len(transport_names):
            selected_transport_name = transport_names[selected_index]
            print(f"\nSelected transport name: {selected_transport_name}\n")
            instances = neftcfg_search(selected_transport_name)
            if instances:
                for instance in instances:
                    print(f"NetCfgInstanceId found - value data: {instance[0]} - found within ..\\{instance[1]}")
                    key_path = "SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\" + instance[1]
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
                    network_address = search(key)
                    change_option = input("Bypass found. Do you want to change it? (y/n): ").lower()
                    if change_option == 'y':
                        init_bypass(instance[1])
                    print(f"NetworkAddress: {network_address}\n")
                    winreg.CloseKey(key)
                spoofer = ArpSpoofer(selected_transport_name)
                print("\n!IMPORTANT! \nPlease note that this is a new method im trying and its just a work in progress so might not work as intended :)\nif you have any issues please let me know\n")
                user_input = input("Press 1 to start the bypass process: ")
                if user_input == '1':
                    spoofer.start()
            else:
                input("No instances found for the selected transport name.")
        else:
            input("Invalid index selected.")
    else:
        input("No transport names found.")
