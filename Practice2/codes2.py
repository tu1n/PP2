a = int(input("Первое число: "))
b = int(input("Второе число: "))
op = input("Операция (+ или -): ")

if op == "+":
    print(a + b)
elif op == "-":
    print(a - b)
else:
    print("Неизвестная операция")
