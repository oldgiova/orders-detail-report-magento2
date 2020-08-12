import requests
from orders-detail-report-magento2 import Config


Class Magento():
    headers = {"Authorization": "Bearer " + app.Config['MAGENTO_TOKEN']}

    def get_all_orders_from_magento():
        r = requests.get(app.Config['MAGENTO_REST_URL'] + '/' + 
                        app.Config['MAGENTO_STORE'] + '/' +
                        'V1/orders/items?searchCriteria=all',
                        headers=headers
                        )
        print(r.json())
        return True