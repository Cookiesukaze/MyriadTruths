# gui/gui_helper.py
import random
import tkinter as tk
from utils.content_display import display_content
from config.config import (
    get_folder_path, get_display_fonts, get_display_mode,
    get_auto_switch_interval, get_pause_on_click, get_always_on_top,
    get_switch_mode, get_current_file_index, get_current_line_index, get_window_geometry
)
from utils.file_loader import load_files
from utils.window_utils import add_drag_functionality, add_resize_handles

def initialize_gui(app):
    app.folder_path = get_folder_path(app.config)
    app.font_primary, app.font_secondary = get_display_fonts(app.config)
    app.display_mode = get_display_mode(app.config)
    app.auto_switch_interval = get_auto_switch_interval(app.config)
    app.pause_on_click = get_pause_on_click(app.config)
    app.bg_color = app.config.get('colors', 'background', fallback='white')
    app.fg_color = app.config.get('colors', 'foreground', fallback='black')
    app.opacity = app.config.getfloat('colors', 'opacity', fallback=1.0)
    app.always_on_top = get_always_on_top(app.config)
    app.switch_mode = get_switch_mode(app.config)

    geometry = get_window_geometry(app.config)
    app.geometry(geometry)
    app.overrideredirect(True)  # 去掉顶栏
    app.attributes("-topmost", app.always_on_top)  # 设置窗口置顶

    # 添加可拖动的顶部条，调整高度为 15
    app.top_bar = tk.Frame(app, bg='gray', height=10, cursor='fleur')
    app.top_bar.pack(fill=tk.X)
    add_drag_functionality(app, app.top_bar)

    # 定义一个小字体
    small_font = ('Arial', 8)

    # 添加回滚和前进按钮
    app.prev_button = tk.Button(app.top_bar, text="<", command=app.previous_content,
                                bg='gray', fg='white', relief=tk.FLAT,
                                font=small_font, pady=0, padx=0)
    app.prev_button.pack(side=tk.LEFT, padx=2, pady=0)

    app.pause_label = tk.Label(app.top_bar, text="", bg='gray', fg='white')
    app.pause_label.pack(side=tk.LEFT, padx=8)

    app.next_button = tk.Button(app.top_bar, text=">", command=app.next_content,
                                bg='gray', fg='white', relief=tk.FLAT,
                                font=small_font, pady=0, padx=0)
    app.next_button.pack(side=tk.RIGHT, padx=2, pady=0)

    # 添加文本区域
    app.text_area = tk.Text(app, wrap=tk.WORD, bg=app.bg_color, fg=app.fg_color)
    app.text_area.pack(fill=tk.BOTH, expand=True)
    app.text_area.bind("<Button-1>", app.toggle_pause)
    app.text_area.bind("<Button-3>", app.show_context_menu)

    app.text_area.tag_configure('primary', font=app.parse_font(app.font_primary) or 'Arial 16')
    app.text_area.tag_configure('secondary', font=app.parse_font(app.font_secondary) or 'Arial 12')

    app.context_menu = tk.Menu(app, tearoff=0)
    app.context_menu.add_command(label="设置", command=app.open_settings)
    app.context_menu.add_separator()
    app.context_menu.add_command(label="退出", command=app.on_closing)

    app.files_content = []
    app.current_file_index = get_current_file_index(app.config)
    app.current_line_index = get_current_line_index(app.config)
    app.is_paused = False

    app.attributes('-alpha', app.opacity)
    load_app_files(app)
    app.display_current_content()
    app.after(app.auto_switch_interval * 1000, app.switch_content)

def parse_font(font_str):
    parts = font_str.rsplit(' ', 1)
    if len(parts) == 2:
        font_name, font_size = parts
        return (font_name, int(font_size))
    return font_str

def load_app_files(app):
    app.files_content = load_files(app.folder_path)

def display_current_content(app):
    if app.text_area.winfo_exists() and app.files_content:
        filename, content = app.files_content[app.current_file_index]
        display_content(app.text_area, content, app.display_mode, app.config, app.current_line_index, app.font_primary, app.font_secondary)

def switch_content(app):
    if app.text_area.winfo_exists():
        if app.switch_mode == 'sequential':
            app.next_content()
        elif app.switch_mode == 'sequential_resume':
            app.next_content()
        elif app.switch_mode == 'random':
            app.random_content()
        app.after(app.auto_switch_interval * 1000, app.switch_content)

def random_content(app):
    app.current_file_index = random.randint(0, len(app.files_content) - 1)
    app.current_line_index = random.randint(0, len(app.files_content[app.current_file_index][1]) - 1)
    app.display_current_content()