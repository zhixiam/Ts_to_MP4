# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:55:26 2024

@author: mot66
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, concatenate_videoclips

class VideoConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("TS 轉 MP4 轉換器")

        self.file_label = tk.Label(master, text="已選擇的 TS 檔案:")
        self.file_label.pack()

        self.file_listbox = tk.Listbox(master, selectbackground='lightblue', selectmode=tk.EXTENDED)
        self.file_listbox.pack(expand=True, fill=tk.BOTH)

        self.add_button = tk.Button(master, text="新增檔案", command=self.add_files)
        self.add_button.pack()

        self.output_label = tk.Label(master, text="選擇輸出資料夾:")
        self.output_label.pack()

        self.output_button = tk.Button(master, text="瀏覽", command=self.browse_output)
        self.output_button.pack()

        self.convert_button = tk.Button(master, text="轉換", command=self.convert)
        self.convert_button.pack()
        
        self.master.geometry("500x500")

    def add_files(self):
        # 新增檔案
        files = filedialog.askopenfilenames(filetypes=[("TS 檔案", "*.ts")])
        if files:
            self.input_files = list(files)
            self.update_file_listbox()
        print(files)
    def browse_output(self):
        # 選擇輸出資料夾
        self.output_folder = filedialog.askdirectory()
        self.output_label.config(text=f"已選擇的輸出資料夾: {self.output_folder}")
        
    def convert(self):
        try:
            video_clips = []

            for input_file in self.input_files:
                # 讀取TS檔案
                video_clip = VideoFileClip(input_file)
                video_clips.append(video_clip)

            # 拼接多個影片
            final_clip = concatenate_videoclips(video_clips, method="compose")

            # 獲取檔案名稱（不含副檔名）
            base_name = os.path.splitext(os.path.basename(self.input_files[0]))[0]

            # 組合完整輸出檔案路徑
            output_file_path = os.path.join(self.output_folder, f"{base_name}.mp4")

            # 將TS檔案轉換為MP4
            final_clip.write_videofile(output_file_path, codec='libx264', audio_codec='aac')

            tk.messagebox.showinfo("轉換完成", "轉換成功！")
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"轉換過程中發生錯誤:\n{str(e)}")

    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for index, file in enumerate(self.input_files, start=1):
            self.file_listbox.insert(tk.END, f"{index}. {os.path.basename(file)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()