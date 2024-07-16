import tkinter as tk
from tkinter import font, colorchooser, filedialog
import os
from config.config import (
    get_folder_path, get_display_fonts, get_display_mode, set_folder_path,
    set_display_fonts, save_config, set_display_mode
)

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("设置")
        self.geometry("400x500")
        self.parent = parent
        self.config = parent.config

        tk.Label(self, text="文件夹路径:").grid(row=0, column=0, sticky=tk.W)
        self.folder_path_entry = tk.Entry(self)
        self.folder_path_entry.grid(row=0, column=1, columnspan=2, sticky=tk.EW)
        self.folder_path_entry.insert(0, get_folder_path(self.config))

        tk.Label(self, text="主字体:").grid(row=1, column=0, sticky=tk.W)
        self.font_primary_family = tk.StringVar(value=self.parse_font_family(get_display_fonts(self.config)[0]))
        self.font_primary_family_entry = tk.Entry(self, textvariable=self.font_primary_family)
        self.font_primary_family_entry.grid(row=1, column=1, sticky=tk.EW)
        self.font_primary_browse = tk.Button(self, text="浏览", command=self.browse_primary_font)
        self.font_primary_browse.grid(row=1, column=2, sticky=tk.EW)

        tk.Label(self, text="主字体大小:").grid(row=2, column=0, sticky=tk.W)
        self.font_primary_size = tk.StringVar(value=self.parse_font_size(get_display_fonts(self.config)[0]))
        self.font_primary_size_entry = tk.Entry(self, textvariable=self.font_primary_size)
        self.font_primary_size_entry.grid(row=2, column=1, columnspan=2, sticky=tk.EW)

        tk.Label(self, text="次字体:").grid(row=3, column=0, sticky=tk.W)
        self.font_secondary_family = tk.StringVar(value=self.parse_font_family(get_display_fonts(self.config)[1]))
        self.font_secondary_family_entry = tk.Entry(self, textvariable=self.font_secondary_family)
        self.font_secondary_family_entry.grid(row=3, column=1, sticky=tk.EW)
        self.font_secondary_browse = tk.Button(self, text="浏览", command=self.browse_secondary_font)
        self.font_secondary_browse.grid(row=3, column=2, sticky=tk.EW)

        tk.Label(self, text="次字体大小:").grid(row=4, column=0, sticky=tk.W)
        self.font_secondary_size = tk.StringVar(value=self.parse_font_size(get_display_fonts(self.config)[1]))
        self.font_secondary_size_entry = tk.Entry(self, textvariable=self.font_secondary_size)
        self.font_secondary_size_entry.grid(row=4, column=1, columnspan=2, sticky=tk.EW)

        tk.Label(self, text="背景颜色:").grid(row=5, column=0, sticky=tk.W)
        self.bg_color_button = tk.Button(self, text="选择颜色", command=self.choose_bg_color)
        self.bg_color_button.grid(row=5, column=1, columnspan=2, sticky=tk.EW)

        tk.Label(self, text="文字颜色:").grid(row=6, column=0, sticky=tk.W)
        self.fg_color_button = tk.Button(self, text="选择颜色", command=self.choose_fg_color)
        self.fg_color_button.grid(row=6, column=1, columnspan=2, sticky=tk.EW)

        tk.Label(self, text="透明度:").grid(row=7, column=0, sticky=tk.W)
        self.opacity_scale = tk.Scale(self, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.opacity_scale.grid(row=7, column=1, columnspan=2, sticky=tk.EW)
        self.opacity_scale.set(self.config.getfloat('colors', 'opacity', fallback=1.0))

        tk.Label(self, text="显示模式:").grid(row=8, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value=get_display_mode(self.config))
        self.mode_options = {"单行显示": "single_line", "双行显示": "double_line", "双行混合字体显示": "double_line_mixed_font"}
        self.mode_menu = tk.OptionMenu(self, self.mode_var, *self.mode_options.keys())
        self.mode_menu.grid(row=8, column=1, columnspan=2, sticky=tk.EW)

        tk.Button(self, text="保存", command=self.save_settings).grid(row=9, column=0, columnspan=3, sticky=tk.EW)

        self.grid_columnconfigure(1, weight=1)

    def parse_font_family(self, font_str):
        return " ".join(font_str.split()[:-1])

    def parse_font_size(self, font_str):
        return font_str.split()[-1]

    def browse_primary_font(self):
        font_path = filedialog.askopenfilename(filetypes=[("TrueType Font", "*.ttf"), ("OpenType Font", "*.otf")])
        if font_path:
            self.font_primary_family.set(font_path)

    def browse_secondary_font(self):
        font_path = filedialog.askopenfilename(filetypes=[("TrueType Font", "*.ttf"), ("OpenType Font", "*.otf")])
        if font_path:
            self.font_secondary_family.set(font_path)

    def load_font(self, font_path, font_size):
        font_name = os.path.basename(font_path)
        font_font = font.Font(family=font_name, size=font_size)
        font.nametofont(font_name).configure(size=font_size)
        return font_name

    def choose_bg_color(self):
        color_code = colorchooser.askcolor(title="选择背景颜色")[1]
        if color_code:
            self.bg_color_button.config(bg=color_code)

    def choose_fg_color(self):
        color_code = colorchooser.askcolor(title="选择文字颜色")[1]
        if color_code:
            self.fg_color_button.config(fg=color_code)

    def save_settings(self):
        primary_font_path = self.font_primary_family.get()
        primary_font_size = int(self.font_primary_size.get())
        secondary_font_path = self.font_secondary_family.get()
        secondary_font_size = int(self.font_secondary_size.get())

        if primary_font_path:
            primary_font = self.load_font(primary_font_path, primary_font_size)
        else:
            primary_font = f"{font.families()[0]} {primary_font_size}"  # 默认字体

        if secondary_font_path:
            secondary_font = self.load_font(secondary_font_path, secondary_font_size)
        else:
            secondary_font = f"{font.families()[0]} {secondary_font_size}"  # 默认字体

        set_folder_path(self.config, self.folder_path_entry.get())
        set_display_fonts(self.config, primary_font, secondary_font)
        self.config.set('colors', 'background', self.bg_color_button.cget('bg'))
        self.config.set('colors', 'foreground', self.fg_color_button.cget('fg'))
        self.config.set('colors', 'opacity', str(self.opacity_scale.get()))
        set_display_mode(self.config, self.mode_options.get(self.mode_var.get(), 'single_line'))
        save_config(self.config)
        self.parent.apply_settings(self.config)
        self.destroy()