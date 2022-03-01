import requests, json, re
from bs4 import BeautifulSoup


def get_soup(url):
    
    '''Return soup object for the url provided'''
    response = requests.get(url)
    response_code, soup = response.status_code, BeautifulSoup(response.text, features='lxml')
    return soup

def extract_data(url):
    
    ''''''
    product_urls, data_list = ['https://computerspace.in' + i.select('a.grid-link.text-center')[0].get('href') for i in get_soup(url).select('.grid .home-product')], []
    for product_url in product_urls:
        soup = get_soup(product_url)
        product_dict = {}
        product_dict['product_id'] = ' '.join(soup.select('.variant-sku')[0].text.split()) if soup.select('.variant-sku') else 'n/a'
        product_dict['regular_price'] = soup.select('.product-single__price')[0].text.strip() if soup.select('.product-single__price') else 'n/a'
        if soup.select('.product-single__sale-price'): product_dict['markdown_price'] = soup.select('.product-single__sale-price')[0].text.strip()
        # stock_status comes as In Stock for all
        # product_dict['stock_status'] = ' '.join(soup.select('#AddToCartText')[0].text.split()) if soup.select('#AddToCartText') else 'n/a'
        product_dict['product_page_url'] = product_url
        # Technical specifications are improperly formatted
        product_dict['technical_specifications'] = [' '.join(i.split()) for i in soup.select('.product-description.rte')[0].find_all(text=True) if ' '.join(i.split())] if soup.select('.product-description.rte') else []
        if product_dict: data_list.append(product_dict)
    return data_list
        

url = 'https://computerspace.in/collections/custom-pc'
extracted_data = extract_data(url)
print(extracted_data)
