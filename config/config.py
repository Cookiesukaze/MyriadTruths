import configparser
import os

CONFIG_FILE = 'data/config.ini'


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')

    # 检查和添加缺失的部分
    if 'window' not in config:
        config.add_section('window')
        config.set('window', 'geometry', '600x400+100+100')
        config.set('window', 'always_on_top', 'False')

    if 'display' not in config:
        config.add_section('display')
        config.set('display', 'font_primary', 'Arial 16')
        config.set('display', 'font_secondary', 'Arial 12')

    if 'behavior' not in config:
        config.add_section('behavior')
        config.set('behavior', 'auto_switch_interval', '5')
        config.set('behavior', 'switch_mode', 'sequential')
    else:
        # 如果 'behavior' 部分存在，但缺少 'switch_mode' 设置
        if 'switch_mode' not in config['behavior']:
            config.set('behavior', 'switch_mode', 'sequential')

    if 'files' not in config:
        config.add_section('files')
        config.set('files', 'folder_path', os.path.abspath('.'))

    if 'progress' not in config:
        config.add_section('progress')
        config.set('progress', 'current_file_index', '0')
        config.set('progress', 'current_line_index', '0')

    return config


def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def get_folder_path(config):
    folder_path = config.get('files', 'folder_path', fallback=None)
    if folder_path is not None:
        folder_path = os.path.abspath(folder_path.encode('utf-8').decode('utf-8'))
    return folder_path


def set_folder_path(config, folder_path):
    config.set('files', 'folder_path', os.path.abspath(folder_path))
    save_config(config)


def get_display_fonts(config):
    font_primary = config.get('display', 'font_primary', fallback='Arial 16')
    font_secondary = config.get('display', 'font_secondary', fallback='Arial 12')
    return font_primary, font_secondary


def set_display_fonts(config, font_primary, font_secondary):
    config.set('display', 'font_primary', font_primary)
    config.set('display', 'font_secondary', font_secondary)
    save_config(config)


def get_display_mode(config):
    mode = config.get('display', 'mode', fallback='single_line')
    return mode


def set_display_mode(config, mode):
    config.set('display', 'mode', mode)
    save_config(config)


def get_auto_switch_interval(config):
    interval = config.getint('behavior', 'auto_switch_interval', fallback=5)
    return interval


def set_auto_switch_interval(config, interval):
    config.set('behavior', 'auto_switch_interval', str(interval))
    save_config(config)


def get_pause_on_click(config):
    pause_on_click = config.getboolean('behavior', 'pause_on_click', fallback=True)
    return pause_on_click


def get_window_geometry(config):
    return config.get('window', 'geometry', fallback='600x400+100+100')


def set_window_geometry(config, geometry):
    config.set('window', 'geometry', geometry)
    save_config(config)


def get_always_on_top(config):
    return config.getboolean('window', 'always_on_top', fallback=False)


def set_always_on_top(config, always_on_top):
    config.set('window', 'always_on_top', str(always_on_top))
    save_config(config)


def get_switch_mode(config):
    return config.get('behavior', 'switch_mode', fallback='sequential')


def set_switch_mode(config, switch_mode):
    config.set('behavior', 'switch_mode', switch_mode)
    save_config(config)


def get_current_file_index(config):
    return config.getint('progress', 'current_file_index', fallback=0)


def set_current_file_index(config, index):
    config.set('progress', 'current_file_index', str(index))
    save_config(config)


def get_current_line_index(config):
    return config.getint('progress', 'current_line_index', fallback=0)


def set_current_line_index(config, index):
    config.set('progress', 'current_line_index', str(index))
    save_config(config)