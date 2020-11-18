class Car:
    name: str
    brand: str

    def __init__(self, name, brand):
        self.name = name
        self.brand = brand


c = Car('the first ferrari', 'ferrari')

di = c.__dict__
d = Car(**di)
d.name = 'the second ferrari'
print(d.__dict__)
