import requests, json, re
from bs4 import BeautifulSoup


def get_soup(url):
    
    '''Return soup object for the url provided'''
    response = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'})
    response_code, soup = response.status_code, BeautifulSoup(response.text, features='lxml')
    return soup

def extract_data(url):
    
    ''''''
    product_urls, data_list = [i.select('a')[0].get('href', 'n/a') for i in get_soup(url).select('.site-main ul.products li.product') if i.select('a')], []
    for product_url in product_urls:
        soup = get_soup(product_url)
        product_dict = {}
        product_dict['product_id'] = re.search(r'"post_id"\s*:\s*"(.*?)"', str(soup)).group(1) if re.search(r'"post_id"\s*:\s*"(.*?)"', str(soup)) else 'n/a'
        product_dict['regular_price'] = soup.select('.price del')[0].text.strip() if soup.select('.price del') else 'n/a'
        product_dict['markdown_price'] = soup.select('.price ins')[0].text.strip() if soup.select('.price ins') else 'n/a'
        product_dict['stock_status'] = re.search(r'"availability":"http:\\/\\/schema.org\\/(.*?)","', str(soup)).group(1) if re.search(r'"availability":"http:\\/\\/schema.org\\/(.*?)","', str(soup)) else 'n/a'
        product_dict['product_page_url'] = product_url
        technical_specifications = dict([(i.select('td')[0].text.strip().lower(), i.select('td')[1].text.strip()) for i in soup.select('.woocommerce-Tabs-panel--description tr') if len(i.select('td')) == 2])
        if technical_specifications: product_dict.update({{'cooler': 'cpu cooler', 'case': 'cpu case'}.get(k, k): v for k, v in technical_specifications.items() if 'rockpack' not in k})        
        if not technical_specifications: product_dict['product_description'] = [' '.join(i.split()) for i in soup.select('.woocommerce-Tabs-panel--description')[0].find_all(text=True) if ' '.join(i.split())] if soup.select('.woocommerce-Tabs-panel--description') else []
        if product_dict: data_list.append(product_dict)
    return data_list
        

url = 'https://www.primeabgb.com/buy-online-price-india/prime-pc/'
extracted_data = extract_data(url)
print(extracted_data)
