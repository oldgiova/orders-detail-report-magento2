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
    print(r.json())
    return r.json()