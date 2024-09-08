import subprocess
import threading
from tkinter import Toplevel, Text, Scrollbar, END, Button, Frame

play_obj = None
root = None
ffmpeg_path = "D:\\APP\\code\\Python\\Music_Player\\Windows\\ffplay.exe"

def set_root(tk_root):
    global root
    root = tk_root

def play_music(file_path, on_complete=None):
    global play_obj
    stop_all_music()
    # 使用 subprocess.Popen 启动 FFmpeg 进程
    creation_flags = 0x08000000  # CREATE_NO_WINDOW 标志
    play_obj = subprocess.Popen(
        [ffmpeg_path, '-nodisp', '-autoexit', file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=creation_flags  # 设置 CREATE_NO_WINDOW 标志
    )
    
    # 在后台线程中等待进程结束
    threading.Thread(target=_wait_and_call_on_complete, args=(on_complete,)).start()

def _wait_and_call_on_complete(on_complete):
    global play_obj
    if play_obj is not None:
        stdout, stderr = play_obj.communicate()  # 立即获取标准错误
        print('<------下面的报错不用管------>')
        play_obj.wait()  # 等待子进程结束
        # 检查标准错误输出，如果有错误信息，则显示错误窗口
        if stderr:
            error_message = f'播放失败：{stderr.decode("utf-8")}请报告给开发者,开发者邮箱:appleidqiufeng@outlook.com'
            root.after(0, show_error_with_copy, error_message)  # 在主线程中显示错误信息
        else:
            # 如果没有标准错误输出，检查标准输出
            if stdout:
                error_message = f'播放失败：{stdout.decode("utf-8")}请报告给开发者,开发者邮箱:appleidqiufeng@outlook.com'
                root.after(0, show_error_with_copy, error_message)
            else:
                # 如果标准输出和标准错误都没有内容，可能是文件问题或其他原因
                error_message = f'播放失败：未知错误，请检查文件路径和格式是否正确。'
                root.after(0, show_error_with_copy, error_message,False)
    on_complete()

def stop_all_music():
    global play_obj
    if play_obj is not None:
        play_obj.terminate()  # 发送终止信号
        play_obj = None

def show_error_with_copy(message,copy=True):
    def copy_to_clipboard():
        rootw.clipboard_clear()
        rootw.clipboard_append(message)
        rootw.update()

    def on_close():
        rootw.destroy()

    rootw = Toplevel()
    rootw.title('错误')
    rootw.transient()  # 使对话框依赖于主窗口
    rootw.grab_set()  # 确保对话框获得焦点

    # 创建一个文本框来显示错误信息
    text_box = Text(rootw, wrap='word', height=10, width=50)
    text_box.insert(END, message)
    text_box.pack(pady=10)

    # 创建一个滚动条
    scrollbar = Scrollbar(rootw, command=text_box.yview)
    scrollbar.pack(side='right', fill='y')
    text_box.config(yscrollcommand=scrollbar.set)

    # 创建按钮框架
    button_frame = Frame(rootw)
    button_frame.pack(pady=10)

    # 创建“确定”按钮
    ok_button = Button(button_frame, text='确定', command=on_close)
    ok_button.pack(side='left', padx=5)

    if copy:
        # 创建“复制”按钮
        copy_button = Button(button_frame, text='复制', command=copy_to_clipboard)
        copy_button.pack(side='right', padx=5)

    # 显示窗口
    root.wait_window()  # 等待对话框关闭