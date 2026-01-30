import random
import time
from arcade_utils import clear_screen, get_key, C_RESET, C_BOLD, C_RED, C_GREEN, C_YELLOW, C_CYAN, C_WHITE, C_MAGENTA, update_stats, load_stats

def solve(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for n in nums:
                    if is_valid_move(board, r, c, n)[0]:
                        board[r][c] = n
                        if solve(board): return True
                        board[r][c] = 0
                return False
    return True

def generate_board(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve(board)
    solution = [row[:] for row in board]
    remove = {"easy": 35, "medium": 45, "hard": 55}.get(difficulty, 35)
    while remove > 0:
        r, c = random.randint(0, 8), random.randint(0, 8)
        if board[r][c] != 0:
            board[r][c] = 0
            remove -= 1
    return board, solution

def is_valid_move(board, row, col, num):
    for i in range(9):
        if board[row][i] == num: return False, "Row conflict"
        if board[i][col] == num: return False, "Column conflict"
    br, bc = (row // 3) * 3, (col // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if board[i][j] == num: return False, "3x3 Box conflict"
    return True, ""

def print_board(board, original_cells, cursor, msg, elapsed):
    clear_screen()
    print(f"{C_MAGENTA}╔══════════════════════════════════╗")
    print(f"║ SUDOKU | Time: {elapsed:>3}s             ║")
    print(f"╚══════════════════════════════════╝{C_RESET}")
    print(f" {C_CYAN}  ╔═══════╦═══════╦═══════╗{C_RESET}")
    for r in range(9):
        line = f" {C_CYAN}{r+1} ║ {C_RESET}"
        for c in range(9):
            cell = board[r][c]
            style = ""
            if (r, c) == cursor: style = "\033[47m\033[30m"
            elif (r, c) in original_cells: style = C_CYAN
            elif cell != 0: style = C_GREEN
            
            val = f"{style}{cell if cell != 0 else '.'}{C_RESET}"
            line += val + " "
            if (c + 1) % 3 == 0: line += f"{C_CYAN}║ {C_RESET}"
        print(line)
        if (r + 1) % 3 == 0 and r < 8:
            print(f" {C_CYAN}  ╠═══════╬═══════╬═══════╣{C_RESET}")
    print(f" {C_CYAN}  ╚═══════╩═══════╩═══════╝{C_RESET}")
    print(f"      1 2 3   4 5 6   7 8 9")
    if msg: print(f"\n{C_RED}⚠ {msg}{C_RESET}")
    print(f"\n{C_YELLOW}Arrows: Move | 1-9: Place | H: Hint | Q: Exit{C_RESET}")

def play_sudoku():
    clear_screen()
    print(f"{C_MAGENTA}SUDOKU: (1) Easy (2) Medium (3) Hard (Q) Back{C_RESET}")
    while True:
        choice = get_key()
        if choice in ['q', 'Q']: return
        if choice in ['1', '2', '3']: break
        
    diff = {"2": "medium", "3": "hard"}.get(choice, "easy")
    board, solution = generate_board(diff)
    original_cells = [(r, c) for r in range(9) for c in range(9) if board[r][c] != 0]
    cursor = [0, 0]
    start_time = time.time()
    msg = ""
    hints_used = 0

    while True:
        elapsed = int(time.time() - start_time)
        print_board(board, original_cells, tuple(cursor), msg, elapsed)
        msg = ""

        if all(board[r][c] == solution[r][c] for r in range(9) for c in range(9)):
            print(f"\n{C_GREEN}🎉 VICTORY! Solved in {elapsed}s{C_RESET}")
            stats = load_stats().get("sudoku", {})
            best = stats.get("best_times", {}).get(diff)
            if best is None or elapsed < best:
                update_stats("sudoku", "best_times", elapsed, diff)
            update_stats("sudoku", "wins", stats.get("wins", 0) + 1)
            if hints_used == 0:
                update_stats("sudoku", "no_hint_wins", stats.get("no_hint_wins", 0) + 1)
            time.sleep(2); break

        key = get_key()
        if key in ['q', 'Q']: break
        elif key == 'up': cursor[0] = max(0, cursor[0] - 1)
        elif key == 'down': cursor[0] = min(8, cursor[0] + 1)
        elif key == 'left': cursor[1] = max(0, cursor[1] - 1)
        elif key == 'right': cursor[1] = min(8, cursor[1] + 1)
        elif key in '123456789':
            r, c = cursor
            if (r, c) in original_cells:
                msg = "Original cell!"
                continue
            num = int(key)
            valid, err = is_valid_move(board, r, c, num)
            if valid: board[r][c] = num
            else: msg = err
        elif key in ['0', ' ']:
            r, c = cursor
            if (r, c) not in original_cells: board[r][c] = 0
        elif key in ['h', 'H']:
            hints_used += 1
            # Simple hint: Fill current cell if empty or wrong
            r, c = cursor
            if (r, c) not in original_cells:
                board[r][c] = solution[r][c]
                msg = "Hint applied!"

if __name__ == "__main__":
    play_sudoku()
