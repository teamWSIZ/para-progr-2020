def dodaj(a, b):
    return a + b


print(dodaj(5, 6))


def generate_username(number, prefix='user'):
    return f'{prefix}{number}'


print(generate_username(14, 'benutzer'))
print(generate_username(14))
