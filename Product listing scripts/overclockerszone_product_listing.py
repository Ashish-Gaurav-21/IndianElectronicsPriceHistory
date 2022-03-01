import requests, re
from bs4 import BeautifulSoup


def get_soup(pagination_url, page_num=1):
    
    '''Get soup object for the Product listing url. Default page number of 1 will be used. Site displays maximum of 20 products on a single page.'''
    response = requests.get(pagination_url + '?page=' + str(page_num))
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, model_no, product_name, price, url, stock status, rating info.'''
    soup = get_soup(pagination_url)
    num_pages = len(soup.select('ul.PagingList li')) if soup.select('ul.PagingList li') else 1
    data_list = []
    for current_page in range(1, int(num_pages) + 1):
        for product in soup.select('ul.ProductList li'):
            product_dict = {}
            product_dict['product_id'] = product.select('.QuickView')[0].get('data-product', 'n/a') if product.select('.QuickView') else 'n/a'
            product_dict['product_page_url'] = product.select('a.pname')[0].get('href', 'n/a') if product.select('a.pname') else 'n/a'
            product_dict['product_name'] = ' '.join(product.select('a.pname')[0].text.split()) if product.select('a.pname') else 'n/a'
            product_dict['model_no'] = re.search(r'\)(.*?)\(', product_dict['product_name'][::-1]).group(1)[::-1] if re.search(r'\)(.*?)\(', product_dict['product_name'][::-1]) else 'n/a'
            product_dict['average_rating'] = ' '.join(product.select('span.Rating')[0].get('class', 'n/a')).replace('Rating Rating', '') if product.select('span.Rating') else 'n/a'
            if product.select('.RetailPriceValue'): product_dict['regular_price'], product_dict['markdown_price'] = ' '.join(product.select('.RetailPriceValue')[0].text.split()), (' '.join(product.select('.p-price')[0].find_all(text=True)[-1].split()) if product.select('.p-price')[0].find_all(text=True) else 'n/a') if product.select('.p-price') else 'n/a'
            else: product_dict['regular_price'] = ' '.join(product.select('.p-price')[0].text.split()) if product.select('.p-price') else 'n/a'
            product_dict['stock_status'] = 'In Stock'
            if product_dict: data_list.append(product_dict)
        soup = get_soup(pagination_url, str(current_page + 1))
    return data_list


# pagination_url = 'http://www.overclockerszone.com/graphic-cards-1/'
# pagination_url = 'http://www.overclockerszone.com/ssd/'
pagination_url = 'http://www.overclockerszone.com/memory-modules/'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))
