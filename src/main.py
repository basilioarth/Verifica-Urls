import requests
from unicodedata import normalize

def remove_accents(string):
    return normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')

def adjustMunicipioName(municipio):
    return remove_accents(municipio.lower()).replace(" ", "")

def getMunicipios(municipiosList):
    file = open('assets/municipios.txt', 'r', encoding='utf8')

    for municipio in file:
        municipiosList.append(municipio.replace("\n", ""))

    file.close()

def createUrl(municipio, type_url):
    municipio_url_prefix = adjustMunicipioName(municipio)
    
    if type_url == 0:
        return municipio_url_prefix + '.pi.gov.br'
    else: 
        return municipio_url_prefix + '.pi.leg.br'

def testConnection(municipio):
    gov = 0
    leg = 1

    urlGov = createUrl(municipio, gov)
    urlLeg = createUrl(municipio, leg)

    return [urlGov, urlLeg]
    

if __name__ == '__main__':
    municipios = []
    urls = []
    count = 0

    getMunicipios(municipios)
    print(municipios)
    
    for municipio in municipios:
        urls.append(testConnection(municipio))

        '''
        urlsGov.append(createUrlGov(municipio))
        urlsLeg.append(createUrlLeg(municipio))

        print(urlsGov[count])
        print(urlsLeg[count])
        print('\n')
        count = count + 1
    '''
    print("Total de municípios: {}".format(len(municipios)))
    print(urls)
'''
Devolve cópia de uma str substituindo os caracteres
acentuados pelos seus equivalentes não acentuados.

ATENÇÃO: carateres gráficos não ASCII e não alfa-numéricos,
tais como bullets, travessões, aspas assimétricas, etc.
são simplesmente removidos!

>>> remover_acentos('[ACENTUAÇÃO] ç: áàãâä! éèêë? íìîï, óòõôö; úùûü.')
'[ACENTUACAO] c: aaaaa! eeee? iiii, ooooo; uuuu.'
''' 