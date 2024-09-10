import subprocess
import re
import winreg
import random
import os

def transport_names():
    try:
        output = subprocess.check_output(["getmac", "/fo", "table", "/nh"], universal_newlines=True)
        lines = output.splitlines()

        transport_names = []
        mp_transport = None

        for line in lines:
            match = re.search(r'(\{[\w-]+\})', line)
            if match:
                transport_name = match.group(1)
                transport_names.append(transport_name)
                if mp_transport is None and transport_name != '':
                    mp_transport = transport_name

        return transport_names, mp_transport

    except subprocess.CalledProcessError as e:
        input(f"Error: {e}")
        return [], None

def neftcfg_search(transport_name):
    key_path = r"SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
    value_name = 'NetCfgInstanceId'

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
        subkey_index = 0

        found_instances = []

        while True:
            try:
                sub_name = winreg.EnumKey(key, subkey_index)
                subkey = winreg.OpenKey(key, sub_name)
                try:
                    value, _ = winreg.QueryValueEx(subkey, value_name)
                    if value == transport_name:
                        found_instances.append((value, sub_name))
                except FileNotFoundError:
                    pass
                finally:
                    winreg.CloseKey(subkey)
                subkey_index += 1
            except OSError:
                break

        winreg.CloseKey(key)

        return found_instances

    except FileNotFoundError:
        input("bypass will not work on this system")
        return []

def search(subkey):
    value_name = 'NetworkAddress'
    try:
        value_data, _ = winreg.QueryValueEx(subkey, value_name)
        return value_data
    except FileNotFoundError:
        return None

def rand0m_hex():
    random_hex = ''.join(random.choices('0123456789ABCDEF', k=10))
    return 'DE' + random_hex

def get_selected_transport():
    _, mp_transport = transport_names()
    return mp_transport

def trans_dir(sub_name):
    return "SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\" + sub_name

import os
import winreg
from datetime import datetime

def mac_saver():
    _, mp_transport = transport_names()
    instances = neftcfg_search(mp_transport)

    if instances:
        _, sub_name = instances[0]
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, trans_dir(sub_name), 0, winreg.KEY_READ)
        old_mac = winreg.QueryValueEx(key, 'NetworkAddress')[0]
        winreg.CloseKey(key)

        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        file_path = os.path.join(desktop_path, 'howtochange.txt')
        with open(file_path, 'w') as file:
            file.write(f"{old_mac}\n")
            file.write("to change it back use this command in cmd:\n")
            file.write(f"reg add \"HKEY_LOCAL_MACHINE\\{trans_dir(sub_name)}\" /v NetworkAddress /d {old_mac} /f\n")

        return old_mac
    return None

def init_bypass(sub_name):
    value_name = 'NetworkAddress'
    attempts = 3 
    key_path = "SYSTEM\\ControlSet001\\Control\\Class\\{4d36e972-e325-11ce-bfc1-08002be10318}\\" + sub_name
    while attempts > 0:
        value_data = rand0m_hex()
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value_data)
            print(f"NetworkAddress created - Value Data: {value_data}")
            winreg.CloseKey(key)
            return value_data
        except Exception as e:
            input(f"uh oh: {e}")
            attempts -= 1

    print("failed after multiple attempts")
    return None 
