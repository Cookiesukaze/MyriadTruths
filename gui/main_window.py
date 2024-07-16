import tkinter as tk
from config.config import (
    load_config, get_folder_path, get_display_fonts, get_display_mode,
    get_auto_switch_interval, get_pause_on_click, set_folder_path,
    set_display_fonts, save_config, set_display_mode
)
from utils.file_utils import load_files_from_folder
from gui.settings_window import SettingsWindow

class MyriadTruthsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MyriadTruths")
        self.geometry("600x400")

        self.config = load_config()

        self.folder_path = get_folder_path(self.config)
        self.font_primary, self.font_secondary = get_display_fonts(self.config)
        self.display_mode = get_display_mode(self.config)
        self.auto_switch_interval = get_auto_switch_interval(self.config)
        self.pause_on_click = get_pause_on_click(self.config)
        self.bg_color = self.config.get('colors', 'background', fallback='white')
        self.fg_color = self.config.get('colors', 'foreground', fallback='black')
        self.opacity = self.config.getfloat('colors', 'opacity', fallback=1.0)

        self.text_area = tk.Text(self, wrap=tk.WORD, bg=self.bg_color, fg=self.fg_color)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind("<Button-1>", self.toggle_pause)
        self.text_area.bind("<Button-3>", self.show_context_menu)

        self.text_area.tag_configure('primary', font=self.font_primary)
        self.text_area.tag_configure('secondary', font=self.font_secondary)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="设置", command=self.open_settings)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="退出", command=self.quit)

        self.files_content = []
        self.current_file_index = 0
        self.current_line_index = 0
        self.is_paused = False

        self.attributes('-alpha', self.opacity)
        self.load_files()
        self.display_current_content()
        self.after(self.auto_switch_interval * 1000, self.switch_content)

    def load_files(self):
        self.files_content = load_files_from_folder(self.folder_path)
        if not self.files_content:
            print(f"文件夹 {self.folder_path} 为空或不存在")
        else:
            print(f"成功读取 {len(self.files_content)} 个文件")

    def display_current_content(self):
        if self.files_content:
            filename, content = self.files_content[self.current_file_index]
            self.display_content(content, self.display_mode)

    def display_content(self, content, mode):
        self.text_area.delete(1.0, tk.END)
        if mode == 'single_line':
            lines_per_display = self.config.getint('display', 'lines_per_display', fallback=1)
            for line in content[self.current_line_index:self.current_line_index+lines_per_display]:
                self.text_area.insert(tk.END, line + '\n', 'primary')
        elif mode == 'double_line':
            if self.current_line_index < len(content):
                self.text_area.insert(tk.END, content[self.current_line_index] + '\n', 'primary')
            if self.current_line_index + 1 < len(content):
                self.text_area.insert(tk.END, content[self.current_line_index + 1] + '\n', 'primary')
        elif mode == 'double_line_mixed_font':
            if self.current_line_index < len(content):
                parts = content[self.current_line_index].split('\t')
                if len(parts) >= 2:
                    self.text_area.insert(tk.END, parts[0] + '\n', 'primary')
                    self.text_area.insert(tk.END, parts[1] + '\n', 'secondary')

    def switch_content(self):
        if not self.is_paused:
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
        self.after(self.auto_switch_interval * 1000, self.switch_content)

    def toggle_pause(self, event):
        if self.pause_on_click:
            self.is_paused = not self.is_paused

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

if __name__ == "__main__":
    app = MyriadTruthsApp()
    app.mainloop()