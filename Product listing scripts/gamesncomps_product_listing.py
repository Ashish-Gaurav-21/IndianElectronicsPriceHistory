import requests, re, json
from bs4 import BeautifulSoup


def get_soup(pagination_url):
    
    '''Get soup object for the Product listing url. Default page number of 1 will be used. Site has option to display all the products in 1st page.'''
    response = requests.get(pagination_url + '?ppp=-1')
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, model_no, product_name, price, url, stock status, average_rating.'''
    soup = get_soup(pagination_url)
    result_count = (re.search('all (.*?) results', soup.select('.woocommerce-result-count')[0].text, flags=re.IGNORECASE).group(1) if re.search('all (.*?) results', soup.select('.woocommerce-result-count')[0].text, flags=re.IGNORECASE) else (re.search('of (.*?) results', soup.select('.woocommerce-result-count')[0].text, flags=re.IGNORECASE).group(1) if re.search('of (.*?) results', soup.select('.woocommerce-result-count')[0].text, flags=re.IGNORECASE) else 'n/a')) if soup.select('.woocommerce-result-count') else 'n/a'
    data_list = []
    for product in soup.select('ul.products li.product'):
        product_dict = {}
        product_dict['product_id'] = product.select('div.add-to-cart-wrap a')[0].get('data-product_id', 'n/a') if product.select('div.add-to-cart-wrap a') else 'n/a'
        product_dict['model_no'] = product.select('div.add-to-cart-wrap a')[0].get('data-product_sku', 'n/a') if product.select('div.add-to-cart-wrap a') else 'n/a'
        product_dict['product_page_url'] = product.select('a.woocommerce-loop-product__link')[0].get('href', 'n/a') if product.select('a.woocommerce-loop-product__link') else 'n/a'
        product_dict['product_name'] = ' '.join(product.select('a.woocommerce-loop-product__link')[0].text.split()) if product.select('a.woocommerce-loop-product__link') else 'n/a'
        if product.select('span.price del'): product_dict['regular_price'], product_dict['markdown_price'] = ' '.join(product.select('span.price del')[0].text.split()), ' '.join(product.select('span.price ins')[0].text.split())  
        elif product.select('span.woocommerce-Price-amount.amount bdi'): product_dict['regular_price'] = ' '.join(product.select('span.woocommerce-Price-amount.amount bdi')[0].text.split())
        product_dict['stock_status'] = 'In Stock' if [i for i in product.attrs.get('class', ['n/a']) if 'instock' in i.lower()] else 'Out of Stock'
        product_dict['average_rating'] = product.select('strong.rating')[0].text.strip() if product.select('strong.rating') else 'n/a'
        if product_dict: data_list.append(product_dict)
    return data_list


# pagination_url = 'https://gamesncomps.com/product-category/storage/'
pagination_url = 'https://gamesncomps.com/product-category/cpu/'
# pagination_url = 'https://gamesncomps.com/product-category/graphics-card/'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))
