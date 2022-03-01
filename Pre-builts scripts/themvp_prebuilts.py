import requests
from bs4 import BeautifulSoup


def get_soup(url):
    
    '''Return soup object for the url provided'''
    response = requests.get(url)
    response_code, soup = response.status_code, BeautifulSoup(response.text, features='lxml')
    return soup

def extract_data(url):
    
    ''''''
    product_urls, data_list = [i.select('a')[0].get('href', 'n/a') for i in get_soup(url).select('.product_build_cat .product-thumb') if i.select('a')], []
    for product_url in product_urls:
        soup = get_soup(product_url)
        product_dict = {}
        product_dict['product_id'] = soup.find('input', {'name': 'product_id'}).get('value', 'n/a') if soup.find('input', {'name': 'product_id'}) else 'n/a'
        product_dict['regular_price'] = soup.select('.total-price')[0].find_all(text=True)[0].strip() if soup.select('.total-price') else 'n/a'
        product_dict['product_page_url'] = product_url
        technical_specifications = dict([(i.select('p')[0].text.strip().lower(), i.select('p')[1].text.strip()) for i in soup.select('ul.build-spec-list li') if len(i.select('p')) == 2])
        if technical_specifications: product_dict.update({{'cooler': 'cpu cooler', 'case': 'cpu case'}.get(k, k): v for k, v in technical_specifications.items() if 'rockpack' not in k})        
        if product_dict: data_list.append(product_dict)
    return data_list
        

url = 'https://www.themvp.in/prebuilt-research-pc/'
# url = 'https://www.themvp.in/content-creation-prebuilts'
# url = 'https://www.themvp.in/prebuilt-gaming-pc'
extracted_data = extract_data(url)
print(extracted_data)
