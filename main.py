import winreg

from network.net import transport_names, neftcfg_search, search, init_bypass, mac_saver
from utils.utils import title, has_perms, permission_giver, clear_console

ignore = [
    "Hyper-V Virtual Ethernet Adapter",
    "VirtualBox Host-Only Ethernet Adapter",
    "VMware Virtual Ethernet Adapter",
    "Microsoft Wi-Fi Direct Virtual Adapter",
    "Microsoft Hosted Network Virtual Adapter"
]

if __name__ == "__main__":
    title()

    if not has_perms():
        permission_giver()
    clear_console()
    user_input = input("Would you like to save your current mac address? (y/n): ").lower()
    if user_input == 'y':
        mac_saver()
        input("it has been saved to your desktop named 'howtochange.txt'\nthis also tells you how to change it back using cmd\npress enter to continue")
        clear_console()
    transport_names_list, driver_desc_list, mp_transport = transport_names()
    if transport_names_list:
        print("Available transport names with descriptions:")
        filtered_transport_names = [
            (name, driver_desc_list[idx]) for idx, name in enumerate(transport_names_list[:5])
            if driver_desc_list[idx] not in ignore
        ]
        for idx, (name, driver_desc) in enumerate(filtered_transport_names):
            if name == mp_transport:
                print(f"{idx + 1}. {name} ({driver_desc}) (default)")
            else:
                print(f"{idx + 1}. {name} ({driver_desc})")
        selected_index = int(input("enter the number: ")) - 1
        if 0 <= selected_index < len(filtered_transport_names):
            selected_transport_name = filtered_transport_names[selected_index][0]
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