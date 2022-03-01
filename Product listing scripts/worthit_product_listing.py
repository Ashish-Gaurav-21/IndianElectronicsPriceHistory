import requests, re, json
from bs4 import BeautifulSoup


def get_json(url):
    
    '''Get json object for the url provided.'''
    response = requests.get(url)
    response_code, json_data = response.status_code, json.loads(response.text)
    return json_data


def get_source(url):
    
    '''Get HTML source for the url provided.'''
    response = requests.get(url)
    response_code, source = response.status_code, response.text
    return source


def extract_data(product_listing_url):
    
    '''Extract the data of product present in listing page. product_id, stock_volume, product_name, brand, model_no, barcode, price, url, stock status'''
    soup = BeautifulSoup(get_source(product_listing_url))
    num_pages = 1
    if soup.select('ul.pagination'): num_pages = len(soup.select('ul.pagination')[0].select('li')) - int(2)
    products = soup.select('.as-product-list .as-product') if soup.select('.as-product-list .as-product') else []
    data_list = []
    for current_page in range(1, int(num_pages) + 1):
        for product in products:
            product_dict = {}
            product_dict['product_id'] = product.find('input', {'name': 'product_id'}).get('value', 'n/a') if product.find('input', {'name': 'product_id'}) else 'n/a'
            product_dict['condition'] = product.find('span', {'data-oe-field': 'condition_type'}).text if product.find('span', {'data-oe-field': 'condition_type'}) else 'n/a'
            product_dict['stock_volume'] = ' '.join(product.select('#availableQty')[0].text.split()) if product.select('#availableQty') else 'n/a'
            product_dict['product_name'] = ' '.join(product.find('a', {'itemprop': 'name'}).text.split()) if product.find('a', {'itemprop': 'name'}) else 'n/a'
            if product_dict.get('stock_volume', 'n/a') not in ['', 'n/a', None]: product_dict['stock_status'] = 'In Stock' if int(product_dict.get('stock_volume')) > int(0) else 'Out of Stock'
            product_dict['product_page_url'] = re.sub(r'^/', 'https://worthit.in/', product.find('a', {'itemprop': 'name'}).get('href', 'n/a')) if product.find('a', {'itemprop': 'name'}) else 'n/a'
            if all([product_dict.get('product_name', 'n/a') not in ['', 'n/a', None], product_dict.get('product_page_url', 'n/a') not in ['', 'n/a', None]]):
                if all([isinstance(product_dict['product_name'].split(' '), list), isinstance(product_dict['product_page_url'].split('/'), list)]): product_dict['model_no'] = product_dict['product_page_url'].lower().split('/')[-1].split(product_dict['product_name'].lower().split(' ')[0])[0].strip('-')
            if product.select('.product_price del'):
                product_dict['regular_price'] = ' '.join(product.select('.product_price del')[0].text.split())
                product_dict['markdown_price'] = ' '.join(product.select('.product_price span')[0].text.split())
            else: product_dict['regular_price'] = ' '.join(product.select('.product_price span')[0].text.split()) if product.select('.product_price span') else 'n/a'
            if product_dict: data_list.append(product_dict)
        if current_page < num_pages:
            soup = BeautifulSoup(get_source(product_listing_url + 'page/' + str(current_page + 1)))
            products = soup.select('.as-product-list .as-product') if soup.select('.as-product-list .as-product') else []
    return data_list


product_listing_url = 'https://worthit.in/shop/category/peripherals-graphics-card-5'
# product_listing_url = 'https://worthit.in/shop/category/peripherals-memories-7'
# product_listing_url = 'https://worthit.in/shop/category/peripherals-motherboards-9'
# product_listing_url = 'https://worthit.in/shop/category/laptops-2/'
extracted_data = extract_data(product_listing_url)
print(extracted_data)
print(len(extracted_data))
