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
    products = soup.select('ul.products.products.list-unstyled li.product') if soup.select('ul.products.products.list-unstyled li.product') else []
    data_list = []
    for product in products:
        product_dict = {}
        product_dict['product_id'] = [i.lower().replace('post-', '') for i in product.get('class') if 'post-' in i.lower()][0] if isinstance(product.get('class', 'n/a'), list) else 'n/a'
        product_dict['product_page_url'] = product.select('a.woocommerce-loop-product__link')[0].get('href', 'n/a') if product.select('a.woocommerce-loop-product__link') else 'n/a'
        product_dict['product_name'] = ' '.join(product.select('.woocommerce-loop-product__title')[0].text.split()) if product.select('.woocommerce-loop-product__title') else 'n/a'
        product_dict['stock_status'] = [i.lower() for i in product.get('class') if 'stock' in i.lower()][0].replace('outofstock', 'Out of Stock').replace('instock', 'In Stock') if isinstance(product.get('class', 'n/a'), list) else 'n/a'
        product_dict['model_no'] = re.search(r'data-product_sku="(.*?)"', str(product)).group(1) if re.search(r'data-product_sku="(.*?)"', str(product)) else 'n/a'
        if product_dict.get('model_no', 'n/a') in ['', 'n/a', None]: product_dict['model_no'] = ' '.join(product.select('.product-sku')[0].text.split()) if product.select('.product-sku') else 'n/a'
        product_dict['brand'] = [i.lower().replace('product_tag-', '') for i in product.get('class') if 'product_tag-' in i.lower()] if isinstance(product.get('class', 'n/a'), list) else 'n/a'
        if product.select('.price del'):
            product_dict['regular_price'] = ' '.join(product.select('.price del')[0].text.split()) if product.select('.price del') else 'n/a'
            product_dict['markdown_price'] = ' '.join(product.select('.price bdi')[0].text.split()) if product.select('.price bdi') else 'n/a'
        else: product_dict['regular_price'] = ' '.join(product.select('.price bdi')[0].text.split()) if product.select('.price bdi') else 'n/a'
        if product_dict: data_list.append(product_dict)
    return data_list


product_listing_url = 'https://www.pcshop.in/product-category/graphic-card/?ppp=-1'
# product_listing_url = 'https://worthit.in/shop/category/peripherals-memories-7'
# product_listing_url = 'https://worthit.in/shop/category/peripherals-motherboards-9'
# product_listing_url = 'https://worthit.in/shop/category/laptops-2/'
extracted_data = extract_data(product_listing_url)
print(extracted_data)
print(len(extracted_data))
