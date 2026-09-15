letters = [
['A', 'C', 'D'],
['W', 'A', 'O'],
['T', 'S', 'A']
]


print(letters)
for list in letters:
    for i in range(3):
        if list[i] == "A":
            list[i] = "B"

print(letters)
