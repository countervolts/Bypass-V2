import colorama
import winreg

from network.net import transport_names, neftcfg_search, search, init_bypass, mac_saver
from utils.utils import title, has_perms, permission_giver, clear_console

colorama.init()

if __name__ == "__main__":
    title()

    if not has_perms():
        permission_giver()
    clear_console()
    user_input = input("Would you like to save your current mac address? (y/n): ").lower()
    if user_input == 'y':
        mac_saver()
        input("it has been saved to your desktop named 'howtochange.txt'\nthis also tells you how to change it back using cmd\npress enter to continue")
    transport_names, mp_transport = transport_names()
    if transport_names:
        print("\nAvailable transport names (the first one is usually the correct one):")
        for idx, name in enumerate(transport_names[:5]):
            if name == mp_transport:
                print(f"{idx + 1}. {name} (default)")
            else:
                print(f"{idx + 1}. {name}")
        selected_index = int(input("enter the number: ")) - 1
        if 0 <= selected_index < len(transport_names):
            selected_transport_name = transport_names[selected_index]
            print(f"\nSelected transport name: {selected_transport_name}\n")
            instances = neftcfg_search(selected_transport_name)
            if instances:
                for instance in instances:
                    print(f"NetCfgInstanceId found - value data: {instance[0]} - found within ..\\{instance[1]}\n")
                    key_path = "SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\" + instance[1]
                    print("full path for reg\nComputer\\HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\" + instance[1])
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
                    network_address = search(key)
                    change_option = input("\nBypass found. Do you want to change it? (y/n): ").lower()
                    if change_option == 'y':
                        init_bypass(instance[1])
                        input(f"network address: {network_address}\nrestart computer now :)")
                    else:
                        input(f"network address: {network_address}")
                    winreg.CloseKey(key)
            else:
                input("no instances found for the selected transport name. ")
        else:
            input("invalid index selected. rerun")
    else:
        input("no transport names found. will not work")