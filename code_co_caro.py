import tkinter as tk
from tkinter import messagebox
import math

board = [[0 for _ in range(3)] for _ in range(3)]

def check_winner(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): return True
        if all(board[j][i] == player for j in range(3)): return True
    if all(board[i][i] == player for i in range(3)): return True
    if all(board[i][2 - i] == player for i in range(3)): return True
    return False

def evaluate():
    if check_winner(-1):
        return 1
    elif check_winner(1):
        return -1
    return 0

def is_full():
    return all(board[i][j] != 0 for i in range(3) for j in range(3))

def minimax(depth, is_maximizing, alpha, beta):
    score = evaluate()
    if score != 0 or is_full():
        return score

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = -1
                    eval = minimax(depth + 1, False, alpha, beta)
                    board[i][j] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        return max_eval
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    eval = minimax(depth + 1, True, alpha, beta)
                    board[i][j] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        return min_eval
        return min_eval

def best_move():
    best_val = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = -1
                move_val = minimax(0, False, -math.inf, math.inf)
                board[i][j] = 0
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    return move

# --- Biến và hàm hỗ trợ cho GUI ---
current_player = 1 # 1 cho người chơi (X), -1 cho máy (O)
game_over = False
history = [] # Lưu trữ các trạng thái bàn cờ để phục vụ Undo

# Đối tượng cửa sổ chính của Tkinter
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("400x550") # Tăng chiều cao để đủ chỗ cho nút điều khiển

# Khung cho màn hình chính (trang chủ)
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill="both")

# Khung cho màn hình trò chơi
game_frame = tk.Frame(root) # Ban đầu chưa pack, chỉ hiển thị khi bắt đầu chơi

buttons = [[None for _ in range(3)] for _ in range(3)]
status_label = tk.Label(game_frame, text="Lượt của bạn (X)", font=('Helvetica', 16))

def update_board_gui():
    for r in range(3):
        for c in range(3):
            symbol = {0: ' ', 1: 'X', -1: 'O'}[board[r][c]]
            buttons[r][c].config(text=symbol, state=tk.NORMAL if symbol == ' ' and not game_over else tk.DISABLED)

def reset_game():
    global board, current_player, game_over, history
    board = [[0 for _ in range(3)] for _ in range(3)]
    current_player = 1
    game_over = False
    history = []
    status_label.config(text="Lượt của bạn (X)")
    update_board_gui()

def make_move(row, col):
    global game_over, current_player

    if board[row][col] == 0 and not game_over:
        # Lưu trạng thái trước khi đánh để phục vụ Undo
        history.append([row[:] for row in board]) # Lưu bản sao của board

        board[row][col] = current_player
        update_board_gui()

        if check_winner(current_player):
            symbol_winner = 'X' if current_player == 1 else 'O'
            status_label.config(text=f"'{symbol_winner}' đã thắng!")
            messagebox.showinfo("Kết thúc", f"'{symbol_winner}' đã thắng!")
            game_over = True
            disable_all_buttons()
            return
        elif is_full():
            status_label.config(text="Trò chơi hòa!")
            messagebox.showinfo("Kết thúc", "Trò chơi hòa!")
            game_over = True
            disable_all_buttons()
            return

        current_player *= -1 # Đổi lượt

        # Lượt của máy
        if current_player == -1 and not game_over:
            status_label.config(text="Máy đang suy nghĩ...")
            root.update_idletasks() # Cập nhật giao diện để hiển thị thông báo
            r_ai, c_ai = best_move()
            # Lưu trạng thái trước khi máy đánh
            history.append([row[:] for row in board])
            board[r_ai][c_ai] = -1
            update_board_gui()
            status_label.config(text="Lượt của bạn (X)")

            if check_winner(-1):
                status_label.config(text="Máy ('O') đã thắng!")
                messagebox.showinfo("Kết thúc", "Máy ('O') đã thắng!")
                game_over = True
                disable_all_buttons()
                return
            elif is_full():
                status_label.config(text="Trò chơi hòa!")
                messagebox.showinfo("Kết thúc", "Trò chơi hòa!")
                game_over = True
                disable_all_buttons()
                return
            current_player *= -1 # Đổi lượt về người chơi

def disable_all_buttons():
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(state=tk.DISABLED)

def undo_move():
    global board, game_over, current_player, history
    if len(history) > 0:
        # Nếu lượt cuối là của máy, thì cần undo 2 nước (máy và người)
        # Kiểm tra nếu board hiện tại khác với trạng thái trước đó trong history
        # và người chơi hiện tại là 1 (tức là vừa kết thúc lượt của máy)
        if current_player == 1 and board != history[-1] and len(history) >= 2:
            # Máy vừa đánh, nên ta hoàn tác 2 bước: nước máy và nước người chơi trước đó
            board = [row[:] for row in history[-2]]
            history = history[:-2]
            current_player = 1 # Trở về lượt người chơi
        elif current_player == -1 and len(history) >= 1: # Nếu đang là lượt của máy và người vừa đánh
            board = [row[:] for row in history[-1]]
            history.pop()
            current_player = 1 # Trở về lượt của người chơi
        else: # Không có nước đi để hoàn tác hoặc chỉ có 1 nước đi từ đầu game
            reset_game() # Hoặc có thể hiển thị thông báo "Không có nước đi để hoàn tác"
            return


        game_over = False
        status_label.config(text=f"Lượt của {'bạn (X)' if current_player == 1 else 'máy (O)'}")
        update_board_gui()
    else:
        messagebox.showinfo("Undo", "Không có nước đi nào để hoàn tác!")

def start_game_gui():
    main_frame.pack_forget()  # Ẩn màn hình chính
    game_frame.pack(expand=True, fill="both")  # Hiển thị màn hình trò chơi
    reset_game()  # Đảm bảo trò chơi được reset khi bắt đầu

# --- Thiết lập giao diện màn hình chính ---
main_label = tk.Label(main_frame, text="Chào mừng đến với Tic Tac Toe!", font=('Helvetica', 20, 'bold'))
main_label.pack(pady=50)

play_button = tk.Button(main_frame, text="Chơi Ngay", font=('Helvetica', 18), command=start_game_gui)
play_button.pack(pady=20)

# --- Thiết lập giao diện màn hình chơi ---
# Khung cho bàn cờ
board_frame = tk.Frame(game_frame, bg="lightgray", bd=5, relief="ridge")
board_frame.pack(pady=20)

for r in range(3):
    for c in range(3):
        button = tk.Button(board_frame, text=" ", font=('Helvetica', 30, 'bold'),
                           width=4, height=2, bd=2, relief="raised",
                           command=lambda r=r, c=c: make_move(r, c))
        button.grid(row=r, column=c, padx=5, pady=5)
        buttons[r][c] = button

status_label.pack(pady=10)

# Khung cho các nút điều khiển (Undo, Reset)
control_frame = tk.Frame(game_frame)
control_frame.pack(pady=10)

undo_button = tk.Button(control_frame, text="Undo", font=('Helvetica', 14), command=undo_move)
undo_button.pack(side=tk.LEFT, padx=10)

reset_button = tk.Button(control_frame, text="Chơi Lại", font=('Helvetica', 14), command=reset_game)
reset_button.pack(side=tk.RIGHT, padx=10)

# Khởi chạy ứng dụng
root.mainloop()
