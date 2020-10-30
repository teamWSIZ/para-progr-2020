from random import randint

s = {}
s['abc'] = 11
s['norbert'] = 10
s['czesław'] = 4
print(s)  # {'abc': 11, 'norbert': 10, 'czesław': 4}

print(s['czesław'])  # dostęp do elementów
print(len(s))  # liczba elementów w słowniku

s.__delitem__('norbert')
print(len(s))

print(randint(1, 10000))

for i in range(200):
    print(randint(1000, 10000))
