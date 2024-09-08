import Music as music
from tkinter import *
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import messagebox
import os

root = tk.Tk()
root.title("音乐播放器")
root.geometry("300x400")
is_playing = False

music.set_root(root)

def load_icon(icon_path):
    return tk.PhotoImage(file=icon_path)

def set_icon(window, icon):
    window.iconphoto(True, icon)

def select_file():
    global file,is_playing

    music_file_types = [
        ('All music files', ('.mp3', '.wav', '.aac', '.flac', '.ogg')),
        ('MP3 files', '*.mp3'),
        ('WAV files', '*.wav'),
        ('AAC files', '*.aac'),
        ('FLAC files', '*.flac'),
        ('OGG files', '*.ogg'),
        ('ALL files', '*.*')
    ]

    if not is_playing:
        file = filedialog.askopenfilename(title='选择音乐文件', filetypes=music_file_types)
        if file != '':
            select_entry.delete(0, END)
            select_entry.insert(0, file)
    else:
        messagebox.showwarning('提示', '播放音乐期间无法选择文件')

def play_music():
    global is_playing,play_button

    if is_playing:
        is_playing = False
        play_button.config(text='播放')
        music.stop_all_music()
    else:
        music_file = select_entry.get()
        if music_file == '':
            messagebox.showwarning('提示', '请先选择音乐文件')
        else:
            if os.path.exists(music_file):
                music.play_music(music_file, on_complete=lambda: play_complete())
                is_playing = True
                play_button.config(text='暂停')
            else:
                messagebox.showwarning('提示', '文件不存在')

def play_complete():
    global is_playing, play_button
    is_playing = False
    play_button.config(text='播放')

def on_closing():
    music.stop_all_music()
    if music.play_obj is not None:
        music.stop_all_music()
    play_button.config(text='播放')
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

icon = load_icon('D:\APP\code\Python\Music_Player\Windows\icon.ico')
set_icon(root, icon)

name_lable = Label(root, text='音乐播放器', font=('微软雅黑', 24))
select_lable = Label(root, text='选择音乐文件', font=('微软雅黑', 12))
select_entry = Entry(root, width=50, font=('微软雅黑', 10))
select_button = Button(root, text='选择文件', command=select_file, font=('微软雅黑', 10))
play_button = Button(root, text='播放', command=play_music, font=('微软雅黑', 14))

name_lable.pack(pady=10)
select_lable.pack(pady=10)
select_entry.pack(pady=10)
select_button.pack(pady=10)
play_button.pack(pady=10)

root.mainloop()
