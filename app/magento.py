import requests
# from config import Config
from app import app

# app.config.from_object(Config)
headers = {"Authorization": "Bearer " + app.config['MAGENTO_TOKEN']}

def get_mage_orders():
    r = requests.get(app.config['MAGENTO_REST_URL'] + '/' + 
                    app.config['MAGENTO_STORE'] + '/' +
                    'V1/orders/items?searchCriteria=all',
                    headers=headers
                    )
    return r.json()

def get_mage_orders_with_name_filter(mage_product_name):
    r = requests.get(app.config['MAGENTO_REST_URL'] + '/' + 
                    app.config['MAGENTO_STORE'] + '/' +
                    'V1/orders/items?' +
                    'searchCriteria[filter_groups][0][filters][0][field]=name&' +
                    'searchCriteria[filter_groups][0][filters][0][value]=%25' + mage_product_name + '%25&' +
                    'searchCriteria[filter_groups][0][filters][0][condition_type]=like',
                    headers=headers
                    )
    return r.json()

def mage_get_all_order_ids(orders_json):
    '''
    Return a list with just the orders information you need
    '''
    order_id_list = []

    for order_item in orders_json["items"]:
        order_id = order_item["order_id"]
        print(order_id)
        order_id_list.append(order_item["order_id"])

    # remove duplicate
    order_id_list = list(dict.fromkeys(order_id_list))

    return order_id_list