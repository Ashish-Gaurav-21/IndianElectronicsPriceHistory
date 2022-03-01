import requests, json, re
from bs4 import BeautifulSoup


def get_soup(url):
    
    '''Return soup object for the url provided'''
    response = requests.get(url)
    response_code, soup = response.status_code, BeautifulSoup(response.text, features='lxml')
    return soup

def extract_data(url):
    
    ''''''
    product_urls, data_list = ['https://golchhait.com' + i.select('.product-card')[0].get('href', 'n/a') for i in get_soup(url).select('.main-content .grid__item') if i.select('.product-card')], []
    for product_url in product_urls:
        soup = get_soup(product_url)
        product_dict = {}
        product_dict['product_id'] = re.search('"productId":(.*?),"', str(soup)).group(1) if re.search('"productId":(.*?),"', str(soup)) else 'n/a'
        product_dict['regular_price'] = soup.select('.product-single__price')[0].text.strip() if soup.select('.product-single__price') else 'n/a'
        product_dict['stock_status'] = soup.find('link', {'itemprop': 'availability'}).get('href', 'n/a') if soup.find('link', {'itemprop': 'availability'}) else 'n/a'
        product_dict['product_page_url'] = product_url
        technical_specifications = dict([(i.select('td')[0].text.strip().lower(), i.select('td')[1].text.strip()) for i in soup.select('tbody tr') if len(i.select('td')) == 2])
        if not technical_specifications: technical_specifications = dict([(i.select('th')[0].text.strip().lower(), i.select('td')[0].text.strip()) for i in soup.select('.a-keyvalue.prodDetTable tr') if i.select('th') and i.select('td')])
        if technical_specifications: product_dict.update({{'cooler': 'cpu cooler', 'case': 'cpu case'}.get(k, k): v for k, v in technical_specifications.items() if 'rockpack' not in k})        
        if product_dict: data_list.append(product_dict)
    return data_list
        

url = 'https://golchhait.com/collections/gaming-pc'
# url = 'https://golchhait.com/collections/ai-3d-rendering'
# url = 'https://golchhait.com/collections/streaming-pc'
extracted_data = extract_data(url)
print(extracted_data)
