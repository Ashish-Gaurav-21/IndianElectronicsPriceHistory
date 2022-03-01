import requests, re
from bs4 import BeautifulSoup
from math import ceil


def get_soup(pagination_url, page_num=1):
    
    '''Get soup object for the Product listing url. Default page number of 1 will be used.'''
    response = requests.get(pagination_url + 'page/' + str(page_num) + '/', headers={'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'})
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, model_no, product_name, price, url, stock status, review and rating info.'''
    soup = get_soup(pagination_url)
    result_count = (re.search('all (.*?) result', soup.select('.woocommerce-result-count')[0].text, flags=re.IGNORECASE).group(1) if re.search('all (.*?) result', soup.select('.woocommerce-result-count')[0].text, flags=re.IGNORECASE) else (re.search('of (.*?) result', soup.select('.woocommerce-result-count')[0].text, flags=re.IGNORECASE).group(1) if re.search('of (.*?) result', soup.select('.woocommerce-result-count')[0].text, flags=re.IGNORECASE) else 'n/a')) if soup.select('.woocommerce-result-count') else 'n/a'
    num_pages = int(ceil(int(result_count) / 12)) if result_count != 'n/a' else 'n/a'
    data_list = []
    for current_page in range(1, int(num_pages) + 1):
        for product in soup.select('ul.products li.product'):
            product_dict = {}
            product_dict['product_id'] = product.select('a.add_to_cart_button')[0].get('data-product_id', 'n/a') if product.select('a.add_to_cart_button') else 'n/a'
            product_dict['model_no'] = product.select('a.add_to_cart_button')[0].get('data-product_sku', 'n/a') if product.select('a.add_to_cart_button') else 'n/a'
            product_dict['product_page_url'] = product.select('h3 a')[0].get('href', 'n/a') if product.select('h3 a') else 'n/a'
            product_dict['product_name'] = ' '.join(product.select('h3 a')[0].text.split()) if product.select('h3 a') else 'n/a'
            if product.select('.price del'): product_dict['regular_price'], product_dict['markdown_price'] = ' '.join(product.select('.price del')[0].text.split()), ' '.join(product.select('.price ins')[0].text.split())  
            elif product.select('.price'): product_dict['regular_price'] = ' '.join(product.select('.price')[0].text.split())
            product_dict['stock_status'], product_dict['brand'] = [i for i in product.get('class', ['n/a']) if 'stock' in i.lower()], [i for i in product.get('class', ['n/a']) if 'manufacturer' in i.lower()]
            if isinstance(product_dict['stock_status'], list) and len(product_dict['stock_status']) > 0: product_dict['stock_status'] = product_dict['stock_status'][0].replace('instock', 'In Stock').replace('outofstock', 'Out of Stock')
            if isinstance(product_dict['brand'], list) and len(product_dict['brand']) > 0: product_dict['brand'] = product_dict['brand'][0].replace('manufacturer-', '')
            if product_dict['product_id'] != 'n/a': data_list.append(product_dict)
        soup = get_soup(pagination_url, str(current_page + 1))
    return data_list


# pagination_url = 'https://www.pcbworldtech.com/product-category/gaming-chairs/'
# pagination_url = 'https://www.pcbworldtech.com/product-category/processor/'
pagination_url = 'https://www.pcbworldtech.com/product-category/graphics-card/'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))
