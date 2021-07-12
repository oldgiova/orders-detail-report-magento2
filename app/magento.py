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
                    'searchCriteria[filter_groups][0][filters][0][condition_type]=like&' +
                    'searchCriteria[filter_groups][1][filters][0][field]=product_type&' +
                    'searchCriteria[filter_groups][1][filters][0][value]=virtual&' +
                    'searchCriteria[filter_groups][1][filters][0][condition_type]=eq&' +
                    'searchCriteria[filter_groups][2][filters][0][field]=product_id&' +
                    'searchCriteria[filter_groups][2][filters][0][value]=102&' +
                    'searchCriteria[filter_groups][2][filters][0][condition_type]=neq&' +
                    'searchCriteria[filter_groups][3][filters][0][field]=product_id&' +
                    'searchCriteria[filter_groups][3][filters][0][value]=103&' +
                    'searchCriteria[filter_groups][3][filters][0][condition_type]=neq&' +
                    'searchCriteria[filter_groups][4][filters][0][field]=product_id&' +
                    'searchCriteria[filter_groups][4][filters][0][value]=104&' +
                    'searchCriteria[filter_groups][4][filters][0][condition_type]=neq',
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

def mage_get_details_from_single_order(order_id):
    '''
    Return all details from single magento order
    '''
    r = requests.get(app.config['MAGENTO_REST_URL'] + '/' + 
                    app.config['MAGENTO_STORE'] + '/' +
                    'V1/orders/' + str(order_id),
                    headers=headers
                    )
    return r.json()

def mage_return_order_important_details_only(order_details):
    '''
    Takes in input a json with all order details
    and return a list with just the details you need
    '''
    # if order is canceled then do nothing
    if order_details["status"] == "canceled":
        return None
    order_details_dict = {}
    order_details_dict["email"] = order_details["customer_email"]
    order_details_dict["creazione"] = order_details["created_at"]
    order_details_dict["nome"] = order_details["billing_address"]["firstname"]
    order_details_dict["cognome"] = order_details["billing_address"]["lastname"]
    order_details_dict["tel"] = order_details["billing_address"]["telephone"]
    order_details_dict["increment_id"] = order_details["increment_id"]
    for detail in order_details["items"]:
        if detail["product_type"] == "virtual":
            order_details_dict["prenotazione"] = detail["sku"]
            order_details_dict["data"], order_details_dict["ora"] = detail["sku"].split('-') # Coperto cena Venerdi 11-21:00
            order_details_dict["data"] = order_details_dict["data"][-2:] # 11
            order_details_dict["quantita"] = detail["qty_ordered"]
    return order_details_dict

def mage_return_order_important_details_only_bambu(order_details):
    '''
    Takes in input a json with all order details
    and return a list with just the details you need
    '''
    # if order is canceled then do nothing
    if order_details["status"] == "canceled":
        return None
    order_details_dict = {}
    order_details_dict["email"] = order_details["customer_email"]
    order_details_dict["creazione"] = order_details["created_at"]
    order_details_dict["nome"] = order_details["billing_address"]["firstname"]
    order_details_dict["cognome"] = order_details["billing_address"]["lastname"]
    order_details_dict["tel"] = order_details["billing_address"]["telephone"]
    order_details_dict["increment_id"] = order_details["increment_id"]
    for detail in order_details["items"]:
        if detail["product_type"] == "virtual":
            order_details_dict["prenotazione"] = detail["sku"]
            order_details_dict["data"] = detail["sku"].split(' ')[1] + detail["sku"].split(' ')[2] #['Coperto', '26', 'Giugno', 'Menu', 'Emiliano']
            order_details_dict["ora"] = "20:00"
            order_details_dict["quantita"] = detail["qty_ordered"]
    return order_details_dict


def mage_group_all_order_details_important(order_id_list):
    mage_final_details_list = []
    for order_id in order_id_list:
        json_all_detail_single_order = mage_get_details_from_single_order(order_id)
        #single_order_important_details_only = mage_return_order_important_details_only(json_all_detail_single_order)
        single_order_important_details_only = mage_return_order_important_details_only_bambu(json_all_detail_single_order)
        if single_order_important_details_only is not None:
            mage_final_details_list.append(single_order_important_details_only)

    return mage_final_details_list


def mage_get_salable_quantity():
    all_skus = mage_get_all_skus()
    mage_final_salable_list = []
    for sku in all_skus["items"]:
        sku_salable_dict = {}
        sku_salable_dict["sku"] = sku["sku"]
        sku_salable_dict["salable_qty"] = mage_get_this_product_salable_qty(sku["sku"])
        mage_final_salable_list.append(sku_salable_dict)
    return mage_final_salable_list



def mage_get_all_skus():
    r = requests.get(app.config['MAGENTO_REST_URL'] + '/' + 
                    app.config['MAGENTO_STORE'] + '/' +
                    'V1/products?' +
                    'fields=items[sku,name,id]&' +
                    'searchCriteria[filter_groups][0][filters][0][field]=sku&' +
                    'searchCriteria[filter_groups][0][filters][0][value]=%25Menu%25&' +
                    'searchCriteria[filter_groups][0][filters][0][condition_type]=like&' +
                    'searchCriteria[filter_groups][1][filters][0][field]=type_id&' +
                    'searchCriteria[filter_groups][1][filters][0][value]=virtual&' +
                    'searchCriteria[filter_groups][1][filters][0][condition_type]=eq&' +
                    'searchCriteria[filter_groups][2][filters][0][field]=status&' +
                    'searchCriteria[filter_groups][2][filters][0][value]=1&' +
                    'searchCriteria[filter_groups][2][filters][0][condition_type]=eq',
                    headers=headers
                    )
    return r.json()

def mage_get_this_product_salable_qty(sku):
    r = requests.get(app.config['MAGENTO_REST_URL'] + '/' + 
                    app.config['MAGENTO_STORE'] + '/' +
                    'V1/inventory/get-product-salable-quantity/' +
                    sku.replace(' ', '%20') +
                    '/1', #the default stockid
                    headers=headers
                    )
    return r.text

    

        
    
