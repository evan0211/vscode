import numpy as np
"""改動了勝利條件以及order函數就不必歷便所有可能性572種以及所有空白點"""
GRID_WIDTH = 40
COLUMN = 10  # 10列
ROW = 10     # 10行
BOARD_SIZE = 10  # 棋盤大小

ai1_moves = []  # AI1
ai2_moves = []  # AI2
all_moves = []  # all

list_all = []  # 整個棋盤的點
next_point = [0, 0]  # AI下一步最應該下的

ratio = 1  # 進攻的係數   大於一，進攻型，  小於一，防守型
DEPTH = 4  # 搜索深度

# 初始化胜利矩阵
win = np.zeros((572, BOARD_SIZE, BOARD_SIZE), int)

# 横排胜利条件（水平）
count = 0
for i in range(BOARD_SIZE):
    for j in range(6):  # 從0道5(起點)
        for k in range(5):  # 5 個連續的點
            win[count, i, j + k] = 5
        count += 1

# 直排胜利条件（垂直）
for i in range(6):
    for j in range(BOARD_SIZE):
        for k in range(5):
            win[count, i + k, j] = 5
        count += 1

# 主對角線勝利條件
for i in range(6):
    for j in range(6):
        for k in range(5):
            win[count, i + k, j + k] = 5
        count += 1

# 副對角線勝利條件
for i in range(6):
    for j in range(4, 10):
        for k in range(5):
            win[count, i + k, j - k] = 5
        count += 1

# 棋型的評估分數
shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))]

def ai(is_ai1):
    """AI走一步棋，返回下一步的座標"""
    global cut_count, search_count
    cut_count = 0
    search_count = 0
    negamax(is_ai1, DEPTH, -99999999, 99999999)
    return next_point[0], next_point[1]


def negamax(is_ai, depth, alpha, beta):
    if check_win_board(ai1_moves) or check_win_board(ai2_moves) or depth == 0:
        return evaluation(is_ai)

    blank_list = list(set(list_all).difference(set(all_moves)))
    order(blank_list)

    # 新增檢查，確保空位可用
    blank_list = [pt for pt in blank_list if pt not in all_moves]

    for next_step in blank_list:
        global search_count
        search_count += 1

        if not has_neightnor(next_step):
            continue

        if is_ai:
            ai1_moves.append(next_step)
        else:
            ai2_moves.append(next_step)
        all_moves.append(next_step)

        value = -negamax(not is_ai, depth - 1, -beta, -alpha)

        if is_ai:
            ai1_moves.remove(next_step)
        else:
            ai2_moves.remove(next_step)
        all_moves.remove(next_step)

        if value > alpha:
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            if value >= beta:
                global cut_count
                cut_count += 1
                return beta
            alpha = value

    return alpha


def order(blank_list):
    if not all_moves:  # 如果沒有下棋直接返回
        return

    last_pt = all_moves[-1]  # 獲取最近的下棋點
    neighbors = []  # 用於儲存鄰居點

    # 便利所有以下的棋子，收集鄰居
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor = (last_pt[0] + i, last_pt[1] + j)
            if neighbor in blank_list:  # 只紀錄空白的鄰居
                neighbors.append(neighbor)

    # 將鄰居點放前面
    blank_list[:] = neighbors + [pt for pt in blank_list if pt not in neighbors]  # 維護順序


def has_neightnor(pt):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1] + j) in all_moves:
                return True
    return False


def evaluation(is_ai):
    total_score = 0

    if is_ai:
        my_list = ai1_moves
        enemy_list = ai2_moves
    else:
        my_list = ai2_moves
        enemy_list = ai1_moves

    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list)

    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list, enemy_list)
        enemy_score += cal_score(m, n, 1, 0, my_list, enemy_list)
        enemy_score += cal_score(m, n, 1, 1, my_list, enemy_list)
        enemy_score += cal_score(m, n, -1, 1, my_list, enemy_list)

    total_score = my_score - enemy_score * ratio * 0.1 #可挑整這個參數去平衡進攻防守
    return total_score

def cal_score(m, n, x_dir, y_dir, enemy_list, my_list):
    max_score = 0
    for offset in range(-5, 1):
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_dir, n + (i + offset) * y_dir) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_dir, n + (i + offset) * y_dir) in my_list:
                pos.append(1)
            else:
                pos.append(0)

        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                max_score = max(max_score, score)

    return max_score


def check_win_board(player_list):
    """檢查玩家是否勝利(優化)"""
    board = set(player_list)  # 使用集合来存储玩家棋子的位置
    return check_win(board)


def check_win(board):
    """判断是否有 5 子連線(優化)"""
    # 定義勝利的方向：水平、垂直、主對角、副對角
    directions = [
        (1, 0),  # 水平
        (0, 1),  # 垂直
        (1, 1),  # 主對角
        (1, -1)  # 副對角
    ]

    for x, y in board:  # 便利所有棋子
        for dx, dy in directions:  # 便利四個方向
            count = 1  # 當前棋子算做一顆

            # 檢查正方向
            nx, ny = x + dx, y + dy
            while (nx, ny) in board:
                count += 1
                if count >= 5:
                    return True
                nx += dx
                ny += dy

            # 檢查反方向
            nx, ny = x - dx, y - dy
            while (nx, ny) in board:
                count += 1
                if count >= 5:
                    return True
                nx -= dx
                ny -= dy

    return False



def print_board():
    board = np.full((BOARD_SIZE, BOARD_SIZE), "＋")
    for (m, n) in ai1_moves:
        board[n][m] = "○"
    for (m, n) in ai2_moves:
        board[n][m] = "●"
    for row in board:
        print(" ".join(row))


def main():
    global next_point
    list_all.extend([(m, n) for m in range(COLUMN) for n in range(ROW)])
    while True:
        try:
            x = int(input("請輸入第一步棋的x坐標（0-9）："))
            y = int(input("請輸入第一步棋的y坐標（0-9）："))
            if (x, y) in list_all and (x, y) not in all_moves:
                break
            else:
                print("無效的位置，請重新輸入。")
        except ValueError:
            print("請輸入有效的整數。")

    # 設置玩家的第一步棋
    first_move = (x, y)
    ai1_moves.append(first_move)
    all_moves.append(first_move)
    print(f"玩家選擇的第一步棋位置是: {first_move}")
    print_board()

    while True:  #走到結束
        print("AI2正在思考...")
        x, y = ai(is_ai1=False)
        ai2_moves.append((x, y))
        all_moves.append((x, y))
        print(f"AI2走棋: {x}, {y}")
        print_board()

        if check_win_board(ai2_moves):
            print("AI2獲勝")
            break
        if len(all_moves) >= COLUMN *ROW :
            print("平局")
            break

        while True:
            try:
                x = int(input("請輸入你的下棋坐標（0-9）："))
                y = int(input("請輸入你的下棋坐標（0-9）："))
                if (x, y) in list_all and (x, y) not in all_moves:
                    break
                else:
                    print("無效的位置，請重新輸入。")
            except ValueError:
                print("請輸入有效的整數。")

        ai1_moves.append((x, y))
        all_moves.append((x, y))
        print(f"玩家走棋: {x}, {y}")
        print_board()

        if check_win_board(ai1_moves):
            print("玩家獲勝")
            break

        if len(all_moves) >= COLUMN * ROW:
            print("平局")
            break
if __name__ == "__main__":
    main()
#