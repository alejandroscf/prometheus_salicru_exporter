#!/usr/bin/python3
from prometheus_client import start_http_server, Summary, Gauge
import random
import time
import requests
import config

# Credentials
login_data={"email":config.username,"password":config.password,"appVersion":"web"}

url_login='https://eqx-sun.salicru.com/api/users/login'
url_data='https://eqx-sun.salicru.com/api/plants/'+config.plant

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

#outputPower
GENERATION = Gauge('generated_kW', 'Solar generation in kW')
#gridPower
CONSUMPTION = Gauge('consumed_kW', 'Plant consumption in kW')

# Decorate function with metric.
@REQUEST_TIME.time()
def get_data(headers):
    """Get the data from salicru 'api'."""
    r = requests.get(url_data, headers=headers)
    if (r.status_code == 200):
        #print(r.json())
        print(r.json()['data']['lastUpdated'])
        print(r.json()['data']['outputPower'])
        print(r.json()['data']['gridPower'])
        GENERATION.set(float(r.json()['data']['outputPower']))
        CONSUMPTION.set(float(r.json()['data']['gridPower']))
    else:
        print('Get failed')
        if (r.status_code >= 400 and r.status_code < 500):
            print('Trying to reauth')
            time.sleep(1+random.random()*1)
            headers = login()
        else:
            print('Waiting a bit')
            time.sleep(5+random.random()*5)
        r = requests.get(url_data, headers=headers)

def login():
    """Do login and return header with auth"""
    r = requests.post(url_login, data=login_data)
    if (r.status_code == 200):
        headers = { 'Authorization': 'Bearer ' + r.json()['data']['token'] }
        return headers
    else:
        print('Auth failed')
        return None
        
if __name__ == '__main__':
    headers = login()
    while (headers == None):
        # API refresh freq = 2 min
        time.sleep(60+random.random()*5)
        headers = login()

    # Start up the server to expose the metrics.
    start_http_server(9887)

    # Get the the data
    while True:
        get_data(headers)
        time.sleep(30)
