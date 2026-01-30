import os
import sys
import json
import time

# ANSI Color Codes
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_MAGENTA = "\033[35m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"
C_BLACK = "\033[30m"

# Backgrounds
BG_DARK = "\033[48;5;236m"
BG_LIGHT = "\033[48;5;250m"
BG_CUR = "\033[48;5;220m"
BG_SEL = "\033[48;5;34m"
BG_RED = "\033[41m"

STATS_FILE = "player_stats.json"

def get_input_util():
    if os.name == 'nt':
        import msvcrt
        def getch():
            ch = msvcrt.getch()
            if ch in [b'\x00', b'\xe0']:
                ch2 = msvcrt.getch()
                return {b'H': 'up', b'P': 'down', b'K': 'left', b'M': 'right'}.get(ch2, None)
            try: return ch.decode('utf-8')
            except: return None
        return getch
    else:
        import tty, termios
        def getch():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\033':
                    ch2 = sys.stdin.read(1)
                    if ch2 == '[':
                        ch3 = sys.stdin.read(1)
                        return {'A': 'up', 'B': 'down', 'D': 'left', 'C': 'right'}.get(ch3, None)
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return getch

get_key = get_input_util()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                return json.load(f)
        except: return {}
    return {}

def update_stats(game, key, value, subkey=None):
    stats = load_stats()
    if game not in stats: stats[game] = {}
    if subkey:
        if key not in stats[game] or not isinstance(stats[game][key], dict):
            stats[game][key] = {}
        stats[game][key][subkey] = value
    else:
        stats[game][key] = value
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=4)

def show_popup(msg, color=C_CYAN):
    print(f"\n{color}╔" + "═" * (len(msg) + 2) + "╗")
    print(f"║ {msg} ║")
    print(f"╚" + "═" * (len(msg) + 2) + "╝{C_RESET}")
