import requests, re, json
from bs4 import BeautifulSoup
from math import ceil


def get_soup(pagination_url, page_num=1):
    
    '''Get soup object for the Product listing url. Default page number of 1 will be used. Site displays maximum of 12 products on a single page.'''
    response = requests.get(pagination_url + 'page/' + str(page_num) + '/')
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, model_no, product_name, price (GST excluded), url, stock status, average_rating.'''
    soup = get_soup(pagination_url)
    result_count = (re.search('all (.*?) results', soup.select('.woocommerce-result-count')[0].text, flags=re.IGNORECASE).group(1) if re.search('all (.*?) results', str(soup), flags=re.IGNORECASE) else (re.search('of (.*?) results', str(soup), flags=re.IGNORECASE).group(1) if re.search('of (.*?) results', str(soup), flags=re.IGNORECASE) else 'n/a')) if soup.select('.woocommerce-result-count') else 'n/a'
    num_pages = int(ceil(int(result_count) / 12)) if result_count != 'n/a' else 'n/a'
    data_list = []
    for current_page in range(1, int(num_pages) + 1):
        for product in soup.select('div.product-small.col'):
            product_dict = {}
            product_dict['product_id'] = product.select('div.add-to-cart-button a')[0].get('data-product_id', 'n/a') if product.select('div.add-to-cart-button a') else 'n/a'
            product_dict['model_no'] = product.select('div.add-to-cart-button a')[0].get('data-product_sku', 'n/a') if product.select('div.add-to-cart-button a') else 'n/a'
            product_dict['product_page_url'] = product.select('p.name.product-title a')[0].get('href', 'n/a') if product.select('p.name.product-title a') else 'n/a'
            product_dict['product_name'] = ' '.join(product.select('p.name.product-title a')[0].text.split()) if product.select('p.name.product-title a') else 'n/a'
            if product.select('span.price del'): product_dict['regular_price'], product_dict['markdown_price'] = ' '.join(product.select('span.price del')[0].text.split()), ' '.join(product.select('span.price ins')[0].text.split())  
            elif product.select('span.woocommerce-Price-amount.amount bdi'): product_dict['regular_price'] = ' '.join(product.select('span.woocommerce-Price-amount.amount bdi')[0].text.split())
            product_dict['stock_status'] = 'Out of Stock' if product.select('.out-of-stock-label') else 'In Stock'
            product_dict['average_rating'] = product.select('strong.rating')[0].text.strip() if product.select('strong.rating') else 'n/a'
            if product_dict: data_list.append(product_dict)
        soup = get_soup(pagination_url, str(current_page + 1))
    return data_list


# pagination_url = 'https://techmartunbox.com/product-category/ram/'
# pagination_url = 'https://techmartunbox.com/product-category/processor/'
pagination_url = 'https://techmartunbox.com/product-category/graphic-cards/'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))