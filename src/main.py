import requests
from requests.exceptions import HTTPError
from unicodedata import normalize
import pandas as pd
import time
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

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
    status = "Success"
    request_response_message = ""

    adapter = HTTPAdapter(max_retries=5)
    session = requests.Session()
    session.mount(url, adapter)

    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    } # To avoid "TooManyRedirects: Exceeded 30 redirects"

    try:
        response = session.get(url, headers = headers, verify = False) # "verify = false" to avoid SSL certificate errors 
        request_response_message = response.status_code
        if(int(request_response_message) >= 400): status = "Fail"
    except ConnectionError as ce:
        status = "Fail"
        request_response_message = ce
    return [url, status, request_response_message]
    
def testConnection(municipio):
    gov_type = 0
    leg_type = 1

    gov_result = request(createUrl(municipio, gov_type))
    leg_result = request(createUrl(municipio, leg_type))

    return [gov_result, leg_result]

def handleResult(response, municipio, persistFormat, Municipio, UrlGov, StatusGov, RequestResponseGov, UrlLeg, StatusLeg, RequestResponseLeg):

    if (persistFormat == "txt") | (persistFormat == "all"):
        resultsTxt = open("assets/results.txt", "a")
        print("\nMunicípio: {}".format(municipio))
        resultsTxt.write("\n\n" + municipio)

        resultsTxt.write("\n" + response[0][0])
        print("url: {}".format(response[0][0]))

        resultsTxt.write("\n" + response[0][1])
        print("status: {}".format(response[0][1]))

        resultsTxt.write("\n" + str(response[0][2]))
        print("response request message: {}".format(response[0][2]))

        resultsTxt.write("\n" + response[1][0])
        print("url: {}".format(response[1][0]))

        resultsTxt.write("\n" + response[1][1])
        print("status: {}".format(response[1][1]))

        resultsTxt.write("\n" + str(response[1][2]))
        print("response request message: {}".format(response[1][2]))

    if (persistFormat == "xlsx") | (persistFormat == "all"):

        Municipio.append(municipio)

        UrlGov.append(response[0][0])
        StatusGov.append(response[0][1])
        RequestResponseGov.append(str(response[0][2]))

        UrlLeg.append(response[1][0])
        StatusLeg.append(response[1][1])
        RequestResponseLeg.append(str(response[1][2]))

if __name__ == '__main__':

    municipios = []
    Municipio = []
    UrlGov = []
    StatusGov = []
    RequestResponseGov = []
    UrlLeg = []
    StatusLeg = []
    RequestResponseLeg = []

    getMunicipios(municipios)
    
    for municipio in municipios:
        handleResult(testConnection(municipio), municipio, 'all', 
                    Municipio, 
                    UrlGov, StatusGov, RequestResponseGov, 
                    UrlLeg, StatusLeg, RequestResponseLeg
        )

    planilha = pd.DataFrame({
        'Município': Municipio,
        'UrlGov': UrlGov,
        'StatusGov': StatusGov,
        'RequestResponseGov': RequestResponseGov,
        'UrlLeg': UrlLeg,
        'StatusLeg': StatusLeg,
        'RequestResponseLeg': RequestResponseLeg
    })

    planilha.to_excel('assets/MunicipiosUrls.xlsx')