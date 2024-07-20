import os

import os

def load_files_from_folder(folder_path):
    """
    加载指定文件夹中的所有文本文件内容，以列表的形式返回。
    每个元素是一个元组，第一个元素是文件名，第二个元素是文件内容（按行分割的列表）。
    """
    files_content = []
    if folder_path and os.path.isdir(folder_path):
        print(f"正在读取文件夹: {folder_path}")
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                print(f"正在读取文件: {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.readlines()
                    files_content.append((filename, content))
                except (UnicodeDecodeError, IOError) as e:
                    print(f"读取文件 {file_path} 时出错: {e}")
    else:
        print(f"错误：文件夹 {folder_path} 不存在或不是一个有效的目录")
    return files_content