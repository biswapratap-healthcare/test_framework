def get_endpoints():
    with open('endpoints.conf', 'r') as f:
        endpoints = f.readlines()
        endpoints = [endpoint[:-1] for endpoint in endpoints]
        return endpoints
