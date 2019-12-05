import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

# getting access to the url of source data 
results = requests.get('https://meqasa.com/houses-for-rent-in-ghana')

#  pulling data down locally from the results
soup = BeautifulSoup(results.content, 'lxml')

#  using the the tags that contains the neede data 
listings = soup.find_all('div', {'class':'mqs-prop-dt-wrapper'})

#  this is to control value of x if it is None
def if_exists(x):
    if x is not None:
        return x.text
    else:
        return ''


#   function to automate the extraction of data from soup
real_estate = []
for a in listings:
    property_name = a.find('h2').text.replace('\n', '')
    beds =  a.find('li', {'class':'bed'}).text.replace('\n', '')
    garages = if_exists(a.find('li', {'class':'garage'}))
    showers = a.find('li', {'class':'shower'}).text.replace('\n', '')
    area = if_exists(a.find('li', {'class':'area'}))
    description = if_exists(a.find_all('p')[1])
    price = a.find('p', {'class':'h3'}).text.replace('\nPrice', '').replace('/ month\n', '').replace('[Price disclosed on request] \n', '')
    currency = a.find('p', {'class':'h3'}).text.replace('\nPrice', '').replace('/ month\n', '').replace('[Price disclosed on request] \n', '')
    currency = re.sub('\d', '', currency)
    rent = a.find('p', {'class':'h3'}).text.replace('\nPrice$', '').replace('\nPriceGH₵', '').replace('\n', '').replace('PricePricedisclosedonrequest', '')
    c = re.sub('\d.....\W', '', rent)
    d = re.sub('\d....\W', '', c)
    rentperiod = re.sub('\W', '', d)
    url = a.find('a')['href']
    url = 'https://meqasa.com/houses-for-rent-in-ghana' + url
    address = a.find('h2').text.replace('\n', '').split('at')[1]
    timeposted = ''
    
    
#   appending data collected into the appropriate columns        
    real_estate.append(
        {
            'property': property_name,             
            'showers': showers,
            'beds': beds,            
            'garages': garages,
            'area': area,
            'description': description,
            'price': price,
            'currency': currency,
            'rent period': rentperiod,
            'url': url,  
            'address': address,
            'time posted': timeposted,
            
        }
    )
  
# real_estate

#    dataframe of scraped data
df = pd.DataFrame(real_estate)

df_csv = df.to_csv('real_estate.csv', index = None, header=True)
