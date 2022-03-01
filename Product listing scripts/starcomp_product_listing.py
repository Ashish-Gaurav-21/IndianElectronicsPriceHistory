import requests, re
from bs4 import BeautifulSoup
from math import ceil


def get_soup(pagination_url, page_num=1):
    
    '''Get soup object for the Product listing url. Default page number of 1 will be used. Site displays maximum of 36 products on a single page.'''
    response = requests.get(pagination_url + '?p=' + str(page_num) + '&product_list_limit=36', headers = {'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'})
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, model_no, product_name, price, url, review and rating info.'''
    soup = get_soup(pagination_url)
    result_count = ' '.join(soup.select('.toolbar-amount')[0].text.lower().split()) if soup.select('.toolbar-amount') else 'n/a'
    result_count = (result_count.split()[-1] if result_count.startswith('items') else result_count.split()[0]) if result_count != 'n/a' else 'n/a'
    num_pages = int(ceil(int(result_count) / 36)) if result_count != 'n/a' else 'n/a'
    data_list = []
    for current_page in range(1, int(num_pages) + 1):
        for product in soup.select('.products.wrapper.grid.products-grid.category-product-grid .item.product.product-item'):
            product_dict = {}
            product_dict['product_id'] = product.select('.price-box.price-final_price')[0].get('data-product-id', 'n/a') if product.select('.price-box.price-final_price') else 'n/a'
            product_dict['model_no'] = ' '.join(product.select('.sku')[0].find_all(text=True)[-1].split()) if product.select('.sku') else 'n/a'
            product_dict['product_page_url'] = product.select('a.product-item-link')[0].get('href', 'n/a') if product.select('a.product-item-link') else 'n/a'
            product_dict['product_name'] = ' '.join(product.select('a.product-item-link')[0].text.split()) if product.select('a.product-item-link') else 'n/a'
            product_dict['review_count'] = re.sub('[^0-9]+', '', product.select('.reviews-actions')[0].text) if product.select('.reviews-actions') else 'n/a'
            product_dict['average_rating'] = (0.05 * float(product.select('.rating-result')[0].get('title', 'n/a').replace('%', '')) if product.select('.rating-result')[0].get('title', 'n/a') != 'n/a' else 'n/a') if product.select('.rating-result') else 'n/a'
            product_dict['markdown_price'] = ' '.join(product.select('.price')[0].text.split()) if product.select('.price') else 'n/a' # site does not display regular price
            if product_dict['product_id'] != 'n/a': data_list.append(product_dict)
        soup = get_soup(pagination_url, str(current_page + 1))
    return data_list

    
# pagination_url = 'https://starcomp.in/desktop-components/cpu.html'
pagination_url = 'https://starcomp.in/desktop-components/graphics-card.html'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))