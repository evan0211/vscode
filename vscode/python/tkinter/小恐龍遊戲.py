import tkinter as tk
import random

# 遊戲參數
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
GROUND_LEVEL = 300
DINO_SIZE = 40
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 50
JUMP_HEIGHT = 150  # 增高跳躍高度
JUMP_SPEED = 15
GAME_SPEED = 10

class DinoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("小恐龍遊戲")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")  # 設為白色背景
        self.canvas.pack()

        # 初始化遊戲
        self.reset_game()

        # 綁定按鍵
        self.root.bind("<space>", self.jump)

    def reset_game(self):
        self.canvas.delete("all")  # 清空畫布
        self.is_jumping = False
        self.jump_direction = 1  # 1: 上升, -1: 下降
        self.score = 0
        self.running = True

        # 地面
        self.canvas.create_rectangle(0, GROUND_LEVEL, WINDOW_WIDTH, WINDOW_HEIGHT, fill="green", outline="")

        # 恐龍
        self.dino = self.canvas.create_rectangle(50, GROUND_LEVEL - DINO_SIZE, 50 + DINO_SIZE, GROUND_LEVEL, fill="orange")

        # 障礙物
        self.spawn_obstacle()

        # 分數顯示
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", font=("Arial", 16), fill="black", text=f"分數: {self.score}")

        # 開始遊戲循環
        self.update_game()

    def spawn_obstacle(self):
        x_start = WINDOW_WIDTH + random.randint(0, 200)  # 隨機生成間距
        y_start = GROUND_LEVEL - OBSTACLE_HEIGHT
        self.obstacle = self.canvas.create_rectangle(x_start, y_start, x_start + OBSTACLE_WIDTH, GROUND_LEVEL, fill="red")

    def move_obstacle(self):
        if self.obstacle:
            self.canvas.move(self.obstacle, -GAME_SPEED, 0)
            coords = self.canvas.coords(self.obstacle)
            if coords[2] < 0:  # 如果障礙物超出左邊界
                self.canvas.delete(self.obstacle)
                self.spawn_obstacle()
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"分數: {self.score}")

    def jump(self, event):
        if not self.is_jumping and self.running:  # 確保遊戲正在進行且不在跳躍中
            self.is_jumping = True
            self.jump_direction = 1

    def move_dino(self):
        if self.is_jumping:
            self.canvas.move(self.dino, 0, -self.jump_direction * JUMP_SPEED)
            coords = self.canvas.coords(self.dino)

            if coords[1] <= GROUND_LEVEL - DINO_SIZE - JUMP_HEIGHT:  # 跳到最高點
                self.jump_direction = -1
            elif coords[3] >= GROUND_LEVEL:  # 回到地面
                self.jump_direction = 1
                self.is_jumping = False
                self.canvas.coords(self.dino, 50, GROUND_LEVEL - DINO_SIZE, 50 + DINO_SIZE, GROUND_LEVEL)

    def check_collision(self):
        dino_coords = self.canvas.coords(self.dino)
        obstacle_coords = self.canvas.coords(self.obstacle)

        # 調整碰撞檢測區域
        if (dino_coords[2] - 5 > obstacle_coords[0] and dino_coords[0] + 5 < obstacle_coords[2] and
                dino_coords[3] - 5 > obstacle_coords[1] and dino_coords[1] + 5 < obstacle_coords[3]):
            self.running = False

    def update_game(self):
        if self.running:
            self.move_obstacle()
            self.move_dino()
            self.check_collision()
            self.root.after(50, self.update_game)
        else:
            # 顯示遊戲結束訊息
            self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="遊戲結束!", font=("Arial", 24), fill="red")
            self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30, text="按下 R 重新開始", font=("Arial", 16), fill="black")
            self.root.unbind("<r>")  # 移除多餘的綁定
            self.root.bind("<r>", self.restart_game)

    def restart_game(self, event):
        self.reset_game()

# 啟動遊戲
if __name__ == "__main__":
    root = tk.Tk()
    game = DinoGame(root)
    root.mainloop()
