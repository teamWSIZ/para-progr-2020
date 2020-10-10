w = [2, 5, 8, 1, 88]

# print(len(w))   # liczba elementów w liście
# print(w[0])     # pierwszy element
# print(w[-1])    # pierwszy od końca element
# print(w[1:-1])  # elementy poza pierwszym i ostatnim...
#
# w[0] = 77       # przypisanie (nadpisanie) wartości na początku listy
# w.append(100)   # dodanie wartości 100 na koniec listy
# # w[1000] = 8     # wyrzuci bład `IndexError: list assignment index out of range`


for ii in w:
    print(f'liczba: {ii}, kwadrat: {ii * ii}')

z = [1, 2, 3, 4, 5, 6]
for i in z[::2]:
    print(i)

uns = []
for i in range(1,101):
    uns.append(f'user{i}')
print(uns)