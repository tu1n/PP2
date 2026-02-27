import json
a = input("Имя: ")
b = int(input("Возраст: "))
c = input("Навыки : ").split()
person = {
    "name": a,
    "age": b,
    "skills": c
}

print(json.dumps(person,ensure_ascii=False))
