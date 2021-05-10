from unicodedata import normalize

'''
Devolve cópia de uma str substituindo os caracteres
acentuados pelos seus equivalentes não acentuados.

ATENÇÃO: carateres gráficos não ASCII e não alfa-numéricos,
tais como bullets, travessões, aspas assimétricas, etc.
são simplesmente removidos!

>>> remover_acentos('[ACENTUAÇÃO] ç: áàãâä! éèêë? íìîï, óòõôö; úùûü.')
'[ACENTUACAO] c: aaaaa! eeee? iiii, ooooo; uuuu.'
'''
def remove_accents(string):
    return normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')

def transformMunicipios(municipio):
    return remove_accents(municipio.lower()).replace(" ", "").replace("\n", "")

def getMunicipios(municipiosList):
    file = open('assets/municipios.txt', 'r', encoding='utf8')

    for municipio in file:
        municipiosList.append(transformMunicipios(municipio))

    file.close()

def createUrlGov(municipio):
    return municipio + '.pi.gov.br'

def createUrlLeg(municipio):
    return municipio + '.pi.leg.br'

if __name__ == '__main__':
    municipios = []
    urlsGov = []
    urlsLeg = []
    count = 0

    getMunicipios(municipios)

    for municipio in municipios:
        print(municipio)

        urlsGov.append(createUrlGov(municipio))
        urlsLeg.append(createUrlLeg(municipio))

        print(urlsGov[count])
        print(urlsLeg[count])
        print('\n')
        count = count + 1
    
    print("Total de municípios: {}".format(len(municipios)))
    