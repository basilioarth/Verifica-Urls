from unicodedata import normalize

def remove_accents(string):
    return normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')

file = open('assets/municipios.txt', 'r', encoding='utf8')

for line in file:
    print(remove_accents(line.lower()).replace(" ", ""))

file.close()