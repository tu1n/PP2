import shutil
import os

shutil.copy("sample.txt", "backup.txt")
print("File copied")

os.remove("backup.txt")
print("File deleted")
