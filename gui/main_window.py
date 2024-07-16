import configparser
import tkinter as tk
from tkinter import font, simpledialog, colorchooser
from config.config import (
    load_config, get_folder_path, get_display_fonts, get_display_mode,
    get_auto_switch_interval, get_pause_on_click, set_folder_path,
    set_display_fonts, save_config, set_display_mode
)
from utils.file_utils import load_files_from_folder

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

        self.text_area = tk.Text(self, wrap=tk.WORD, font=self.font_primary)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind("<Button-1>", self.toggle_pause)
        self.text_area.bind("<Button-3>", self.show_context_menu)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="设置", command=self.open_settings)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="退出", command=self.quit)

        self.files_content = []
        self.current_file_index = 0
        self.current_line_index = 0
        self.is_paused = False

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
                self.text_area.insert(tk.END, line + '\n')
        elif mode == 'double_line':
            if self.current_line_index < len(content):
                self.text_area.insert(tk.END, content[self.current_line_index] + '\n')
            if self.current_line_index + 1 < len(content):
                self.text_area.insert(tk.END, content[self.current_line_index + 1] + '\n')
        elif mode == 'double_line_mixed_font':
            if self.current_line_index < len(content):
                parts = content[self.current_line_index].split('\t')
                if len(parts) >= 2:
                    self.text_area.insert(tk.END, parts[0] + '\n', ('font', self.font_primary))
                    self.text_area.insert(tk.END, parts[1] + '\n', ('font', self.font_secondary))

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

        self.text_area.config(font=self.font_primary)
        self.load_files()
        self.display_current_content()

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("设置")
        self.geometry("400x300")
        self.parent = parent
        self.config = parent.config

        tk.Label(self, text="文件夹路径:").grid(row=0, column=0, sticky=tk.W)
        self.folder_path_entry = tk.Entry(self)
        self.folder_path_entry.grid(row=0, column=1, sticky=tk.EW)
        self.folder_path_entry.insert(0, get_folder_path(self.config))

        tk.Label(self, text="主字体:").grid(row=1, column=0, sticky=tk.W)
        self.font_primary_entry = tk.Entry(self)
        self.font_primary_entry.grid(row=1, column=1, sticky=tk.EW)
        self.font_primary_entry.insert(0, get_display_fonts(self.config)[0])

        tk.Label(self, text="次字体:").grid(row=2, column=0, sticky=tk.W)
        self.font_secondary_entry = tk.Entry(self)
        self.font_secondary_entry.grid(row=2, column=1, sticky=tk.EW)
        self.font_secondary_entry.insert(0, get_display_fonts(self.config)[1])

        tk.Label(self, text="背景颜色:").grid(row=3, column=0, sticky=tk.W)
        self.bg_color_button = tk.Button(self, text="选择颜色", command=self.choose_bg_color)
        self.bg_color_button.grid(row=3, column=1, sticky=tk.EW)

        tk.Label(self, text="文字颜色:").grid(row=4, column=0, sticky=tk.W)
        self.fg_color_button = tk.Button(self, text="选择颜色", command=self.choose_fg_color)
        self.fg_color_button.grid(row=4, column=1, sticky=tk.EW)

        tk.Label(self, text="透明度:").grid(row=5, column=0, sticky=tk.W)
        self.opacity_scale = tk.Scale(self, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.opacity_scale.grid(row=5, column=1, sticky=tk.EW)
        self.opacity_scale.set(self.config.getfloat('colors', 'opacity', fallback=1.0))

        tk.Label(self, text="显示模式:").grid(row=6, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value=get_display_mode(self.config))
        self.mode_options = {"单行显示": "single_line", "双行显示": "double_line", "双行混合字体显示": "double_line_mixed_font"}
        self.mode_menu = tk.OptionMenu(self, self.mode_var, *self.mode_options.keys())
        self.mode_menu.grid(row=6, column=1, sticky=tk.EW)

        tk.Button(self, text="保存", command=self.save_settings).grid(row=7, column=0, columnspan=2, sticky=tk.EW)

        self.grid_columnconfigure(1, weight=1)

    def choose_bg_color(self):
        color_code = colorchooser.askcolor(title="选择背景颜色")[1]
        if color_code:
            self.bg_color_button.config(bg=color_code)

    def choose_fg_color(self):
        color_code = colorchooser.askcolor(title="选择文字颜色")[1]
        if color_code:
            self.fg_color_button.config(fg=color_code)

    def save_settings(self):
        set_folder_path(self.config, self.folder_path_entry.get())
        set_display_fonts(self.config, self.font_primary_entry.get(), self.font_secondary_entry.get())
        self.config.set('colors', 'background', self.bg_color_button.cget('bg'))
        self.config.set('colors', 'foreground', self.fg_color_button.cget('fg'))
        self.config.set('colors', 'opacity', str(self.opacity_scale.get()))
        set_display_mode(self.config, self.mode_options.get(self.mode_var.get(), 'single_line'))
        save_config(self.config)
        self.parent.apply_settings(self.config)
        self.destroy()

if __name__ == "__main__":
    app = MyriadTruthsApp()
    app.mainloop()