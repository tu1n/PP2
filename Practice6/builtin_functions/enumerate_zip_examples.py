fruits = ["apple", "banana", "cherry"]
prices = [1.50, 0.75, 2.00]

for i, fruit in enumerate(fruits):
    print(i, fruit)

for fruit, price in zip(fruits, prices):
    print(fruit, price)

x = 10
print(type(x))
print(isinstance(x, int))

print(int("5"))
print(float("3.14"))
print(str(100))
