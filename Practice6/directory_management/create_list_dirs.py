import os

os.makedirs("myfolder/subfolder", exist_ok=True)
print("Directories created")

for item in os.listdir("myfolder"):
    print(item)

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            print(file)
