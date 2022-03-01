# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, sys


def get_soup(url):
    
    '''Return soup object for the url provided'''
    response = requests.get(url)
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(url):
    
    '''Extract price, technical_specifications and availability of products for the url provided'''
    soup, data_list = get_soup(url), []
    product_urls = [product.get('href', 'n/a') for product in soup.select('#main a.elementor-button-link.elementor-button.elementor-size-md') if product.get('href')]
    for product_url in product_urls:
        product_dict = {}
        product = get_soup(product_url)
        product_dict['product_page_url'] = product_url
        product_dict['product_id'] = product.find('link', {'rel': 'shortlink'}).get('href', 'n/a').replace('https://techdreams.co.in/?p=', '') if product.find('link', {'rel': 'shortlink'}) else 'n/a'
        product_dict['product_name'] = ' '.join(product.select('h1.product_title')[0].text.split()) if product.select('h1.product_title') else 'n/a'
        if product.select('span.price del'): product_dict['regular_price'], product_dict['markdown_price'] = ' '.join(product.select('span.price del')[0].text.split()), ' '.join(product.select('span.price ins')[0].text.split())  
        elif product.select('span.woocommerce-Price-amount.amount bdi'): product_dict['regular_price'] = ' '.join(product.select('span.woocommerce-Price-amount.amount bdi')[0].text.split())
        product_dict['stock_status'] = ('In Stock' if 'instock' in product.select('#main .product')[0].get('class', ['n/a']) else 'Out of Stock') if product.select('#main .product') else 'Out of Stock'
        technical_specifications = dict([(i.text.split('-')[0].lower(), i.text.split('-')[-1].replace(u'\xa0', u' ')) for i in product.select('.woocommerce-product-details__short-description p') if i.text if '-' in i.text]) if product.select('.woocommerce-product-details__short-description p') else {}
        if technical_specifications: product_dict.update({{'cooler': 'cpu cooler', 'gpu': 'graphics card'}.get(k, k): v for k, v in technical_specifications.items() if 'rockpack' not in k})
        if product_dict: data_list.append(product_dict)
    return data_list
    

# url = 'https://techdreams.co.in/product-category/gaming-pc/entry-level/'
# url = 'https://techdreams.co.in/product-category/gaming-pc/mid-level/'
url = 'https://techdreams.co.in/product-category/gaming-pc/extreme/'
extracted_data = extract_data(url)
print(extracted_data)
