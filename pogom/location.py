import json
from pyicloud import PyiCloudService

with open('credentials.json') as file:
    credentials = json.load(file)

IPHONE_ID = credentials['iphone_dev_id']


def getiPhoneLocation():
    username, password = credentials['icloud_account']['username'], credentials['icloud_account']['password']
    api = PyiCloudService(username, password)

    location = api.devices[IPHONE_ID].location()

    return "%s,%s" % (location['latitude'], location['longitude'])
