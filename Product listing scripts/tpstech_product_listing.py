import requests, re, json


def get_json(url):
    
    '''Get json object for the url provided.'''
    response = requests.get(url)
    response_code, json_data = response.status_code, json.loads(response.text)
    return json_data


def get_source(url):
    
    '''Get HTML source for the url provided.'''
    response = requests.get(url)
    response_code, source = response.status_code, response.text
    return source


def extract_data(product_listing_url):
    
    '''Extract the data of product present in listing page. product_id, stock_volume, product_name, brand, model_no, barcode, price, url, stock status'''
    json_data = get_json(product_listing_url)
    result_count = len(json_data)
    data_list = []
    for product in json_data:
        brand = product.get('vendor', 'n/a')
        stock_volume_dict = dict([(str(i.get('id')), i.get('stock', 'n/a')) for i in product.get('variants')])
        product_json = get_json('https://www.tpstech.in/products/' + product.get('handle') + '.js')
        review_rating_source = get_source('https://productreviews.shopifycdn.com/proxy/v4/reviews/product?product_id=' + str(product.get('id')) + '&version=v4&shop=theperipheralstore.myshopify.com')
        review_count = re.search(r'reviewCount\\": \\"(.*?)\\",', review_rating_source).group(1) if re.search(r'reviewCount\\": \\"(.*?)\\",', review_rating_source) else 'n/a'
        average_rating = re.search(r'ratingValue\\": \\"(.*?)\\",', review_rating_source).group(1) if re.search(r'ratingValue\\": \\"(.*?)\\",', review_rating_source) else 'n/a'
        for variant in product_json.get('variants'):
            product_dict = {}
            product_dict = dict([(v, variant.get(k, 'n/a')) for k, v in {'id': 'product_id', 'name': 'product_name', 'sku': 'model_no', 'barcode': 'barcode', 'compare_at_price': 'regular_price', 'price': 'markdown_price'}.items()])
            product_dict['stock_volume'], product_dict['product_page_url'] = stock_volume_dict.get(str(product_dict['product_id']), 'n/a'), 'https://www.tpstech.in/products/' + product.get('handle') + '?variant=' + str(product_dict['product_id'])
            product_dict['brand'], product_dict['average_rating'], product_dict['review_count'] = brand, average_rating, review_count  
            product_dict['markdown_price'], product_dict['regular_price'] = product_dict['markdown_price'] * 0.01 if isinstance(product_dict['markdown_price'], int) else product_dict['markdown_price'], product_dict['regular_price'] * 0.01 if isinstance(product_dict['regular_price'], int) else product_dict['regular_price'] 
            if product_dict: data_list.append(product_dict)
    return data_list


# product_listing_url = 'https://www.tpstech.in/collections/memory?view=json'
# product_listing_url = 'https://www.tpstech.in/collections/processors?view=json'
product_listing_url = 'https://www.tpstech.in/collections/graphic-card?view=json'
extracted_data = extract_data(product_listing_url)
print(extracted_data)
print(len(extracted_data))
