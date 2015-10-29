import sys

import requests  # http://docs.python-requests.org/en/latest/user/quickstart/

try:
    wikipediaName = input('What Wikipedia page should we browse?\n')

    # STEP 1 - search for links in the article text
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

    # for each <a></a> in the text, save it's content to a dictionary(?)

    # STEP 2 - search each dictionary(?) entry in geonames

    """geonamesName = input("What place do you want to search in Geonames?\n")
    payload = {'q': geonamesName, 'maxRows': '10', 'username': 'ivozor'}
    r2 = requests.get("http://api.geonames.org/search", params=payload)
    print(r2.text)"""

    #   for each entry, depending on the result array length:
    #       if there is none, the links doesn't refer to a place;
    #       if there is one, store in the final dictionary (names and coordinates?);
    #       if there are several, for each one:
    #           using the data of the item from geonames:
    #               search for it in the "infobox geography" div of the article the link refers to:
    #                   if it matches, store in the final dictionary and break;
    #                   if there is no match, discard;

    # STEP 3 - print dictionary items

except requests.exceptions.RequestException as ex:
    print("REQUESTS ERROR: " + str(ex))
    sys.exit(1)
except Exception as ex:
    print("ERROR: " + str(ex))
    sys.exit(1)
