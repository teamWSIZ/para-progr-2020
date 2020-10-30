w = 12
print(w, type(w))
w = 'abc'
print(w, type(w))
print('-----------')

z: int
z = 'abcd'  # przypisanie złego typu -- conajmniej ostrzeżenie w IDE
print(z)

print('---------------')


def generate_username(number: int, prefix: str = 'user') -> str:
    return f'{prefix}{number}'


print(generate_username(5, 'użytkownik'))
