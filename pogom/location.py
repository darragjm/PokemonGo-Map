from pyicloud import PyiCloudService


def get_iphone_location(username, password, device_id):
    api = PyiCloudService(username, password)

    location = api.devices[device_id].location()

    return location['latitude'], location['longitude'], 0
