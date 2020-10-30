from etap2.klasy_user import User


class TeslaUser(User):
    division: str

    def __init__(self, name, age, division):
        super().__init__(name, age)
        self.division = division


tu = TeslaUser(division='design', name='Elon Deng', age=69420)

print(tu.verify_id('Elon Deng69420')) # True
