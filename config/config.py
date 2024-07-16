import configparser
import os

CONFIG_FILE = 'data/config.ini'

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding='utf-8')
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def get_folder_path(config):
    folder_path = config.get('files', 'folder_path', fallback=None)
    if folder_path is not None:
        folder_path = folder_path.encode('utf-8').decode('utf-8')
    return folder_path

def set_folder_path(config, folder_path):
    config.set('files', 'folder_path', folder_path)
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

def get_auto_switch_interval(config):
    interval = config.getint('behavior', 'auto_switch_interval', fallback=5)
    return interval

def get_pause_on_click(config):
    pause_on_click = config.getboolean('behavior', 'pause_on_click', fallback=True)
    return pause_on_click