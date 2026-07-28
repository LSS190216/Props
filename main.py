import time
import datetime
import platform
import urllib.request
import os
import threading
import sys
import subprocess
import math
import random

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import font
except:
    if platform.system() == "Darwin":
        print("依赖配置错误，正在为您修复，请勿关闭软件。（1/2）", end = "\r")
        os.system("brew install python-tk")
    else:
        print("系统Python损坏，请重装！")
        sys.exit(0)

ipts = ""

try:
    import pyautogui as pag
except:
    ipts += " pyautogui"
try:
    import pyperclip as clp
except:
    ipts += " pyperclip"
try:
    import akshare as ak
except:
    ipts += " akshare"
try:
    import pandas as pd
except:
    ipts += " pandas"


if ipts:
    print("依赖配置错误，正在为您修复，请勿关闭软件。（2/2）")
    os.system(f"pip3 install{ipts} --user -i https://pypi.tuna.tsinghua.edu.cn/simple")
    print("修复完成，将在3秒后重启。", end = "\r")
    time.sleep(1)
    print("修复完成，将在2秒后重启。", end = "\r")
    time.sleep(1)
    print("修复完成，将在1秒后重启。", end = "\r")
    time.sleep(1)
    print("                           ")
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
        urls = [
            "https://raw.githubusercontent.com/LSS190216/Props/refs/heads/main/main.py",
            "https://cdn.jsdelivr.net/gh/LSS190216/Props@main/main.py"
        ]
        local_path = os.path.abspath(__file__)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        content = None
        for url in urls:
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    content = response.read()
                break
            except Exception as e:
                print(f"Failed to fetch from {url}: {e}")
        
        if content:
            decoded_content = content.decode("utf-8", errors="ignore")
            
            if decoded_content.startswith("import ") or decoded_content.startswith("#") or decoded_content.strip().startswith("def ") or decoded_content.strip().startswith("class "):
                with open(local_path, "wb") as f:
                    f.write(content)
            else:
                print(decoded_content)
        else:
            print("Failed to fetch from all URLs")
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
    
    bt_late = tk.Button(control_frame, text="计时", command=lambda: show_late_duration(root, frame, bt_add, control_frame))
    bt_late.pack(side="left", padx=5)

    hint = tk.Label(control_frame, text="计时元素常用于告诉迟到的学生距离上课的时间", fg = "gray")
    hint.pack(side="left", padx=30)

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
    
    label_time = tk.Label(control_frame, text="请输入开始时间 (格式: HH:MM 或 HH:MM:SS)")
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
    
    label_time = tk.Label(control_frame, text="请输入开始时间 (格式: HH:MM 或 HH:MM:SS)")
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

def create_breathing_text(
    root, 
    base_size=18, 
    amplitude=2, 
    period=1500, 
    color="orange", 
    angle=0, 
    pos_relx=1.0, 
    pos_rely=1.0, 
    pos_anchor="se", 
    pos_x=-10, 
    pos_y=-10, 
    fps=30
    ):

    texts = ["LSS出品，必属精品！", 
    "您的股票涨了吗？", 
    "该程序不会黑掉您的电脑！", 
    "GWW_Everything-wins", 
    "距离东山再起只差10个学生了！", 
    "该文本使用sin函数来计算缩放大小！", 
    "LSS.exe未响应，因为数学题太难了", 
    "为什么那么难！", 
    "我这个理工男已经很努力地排版该应用了！", 
    "猜猜同时抽中3个相同的文字的概率是多大？"]
    
    text = random.choice(texts)

    if platform.system() == "Darwin":
        font_name = "PingFang SC"
    else:
        font_name = "Microsoft YaHei"
    
    # 计算文字最大尺寸，留出呼吸空间
    max_size = base_size + amplitude
    font_obj = font.Font(family=font_name, size=max_size, weight="bold")
    text_width = font_obj.measure(text)
    text_height = font_obj.metrics("linespace")
    
    # Canvas尺寸略大于文字最大尺寸，留出边距
    padding = 10
    canvas_width = text_width + padding * 2
    canvas_height = text_height + padding * 2
    
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, highlightthickness=0, bg=root.cget("bg"))
    canvas.place(relx=pos_relx, rely=pos_rely, anchor=pos_anchor, x=pos_x, y=pos_y)

    # 在Canvas中心创建文字
    text_id = canvas.create_text(canvas_width // 2, canvas_height // 2, text=text, fill=color, 
                                  angle=angle, font=(font_name, base_size, "bold"))
    
    start_time = time.time()
    interval = int(1000 / fps)  # 计算每帧间隔（毫秒）
    
    def animate():
        elapsed = (time.time() - start_time) * 1000
        scale = 1 + (amplitude / base_size) * math.sin(2 * math.pi * elapsed / period)
        current_size = int(base_size * scale)
        canvas.itemconfig(text_id, font=(font_name, current_size, "bold"))
        root.after(interval, animate)
    
    def set_text(new_text):
        canvas.itemconfig(text_id, text=new_text)
        # 重新计算尺寸
        new_width = font_obj.measure(new_text)
        new_height = font_obj.metrics("linespace")
        new_canvas_width = new_width + padding * 2
        new_canvas_height = new_height + padding * 2
        canvas.config(width=new_canvas_width, height=new_canvas_height)
        canvas.coords(text_id, new_canvas_width // 2, new_canvas_height // 2)
    
    animate()
    return canvas, set_text

def fetch_stock_data():
    sources = [
        ("新浪财经", lambda: ak.stock_zh_a_spot()),
        ("东方财富", lambda: ak.stock_zh_a_spot_em()),
    ]
    last_error = None
    for name, fetch_func in sources:
        try:
            df = fetch_func()
            col_map = {}
            for col in df.columns:
                col_lower = str(col).lower()
                if "涨跌幅" in str(col) or ("change" in col_lower and "pct" in col_lower):
                    col_map[col] = "涨跌幅"
                elif "最新价" in str(col) or "close" in col_lower or "trade" in col_lower:
                    col_map[col] = "最新价"
                elif "成交额" in str(col) or "amount" in col_lower or "turnover" in col_lower:
                    col_map[col] = "成交额"
                elif "代码" in str(col) or "code" in col_lower:
                    col_map[col] = "代码"
                elif "名称" in str(col) or "name" in col_lower:
                    col_map[col] = "名称"
            df = df.rename(columns=col_map)
            if "涨跌幅" in df.columns:
                df = df.sort_values(by="涨跌幅", ascending=False).head(300)
            else:
                df = df.head(300)
            return df, name
        except Exception as e:
            last_error = str(e)
            print(f"Failed to fetch from {name}: {e}")
            continue
    return None, last_error or "所有数据源均不可用"

def show_stock_window():
    stock_win = tk.Toplevel(root)
    stock_win.title("神秘功能")
    stock_win.geometry("800x650")
    stock_win.attributes("-topmost", True)
    
    loading_label = tk.Label(stock_win, text="正在加载...", font=("Microsoft YaHei", 12))
    loading_label.pack(pady=50)
    
    def do_fetch():
        df, source_name = fetch_stock_data()
        if df is not None:
            stock_win.after(0, lambda d=df, src=source_name: render_stocks(stock_win, d, src))
        else:
            err_msg = source_name
            stock_win.after(0, lambda msg=err_msg: render_error(stock_win, msg, retry_fetch))
    
    def retry_fetch():
        for widget in stock_win.winfo_children():
            widget.destroy()
        tk.Label(stock_win, text="正在加载...", font=("Microsoft YaHei", 12)).pack(pady=50)
        threading.Thread(target=do_fetch, daemon=True).start()
    
    threading.Thread(target=do_fetch, daemon=True).start()

def render_stocks(win, df, source_name):
    for widget in win.winfo_children():
        widget.destroy()
    
    # 顶部状态栏
    status_frame = tk.Frame(win)
    status_frame.pack(fill="x", padx=10, pady=(5, 0))
    tk.Label(status_frame, text=f"数据来源: {source_name}", font=("Microsoft YaHei", 9), fg="gray").pack(side="left")
    count_label = tk.Label(status_frame, text=f"共 {len(df)} 条", font=("Microsoft YaHei", 9), fg="gray")
    count_label.pack(side="right")
    
    # 表头
    header_frame = tk.Frame(win)
    header_frame.pack(fill="x", padx=10, pady=5)
    headers = ["序号", "代码", "名称", "最新价", "涨跌幅", "成交额"]
    widths = [5, 10, 8, 8, 10, 10]
    for i, (h, w) in enumerate(zip(headers, widths)):
        tk.Label(header_frame, text=h, font=("Microsoft YaHei", 10, "bold"), width=w, anchor="center").grid(row=0, column=i, padx=2, pady=2)
    
    # 数据区域：Canvas + 滚动条
    container = tk.Frame(win)
    container.pack(fill="both", expand=True, padx=10, pady=5)
    
    canvas = tk.Canvas(container, highlightthickness=0, borderwidth=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)
    
    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    for idx, (_, row) in enumerate(df.iterrows()):
        change_pct = row.get("涨跌幅", 0)
        if pd.isna(change_pct):
            change_pct = 0
        if change_pct > 0:
            fg_color = "red"
            arrow = "▲"
        elif change_pct < 0:
            fg_color = "green"
            arrow = "▼"
        else:
            fg_color = "black"
            arrow = "—"
        
        row_frame = tk.Frame(scroll_frame)
        row_frame.pack(fill="x", padx=5, pady=1)
        
        tk.Label(row_frame, text=str(idx + 1), font=("Microsoft YaHei", 10), width=5, anchor="center").grid(row=0, column=0, padx=2)
        tk.Label(row_frame, text=str(row.get("代码", "")), font=("Microsoft YaHei", 10), width=10, anchor="center").grid(row=0, column=1, padx=2)
        tk.Label(row_frame, text=str(row.get("名称", "")), font=("Microsoft YaHei", 10), width=10, anchor="center").grid(row=0, column=2, padx=2)
        price = row.get("最新价", 0)
        if pd.isna(price):
            price = 0
        tk.Label(row_frame, text=f"{price:.2f}", font=("Microsoft YaHei", 10), width=8, anchor="center", fg=fg_color).grid(row=0, column=3, padx=2)
        tk.Label(row_frame, text=f"{arrow} {change_pct:.2f}%", font=("Microsoft YaHei", 10, "bold"), width=10, anchor="center", fg=fg_color).grid(row=0, column=4, padx=2)
        amount = row.get("成交额", 0)
        if pd.isna(amount):
            amount = 0
        tk.Label(row_frame, text=f"{amount/1e8:.2f}亿", font=("Microsoft YaHei", 10), width=12, anchor="center").grid(row=0, column=5, padx=2)

def render_error(win, error_msg, retry_func):
    for widget in win.winfo_children():
        widget.destroy()
    tk.Label(win, text="获取数据失败", font=("Microsoft YaHei", 14, "bold"), fg="red").pack(pady=(30, 10))
    tk.Label(win, text=error_msg, font=("Microsoft YaHei", 10), fg="gray", wraplength=500).pack(pady=10)
    tk.Button(win, text="重试", command=retry_func, font=("Microsoft YaHei", 10), width=15).pack(pady=10)

def main(root):
    global control_frame
    
    title = tk.Label(root, text="超级尊贵紫钻VIP顾旺旺专属微信轰炸器", font=("Arial", 15))
    title.pack()
    author = tk.Label(root, text="by LSS")
    author.place(x=10, y=5)
    
    btn_mystery = tk.Label(root, text="神秘功能", fg="blue", cursor="hand2", 
                          font=("Microsoft YaHei", 9, "underline"))
    btn_mystery.place(relx=1.0, y=5, anchor="ne", x=-10)
    btn_mystery.bind("<Button-1>", lambda e: show_stock_window())
    btn_mystery.bind("<Enter>", lambda e: btn_mystery.config(fg="#0000EE"))
    btn_mystery.bind("<Leave>", lambda e: btn_mystery.config(fg="blue"))

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

    create_breathing_text(root, fps = 30)

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
