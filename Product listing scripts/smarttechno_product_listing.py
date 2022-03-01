import requests, re
from bs4 import BeautifulSoup


def get_soup(pagination_url, page_num=1):
    
    '''Get soup object for the Product listing url. Default page number of 1 will be used. Site displays maximum of 100 products on a single page.'''
    response = requests.get(pagination_url + '?limit=100&page=' + str(page_num))
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, model_no, product_name, price, url, stock status, average_rating.'''
    soup = get_soup(pagination_url)
    result_count = (re.search('of (.*?) \(', soup.select('.row.pagination-results')[0].text).group(1) if re.search('of (.*?) \(', str(soup)) else 'n/a') if soup.select('.row.pagination-results') else 'n/a'
    num_pages = (re.search('\((.*?) Pages\)', soup.select('.row.pagination-results')[0].text).group(1) if re.search('\((.*?) Pages\)', str(soup)) else 'n/a') if soup.select('.row.pagination-results') else 'n/a'
    data_list = []
    for current_page in range(1, int(num_pages) + 1):
        for product in soup.select('.main-products-wrapper .product-layout'):
            product_dict = {}
            product_dict['product_id'] = product.find('input', {'name': 'product_id'}).get('value', 'n/a') if product.find('input', {'name': 'product_id'}) else 'n/a'
            product_dict['model_no'] = ' '.join(product.select('.stat-2')[0].text.replace('Model:', '').split()) if product.select('.stat-2') else 'n/a'
            product_dict['brand'] = ' '.join(product.select('.stat-1')[0].text.replace('Brand:', '').split()) if product.select('.stat-1') else 'n/a'
            product_dict['product_page_url'] = product.select('.name a')[0].get('href', 'n/a') if product.select('.name a') else 'n/a'
            product_dict['product_name'] = ' '.join(product.select('.name a')[0].text.split()) if product.select('.name a') else 'n/a'
            product_dict['average_rating'] = sum([float(re.search('fa-stack-(.*?)x"', str(i).replace('<i class="fa fa-star-o fa-stack-2x"></i></span>', '').replace('<span class="fa fa-stack">', '')).group(1)) for i in product.select('.rating-stars span') if re.search('fa-stack-(.*?)x"', str(i).replace('<i class="fa fa-star-o fa-stack-2x"></i></span>', '').replace('<span class="fa fa-stack">', ''))]) / 2.0
            if product.select('.price-normal'): product_dict['regular_price'] = ' '.join(product.select('.price-normal')[0].text.split())
            elif product.select('.price-new') and product.select('.price-old'): product_dict['markdown_price'], product_dict['regular_price'] = ' '.join(product.select('.price-new')[0].text.split()), ' '.join(product.select('.price-old')[0].text.split())
            else: product_dict['markdown_price'] = ' '.join(product.select('.price')[0].text.split()) if product.select('.price') else 'n/a'
            product_dict['stock_status'] = 'Out of Stock' if 'out-of-stock' in product.attrs.get('class') else 'In Stock'
            if product_dict: data_list.append(product_dict)
        soup = get_soup(pagination_url, str(current_page + 1))
    return data_list


pagination_url = 'https://smarttechno.in/ssd'
# pagination_url = 'https://smarttechno.in/processors'
# pagination_url = 'https://smarttechno.in/graphic-cards'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))
