import sys

import requests  # http://docs.python-requests.org/en/latest/user/quickstart/

try:
    wikipediaName = input('What Wikipedia page should we browse?\n')

    # STEP 1 - procurar links no texto do artigo
    r = requests.get("https://en.wikipedia.org/wiki/" + wikipediaName)

    if r.status_code == requests.codes.ok:
        print("=== SOURCE OF PAGE ===")
        print(r.text)
        print("======================")
    else:
        if r.status_code == 404:
            print("Could not find a Wikipedia page for '" + wikipediaName + "'.")
        else:
            print("There was an error (" + str(r.status_code) + ") fetching Wikipedia page for '" + wikipediaName + "'.")

    #   percorrer o texto do artigo e para cada <a></a> guardar o texto e o href num dicionario(?)

    # STEP 2 - procurar cada entrada do dicionario no geonames

    """geonamesName = input("What place do you want to search in Geonames?\n")
    payload = {'q': geonamesName, 'maxRows': '10', 'username': 'ivozor'}
    r2 = requests.get("http://api.geonames.org/search", params=payload)
    print(r2.text)"""

    #   para cada entrada, dependendo do numero de resultados:
    #       se nao tiver nenhum então abandonar, não será um local;
    #       se tiver só um guardar no dicionario de coisas a imprimir (nome e coordenadas);
    #       se tiver mais que uma entrada, para cada uma das entradas:
    #           ir buscar o conteudo da infobox geography e fazer match:
    #               se fizer match, guardar no dicionario de coisas a imprimir e fazer break;
    #               se nao fizer match, abandonar, não será nenhum dos locais

    # STEP 3 - imprimir o dicionario de nomes e coordenadas

except requests.exceptions.RequestException as ex:
    print("REQUESTS ERROR: " + str(ex))
    sys.exit(1)
except Exception as ex:
    print("ERROR: " + str(ex))
    sys.exit(1)
