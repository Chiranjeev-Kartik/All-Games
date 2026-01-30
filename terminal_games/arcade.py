import os
import sys
import time
from arcade_utils import clear_screen, get_key, load_stats, C_RESET, C_BOLD, C_RED, C_GREEN, C_YELLOW, C_CYAN, C_WHITE, C_MAGENTA
from sudoku import play_sudoku
from minesweeper import play_minesweeper
from chess_game import play_chess

BANNER = f"""
{C_CYAN}╔═══════════════════════════════════════════════╗
║ {C_YELLOW}{C_BOLD}   ____  _  _  ____  _   _  _____  _   _    {C_CYAN}║
║ {C_YELLOW}{C_BOLD}  |  _ \| || ||_  _|| | | ||  _  || \ | |   {C_CYAN}║
║ {C_YELLOW}{C_BOLD}  |  __/| \/ |  ||  | |_| || |_| ||  \| |   {C_CYAN}║
║ {C_YELLOW}{C_BOLD}  |_|    \__/   |_|  \___/ |_| |_||_|\__|   {C_CYAN}║
║ {C_MAGENTA}{C_BOLD}   _____  ____  ____  __  ____  ____  ____  {C_CYAN}║
║ {C_MAGENTA}{C_BOLD}  |  _  ||  _ \|  _ \|  ||  _ \|  __||_  _| {C_CYAN}║
║ {C_MAGENTA}{C_BOLD}  | |_| ||  _/| |  | \__/|  _/|  __|  ||   {C_CYAN}║
║ {C_MAGENTA}{C_BOLD}  |_| |_||_|  |_|__| |__| |_|  |____| |_|   {C_CYAN}║
║                                               ║
║ {C_WHITE}        --- TERMINAL ARCADE V3 ---            {C_CYAN}║
╚═══════════════════════════════════════════════╝{C_RESET}
"""

def print_menu(selection, stats):
    clear_screen()
    print(BANNER)
    
    s_stats = stats.get("sudoku", {})
    m_stats = stats.get("minesweeper", {})
    c_stats = stats.get("chess", {})
    
    m_wins = sum(m_stats.get('wins', {}).values()) if isinstance(m_stats.get('wins'), dict) else 0
    print(f" {C_WHITE}🏆 STATS: Sudoku Wins: {s_stats.get('wins',0)} | Chess Wins: {c_stats.get('wins',0)} | Mines Wins: {m_wins}{C_RESET}")
    print("\n      " + f"{C_CYAN}╔══════════════════════════════╗{C_RESET}")
    options = [
        ("1 - 🧩 Sudoku", C_GREEN),
        ("2 - ♟  Chess vs AI", C_MAGENTA),
        ("3 - 💣 Minesweeper", C_YELLOW),
        ("q - 🚪 Quit", C_RED)
    ]
    
    for i, (text, color) in enumerate(options):
        prefix = f"{C_WHITE} > {C_RESET}" if i == selection else "   "
        style = f"\033[47m\033[30m" if i == selection else ""
        print(f"      {C_CYAN}║{C_RESET}{prefix}{style}{text:<26}{C_RESET}{C_CYAN}║{C_RESET}")
        
    print(f"      {C_CYAN}╚══════════════════════════════╝{C_RESET}")
    print(f"\n      {C_WHITE}Use Arrows to navigate, Enter to play{C_RESET}")

def main():
    if os.name == 'nt': os.system('') # Initialize ANSI on Windows
    selection = 0
    while True:
        stats = load_stats()
        print_menu(selection, stats)
        key = get_key()
        
        if key == 'up': selection = (selection - 1) % 4
        elif key == 'down': selection = (selection + 1) % 4
        elif key in ['\r', '\n', ' ']:
            if selection == 0: play_sudoku()
            elif selection == 1:
                try:
                    import chess
                    play_chess()
                except ImportError:
                    clear_screen()
                    print(f"\n{C_RED} Error: python-chess not found! Run pip install -r requirements.txt{C_RESET}")
                    time.sleep(2)
            elif selection == 2: play_minesweeper()
            elif selection == 3: break
        elif key in ['1', '2', '3', 'q', 'Q']:
            if key == '1': play_sudoku()
            elif key == '2': play_chess()
            elif key == '3': play_minesweeper()
            elif key in ['q', 'Q']: break

if __name__ == "__main__":
    main()
