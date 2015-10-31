# GROUP 6
# 59126 - Ivan Freire
# 63536 - Ivo Martins
# 83063 - Felix Brade

# PYTHON 3.5.0

import sys

import requests

from bs4 import BeautifulSoup

try:
    articleLinksDictionary = {}
    locationsFinal = {}
    wikipediaName = input('What Wiki page should we browse for locations?\n')
    # wikipediaName = "Paris"
    r = requests.get("https://en.wikipedia.org/wiki/" + wikipediaName)

    if r.status_code == requests.codes.ok:
        wikipediaPageHtml = r.text
    else:
        if r.status_code == 404:
            print("Could not find a Wikipedia page for '" + wikipediaName + "'.")
        else:
            print(
                "There was an error (" + str(r.status_code) + ") fetching Wikipedia page for '" + wikipediaName + "'.")

    wikipediaPageSoup = BeautifulSoup(wikipediaPageHtml, 'html.parser')
    # STEP 1 - search for links in the article text
    contentText = wikipediaPageSoup.find(id="mw-content-text")
    for paragraph in contentText.find_all('p'):
        for link in paragraph.find_all('a'):
            if "wiki" in link.get("href"):
                # for each <a></a> in the text, save it's content to a dictionary(?)
                articleLinksDictionary[link.text] = link.get("href")


    # STEP 2 - search each dictionary(?) entry in geonames
    for keys, values in articleLinksDictionary.items():
        # see if its a geography page, else continue cycle
        r = requests.get("https://en.wikipedia.org" + values)

        if r.status_code == requests.codes.ok:
            wikipediaPageHtml = r.text
        else:
            if r.status_code == 404:
                print("Could not open link to Wikipedia page at '" + wikipediaName + "'.")
            else:
                print(
                    "There was an error (" + str(
                        r.status_code) + ") opening link to Wikipedia page at '" + wikipediaName + "'.")

        query = keys
        wikipediaPageSoup = BeautifulSoup(wikipediaPageHtml, 'html.parser')
        geoDefault = wikipediaPageSoup.find_all("span", class_="geo-default")
        if (geoDefault is None) or (len(geoDefault) == 0):
            print("### Not a place:\t" + keys)
            continue
        else:
            print("### Maybe a place:\t" + keys)
            infobox = wikipediaPageSoup.find_all("table", class_="infobox", limit=1)
            if len(infobox) > 0:
                for tr in infobox[0].find_all('tr'):
                    if (tr is None) or (len(tr) == 0):
                        continue
                    th = tr.find("th")
                    if (th is None) or (len(th) == 0):
                        continue
                    else:
                        thT = th.text
                        if "Country" in thT or "Province" in thT or "State" in thT or "Sovereign state" in thT:
                            td = tr.find('td')
                            if (td is None) or (len(td) == 0):
                                continue
                            trA = td.find('a')
                            if (trA is None) or (len(trA) == 0):
                                td = tr.find("td")
                                query += " " + td.text
                            elif "wiki" in str(trA):
                                query += " " + trA.text

        # search geonames
        geonamesName = keys
        payload = {'q': query,
                   'maxRows': '1',
                   'username': 'ivozor',
                   'style': 'medium',
                   'orderby': 'relevance',
                   'isNameRequired': 'true'
                   }
        geonamesResponse = requests.get("http://api.geonames.org/search", params=payload)
        geonamesResponseSoup = BeautifulSoup(geonamesResponse.text, 'xml')
        # number of results from geonames
        count = int(geonamesResponseSoup.find("totalResultsCount").text)
        if count == 0:
            # if there is none, the links doesn't refer to a place;
            continue
        elif count == 1:
            # if there is one, store in the final dictionary (names and coordinates?);
            lat = geonamesResponseSoup.find("lat").text
            lng = geonamesResponseSoup.find("lng").text
            locationsFinal[geonamesResponseSoup.find("name").text] = "(lat:" + lat + ", lng:" + lng + ")"
        elif count > 1:
            # use first result, as they are ordered by relevance
            lat = geonamesResponseSoup.find("geoname").find("lat").text
            lng = geonamesResponseSoup.find("geoname").find("lng").text
            locationsFinal[geonamesResponseSoup.find("name").text] = "(lat:" + lat + ", lng:" + lng + ")"


    # STEP 3 - print dictionary items
    print("\n### RESULTS ####################################")
    for keys, values in locationsFinal.items():
        print(keys + " " + values)
    print("################################################\n")


except requests.exceptions.RequestException as ex:
    print("REQUESTS ERROR: " + str(ex))
    sys.exit(1)
except Exception as ex:
    print("ERROR: " + str(ex))
    sys.exit(1)
