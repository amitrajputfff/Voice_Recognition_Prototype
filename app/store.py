import shutil
import os

def move_file(src, dst):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source file '{src}' does not exist.")
    shutil.move(src, dst)
    print(f"Moved '{src}' to '{dst}'")

def store_recorded_audio(file_name):
    src_path = file_name
    dst_path = f"stored/{file_name}"
    try:
        move_file(src_path, dst_path)
    except Exception as e:
        print(f"Error during file storage: {e}")
