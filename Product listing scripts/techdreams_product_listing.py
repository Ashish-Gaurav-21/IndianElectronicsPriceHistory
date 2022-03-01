import requests, re, json
from bs4 import BeautifulSoup


def get_soup(pagination_url):
    
    '''Get soup object for the Product listing url. Site has option to display all the products in 1st page.'''
    response = requests.get(pagination_url + '?products-per-page=all')
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, model_no, product_name, price, url, stock status'''
    soup = get_soup(pagination_url)
    data_list = []
    for product in soup.select('ul.products li.product'):
        product_dict = {}
        product_dict['product_id'] = product.select('.product_type_simple')[0].get('data-product_id', 'n/a') if product.select('.product_type_simple') else 'n/a'
        product_dict['model_no'] = product.select('.product_type_simple')[0].get('data-product_sku', 'n/a') if product.select('.product_type_simple') else 'n/a'
        product_dict['product_page_url'] = product.select('li.title a')[0].get('href', 'n/a') if product.select('li.title a') else 'n/a'
        product_dict['product_name'] = ' '.join(product.select('li.title a')[0].text.split()) if product.select('li.title a') else 'n/a'
        if product.select('span.price del'): product_dict['regular_price'], product_dict['markdown_price'] = ' '.join(product.select('span.price del')[0].text.split()), ' '.join(product.select('span.price ins')[0].text.split())  
        elif product.select('span.woocommerce-Price-amount.amount bdi'): product_dict['regular_price'] = ' '.join(product.select('span.woocommerce-Price-amount.amount bdi')[0].text.split())
        product_dict['stock_status'] = 'In Stock' if [i for i in product.attrs.get('class', ['n/a']) if 'instock' in i.lower()] else 'Out of Stock'
        if product_dict: data_list.append(product_dict)
    return data_list


pagination_url = 'https://techdreams.co.in/product-category/processor/'
# pagination_url = 'https://techdreams.co.in/product-category/graphics-cards/'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))
