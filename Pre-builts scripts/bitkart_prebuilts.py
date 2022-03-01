import requests
from bs4 import BeautifulSoup


def get_soup(url):
    
    '''Return soup object for the url provided'''
    response = requests.get(url)
    response_code, soup = response.status_code, BeautifulSoup(response.text, features='lxml')
    return soup

def extract_data(url):
    
    ''''''
    soup, data_list, product_urls = get_soup(url + '?p=' + str(1)), [], []
    num_products = int(soup.select('.toolbar.toolbar-products .toolbar-number')[0].text.strip()) if soup.select('.toolbar.toolbar-products .toolbar-number') else 'n/a'
    product_limit_per_page = int(soup.select('.limiter-options option')[0].get('value', '6')) if soup.select('.limiter-options option') else 6
    num_pages = num_products // product_limit_per_page + 1
    for i in range(1, num_pages + 1):
        [product_urls.append(product.select('a.product-item-link')[0].get('href', 'n/a')) for product in soup.select('ol.products li.item.product') if product.select('a.product-item-link')]
        soup = get_soup('https://www.bitkart.com/device.html' + '?p=' + str(i + 1))
    for product_url in product_urls:
        soup = get_soup(product_url)
        product_dict = {}
        product_dict['product_id'] = soup.find('input', {'name': 'product'}).get('value', 'n/a') if soup.find('input', {'name': 'product'}) else 'n/a'
        product_dict['regular_price'] = soup.find('meta', {'itemprop': 'price'}).get('content', 'n/a') if soup.find('meta', {'itemprop': 'price'}) else 'n/a'
        product_dict['product_page_url'] = product_url
        technical_specifications = dict([(i.select('th')[0].text.strip().lower(), i.select('td')[0].text.strip()) for i in soup.select('#product-attribute-specs-table tr') if i.select('th') and i.select('td')])
        if technical_specifications: product_dict.update({{'cooler': 'cpu cooler', 'chassiss': 'cpu case'}.get(k, k): v for k, v in technical_specifications.items() if 'rockpack' not in k})        
        if product_dict: data_list.append(product_dict)
    return data_list
        

url = 'https://www.bitkart.com/device.html'
extracted_data = extract_data(url)
print(extracted_data)