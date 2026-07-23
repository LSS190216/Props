import tkinter as tk
from tkinter import ttk
import time
import datetime
import platform
import urllib.request
import os
import threading

ipts = ""

try:
    import pyautogui as pag
except:
    ipts += " pyautogui"
try:
    import pyperclip as clp
except:
    ipts += " pyperclip"

if platform.system() == "Darwin":
    print("依赖配置错误，正在为您修复，请勿关闭软件。（1/2）", end = "\r")
    os.system("brew install python-tk")

if ipts:
    print("依赖配置错误，正在为您修复，请勿关闭软件。（2/2）")
    os.system("pip3 install{ipts} --user -i https://pypi.tuna.tsinghua.edu.cn/simple")
    print("修复完成，将在3秒后重启。", end = "\r")
    time.sleep(1)
    print("修复完成，将在2秒后重启。", end = "\r")
    time.sleep(1)
    print("修复完成，将在1秒后重启。", end = "\r")
    time.sleep(1)
    python_exe = sys.executable
    script_path = os.path.abspath(sys.argv[0])
    args = sys.argv[1:]

    if sys.platform == "win32":
        subprocess.Popen([python_exe, script_path] + args)
        sys.exit(0)
    else:
        os.execl(python_exe, python_exe, script_path, *args)

def auto_update():
    try:
        url = "https://cdn.jsdelivr.net/gh/LSS190216/Props@main/main.py"
        local_path = os.path.abspath(__file__)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
        
        decoded_content = content.decode("utf-8", errors="ignore")
        
        if decoded_content.startswith("import ") or decoded_content.startswith("#") or decoded_content.strip().startswith("def ") or decoded_content.strip().startswith("class "):
            with open(local_path, "wb") as f:
                f.write(content)
        else:
            print(decoded_content)
    except Exception as e:
        print(e)

elements = []
start_time = 0
is_sending = False
send_interval = 5
last_send_time = 0

def send(text):
    clp.copy(text)
    if platform.system() == "Darwin":
        pag.hotkey("command", "v")
    else:
        pag.hotkey("ctrl", "v")

def generate_message():
    message = ""
    for elem in elements:
        if elem["type"] == "text":
            message += elem["content"]
        elif elem["type"] == "time":
            message += format_time(elem["content"])
        elif elem["type"] == "late_duration":
            message += format_late_duration(elem["content"])
    return message

def format_time(style):
    now = time.localtime()
    year = str(now.tm_year)
    month = str(now.tm_mon).zfill(2)
    day = str(now.tm_mday).zfill(2)
    hour = str(now.tm_hour).zfill(2)
    minute = str(now.tm_min).zfill(2)
    second = str(now.tm_sec).zfill(2)
    weekday = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"][now.tm_wday]
    
    mapping = {
        "年 月 日 时 分": f"{year}年{month}月{day}日 {hour}:{minute}",
        "年 月 日 时 分 秒": f"{year}年{month}月{day}日 {hour}:{minute}:{second}",
        "月 日 时 分": f"{month}月{day}日 {hour}:{minute}",
        "月 日 时 分 秒": f"{month}月{day}日 {hour}:{minute}:{second}",
        "日 时 分": f"{day}日 {hour}:{minute}",
        "日 时 分 秒": f"{day}日 {hour}:{minute}:{second}",
        "星期 时 分": f"{weekday} {hour}:{minute}",
        "星期 时 分 秒": f"{weekday} {hour}:{minute}:{second}",
        "时 分": f"{hour}:{minute}",
        "时 分 秒": f"{hour}:{minute}:{second}",
        "分 秒": f"{minute}分{second}秒"
    }
    return mapping.get(style, "")

def format_late_duration(content):
    parts = content.split(" - ")
    if len(parts) != 2:
        return ""
    
    style = parts[0]
    class_time_str = parts[1]
    
    try:
        class_parts = class_time_str.split(":")
        if len(class_parts) == 2:
            class_hour, class_minute = int(class_parts[0]), int(class_parts[1])
            class_second = 0
        elif len(class_parts) == 3:
            class_hour, class_minute, class_second = int(class_parts[0]), int(class_parts[1]), int(class_parts[2])
        else:
            return ""
        
        now = datetime.datetime.now()
        class_time = datetime.datetime(now.year, now.month, now.day, class_hour, class_minute, class_second)
        
        if now < class_time:
            delta = class_time - now
            diff_seconds = int(delta.total_seconds())
        else:
            delta = now - class_time
            diff_seconds = int(delta.total_seconds())
        
        hours = diff_seconds // 3600
        minutes = (diff_seconds % 3600) // 60
        seconds = diff_seconds % 60
        
        total_minutes = diff_seconds // 60
        
        mapping = {
            "时 分": f"{hours}时{minutes}分",
            "时 分 秒": f"{hours}时{minutes}分{seconds}秒",
            "分": f"{total_minutes}分",
            "分 秒": f"{total_minutes}分{seconds}秒",
            "秒": f"{diff_seconds}秒"
        }
        return mapping.get(style, "")
    except:
        return ""

def add_ele(root, frame, bt_add, control_frame):
    clear_control_frame(control_frame)
    
    label = tk.Label(control_frame, text="请问您想要添加什么元素")
    label.pack(side="left", padx=5)
    
    bt_text = tk.Button(control_frame, text="文字", command=lambda: show_text_input(root, frame, bt_add, control_frame))
    bt_text.pack(side="left", padx=5)
    
    bt_time = tk.Button(control_frame, text="时间", command=lambda: show_time_select(root, frame, bt_add, control_frame))
    bt_time.pack(side="left", padx=5)
    
    bt_late = tk.Button(control_frame, text="距离上课时间", command=lambda: show_late_duration(root, frame, bt_add, control_frame))
    bt_late.pack(side="left", padx=5)

def clear_control_frame(control_frame):
    for widget in control_frame.winfo_children():
        widget.destroy()

def show_text_input(root, frame, bt_add, control_frame):
    clear_control_frame(control_frame)
    
    label = tk.Label(control_frame, text="请编辑该元素")
    label.pack(pady=5)
    
    text_input = tk.Entry(control_frame, width=50)
    text_input.pack(pady=5)
    text_input.focus()
    
    def confirm_text():
        text = text_input.get().strip()
        if text:
            create_element_button(root, frame, bt_add, control_frame, "text", text)
            clear_control_frame(control_frame)
    
    def cancel_text():
        clear_control_frame(control_frame)
    
    btn_frame = tk.Frame(control_frame)
    btn_frame.pack(pady=5)
    
    bt_confirm = tk.Button(btn_frame, text="确定", command=confirm_text)
    bt_confirm.pack(side="left", padx=5)
    
    bt_cancel = tk.Button(btn_frame, text="取消", command=cancel_text)
    bt_cancel.pack(side="left", padx=5)

def show_time_select(root, frame, bt_add, control_frame):
    clear_control_frame(control_frame)
    
    label = tk.Label(control_frame, text="请选择你想要的时间样式")
    label.pack(pady=5)
    
    time_styles = [
        "年 月 日 时 分",
        "年 月 日 时 分 秒",
        "月 日 时 分",
        "月 日 时 分 秒",
        "日 时 分",
        "日 时 分 秒",
        "星期 时 分",
        "星期 时 分 秒",
        "时 分",
        "时 分 秒",
        "分 秒"
    ]
    
    combobox = ttk.Combobox(control_frame, values=time_styles, width=38, state="readonly")
    combobox.set(time_styles[0])
    combobox.pack(pady=5)
    
    def confirm_time():
        style = combobox.get()
        if style:
            create_element_button(root, frame, bt_add, control_frame, "time", style)
            clear_control_frame(control_frame)
    
    def cancel_time():
        clear_control_frame(control_frame)
    
    btn_frame = tk.Frame(control_frame)
    btn_frame.pack(pady=5)
    
    bt_confirm = tk.Button(btn_frame, text="确定", command=confirm_time)
    bt_confirm.pack(side="left", padx=5)
    
    bt_cancel = tk.Button(btn_frame, text="取消", command=cancel_time)
    bt_cancel.pack(side="left", padx=5)

def show_late_duration(root, frame, bt_add, control_frame):
    clear_control_frame(control_frame)
    
    label = tk.Label(control_frame, text="请选择时间样式")
    label.pack(pady=5)
    
    duration_styles = [
        "时 分",
        "时 分 秒",
        "分",
        "分 秒",
        "秒"
    ]
    
    combobox = ttk.Combobox(control_frame, values=duration_styles, width=38, state="readonly")
    combobox.set(duration_styles[0])
    combobox.pack(pady=5)
    
    label_time = tk.Label(control_frame, text="请输入上课时间 (格式: HH:MM 或 HH:MM:SS)")
    label_time.pack(pady=5)
    
    time_input = tk.Entry(control_frame, width=20)
    time_input.pack(pady=5)
    time_input.focus()
    
    def confirm_late():
        style = combobox.get()
        class_time = time_input.get().strip()
        if style and class_time:
            content = f"{style} - {class_time}"
            create_element_button(root, frame, bt_add, control_frame, "late_duration", content)
            clear_control_frame(control_frame)
    
    def cancel_late():
        clear_control_frame(control_frame)
    
    btn_frame = tk.Frame(control_frame)
    btn_frame.pack(pady=5)
    
    bt_confirm = tk.Button(btn_frame, text="确定", command=confirm_late)
    bt_confirm.pack(side="left", padx=5)
    
    bt_cancel = tk.Button(btn_frame, text="取消", command=cancel_late)
    bt_cancel.pack(side="left", padx=5)

def show_edit_late_duration(root, frame, bt_add, control_frame, element_btn, current_content):
    clear_control_frame(control_frame)
    
    label = tk.Label(control_frame, text="请选择时间样式")
    label.pack(pady=5)
    
    duration_styles = [
        "时 分",
        "时 分 秒",
        "分",
        "分 秒",
        "秒"
    ]
    
    parts = current_content.split(" - ")
    current_style = parts[0] if len(parts) > 0 else duration_styles[0]
    current_time = parts[1] if len(parts) > 1 else ""
    
    combobox = ttk.Combobox(control_frame, values=duration_styles, width=38, state="readonly")
    combobox.set(current_style)
    combobox.pack(pady=5)
    
    label_time = tk.Label(control_frame, text="请输入上课时间 (格式: HH:MM 或 HH:MM:SS)")
    label_time.pack(pady=5)
    
    time_input = tk.Entry(control_frame, width=20)
    time_input.insert(0, current_time)
    time_input.pack(pady=5)
    time_input.focus()
    
    def confirm_edit():
        style = combobox.get()
        class_time = time_input.get().strip()
        if style and class_time:
            new_content = f"{style} - {class_time}"
            element_btn.config(text=new_content)
            for elem in elements:
                if elem["button"] == element_btn:
                    elem["content"] = new_content
                    break
            clear_control_frame(control_frame)
    
    def delete_element():
        element_btn.destroy()
        elements[:] = [elem for elem in elements if elem["button"] != element_btn]
        clear_control_frame(control_frame)
    
    def cancel_edit():
        clear_control_frame(control_frame)
    
    btn_frame = tk.Frame(control_frame)
    btn_frame.pack(pady=5)
    
    bt_confirm = tk.Button(btn_frame, text="确定", command=confirm_edit)
    bt_confirm.pack(side="left", padx=5)
    
    bt_delete = tk.Button(btn_frame, text="删除", command=delete_element)
    bt_delete.pack(side="left", padx=5)
    
    bt_cancel = tk.Button(btn_frame, text="取消", command=cancel_edit)
    bt_cancel.pack(side="left", padx=5)

def create_element_button(root, frame, bt_add, control_frame, element_type, content):
    def edit_element():
        current_content = element_btn.cget("text")
        if element_type == "text":
            show_edit_text(root, frame, bt_add, control_frame, element_btn, current_content)
        elif element_type == "time":
            show_edit_time(root, frame, bt_add, control_frame, element_btn, current_content)
        elif element_type == "late_duration":
            show_edit_late_duration(root, frame, bt_add, control_frame, element_btn, current_content)
    
    element_btn = tk.Button(frame, text=content, command=edit_element)
    element_btn.pack(side="left", padx=2, pady=2)
    bt_add.pack(side="left", padx=2, pady=2)
    
    elements.append({"type": element_type, "content": content, "button": element_btn})

def show_edit_text(root, frame, bt_add, control_frame, element_btn, current_text):
    clear_control_frame(control_frame)
    
    label = tk.Label(control_frame, text="请编辑该元素")
    label.pack(pady=5)
    
    text_input = tk.Entry(control_frame, width=50)
    text_input.insert(0, current_text)
    text_input.pack(pady=5)
    text_input.focus()
    text_input.select_range(0, tk.END)
    
    def confirm_edit():
        new_text = text_input.get().strip()
        if new_text:
            element_btn.config(text=new_text)
            for elem in elements:
                if elem["button"] == element_btn:
                    elem["content"] = new_text
                    break
            clear_control_frame(control_frame)
    
    def delete_element():
        element_btn.destroy()
        elements[:] = [elem for elem in elements if elem["button"] != element_btn]
        clear_control_frame(control_frame)
    
    def cancel_edit():
        clear_control_frame(control_frame)
    
    btn_frame = tk.Frame(control_frame)
    btn_frame.pack(pady=5)
    
    bt_confirm = tk.Button(btn_frame, text="确定", command=confirm_edit)
    bt_confirm.pack(side="left", padx=5)
    
    bt_delete = tk.Button(btn_frame, text="删除", command=delete_element)
    bt_delete.pack(side="left", padx=5)
    
    bt_cancel = tk.Button(btn_frame, text="取消", command=cancel_edit)
    bt_cancel.pack(side="left", padx=5)

def show_edit_time(root, frame, bt_add, control_frame, element_btn, current_style):
    clear_control_frame(control_frame)
    
    label = tk.Label(control_frame, text="请选择你想要的时间样式")
    label.pack(pady=5)
    
    time_styles = [
        "年 月 日 时 分",
        "年 月 日 时 分 秒",
        "月 日 时 分",
        "月 日 时 分 秒",
        "日 时 分",
        "日 时 分 秒",
        "星期 时 分",
        "星期 时 分 秒",
        "时 分",
        "时 分 秒",
        "分 秒"
    ]
    
    combobox = ttk.Combobox(control_frame, values=time_styles, width=38, state="readonly")
    combobox.set(current_style)
    combobox.pack(pady=5)
    
    def confirm_edit():
        new_style = combobox.get()
        if new_style:
            element_btn.config(text=new_style)
            for elem in elements:
                if elem["button"] == element_btn:
                    elem["content"] = new_style
                    break
            clear_control_frame(control_frame)
    
    def delete_element():
        element_btn.destroy()
        elements[:] = [elem for elem in elements if elem["button"] != element_btn]
        clear_control_frame(control_frame)
    
    def cancel_edit():
        clear_control_frame(control_frame)
    
    btn_frame = tk.Frame(control_frame)
    btn_frame.pack(pady=5)
    
    bt_confirm = tk.Button(btn_frame, text="确定", command=confirm_edit)
    bt_confirm.pack(side="left", padx=5)
    
    bt_delete = tk.Button(btn_frame, text="删除", command=delete_element)
    bt_delete.pack(side="left", padx=5)
    
    bt_cancel = tk.Button(btn_frame, text="取消", command=cancel_edit)
    bt_cancel.pack(side="left", padx=5)

def send_loop(root):
    global is_sending, send_interval, last_send_time
    if is_sending:
        now = time.time()
        if now - last_send_time >= send_interval:
            message = generate_message()
            if message:
                send(message)
                pag.press("enter")
            last_send_time = now
        root.after(100, send_loop, root)

def toggle_sending(root, interval_entry, bt_start):
    global is_sending, send_interval, last_send_time
    if is_sending:
        is_sending = False
        bt_start.config(text="开始生成")
        interval_entry.config(state="normal")
    else:
        try:
            interval = int(interval_entry.get().strip())
            if 1 <= interval <= 60:
                send_interval = interval
                is_sending = True
                last_send_time = time.time()
                bt_start.config(text="停止生成")
                interval_entry.config(state="disabled")
                send_loop(root)
            else:
                interval_entry.delete(0, tk.END)
                interval_entry.insert(0, str(send_interval))
        except:
            interval_entry.delete(0, tk.END)
            interval_entry.insert(0, str(send_interval))

def update_preview(root, preview_var):
    message = generate_message()
    preview_var.set(message if message else "暂无内容")
    root.after(100, update_preview, root, preview_var)

def main(root):
    global control_frame
    
    title = tk.Label(root, text="超级尊贵紫钻VIP顾旺旺专属微信轰炸器", font=("Arial", 15))
    title.pack()
    author = tk.Label(root, text="by LSS")
    author.place(x=10, y=5)

    frame = tk.Frame(root, relief="sunken", bd=3)
    frame.pack(pady=10, fill="x", padx=10)

    bt_add = tk.Button(frame, text="   +   ", command=lambda: add_ele(root, frame, bt_add, control_frame))
    bt_add.pack(side="left", padx=2, pady=2)

    control_frame = tk.Frame(root)
    control_frame.pack(pady=10, fill="x", padx=10)

    preview_frame = tk.Frame(root)
    preview_frame.pack(side="bottom", pady=10, padx=10, fill="x")

    preview_label = tk.Label(preview_frame, text="效果预览:", anchor="w")
    preview_label.pack(side="top", fill="x")

    preview_var = tk.StringVar(value="暂无内容")
    preview_text = tk.Label(preview_frame, textvariable=preview_var, anchor="w", wraplength=760)
    preview_text.pack(side="top", fill="x", pady=2)

    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side="bottom", pady=5, padx=10)

    interval_label = tk.Label(bottom_frame, text="发送间隔(秒):")
    interval_label.pack(side="left", padx=5)

    interval_entry = tk.Entry(bottom_frame, width=10)
    interval_entry.insert(0, str(send_interval))
    interval_entry.pack(side="left", padx=5)

    bt_start = tk.Button(bottom_frame, text="开始生成", command=lambda: toggle_sending(root, interval_entry, bt_start))
    bt_start.pack(side="left", padx=5)

    root.after(100, update_preview, root, preview_var)

if __name__ == "__main__":
    update_thread = threading.Thread(target=auto_update, daemon=True)
    update_thread.start()

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.geometry("1000x550")
    root.title("超级尊贵紫钻VIP顾旺旺专属微信轰炸器")

    main(root)

    root.mainloop()
