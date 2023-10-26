import os

folder_path = 'src/FDH/viz'

if os.path.exists(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"failed to delete {file_path}: {e}")

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            try:
                os.rmdir(dir_path)
            except Exception as e:
                print(f"failed to remove {dir_path}: {e}")
else:
    print(f"folder '{folder_path}' does not exist.")
