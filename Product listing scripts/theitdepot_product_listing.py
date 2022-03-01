import requests, re
from bs4 import BeautifulSoup


def get_soup(product_listing_url):
    
    '''Get soup object for the Product listing url. We can get all the products in a single hit. Although, site displays maximum of 16 products in a single page.'''
    response = requests.get(product_listing_url)
    response_code, soup = response.status_code, BeautifulSoup(response.text)
    return soup


def extract_data(product_listing_url):
    
    '''Extract the data of product present in listing page. product_id, model_no, brand, product_name, price, url, stock status, ating info.'''
    soup = get_soup(product_listing_url)
    data_list = []
    for product in soup.select('.product-item'):
        product_dict = {}
        product_dict['product_id'] = (re.search(r'_(.*?)\.jpg', product.select('img')[0].get('src', 'n/a')).group(1).lstrip('0') if re.search(r'_(.*?)\.jpg', product.select('img')[0].get('src', 'n/a')) else 'n/a') if product.select('img') else 'n/a'
        product_dict['product_page_url'] = 'https://www.theitdepot.com/' + product.select('.product_title a')[0].get('href', 'n/a') if product.select('.product_title a') else 'n/a'
        product_dict['product_name'] = ' '.join(product.select('.product_title a')[0].get('title', 'n/a').split()) if product.select('.product_title a') else 'n/a'
        product_dict['model_no'] = (re.search(r'model\s*:\s*(.*?)\r', product.select('.short-desc')[0].text, flags=re.IGNORECASE).group(1) if re.search(r'model\s*:\s*(.*?)\r', product.select('.short-desc')[0].text, flags=re.IGNORECASE) else 'n/a') if product.select('.short-desc') else 'n/a'
        if (product_dict['model_no'] == 'n/a') or not product_dict['model_no']: product_dict['model_no'] = re.search(r'\((.*?)\)', product_dict['product_name']).group(1) if re.search(r'\((.*?)\)', product_dict['product_name']) else 'n/a'
        product_dict['brand'] = (re.search(r'brand\s*:\s*(.*?)\r', product.select('.short-desc')[0].text, flags=re.IGNORECASE).group(1) if re.search(r'brand\s*:\s*(.*?)\r', product.select('.short-desc')[0].text, flags=re.IGNORECASE) else 'n/a') if product.select('.short-desc') else 'n/a'
        product_dict['average_rating'] = product.find('span', {'itemprop': 'ratingValue'}).text.strip() if product.find('span', {'itemprop': 'ratingValue'}) else 'n/a' # review_count not displayed on PL. But, available in PDP.
        product_dict['markdown_price'] = ' '.join(product.select('.fa.fa-rupee')[0].parent.text.split()) if product.select('.fa.fa-rupee') else 'n/a' # regular_price is available in KC page, but not in GET request used here.
        product_dict['stock_status'] = 'Out of Stock' if 'out of stock' in str(product).lower() else 'In Stock'
        if product_dict['product_id'] != 'n/a': data_list.append(product_dict)
    return data_list


# product_listing_url = 'https://www.theitdepot.com/category_filter.php?categoryname=RAM+(Memory)&filter-limit=999999&category=6&pageno=1&filter=false'
product_listing_url = 'https://www.theitdepot.com/category_filter.php?categoryname=Processors&filter-limit=999999&category=30&pageno=1&filter=false'
# product_listing_url = 'https://www.theitdepot.com/category_filter.php?categoryname=Graphic+Cards&filter-limit=999999&category=45&pageno=1&filter=false'
extracted_data = extract_data(product_listing_url)
print(extracted_data)
print(len(extracted_data))
