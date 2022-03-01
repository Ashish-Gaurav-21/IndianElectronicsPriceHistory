from bs4 import BeautifulSoup
import requests


def get_soup(url):
    
    '''Return soup object for the url provided'''
    response = requests.get(url)
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(url):
    
    '''Extract price, technical_specifications and availability of products for the url provided'''
    soup, data_list = get_soup(url), []
    product_urls = [product.select('li.title a')[0].get('href', 'n/a') for product in soup.select('ul.products li.product') if product.select('li.title a')]
    if not product_urls: product_urls = [product.get('href', 'n/a') for product in soup.select('a.elementor-button-link.elementor-button.elementor-size-sm') if product.get('href', 'n/a') != '#buynow']
    print(product_urls)
    for product_url in product_urls:
        product_dict = {}
        product = get_soup(product_url)
        product_dict['product_page_url'] = product_url
        product_dict['product_id'] = product.find('input', {'name': 'queried_id'}).get('value') if product.find('input', {'name': 'queried_id'}) else 'n/a'
        product_dict['product_name'] = ' '.join(product.select('h1.product_title')[0].text.split()) if product.select('h1.product_title') else 'n/a'
        if product.select('span.price del'): product_dict['regular_price'], product_dict['markdown_price'] = ' '.join(product.select('span.price del')[0].text.split()), ' '.join(product.select('span.price ins')[0].text.split())  
        elif product.select('span.woocommerce-Price-amount.amount bdi'): product_dict['regular_price'] = ' '.join(product.select('span.woocommerce-Price-amount.amount bdi')[0].text.split())
        product_dict['stock_status'] = ('In Stock' if 'instock' in product.select('#main .product')[0].get('class', ['n/a']) else 'Out of Stock') if product.select('#main .product') else 'Out of Stock'
        technical_specifications = dict([(' '.join(i.select('th')[0].text.split()).lower(), ' '.join(i.select('td')[0].text.split())) for i in product.select('table.woocommerce-product-attributes.shop_attributes tr') if i.select('th') and i.select('td')]) if product.select('table.woocommerce-product-attributes.shop_attributes tr') else {}
        if not technical_specifications: technical_specifications = dict([(' '.join(i.select('td')[0].text.split()).lower(), ' '.join(i.select('td')[1].text.split())) for i in product.select('table tr') if len(i.select('td')) == 2]) if product.select('table tr') else {}
        if technical_specifications: product_dict.update({{'memory': 'ram', 'system drive': 'storage', 'chassis': 'case', 'power supply': 'psu', 'ssd / hdd': 'storage', 'graphic': 'graphics card'}.get(k, k): v for k, v in technical_specifications.items()})
        if product_dict: data_list.append(product_dict)
    return data_list
    

# url = 'https://smcinternational.in/product-category/freya/?products-per-page=all'
# url = 'https://smcinternational.in/product-category/aphelios/?products-per-page=all'
# url = 'https://smcinternational.in/product-category/level-two-gaming-pcs/?products-per-page=all'
# url = 'https://smcinternational.in/product-category/level-one-gaming-pcs/?products-per-page=all'
url = 'https://smcinternational.in/msi-desktop-pcs/'
extracted_data = extract_data(url)
print(extracted_data)
