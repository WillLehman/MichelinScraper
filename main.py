import requests
from bs4 import BeautifulSoup
import pandas as pd
import h3
from keplergl import KeplerGl

namesList = []
addressList = []
citiesList = []
zipList = []
stateList = []
h3List = []
latList = []
longList = []

num = 1
while num <= 76:
    if num == 1:
        website = 'https://guide.michelin.com/en/us/restaurants'
    else:
        website = 'https://guide.michelin.com/en/us/restaurants/page/' + (str)(num)

    result = requests.get(website)
    content = result.text

    soup = BeautifulSoup(content, 'lxml')
    #print(soup.prettify())

    resturaunts = soup.find('div', class_='row restaurant__list-row js-toggle-result js-geolocation js-restaurant__list_items').find_all('div', class_='col-md-6 col-lg-6 col-xl-3')

    for resturaunt in resturaunts:

        name = resturaunt.find('div', class_='card__menu-content js-match-height-content').h3.text
        namesList.append(name.strip())
        addressLink = 'https://guide.michelin.com/' + resturaunt.find('div', class_='card__menu-content js-match-height-content').h3.a.get('href')

        addressResult = requests.get(addressLink)
        addressContent = addressResult.text
        addressSoup = BeautifulSoup(addressContent, 'lxml')
        #print(addressLink)
        #print(addressSoup.prettify())
        #address = addressSoup.find('div', class_ = 'restaurant-details__heading d-lg-none').li.text

        coords = addressSoup.find('script', type = 'application/ld+json').text
        #print(coords)

        latitude = (float)(coords[coords.find('latitude') + 10: coords.find('longitude') - 2])
        latList.append(latitude)
        longitude = (float)(coords[coords.find('longitude') + 11: coords.find('hasMap') - 2])
        longList.append(longitude)

        hexagon = h3.geo_to_h3(latitude, longitude, 15)
        h3List.append(hexagon)

        streetAddress = coords[coords.find('streetAddress') + 16: coords.find('addressLocality') - 3]
        addressList.append(streetAddress.strip())

        addressLocality = coords[coords.find('addressLocality') + 18: coords.find('postalCode') - 3]
        citiesList.append(addressLocality.strip())

        postalCode = coords[coords.find('postalCode') + 13: coords.find('addressCountry') - 3]
        zipList.append(postalCode.strip())

        addressRegion = coords[coords.find('addressRegion') + 16: coords.find('name') - 4]
        stateList.append(addressRegion.strip())


        coordPair = (latitude, longitude)
        tags = {'amenity': True}



        #break

    print(num)
    num += 1

    break

raw_data = {'Name': namesList, 'Address': addressList, 'City': citiesList, 'State': stateList, 'Zipcode': zipList, 'H3 Index': h3List, 'Latitude': latList, 'Longitude': longList}
df = pd.DataFrame(raw_data, columns = ['Name', 'Address', 'City', 'State', 'Zipcode', 'H3 Index', 'Latitude', 'Longitude'])
pd.set_option('display.width', None)
#print(df)
#df.to_csv('MichelinStars.csv',sep='\t')
#df.to_excel('MichelinStars.xlsx')




