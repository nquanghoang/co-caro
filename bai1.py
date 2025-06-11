import math

# 1. Khởi tạo bàn cờ (ma trận 3x3 toàn 0)
board = [[0 for _ in range(3)] for _ in range(3)]

# 2. In bàn cờ ra màn hình
def print_board():
    symbol = {0: ' ', 1: 'X', -1: 'O'}
    for row in board:
        print(" | ".join(symbol[cell] for cell in row))
        print("-" * 9)

# 3. Kiểm tra người thắng
def check_winner(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): return True  # hàng
        if all(board[j][i] == player for j in range(3)): return True  # cột
    if all(board[i][i] == player for i in range(3)): return True      # chéo chính
    if all(board[i][2 - i] == player for i in range(3)): return True  # chéo phụ
    return False

# 4. Hàm đánh giá trạng thái bàn cờ
def evaluate():
    if check_winner(-1):
        return 1     # Máy thắng
    elif check_winner(1):
        return -1    # Người thắng
    return 0         # Hòa hoặc chưa ai thắng

# 5. Kiểm tra bàn cờ đã đầy chưa
def is_full():
    return all(board[i][j] != 0 for i in range(3) for j in range(3))

# 6. Thuật toán Minimax có cắt tỉa Alpha-Beta
def minimax(depth, is_maximizing, alpha, beta):
    score = evaluate()
    if score != 0 or is_full():
        return score

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = -1  # Máy đánh
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
                    board[i][j] = 1  # Người đánh
                    eval = minimax(depth + 1, True, alpha, beta)
                    board[i][j] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        return min_eval
        return min_eval

# 7. Tìm nước đi tốt nhất cho máy
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

# 8. Vòng lặp chính của trò chơi
def play_game():
    print("Chào mừng đến với trò chơi Tic Tac Toe!")
    print("Bạn là 'X' (giá trị 1), máy là 'O' (giá trị -1).")
    print("Hãy nhập vị trí theo định dạng: hàng cột (vd: 1 1 để đánh ô góc trên bên trái).")
    print_board()

    while True:
        # ======= Lượt của người chơi =======
        while True:
            try:
                # Nhập nước đi (hàng và cột từ 1 đến 3)
                i, j = map(int, input("Nhập nước đi của bạn (hàng cột): ").split())
                i -= 1  # chuyển về chỉ số từ 0
                j -= 1
                # Kiểm tra hợp lệ và ô còn trống
                if 0 <= i < 3 and 0 <= j < 3 and board[i][j] == 0:
                    board[i][j] = 1  # Người chơi đánh vào ô (i,j)
                    break
                else:
                    print("Vị trí không hợp lệ hoặc đã được đánh. Vui lòng thử lại.")
            except:
                print("Lỗi nhập. Hãy nhập đúng 2 số nguyên cách nhau bằng dấu cách.")

        print_board()

        # Kiểm tra kết quả sau lượt người chơi
        if check_winner(1):
            print("Bạn đã thắng! Xin chúc mừng!")
            break
        if is_full():
            print("Trò chơi hòa!")
            break

        # ======= Lượt của máy =======
        print("Máy đang suy nghĩ...")
        i, j = best_move()       # AI chọn nước đi tốt nhất
        board[i][j] = -1         # Máy đánh vào ô (i,j)
        print(f"Máy đánh vào ô ({i + 1}, {j + 1}):")
        print_board()

        # Kiểm tra kết quả sau lượt máy
        if check_winner(-1):
            print("Máy đã thắng. Chúc bạn may mắn lần sau!")
            break
        if is_full():
            print("Trò chơi hòa!")
            break

# Khởi động trò chơi
play_game()