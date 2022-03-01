import requests, re, json
from bs4 import BeautifulSoup
from math import ceil


def get_soup(pagination_url, page_num=1):
    
    '''Get soup object for the Product listing url. Default page number of 1 will be used. Site displays maximum of 100 products on a single page.'''
    if page_num == 1:
        response = requests.get(pagination_url)
        response_code, soup = response.status_code, BeautifulSoup(response.text)
    else:
        response = requests.get('https://www.pcstudio.in/wp-admin/admin-ajax.php?action=jet_smart_filters&provider=woocommerce-archive%2Fdefault&defaults%5Bpost_status%5D=publish&defaults%5Bwc_query%5D=product_query&defaults%5Borderby%5D=meta_value_num&defaults%5Border%5D=ASC&defaults%5Bpaged%5D=0&defaults%5Bposts_per_page%5D=30&defaults%5Bjet_smart_filters%5D=woocommerce-archive&defaults%5Btaxonomy%5D=product_cat&defaults%5Bterm%5D=' + pagination_url.strip('/').split('/')[-1].strip() + '&defaults%5Bmeta_key%5D=_price&settings%5Bswitcher_enable%5D=false&settings%5Bmain_layout_switcher_label%5D=Main&settings%5Bsecondary_layout_switcher_label%5D=Secondary&settings%5Barchive_item_layout%5D=47455&settings%5B_el_widget_id%5D=287dab3&paged=' + str(page_num))
        response_code, soup = response.status_code, BeautifulSoup(json.loads(response.text).get('content', 'n/a'))
    return soup


def extract_data(pagination_url):
    
    '''Extract the data of product present in listing page. product_id, model_no, product_name, brand, price, url, stock status, review and rating info.'''
    soup = get_soup(pagination_url)
    result_count = (re.search('all (.*?) results', soup.select('.woocommerce-result-count')[0].text, flags=re.IGNORECASE).group(1) if re.search('all (.*?) results', str(soup), flags=re.IGNORECASE) else (re.search('of (.*?) results', str(soup), flags=re.IGNORECASE).group(1) if re.search('of (.*?) results', str(soup), flags=re.IGNORECASE) else 'n/a')) if soup.select('.woocommerce-result-count') else 'n/a'
    num_pages = int(ceil(int(result_count) / 30)) if result_count != 'n/a' else 'n/a'
    data_list = []
    for current_page in range(1, int(num_pages) + 1):
        for product in soup.select('li.jet-woo-builder-product'):
            product_dict = {}
            product_dict['product_id'] = product.select('.elementor-jet-woo-builder-archive-add-to-cart a')[0].get('data-product_id', 'n/a') if product.select('.elementor-jet-woo-builder-archive-add-to-cart a') else 'n/a'
            product_dict['model_no'] = product.select('.elementor-jet-woo-builder-archive-add-to-cart a')[0].get('data-product_sku', 'n/a') if product.select('.elementor-jet-woo-builder-archive-add-to-cart a') else 'n/a'
            product_dict['product_page_url'] = product.select('h3 a')[0].get('href', 'n/a') if product.select('h3 a') else 'n/a'
            product_dict['product_name'] = product.select('.elementor-jet-woo-builder-archive-add-to-cart a')[0].get('aria-label', 'n/a') if product.select('.elementor-jet-woo-builder-archive-add-to-cart a') else 'n/a'
            if re.search(r'“(.*)”', product_dict['product_name']): product_dict['product_name'] = ' '.join(re.search(r'“(.*)”', product_dict['product_name']).group(1).split())
            if product.select('div.jet-woo-product-price del'): product_dict['regular_price'], product_dict['markdown_price'] = ' '.join(product.select('div.jet-woo-product-price del')[0].text.split()), ' '.join(product.select('div.jet-woo-product-price ins')[0].text.split())  
            elif product.select('div.jet-woo-product-price span.woocommerce-Price-amount.amount'): product_dict['regular_price'] = ' '.join(product.select('div.jet-woo-product-price span.woocommerce-Price-amount.amount')[0].text.split())
            product_dict['stock_status'], product_dict['brand'] = [i for i in product.get('class', ['n/a']) if 'stock' in i.lower()], [i for i in product.get('class', ['n/a']) if 'brand' in i.lower()]
            if isinstance(product_dict['stock_status'], list) and len(product_dict['stock_status']) > 0: product_dict['stock_status'] = product_dict['stock_status'][0].replace('instock', 'In Stock').replace('outofstock', 'Out of Stock')
            if isinstance(product_dict['brand'], list) and len(product_dict['brand']) > 0: product_dict['brand'] = product_dict['brand'][0].replace('product_cat-brand-', '').replace('product_cat-', '').replace('product_tag-brand-', '')
            if product_dict['product_id'] != 'n/a': data_list.append(product_dict)
        soup = get_soup(pagination_url, str(current_page + 1))
    return data_list


# pagination_url = 'https://www.pcstudio.in/product-category/gaming-chairs/'
# pagination_url = 'https://www.pcstudio.in/product-category/processor/'
pagination_url = 'https://www.pcstudio.in/product-category/graphics-card/'
extracted_data = extract_data(pagination_url)
print(extracted_data)
print(len(extracted_data))