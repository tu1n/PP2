import random
try:
    a1=int(input("қай саннан бастап: "))
    a2=int(input("қай санға дейін: "))
    if a1>a2:
        print("Бірінші сан екінші саннан үлкен болмауы керек!")
    else:
        san = random.randint(a1, a2)
        print(f"Кездейсоқ сан: {san}")
except ValueError:
    print("Тек бүтін сандарды енгізіңіз!")
