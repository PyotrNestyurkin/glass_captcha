print(ord('А'), ord('Я'))
alphabet = [chr(i) for i in range(ord('А'), ord('Я') + 1)]
alphabet.append('Ё')
alphabet.remove('О')
alphabet.remove('Ъ')
alphabet.remove('Ы')
alphabet.remove('Ь')
print(len(alphabet))
print(alphabet)
