import requests, re
from bs4 import BeautifulSoup


pagination_url = 'https://mdcomputers.in/graphics-card'
pagination_url = 'https://mdcomputers.in/processor'
response = requests.get(pagination_url)
response_code = response.status_code
soup = BeautifulSoup(response.text)
result_count = (re.search('of (.*?) \(', soup.select('.product-filter.product-filter-bottom.filters-panel')[0].text).group(1) if re.search('of (.*?) \(', str(soup)) else 'n/a') if soup.select('.product-filter.product-filter-bottom.filters-panel') else 'n/a'
num_pages = (re.search('\((.*?) Pages\)', soup.select('.product-filter.product-filter-bottom.filters-panel')[0].text).group(1) if re.search('\((.*?) Pages\)', str(soup)) else 'n/a') if soup.select('.product-filter.product-filter-bottom.filters-panel') else 'n/a'
data_list = []
for page in range(1, int(num_pages)+1): # need to add assert statement here to check if num_pages is int or not # brand is also required # has model_no too in product_url, check that
    for product in soup.select('.product-item-container'):
        product_dict = {}
        product_dict['product_id'] = product.select('.quickview.iframe-link.visible-lg.btn-button')[0].get('href', 'n/a').split('product_id=')[-1] if product.select('.quickview.iframe-link.visible-lg.btn-button') else 'n/a'
        product_dict['product_page_url'] = product.select('h4 a')[0].get('href', 'n/a') if product.select('h4 a') else 'n/a'
        product_dict['product_name'] = ' '.join(product.select('h4 a')[0].text.split()) if product.select('h4 a') else 'n/a'
        product_dict['review_count'] = re.sub('[^0-9]+', '', product.select('.rating-num')[0].text) if product.select('.rating-num') else 'n/a'
        product_dict['average_rating'] = sum([float(re.search('fa-stack-(.*?)x"', str(i).replace('<i class="fa fa-star-o fa-stack-1x"></i></span>', '').replace('<span class="fa fa-stack">', '')).group(1)) for i in product.select('.rating-box span') if re.search('fa-stack-(.*?)x"', str(i).replace('<i class="fa fa-star-o fa-stack-1x"></i></span>', '').replace('<span class="fa fa-stack">', ''))])
        product_dict['regular_price'] = ' '.join(product.select('.price .price-old')[0].text.split()) if product.select('.price .price-old') else 'n/a'
        product_dict['markdown_price'] = ' '.join(product.select('.price .price-new')[0].text.split()) if product.select('.price .price-new') else 'n/a'
        if product_dict['regular_price'] == 'n/a': product_dict['regular_price'], product_dict['markdown_price'] = product_dict['markdown_price'], product_dict['regular_price']
        if product_dict['product_id'] != 'n/a': data_list.append(product_dict)
    soup = BeautifulSoup(requests.get(pagination_url + '?page=' + str(page + 1)).text)
print (data_list)