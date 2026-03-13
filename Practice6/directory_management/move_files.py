import shutil
import os

os.makedirs("folder1", exist_ok=True)
os.makedirs("folder2", exist_ok=True)

f = open("folder1/test.txt", "w")
f.write("hello")
f.close()

shutil.copy("folder1/test.txt", "folder2/test.txt")
print("File copied")

shutil.move("folder1/test.txt", "folder2/moved.txt")
print("File moved")
