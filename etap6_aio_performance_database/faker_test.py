from faker import Faker

f = Faker(['pl_PL', 'de_DE'])
for i in range(100):
    print(f'{f.name()}, {f.address()}')