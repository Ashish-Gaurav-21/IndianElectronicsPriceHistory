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
    products = soup.select('ul.products li.product') if soup.select('ul.products li.product') else []
    data_list = []
    for product in products:
        product_dict = {}
        product_dict['product_id'] = [i.lower().replace('post-', '') for i in product.get('class') if 'post-' in i.lower()][0] if product.get('class') else 'n/a'
        product_dict['product_name'] = ' '.join(product.select('.woocommerce-loop-product__title')[0].text.split()) if product.select('.woocommerce-loop-product__title') else 'n/a'
        product_dict['stock_status'] = [i.lower() for i in product.get('class') if 'stock' in i.lower()][0].replace('outofstock', 'Out of Stock').replace('instock', 'In Stock') if product.get('class') else 'n/a'
        product_dict['product_page_url'] = product.select('a.woocommerce-loop-product__link')[0].get('href', 'n/a') if product.select('a.woocommerce-loop-product__link') else 'n/a'
        product_dict['model_no'] = ' '.join(product.select('.product-sku')[0].text.split()).replace('SKU: ', '') if product.select('.product-sku') else 'n/a'
        if product.select('del'): product_dict['regular_price'], product_dict['markdown_price'] = ' '.join(product.select('del')[0].text.split()) if product.select('del') else 'n/a', ' '.join(product.select('.price bdi')[0].text.split()) if product.select('.price bdi') else 'n/a'
        else: product_dict['reguar_price'] = ' '.join(product.select('.price bdi')[0].text.split()) if product.select('.price bdi') else 'n/a'
        if product_dict: data_list.append(product_dict)
    return data_list


product_listing_url = 'https://www.tibgstore.co.in/product-category/cabinet/'
# product_listing_url = 'https://www.tibgstore.co.in/product-category/mother-board/'
# product_listing_url = 'https://www.tibgstore.co.in/product-category/gpu/'
extracted_data = extract_data(product_listing_url)
print(extracted_data)
print(len(extracted_data))

