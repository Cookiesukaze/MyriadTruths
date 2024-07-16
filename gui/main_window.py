import tkinter as tk
import signal
from config.config import (
    load_config, get_folder_path, get_display_fonts, get_display_mode,
    get_auto_switch_interval, get_pause_on_click, set_window_geometry, get_window_geometry
)
from gui.settings_window import SettingsWindow
from utils.window_utils import add_drag_functionality, add_resize_handles
from utils.file_loader import load_files
from utils.content_display import display_content, switch_content

class MyriadTruthsApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.config = load_config()

        self.folder_path = get_folder_path(self.config)
        self.font_primary, self.font_secondary = get_display_fonts(self.config)
        self.display_mode = get_display_mode(self.config)
        self.auto_switch_interval = get_auto_switch_interval(self.config)
        self.pause_on_click = get_pause_on_click(self.config)
        self.bg_color = self.config.get('colors', 'background', fallback='white')
        self.fg_color = self.config.get('colors', 'foreground', fallback='black')
        self.opacity = self.config.getfloat('colors', 'opacity', fallback=1.0)

        # 设置窗口几何位置和大小
        geometry = get_window_geometry(self.config)
        self.geometry(geometry)
        self.overrideredirect(True)  # 去掉顶栏

        # 添加可拖动的顶部条
        self.top_bar = tk.Frame(self, bg='gray', height=20, cursor='fleur')
        self.top_bar.pack(fill=tk.X)
        add_drag_functionality(self, self.top_bar)

        # 添加文本区域
        self.text_area = tk.Text(self, wrap=tk.WORD, bg=self.bg_color, fg=self.fg_color)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind("<Button-1>", self.toggle_pause)
        self.text_area.bind("<Button-3>", self.show_context_menu)

        self.text_area.tag_configure('primary', font=self.font_primary)
        self.text_area.tag_configure('secondary', font=self.font_secondary)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="设置", command=self.open_settings)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="退出", command=self.on_closing)

        self.files_content = []
        self.current_file_index = 0
        self.current_line_index = 0
        self.is_paused = False

        self.attributes('-alpha', self.opacity)
        self.load_files()
        self.display_current_content()
        self.after(self.auto_switch_interval * 1000, self.switch_content)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # 捕捉窗口关闭事件

        # 捕捉终止信号
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # 绑定调整窗口大小的事件
        self.bind("<Enter>", lambda event: add_resize_handles(self))

    def load_files(self):
        self.files_content = load_files(self.folder_path)

    def display_current_content(self):
        if self.files_content:
            filename, content = self.files_content[self.current_file_index]
            display_content(self.text_area, content, self.display_mode, self.config, self.current_line_index, self.font_primary, self.font_secondary)

    def switch_content(self):
        switch_content(self)

    def toggle_pause(self, event):
        if self.pause_on_click:
            self.is_paused = not self.is_paused

    def manual_switch(self, event):
        if event.x < self.text_area.winfo_width() // 2:
            self.previous_content()
        else:
            self.next_content()

    def previous_content(self):
        if self.files_content:
            self.current_file_index = (self.current_file_index - 1) % len(self.files_content)
            self.current_line_index = 0
            self.display_current_content()

    def next_content(self):
        if self.files_content:
            self.current_file_index = (self.current_file_index + 1) % len(self.files_content)
            self.current_line_index = 0
            self.display_current_content()

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def open_settings(self):
        SettingsWindow(self)

    def apply_settings(self, config):
        self.config = config
        self.folder_path = get_folder_path(self.config)
        self.font_primary, self.font_secondary = get_display_fonts(self.config)
        self.display_mode = get_display_mode(self.config)
        self.auto_switch_interval = get_auto_switch_interval(self.config)
        self.pause_on_click = get_pause_on_click(self.config)
        self.bg_color = self.config.get('colors', 'background', fallback='white')
        self.fg_color = self.config.get('colors', 'foreground', fallback='black')
        self.opacity = self.config.getfloat('colors', 'opacity', fallback=1.0)

        self.text_area.config(bg=self.bg_color, fg=self.fg_color)
        self.text_area.tag_configure('primary', font=self.font_primary)
        self.text_area.tag_configure('secondary', font=self.font_secondary)
        self.attributes('-alpha', self.opacity)
        self.load_files()
        self.display_current_content()

    def on_closing(self):
        # 保存窗口几何位置和大小
        geometry = self.winfo_geometry()
        print(f"保存窗口几何位置和大小: {geometry}")  # 在控制台打印几何信息
        set_window_geometry(self.config, geometry)
        self.destroy()

    def signal_handler(self, signal_received, frame):
        self.on_closing()

if __name__ == "__main__":
    app = MyriadTruthsApp()
    app.mainloop()