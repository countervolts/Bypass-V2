import ctypes
import os
import sys

def title():
    ctypes.windll.kernel32.SetConsoleTitleW("pbb v1")

def has_perms():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

def permission_giver():
    try:
        script_path = os.path.abspath(sys.argv[0])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
    except Exception as e:
        input(f"problem with giving permissions: {e}")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
