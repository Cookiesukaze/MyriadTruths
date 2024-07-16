import tkinter as tk

def display_content(text_area, content, mode, config, current_line_index, font_primary, font_secondary):
    if text_area.winfo_exists():
        text_area.delete(1.0, tk.END)
        if mode == 'single_line':
            lines_per_display = config.getint('display', 'lines_per_display', fallback=1)
            for line in content[current_line_index:current_line_index+lines_per_display]:
                text_area.insert(tk.END, line + '\n', 'primary')
        elif mode == 'double_line':
            if current_line_index < len(content):
                text_area.insert(tk.END, content[current_line_index] + '\n', 'primary')
            if current_line_index + 1 < len(content):
                text_area.insert(tk.END, content[current_line_index + 1] + '\n', 'primary')
        elif mode == 'double_line_mixed_font':
            if current_line_index < len(content):
                parts = content[current_line_index].split('\t')
                if len(parts) >= 2:
                    text_area.insert(tk.END, parts[0] + '\n', 'primary')
                    text_area.insert(tk.END, parts[1] + '\n', 'secondary')

def switch_content(app):
    if app.text_area.winfo_exists():
        if not app.is_paused:
            if app.display_mode == 'single_line':
                lines_per_display = app.config.getint('display', 'lines_per_display', fallback=1)
                app.current_line_index += lines_per_display
                if app.current_line_index >= len(app.files_content[app.current_file_index][1]):
                    app.current_line_index = 0
                    app.current_file_index = (app.current_file_index + 1) % len(app.files_content)
            elif app.display_mode == 'double_line':
                app.current_line_index += 2
                if app.current_line_index >= len(app.files_content[app.current_file_index][1]):
                    app.current_line_index = 0
                    app.current_file_index = (app.current_file_index + 1) % len(app.files_content)
            elif app.display_mode == 'double_line_mixed_font':
                app.current_line_index += 1
                if app.current_line_index >= len(app.files_content[app.current_file_index][1]):
                    app.current_line_index = 0
                    app.current_file_index = (app.current_file_index + 1) % len(app.files_content)
            app.display_current_content()
        app.after(app.auto_switch_interval * 1000, app.switch_content)