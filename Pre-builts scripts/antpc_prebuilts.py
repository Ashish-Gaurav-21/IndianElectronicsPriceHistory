import requests, json, re
from bs4 import BeautifulSoup


def get_soup(url):
    
    '''Return soup object for the url provided'''
    response = requests.get(url)
    response_code, soup = response.status_code, BeautifulSoup(response.text, features='lxml')
    return soup

def extract_data(url):
    
    ''''''
    product_urls, data_list = [i.select('a')[0].get('href', 'n/a') for i in get_soup(url).select('.container .element') if i.select('a')], []
    for product_url in product_urls:
        soup = get_soup(product_url)
        product_dict = {}
        product_dict['product_id'] = re.search(r'"productID":"(.*?)",', str(soup)).group(1) if re.search(r'"productID":"(.*?)",', str(soup)) else 'n/a'
        product_dict['regular_price'] = soup.select('.gtotPrices')[0].text.strip() if soup.select('.gtotPrices') else 'n/a'
        product_dict['product_page_url'] = product_url
        technical_specifications = dict([(i.select('.s-heading')[0].text.strip().lower(), i.select('p')[0].text.strip()) for i in soup.select('.row.spe-list div.col-sm-3') if (i.select('.s-heading')) and (i.select('p'))])
        if technical_specifications: product_dict.update({{'cooler': 'cpu cooler', 'case': 'cpu case'}.get(k, k): v for k, v in technical_specifications.items() if 'rockpack' not in k})        
        if product_dict: data_list.append(product_dict)
    return data_list
        

url = 'https://www.ant-pc.com/gaming-pc/dorylus'
# url = 'https://www.ant-pc.com/gaming-pc/pharaoh'
# url = 'https://www.ant-pc.com/gaming-pc/solenopsis'
# url = 'https://www.ant-pc.com/gaming-pc/metallica'
extracted_data = extract_data(url)
print(extracted_data)

