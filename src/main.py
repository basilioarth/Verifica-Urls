import requests
from requests.exceptions import HTTPError
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
        return 'http://' + municipio_url_prefix + '.pi.gov.br'
    else: 
        return 'http://' + municipio_url_prefix + '.pi.leg.br'

def request(url):
    status = "Fail"
    request_response_message = ""

    try: 
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        request_response_message = f'HTTP error occurred: {http_err}'
        print(request_response_message)   
    except Exception as err:
        request_response_message = f'Other error occurred: {err}'
        print(request_response_message)  
    else:
        request_response_message = response
        status = "Success"
    
    return [url, status, request_response_message]
    
def testConnection(municipio):
    gov_type = 0
    leg_type = 1

    gov_result = request(createUrl(municipio, gov_type))
    leg_result = request(createUrl(municipio, leg_type))

    return [gov_result, leg_result]

def handleResult(finalResponse, file):
    file.write("\n" + finalResponse[0][0])
    print("url: {}".format(finalResponse[0][0]))

    file.write("\n" + finalResponse[0][1])
    print("status: {}".format(finalResponse[0][1]))

    file.write("\n" + str(finalResponse[0][2]))
    print("response request message: {}".format(finalResponse[0][2]))

    file.write("\n" + finalResponse[1][0])
    print("url: {}".format(finalResponse[1][0]))

    file.write("\n" + finalResponse[1][1])
    print("status: {}".format(finalResponse[1][1]))

    file.write("\n" + str(finalResponse[1][2]))
    print("response request message: {}".format(finalResponse[1][2]))

if __name__ == '__main__':
    municipios = []
    resultados = open("assets/results.txt", "a")

    getMunicipios(municipios)
    
    for municipio in municipios:
        print('\n')

        print("Município: {}".format(municipio))
        resultados.write("\n\n" + municipio)
        handleResult(testConnection(municipio), resultados)

    resultados.close()
    print("Total de municípios: {}".format(len(municipios)))
'''
Devolve cópia de uma str substituindo os caracteres
acentuados pelos seus equivalentes não acentuados.

ATENÇÃO: carateres gráficos não ASCII e não alfa-numéricos,
tais como bullets, travessões, aspas assimétricas, etc.
são simplesmente removidos!

>>> remover_acentos('[ACENTUAÇÃO] ç: áàãâä! éèêë? íìîï, óòõôö; úùûü.')
'[ACENTUACAO] c: aaaaa! eeee? iiii, ooooo; uuuu.'
''' 