import tkinter as tk
import random
import time

class WhackAMoleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("打地鼠遊戲")
        
        # 遊戲設置
        self.width = 600
        self.height = 400
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        # 分數顯示
        self.score = 0
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.pack()

        # 遊戲計時
        self.game_duration = 30  # 遊戲時間 (秒)
        self.remaining_time = self.game_duration
        self.timer_label = tk.Label(self.root, text=f"Time: {self.remaining_time}s", font=("Arial", 14))
        self.timer_label.pack()

        # 地鼠設定
        self.mole_radius = 30
        self.moles = []

        # 啟動遊戲
        self.game_over = False
        self.start_time = time.time()
        self.update_timer()
        self.create_mole()

        # 綁定鼠標點擊事件
        self.canvas.bind("<Button-1>", self.whack_mole)

        # 遊戲循環
        self.update_game()

    def update_timer(self):
        """更新遊戲計時器"""
        elapsed_time = time.time() - self.start_time
        self.remaining_time = self.game_duration - int(elapsed_time)
        if self.remaining_time <= 0:
            self.game_over = True
            self.timer_label.config(text="遊戲結束！")
        else:
            self.timer_label.config(text=f"Time: {self.remaining_time}s")
            if not self.game_over:
                self.root.after(1000, self.update_timer)

    def create_mole(self):
        """隨機生成地鼠"""
        if not self.game_over:
            # 隨機生成地鼠位置
            x = random.randint(self.mole_radius, self.width - self.mole_radius)
            y = random.randint(self.mole_radius, self.height - self.mole_radius)
            mole = self.canvas.create_oval(x - self.mole_radius, y - self.mole_radius,
                                           x + self.mole_radius, y + self.mole_radius,
                                           fill="green", outline="black")
            self.moles.append(mole)

            # 每秒更新一次地鼠
            self.root.after(1000, self.create_mole)

    def whack_mole(self, event):
        """當玩家點擊地鼠時增加分數"""
        if self.game_over:
            return
        # 檢查鼠標點擊是否在地鼠範圍內
        for mole in self.moles:
            x1, y1, x2, y2 = self.canvas.coords(mole)
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.canvas.delete(mole)
                self.moles.remove(mole)
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")
                break

    def update_game(self):
        """更新遊戲狀態"""
        if not self.game_over:
            self.root.after(100, self.update_game)

# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    game = WhackAMoleGame(root)
    root.mainloop()
