import tkinter as tk
import pygame
from tkinter import filedialog
import os
from mutagen.mp3 import MP3

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("簡易音樂播放器")

        # 初始化播放清單和目前播放的歌曲索引
        self.playlist = []
        self.current_song_idx = 0
        self.is_dragging = False  # 檢測是否正在拖動滑桿
        self.repeat_mode = 0  # 0: 無重複, 1: 單曲重複, 2: 清單重複
        self.flag = 0

        # 初始化 Pygame
        pygame.mixer.init()
        pygame.display.init()  

        # 建立播放清單 Listbox
        self.song_listbox = tk.Listbox(root, height=15, width=50)
        self.song_listbox.grid(row=0, column=0, rowspan=6, columnspan=7, padx=10, pady=10)
        self.song_listbox.bind("<Double-Button-1>", self.play_selected_song)

        # 播放按鈕
        self.play_button = tk.Button(root, text="播放", command=self.play_music)
        self.play_button.grid(row=6, column=4, padx=5, pady=5)

        # 暫停/繼續按鈕
        self.pause_button = tk.Button(root, text="繼續", command=self.toggle_pause)
        self.pause_button.grid(row=6, column=3, padx=5, pady=5)

        # 停止按鈕
        self.stop_button = tk.Button(root, text="停止", command=self.stop_music)
        self.stop_button.grid(row=6, column=2, padx=5, pady=5)

        # 添加歌曲按鈕
        self.add_song_button = tk.Button(root, text="添加歌曲", command=self.add_song)
        self.add_song_button.grid(row=0, column=7, padx=5, pady=5)

        # 上一首和下一首按鈕
        self.prev_button = tk.Button(root, text="上一首", command=self.play_previous_song)
        self.prev_button.grid(row=6, column=1, padx=5, pady=5)

        self.next_button = tk.Button(root, text="下一首", command=self.play_next_song)
        self.next_button.grid(row=6, column=5, padx=5, pady=5)

        # 音量控制滑桿
        self.volume_slider = tk.Scale(root, from_=100, to=0, orient=tk.VERTICAL, label="音量", command=self.set_volume)
        self.volume_slider.set(50)  # 預設音量為 50%
        self.volume_slider.grid(row=1, column=7, rowspan=5, padx=10, pady=10, sticky="ns")

        # 播放進度滑桿
        self.progress_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="播放進度", showvalue=False)
        self.progress_slider.grid(row=7, column=0, columnspan=7, sticky="we", padx=10, pady=5)
        self.progress_slider.bind("<Button-1>", self.start_drag)  # 開始拖動
        self.progress_slider.bind("<ButtonRelease-1>", self.stop_drag)  # 結束拖動

        # 播放時間顯示
        self.current_time_label = tk.Label(root, text="目前播放時間: 0:00")
        self.current_time_label.grid(row=8, column=2, columnspan=3, pady=5)

        # 重複模式按鈕
        self.repeat_button = tk.Button(root, text="不重複播放", command=self.toggle_repeat_mode)
        self.repeat_button.grid(row=6, column=7, padx=10, pady=10)

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.update_current_time_label()  # 啟動時間更新迴圈

    def play_music(self):
        if self.playlist:  # 確保播放清單非空
            pygame.mixer.music.load(self.playlist[self.current_song_idx])
            pygame.mixer.music.play()
            self.pause_button.config(text="暫停")

            # 設定進度滑桿最大值（歌曲總長度）
            song_length = self.get_song_length(self.playlist[self.current_song_idx])
            self.progress_slider.config(to=song_length)
            self.progress_slider.set(0)  # 播放開始時重置進度
            self.flag = 0

    def get_song_length(self, song_path):
        """獲取歌曲總長度（秒）"""
        audio = MP3(song_path)
        return int(audio.info.length)

    def play_selected_song(self, event):
        selected_index = self.song_listbox.curselection()
        if selected_index:
            self.current_song_idx = selected_index[0]
            self.play_music()

    def toggle_pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.pause_button.config(text="繼續")
        else:
            pygame.mixer.music.unpause()
            self.pause_button.config(text="暫停")

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_previous_song(self):
        self.current_song_idx = (self.current_song_idx - 1) % len(self.playlist)
        self.play_music()

    def play_next_song(self):
        self.current_song_idx = (self.current_song_idx + 1) % len(self.playlist)
        self.play_music()

    def add_song(self):
        file = filedialog.askopenfilename(filetypes=[("MP3 文件", "*.mp3")])
        if file:
            self.playlist.append(file)
            self.song_listbox.insert(tk.END, os.path.basename(file))

    def set_volume(self, value):
        volume = int(value) / 100  # 將範圍轉為 0.0 到 1.0
        pygame.mixer.music.set_volume(volume)

    def start_drag(self, event):
        """當開始拖動進度條時，停止更新播放進度"""
        self.is_dragging = True

    def stop_drag(self, event):
        """當停止拖動進度條時，設置播放位置"""
        new_position = self.progress_slider.get()
        self.flag = int(new_position) * 1000 - int(pygame.mixer.music.get_pos())
        pygame.mixer.music.set_pos(new_position)  # 直接設置播放位置
        self.is_dragging = False

    def update_current_time_label(self):
    # 檢查是否有音樂正在播放
        if pygame.mixer.music.get_busy():
            current_time = (pygame.mixer.music.get_pos() + self.flag) // 1000  # 以秒為單位
            self.progress_slider.set(current_time)

            # 更新時間顯示
            minutes = current_time // 60
            seconds = current_time % 60
            self.current_time_label.config(text=f"目前播放時間: {minutes}:{seconds:02d}")
        else:
            self.handle_song_end()  # 當音樂停止時處理結束

        # 繼續每秒更新一次
        self.root.after(1000, self.update_current_time_label)

    def toggle_repeat_mode(self):
        """切換重複播放模式"""
        self.repeat_mode = (self.repeat_mode + 1) % 3
        mode_text = ["不重複播放", "單曲重複", "清單重複"]
        self.repeat_button.config(text=mode_text[self.repeat_mode])

    def handle_song_end(self):
        """根據重複模式處理歌曲播放結束"""
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:  # 音樂播放結束事件
                if self.repeat_mode == 0:
                    # 不重複播放，停止
                    return
                elif self.repeat_mode == 1:
                    # 單曲重複，重新播放目前歌曲
                    self.play_music()
                elif self.repeat_mode == 2:
                    # 清單重複，播放下一首或重新從頭播放
                    self.play_next_song()
# 主程式
root = tk.Tk()
music_player = MusicPlayer(root)
root.mainloop()
