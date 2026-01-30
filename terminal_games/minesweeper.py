import random
import time
from arcade_utils import clear_screen, get_key, C_RESET, C_BOLD, C_RED, C_GREEN, C_YELLOW, C_CYAN, C_WHITE, C_MAGENTA, C_BLACK, update_stats, load_stats

NUM_COLORS = {1: "\033[34m", 2: "\033[32m", 3: "\033[31m", 4: "\033[35m", 5: "\033[33m", 6: "\033[36m", 7: "\033[30m", 8: "\033[37m"}

def create_board(rows, cols, mines):
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_pos = set()
    while len(mine_pos) < mines:
        r, c = random.randint(0, rows-1), random.randint(0, cols-1)
        if (r, c) not in mine_pos:
            mine_pos.add((r, c))
            board[r][c] = 'M'
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'M': continue
            cnt = sum(1 for dr in [-1,0,1] for dc in [-1,0,1] if 0 <= r+dr < rows and 0 <= c+dc < cols and board[r+dr][c+dc] == 'M')
            board[r][c] = cnt
    return board, mine_pos

def print_board(board, revealed, flagged, cursor, elapsed, mines, exploded=None):
    rows, cols = len(board), len(board[0])
    clear_screen()
    f_count = sum(row.count(True) for row in flagged)
    print(f"{C_CYAN}╔═══════════════════════════════════════════════╗")
    print(f"║ ⏱  Time: {elapsed:>3}s | ⚑ Flags: {f_count:>2}/{mines} | 💣 Mines: {mines} ║")
    print(f"╚═══════════════════════════════════════════════╝{C_RESET}")
    
    print("    " + " ".join([f"{C_CYAN}{i+1:2}{C_RESET}" for i in range(cols)]))
    print("   " + f"{C_CYAN}╔" + "═══" * cols + "╗{C_RESET}")
    
    for r in range(rows):
        line = f" {C_CYAN}{r+1:2} ║{C_RESET}"
        for c in range(cols):
            style = ""
            if (r, c) == cursor: style = "\033[47m"
            
            if (r, c) == exploded: char = f"{style}\033[31m💥{C_RESET} "
            elif flagged[r][c]: char = f"{style}{C_YELLOW}⚑{C_RESET} "
            elif revealed[r][c]:
                val = board[r][c]
                if val == 'M': char = f"{style}{C_RED}💣{C_RESET} "
                elif val == 0: char = f"{style}{C_BLACK}.{C_RESET} "
                else: char = f"{style}{NUM_COLORS.get(val, '')}{val}{C_RESET} "
            else: char = f"{style}{C_WHITE}■{C_RESET} "
            line += " " + char
        print(line + f"{C_CYAN}║{C_RESET}")
    print("   " + f"{C_CYAN}╚" + "═══" * cols + "╝{C_RESET}")
    print(f"{C_YELLOW}Arrows: Move | Enter/R: Reveal | F: Flag | Q: Exit{C_RESET}")

def reveal(board, revealed, flagged, r, c):
    if not (0 <= r < len(board) and 0 <= c < len(board[0])) or revealed[r][c] or flagged[r][c]: return
    revealed[r][c] = True
    if board[r][c] == 0:
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                reveal(board, revealed, flagged, r+dr, c+dc)

def play_minesweeper():
    clear_screen()
    print(f"{C_MAGENTA}MINESWEEPER: (1) Beginner (2) Intermediate (3) Expert (Q) Back{C_RESET}")
    while True:
        choice = get_key()
        if choice in ['q', 'Q']: return
        if choice in ['1', '2', '3']: break

    diff_name = {"2": "intermediate", "3": "expert"}.get(choice, "beginner")
    r, c, mines = {"beginner": (8, 8, 10), "intermediate": (16, 16, 40), "expert": (16, 30, 99)}[diff_name]
    
    board, mine_pos = create_board(r, c, mines)
    revealed = [[False for _ in range(c)] for _ in range(r)]
    flagged = [[False for _ in range(c)] for _ in range(r)]
    cursor = [0, 0]
    start_time = time.time()
    
    while True:
        elapsed = int(time.time() - start_time)
        print_board(board, revealed, flagged, tuple(cursor), elapsed, mines)
        
        if sum(1 for i in range(r) for j in range(c) if not revealed[i][j] and board[i][j] != 'M') == 0:
            print(f"\n{C_GREEN}🎉 YOU WIN! Field Cleared!{C_RESET}")
            stats = load_stats().get("minesweeper", {})
            update_stats("minesweeper", "wins", stats.get("wins", {}).get(diff_name, 0) + 1, diff_name)
            if sum(row.count(True) for row in flagged) == 0:
                update_stats("minesweeper", "no_flag_wins", stats.get("no_flag_wins", 0) + 1)
            time.sleep(2); break

        key = get_key()
        if key in ['q', 'Q']: break
        elif key == 'up': cursor[0] = max(0, cursor[0] - 1)
        elif key == 'down': cursor[0] = min(r - 1, cursor[0] + 1)
        elif key == 'left': cursor[1] = max(0, cursor[1] - 1)
        elif key == 'right': cursor[1] = min(c - 1, cursor[1] + 1)
        elif key in ['\r', '\n', ' ', 'r', 'R']:
            cr, cc = cursor
            if board[cr][cc] == 'M':
                for mr, mc in mine_pos: revealed[mr][mc] = True
                print_board(board, revealed, flagged, tuple(cursor), elapsed, mines, exploded=(cr, cc))
                print(f"\n{C_RED}💥 BOOM! GAME OVER.{C_RESET}")
                time.sleep(2); break
            reveal(board, revealed, flagged, cr, cc)
        elif key in ['f', 'F']:
            flagged[cursor[0]][cursor[1]] = not flagged[cursor[0]][cursor[1]]

if __name__ == "__main__":
    play_minesweeper()
