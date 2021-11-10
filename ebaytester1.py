import argparse
import requests
from bs4 import BeautifulSoup
import json


def parse_itemssold (text):
    ''' Takes as input a string  and returns the number of items sold
    
    >>> parse_itemssold('1,112 sold')
    1112
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers+= char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def shipping_price_s(text):
    '''
    Takes as input a string  and returns the shipping price
    
    >>> shipping_price_s('+$31.31 shipping estimate')
    3131

    >>> shipping_price_s('Free shipping')
    0

    >>> shipping_price_s('+$10.65 shipping')
    1065

    '''
    ship_price = ''
    for char in text: 
        if char in '1234567890':
            ship_price+= char
    if '$' in text:
        return int(ship_price)
    if 'Free' in text:
        return 0

def priceofitems(text):
    '''
    Takes as input a str and returns the price of item

    >>> priceofitems('$54.99')
    5499
    >>> priceofitems('$0.99')
    99
    >>> priceofitems('$98.56')
    9856
    
    '''

    itemprice= ''
    for char in text:
        if char in '1234567890':
            itemprice+= char
    return int(itemprice)
            


    
#Tells python file to run code below only when run normally
#Tells python to check doctests when python3 - m doctest [filename] is run
if __name__ == '__main__':

    #command line args
    parser = argparse.ArgumentParser(description='Download info from ebay and convert it into JSON')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default = 1)
    args = parser.parse_args()
    print('args.search_term = ', args.search_term)

    #List of all items found in all ebay page numbers
    items =[]


    #Loop over the webpages
    for pg_nmbr in range (1, int(args.num_pages)+1):
        # Create URL
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' 
        url+= args.search_term
        url+= '&_sacat=0&LH_TitleDesc=0&_pgn=' 
        url+= str(pg_nmbr)
        url+= '&rt=nc'
        print('url=', url)


        #Download the HTML

        f = requests.get(url)
        status = f.status_code
        print ('status=', status)
        html = f.text
        # print ('html=', html[:50])

        #Process the html
        soup = BeautifulSoup(html, 'html.parser')
        title_items = soup.select('.s-item__title')

        #Extracting title of items, creating a dictionary, and appending the dictionary to the item list
        for title_item in title_items:
            print('title of item=', title_item.text)

        # Extracting status of items 
        status_items = soup.select('.SECONDARY_INFO')
        for status_item in status_items:
            print('status of item', status_item.text)
            

        #Extracting Shipping price of an item
        shipping_prices = soup.select('.s-item__shipping')
        for shippingprice in shipping_prices:
            print('shipping price=', shippingprice.text)

        #Extracting free returns items
        free_returns = soup.select('.s-item__free-returns')
        for free_return in free_returns:
            print('free_return=', free_return.text)
        # print('number of free return items = ', len(free_returns))

        #Extracting the price of an item
        price_items = soup.select('.s-item__price')
        for price_item in price_items:
            print('price of item =', price_item.text)

        #Loop over the items in the page 
        item_s = soup.select('.s-item')
        for item in item_s:
            title = None
            title_items = item.select('.s-item__title')
            for title_item in title_items:
                title = title_item.text
            
            freereturns= False
            free_returns = item.select('.s-item__free-returns')
            for title_item in free_returns:
                freereturns= True

            status_items = item.select('.SECONDARY_INFO')
            for status_item in status_items:
                status_i = None
                for status_item in status_items:
                    status_i = status_item.text
            
            items_sold = None
            tags_itemssold = item.select('.s-item__hotness') 
            for title_item in tags_itemssold:
                items_sold = parse_itemssold(title_item.text)
            
            shipping_p = None
            shipping_prices = item.select('.s-item__shipping')
            for title_item in shipping_prices:
                shipping_p = shipping_price_s(title_item.text)
            
            item_p = None
            price_items = item.select('.s-item__price')
            for title_item in price_items:
                item_p = priceofitems(title_item.text)

            #Append a dictionary that contains the name, free return status, status of an item, and shipping price to the items list
            item_d= { 'name': title, 'freereturns' : freereturns, 'Status' : status_item.text, 'items sold': items_sold, 'Shipping price': shipping_p, 'item price': item_p }
            items.append(item_d)
            # print('item dictionary', items)
            # print('item dictionary length', len(items))
        


    #Create and load the Json file of the results of the search term
    filename = args.search_term + '.json'
    with open (filename, 'w', encoding = 'ascii') as f:
        f.write(json.dumps(items))
