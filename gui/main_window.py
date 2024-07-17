import tkinter as tk
import signal
from tkinter import messagebox
from config.config import (
    load_config, save_config, set_window_geometry, set_current_file_index, set_current_line_index,
    get_folder_path, get_display_fonts, get_display_mode,
    get_auto_switch_interval, get_pause_on_click, get_always_on_top,
    get_switch_mode
)
from gui.settings_window import SettingsWindow
from gui.gui_helper import initialize_gui, parse_font, load_app_files, display_current_content, random_content
from utils.window_utils import add_resize_handles


class MyriadTruthsApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.config = load_config()
        initialize_gui(self)
        self.switch_content_id = None  # 初始化 switch_content_id

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # 捕捉窗口关闭事件

        # 捕捉终止信号
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # 绑定调整窗口大小的事件，只保留左下和右下两个小块
        self.bind("<Enter>", lambda event: add_resize_handles(self))

        # 创建右键菜单
        self.create_context_menu()

    def parse_font(self, font_str):
        return parse_font(font_str)

    def load_files(self):
        load_app_files(self)

    def display_current_content(self):
        display_current_content(self)

    def switch_content(self):
        if not self.is_paused:
            if self.switch_mode == 'sequential':
                self.next_content()
            elif self.switch_mode == 'sequential_resume':
                self.next_content()
            elif self.switch_mode == 'random':
                self.random_content()
            self.switch_content_id = self.after(self.auto_switch_interval * 1000, self.switch_content)

    def random_content(self):
        random_content(self)

    def toggle_pause(self, event):
        if self.pause_on_click:
            self.is_paused = not self.is_paused
            self.pause_label.config(text="Pause" if self.is_paused else "")
            if not self.is_paused:
                self.switch_content()

    def manual_switch(self, event):
        if event.x < self.text_area.winfo_width() // 2:
            self.previous_content()
        else:
            self.next_content()

    def previous_content(self):
        if self.display_mode == 'single_line':
            lines_per_display = self.config.getint('display', 'lines_per_display', fallback=1)
            self.current_line_index -= lines_per_display
            if self.current_line_index < 0:
                self.current_file_index = (self.current_file_index - 1) % len(self.files_content)
                self.current_line_index = len(self.files_content[self.current_file_index][1]) - lines_per_display
        elif self.display_mode == 'double_line':
            self.current_line_index -= 2
            if self.current_line_index < 0:
                self.current_file_index = (self.current_file_index - 1) % len(self.files_content)
                self.current_line_index = len(self.files_content[self.current_file_index][1]) - 2
        elif self.display_mode == 'double_line_mixed_font':
            self.current_line_index -= 1
            if self.current_line_index < 0:
                self.current_file_index = (self.current_file_index - 1) % len(self.files_content)
                self.current_line_index = len(self.files_content[self.current_file_index][1]) - 1
        self.display_current_content()

    def next_content(self):
        if self.display_mode == 'single_line':
            lines_per_display = self.config.getint('display', 'lines_per_display', fallback=1)
            self.current_line_index += lines_per_display
            if self.current_line_index >= len(self.files_content[self.current_file_index][1]):
                self.current_line_index = 0
                self.current_file_index = (self.current_file_index + 1) % len(self.files_content)
        elif self.display_mode == 'double_line':
            self.current_line_index += 2
            if self.current_line_index >= len(self.files_content[self.current_file_index][1]):
                self.current_line_index = 0
                self.current_file_index = (self.current_file_index + 1) % len(self.files_content)
        elif self.display_mode == 'double_line_mixed_font':
            self.current_line_index += 1
            if self.current_line_index >= len(self.files_content[self.current_file_index][1]):
                self.current_line_index = 0
                self.current_file_index = (self.current_file_index + 1) % len(self.files_content)
        self.display_current_content()

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def open_settings(self):
        SettingsWindow(self)

    def show_about(self):
        messagebox.showinfo("About Myriad Truths", "Author: Cookiesukaze\nRepository: github.com/Cookiesukaze/MyriadTruths\nVersion: 0.1.0\nThank you for using!\nFeel free to ask questions in issues or email me (Cookiesukaze@qq.com).")

    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="设置", command=self.open_settings)
        self.context_menu.add_command(label="关于", command=self.show_about)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="退出", command=self.on_closing)

        self.bind("<Button-3>", self.show_context_menu)  # 右键点击显示菜单

    def apply_settings(self, config):
        previous_switch_mode = self.switch_mode
        self.config = config
        self.folder_path = get_folder_path(self.config)
        self.font_primary, self.font_secondary = get_display_fonts(self.config)
        self.display_mode = get_display_mode(self.config)
        self.auto_switch_interval = get_auto_switch_interval(self.config)
        self.pause_on_click = get_pause_on_click(self.config)
        self.bg_color = self.config.get('colors', 'background', fallback='white')
        self.fg_color = self.config.get('colors', 'foreground', fallback='black')
        self.opacity = self.config.getfloat('colors', 'opacity', fallback=1.0)
        self.always_on_top = get_always_on_top(self.config)
        self.switch_mode = get_switch_mode(self.config)

        self.text_area.config(bg=self.bg_color, fg=self.fg_color)
        self.text_area.tag_configure('primary', font=self.parse_font(self.font_primary) or 'Arial 16')
        self.text_area.tag_configure('secondary', font=self.parse_font(self.font_secondary) or 'Arial 12')
        self.attributes('-alpha', self.opacity)
        self.attributes("-topmost", self.always_on_top)  # 设置窗口置顶
        self.load_files()

        # 如果切换到顺序模式，从头开始
        if self.switch_mode == 'sequential' and previous_switch_mode != 'sequential':
            self.current_file_index = 0
            self.current_line_index = 0

        self.display_current_content()

        # 重新设置切换内容的定时器
        if not self.is_paused:
            if self.switch_content_id is not None:
                self.after_cancel(self.switch_content_id)
            self.switch_content_id = self.after(self.auto_switch_interval * 1000, self.switch_content)

    def on_closing(self):
        # 保存当前文件索引和行索引
        set_current_file_index(self.config, self.current_file_index)
        set_current_line_index(self.config, self.current_line_index)

        # 保存窗口几何位置和大小
        geometry = self.winfo_geometry()
        print(f"保存窗口几何位置和大小: {geometry}")  # 在控制台打印几何信息
        set_window_geometry(self.config, geometry)
        save_config(self.config)
        self.destroy()

    def signal_handler(self, signal_received, frame):
        self.on_closing()


if __name__ == "__main__":
    app = MyriadTruthsApp()
    app.switch_content_id = app.after(app.auto_switch_interval * 1000, app.switch_content)
    app.mainloop()