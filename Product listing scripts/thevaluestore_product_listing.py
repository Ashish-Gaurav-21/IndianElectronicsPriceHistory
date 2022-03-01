import requests, re
from bs4 import BeautifulSoup


def get_soup(pagination_url, page_num=1):
    
    '''Get soup object for the Product listing url. Default page number of 1 will be used. Site displays maximum of 100 products on a single page.'''
    response = requests.get(pagination_url + '&limit=100&page=' + str(page_num))
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, product_name, model_no, price, url, stock status, average_rating, review_count.'''
    soup = get_soup(pagination_url)
    result_count = (re.search('of (.*?) \(', soup.select('.product-filter.product-filter-bottom.filters-panel .row')[0].text).group(1) if re.search('of (.*?) \(', str(soup)) else 'n/a') if soup.select('.product-filter.product-filter-bottom.filters-panel .row') else 'n/a'
    num_pages = (re.search('\((.*?) Pages\)', soup.select('.product-filter.product-filter-bottom.filters-panel .row')[0].text).group(1) if re.search('\((.*?) Pages\)', str(soup)) else 'n/a') if soup.select('.product-filter.product-filter-bottom.filters-panel .row') else 'n/a'
    data_list = []
    for current_page in range(1, int(num_pages) + 1):
        for product in soup.select('.products-category .product-layout'):
            product_dict = {}
            product_dict['product_id'] = re.search(r'product_id=(.*?)"', str(product)).group(1) if re.search(r'product_id=(.*?)"', str(product)) else 'n/a'
            product_dict['product_page_url'] = product.select('h4 a')[0].get('href', 'n/a') if product.select('h4 a') else 'n/a'
            product_dict['product_name'] = ' '.join(product.select('h4 a')[0].text.split()) if product.select('h4 a') else 'n/a'
            product_dict['model_no'] = re.search(r'\((.*?)\)', product_dict['product_name']).group(1) if re.search(r'\((.*?)\)', product_dict['product_name']) else 'n/a'
            product_dict['average_rating'] = sum([float(re.search(r'fa-stack-(.*?)x', ' '.join(i.get('class', 'n/a'))).group(1)) for i in product.select('i.fa.fa-star') if re.search(r'fa-stack-(.*?)x', ' '.join(i.get('class', 'n/a')))]) if product.select('i.fa.fa-star') else 'n/a'
            product_dict['review_count'] = re.sub('[^0-9]+', '', product.select('.rating-num')[0].text) if product.select('.rating-num') else 'n/a'
            if product.select('.price-normal'): product_dict['regular_price'] = ' '.join(product.select('.price-normal')[0].text.split())
            elif product.select('.price-new') and product.select('.price-old'): product_dict['markdown_price'], product_dict['regular_price'] = ' '.join(product.select('.price-new')[0].text.split()), ' '.join(product.select('.price-old')[0].text.split())
            else: product_dict['regular_price'] = ' '.join(product.select('.price')[0].text.split()) if product.select('.price') else 'n/a'
            product_dict['stock_status'] = 'Out of Stock' if 'unavailable' in str(product.select('.label-stock')).lower() else 'In Stock'
            if product_dict: data_list.append(product_dict)
        soup = get_soup(pagination_url, str(current_page + 1))
    return data_list


pagination_url = 'https://www.thevaluestore.in/computer-components/ssd'
# pagination_url = 'https://www.thevaluestore.in/computer-components/processors-online-india'
# pagination_url = 'https://www.thevaluestore.in/computer-components/computer-accessories/graphic-cards-online-india'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))
