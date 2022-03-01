import requests, json, re
from bs4 import BeautifulSoup


def get_soup(url):
    
    '''Return soup object for the url provided'''
    response = requests.get(url)
    response_code, soup = response.status_code, BeautifulSoup(response.text, features='lxml')
    return soup

def extract_data(url):
    
    ''''''
    product_urls, data_list = [i.select('.jet-woo-product-title a')[0].get('href', 'n/a') for i in get_soup(url).select('.jet-woo-products .jet-woo-products__inner-box') if i.select('.jet-woo-product-title a')], []
    print (product_urls)
    for product_url in product_urls:
        soup = get_soup(product_url)
        product_dict = {}
        product_dict['product_id'] = soup.select('#prod-sku')[0].text.strip() if soup.select('#prod-sku') else 'n/a'
        product_dict['regular_price'] = soup.select('.price')[0].text.strip() if soup.select('.price') else 'n/a'
        product_dict['product_page_url'] = product_url
        technical_specifications = dict([(i.select('td')[0].text.strip().lower(), i.select('td')[1].text.strip()) for i in soup.select('#tab-description tr') if len(i.select('td')) == 2])
        if technical_specifications: product_dict.update({{'cooler': 'cpu cooler', 'case': 'cpu case'}.get(k, k): v for k, v in technical_specifications.items() if 'rockpack' not in k})        
        if product_dict: data_list.append(product_dict)
    return data_list
        

url = 'https://www.pcstudio.in/pre-built-pc/'
extracted_data = extract_data(url)
print(extracted_data)
