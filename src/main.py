# Abrindo o arquivo

file = open('assets/municipios.txt', 'r', encoding='utf8')

for line in file:
    print(line.lower())

file.close()