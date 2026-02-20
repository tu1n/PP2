class Animal:
    def speak(self):
        print("Animal sound")


class Dog(Animal):
    def speak(self):
        print("Bark")


a = Animal()
a.speak()

d = Dog()
d.speak()
