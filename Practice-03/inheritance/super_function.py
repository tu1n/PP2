class Animal:
    def __init__(self, name):
        self.name = name

    def info(self):
        print("Animal:", self.name)


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def info(self):
        super().info()
        print("Breed:", self.breed)


d = Dog("Buddy", "Labrador")
d.info()
