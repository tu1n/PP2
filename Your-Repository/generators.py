def a(n):
    for i in range(1, n + 1):
        yield i
for b in a(int(input())):
    print(b)
