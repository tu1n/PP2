class Car:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def info(self):
        print(self.brand, self.year)


c = Car("Toyota", 2020)
c.info()

