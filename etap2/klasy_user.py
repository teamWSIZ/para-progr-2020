class User:
    name: str
    age: int
    __id: str

    def change_name(self, new_name: str):
        self.name = new_name

    def __init__(self, name='anonymous', age=0):
        self.name = name
        self.age = age
        self.__id = name + str(age)

    def verify_id(self, expected_id):
        return self.__id == expected_id


if __name__ == '__main__':
    u = User()
    u.name = 'Wu Xiaoli'

    print(u.name)

    w = User()
    w.name = 'Xi Rambon'
    print(w.name)  # Xi Rambon
    w.change_name('Abra Kadabra')
    print(w.name)  # Abra Kadabra

    # -------------
    u2 = User(age=4)
    print(u2.age)
    print(u2.name)
    print(u2.verify_id('anonymous4'))  # True
    print(User('Abbu', 99).verify_id('Abbu99'))  # True
    print(User('X', 1).verify_id('1'))  # False

    # print(u2.__verify_id())
    # print(u2.__id)
