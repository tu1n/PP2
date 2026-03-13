f = open("sample.txt", "w")
f.write("Hello\n")
f.write("My name is Ali\n")
f.write("I love Python\n")
f.close()

f = open("sample.txt", "a")
f.write("This line is appended\n")
f.close()

f = open("sample.txt", "r")
print(f.read())
f.close()
