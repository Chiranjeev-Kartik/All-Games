import chess
import chess.engine
import time
from arcade_utils import clear_screen, get_key, C_RESET, C_BOLD, C_RED, C_GREEN, C_YELLOW, C_CYAN, C_WHITE, C_MAGENTA, BG_DARK, BG_LIGHT, BG_CUR, BG_SEL, update_stats, load_stats

PIECES = {'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔', 'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'}

def get_ai_move(board):
    try:
        # Check if stockfish is available, otherwise fallback
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        res = engine.play(board, chess.engine.Limit(time=0.1))
        engine.quit(); return res.move
    except:
        import random
        return random.choice(list(board.legal_moves))

def print_board(board, cursor, selected, capt_w, capt_b):
    clear_screen()
    print(f"{C_CYAN}╔══════════════════════════════════╗")
    print(f"║       CHESS VS AI (2D)           ║")
    print(f"╚══════════════════════════════════╝{C_RESET}")
    print(f" {C_WHITE}White Captures: {C_MAGENTA}{''.join(PIECES.get(p.upper(),p) for p in capt_b)}{C_RESET}")
    print(f" {C_WHITE}Black Captures: {C_CYAN}{''.join(PIECES.get(p.lower(),p) for p in capt_w)}{C_RESET}\n")
    
    print("   a b c d e f g h")
    for r in range(8):
        line = f" {8-r} "
        for c in range(8):
            sq = chess.square(c, 7-r)
            bg = BG_LIGHT if (r + c) % 2 == 0 else BG_DARK
            if sq == cursor: bg = BG_CUR
            if sq == selected: bg = BG_SEL
            p = board.piece_at(sq)
            char = PIECES.get(p.symbol(), p.symbol()) if p else " "
            color = C_WHITE if p and p.color == chess.WHITE else C_MAGENTA
            line += f"{bg}{color} {char} {C_RESET}"
        print(line + f" {8-r}")
    print("   a b c d e f g h\n")
    if board.is_check(): print(f"{C_RED}{C_BOLD}  ⚠️ CHECK!{C_RESET}")
    print(f"{C_YELLOW}Arrows: Move | Enter: Select/Move | U: Undo | Q: Exit{C_RESET}")

def play_chess():
    board = chess.Board()
    cursor = 0 # a1
    selected = None
    capt_w, capt_b = [], []
    
    clear_screen()
    print(f"{C_MAGENTA}CHESS: Select Color (W/B) or (Q) Back{C_RESET}")
    while True:
        choice = get_key()
        if choice in ['q', 'Q']: return
        if choice in ['w', 'W', 'b', 'B', '\r', '\n']: break
    u_white = choice.lower() != 'b'
    
    while not board.is_game_over():
        print_board(board, cursor, selected, capt_w, capt_b)
        is_p = board.turn == (chess.WHITE if u_white else chess.BLACK)
        
        if is_p:
            key = get_key()
            if key in ['q', 'Q']: break
            elif key == 'up': cursor = min(63, cursor + 8) if cursor < 56 else cursor
            elif key == 'down': cursor = max(0, cursor - 8) if cursor > 7 else cursor
            elif key == 'left': cursor = max(0, cursor - 1) if cursor % 8 > 0 else cursor
            elif key == 'right': cursor = min(63, cursor + 1) if cursor % 8 < 7 else cursor
            elif key in ['u', 'U']:
                if len(board.move_stack) >= 2: board.pop(); board.pop()
            elif key in ['\r', '\n', ' ']:
                if selected is None:
                    if board.piece_at(cursor) and board.piece_at(cursor).color == board.turn:
                        selected = cursor
                else:
                    move = chess.Move(selected, cursor)
                    # Promotion logic
                    if board.piece_at(selected).piece_type == chess.PAWN:
                        if (chess.square_rank(cursor) == 7 and board.turn == chess.WHITE) or (chess.square_rank(cursor) == 0 and board.turn == chess.BLACK):
                            move.promotion = chess.QUEEN
                    if move in board.legal_moves:
                        cap = board.piece_at(cursor)
                        if cap:
                            if board.turn == chess.WHITE: capt_b.append(cap.symbol())
                            else: capt_w.append(cap.symbol())
                        board.push(move)
                        selected = None
                    else: selected = None
        else:
            print("AI Thinking..."); time.sleep(0.5)
            m = get_ai_move(board)
            cap = board.piece_at(m.to_square)
            if cap:
                if board.turn == chess.WHITE: capt_b.append(cap.symbol())
                else: capt_w.append(cap.symbol())
            board.push(m)

    print_board(board, cursor, selected, capt_w, capt_b)
    res = board.result()
    print(f"\n{C_BOLD}GAME OVER: {res}{C_RESET}")
    # Update Stats
    stats = load_stats().get("chess", {})
    if res == "1-0": update_stats("chess", "wins" if u_white else "losses", stats.get("wins" if u_white else "losses", 0) + 1)
    elif res == "0-1": update_stats("chess", "losses" if u_white else "wins", stats.get("losses" if u_white else "wins", 0) + 1)
    else: update_stats("chess", "draws", stats.get("draws", 0) + 1)
    time.sleep(2)

if __name__ == "__main__":
    play_chess()
