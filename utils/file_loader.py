from utils.file_utils import load_files_from_folder

def load_files(folder_path):
    files_content = load_files_from_folder(folder_path)
    if not files_content:
        print(f"文件夹 {folder_path} 为空或不存在")
    else:
        print(f"成功读取 {len(files_content)} 个文件")
    return files_content