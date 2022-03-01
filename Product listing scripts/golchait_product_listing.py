import requests, re
from bs4 import BeautifulSoup


def get_soup(pagination_url, page_num=1):
    
    '''Get soup object for the Product listing url. Default page number of 1 will be used. Site displays maximum of 100 products on a single page.'''
    response = requests.get(pagination_url + '?page=' + str(page_num))
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, product_name, price, url, stock status.'''
    soup = get_soup(pagination_url)
    num_pages = soup.select('.pagination .page')[-1].text.strip() if soup.select('.pagination .page') else 1 
    data_list = []
    for current_page in range(1, int(num_pages) + 1):
        for product in soup.select('.main-content .grid__item.small--one-half.medium-up--one-fifth'):
            product_dict = {}
            product_dict['product_id'] = product.select('.product-card__image')[0].get('data-image-id') if product.select('.product-card__image') else 'n/a'
            product_dict['product_page_url'] = 'https://golchhait.com' + product.select('a.product-card')[0].get('href', 'n/a') if product.select('a.product-card') else 'n/a'
            product_dict['product_name'] = ' '.join(product.select('.product-card__name')[0].text.split()) if product.select('.product-card__name') else 'n/a'
            product_dict['regular_price'] = ' '.join(product.select('.product-card__price')[0].text.split()).replace('Regular price ', '') if product.select('.product-card__price') else 'n/a'
            product_dict['stock_status'] = 'Out of Stock' if 'sold out' in str(product.select('.product-card__availability')).lower() else 'In Stock'
            if product_dict: data_list.append(product_dict)
        soup = get_soup(pagination_url, str(current_page + 1))
    return data_list

    
# pagination_url = 'https://golchhait.com/collections/graphics-card'
pagination_url = 'https://golchhait.com/collections/mouse'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))
