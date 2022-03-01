import requests, re
from bs4 import BeautifulSoup


def get_soup(pagination_url, page_num=1):
    
    '''Get soup object for the Product listing url. Default page number of 1 will be used.'''
    response = requests.get(pagination_url + '?page=' + str(page_num))
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, product_name, price, url, stock status'''
    soup = get_soup(pagination_url)
    num_pages = int(soup.select('ul.pagination-custom a')[-2].text.strip()) if soup.select('ul.pagination-custom a') else 1
    data_list = []
    for current_page in range(1, int(num_pages) + 1):
        for product in soup.select('div.grid div.home-product'):
            product_dict = {}
            product_dict['product_id'] = re.search(r'data-id="(.*?)">', str(product)).group(1) if re.search(r'data-id="(.*?)">', str(product)) else 'n/a'
            product_dict['product_page_url'] = 'https://computerspace.in' + product.select('a.grid-link.text-center')[0].get('href', 'n/a') if product.select('a.grid-link.text-center') else 'n/a'
            product_dict['product_name'] = ' '.join(product.select('.product-title')[0].text.split()) if product.select('.product-title') else 'n/a'
            if product.select('.grid-link__sale_price'): product_dict['regular_price'], product_dict['markdown_price'] = ' '.join(product.select('.money')[0].text.split()), ' '.join(product.select('.money')[-1].text.split())
            else: product_dict['regular_price'] = ' '.join(product.select('.money')[0].text.split()) if product.select('.money') else 'n/a'
            product_dict['stock_status'] = 'Out of Stock' if 'sold-out' in product.attrs.get('class') else 'In Stock'
            if product_dict: data_list.append(product_dict)
        soup = get_soup(pagination_url, str(current_page + 1))
    return data_list


# pagination_url = 'https://computerspace.in/collections/storage'
# pagination_url = 'https://computerspace.in/collections/processor'
pagination_url = 'https://computerspace.in/collections/graphics-card'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))

