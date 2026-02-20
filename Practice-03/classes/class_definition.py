class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print("Hello", self.name)


p = Person("Miko", 18)
p.greet()
