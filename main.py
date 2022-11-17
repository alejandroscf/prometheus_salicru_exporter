#!/usr/bin/python3
from prometheus_client import start_http_server, Summary, Gauge, Info
import random
import time
import requests
import config

# Credentials
login_data={"email":config.username,"password":config.password,"appVersion":"web"}

url_login='https://eqx-sun.salicru.com/api/users/login'
url_data='https://eqx-sun.salicru.com/api/plants/'+config.plant

server_port=9887
#server_port=9889

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

metrics = {
    'plant_data' : {},
    'id' : 'plant_data',
    'name' : 'plant_data',
    'address' : 'plant_data',
    'latitude' : 'plant_data',
    'longitude' : 'plant_data',
    'type' : 'plant_data',
    'capacity' : Gauge('salicru_capacity', 'Photovoltaic field power in kWp'),
    'lastUpdated' : Gauge('salicru_lastUpdated', 'Timestamp of last update (NOT true)'),
    'lastEdit' : Gauge('salicru_lastEdit', 'Timestamp of last modification'),
    'generation': Gauge('salicru_generation', 'generation = 0'),
    'consumption': Gauge('salicru_consumption', 'Instant - plant - consumption in kW'),
    'selfConsumption': Gauge('salicru_selfConsumption', 'Daily - self - consumption in kWh'),
    'dailyGeneration': Gauge('salicru_dailyGeneration', 'Daily - total - generation in kWh'),
    'powerDailyGeneration': Gauge('salicru_powerDailyGeneration', 'Instant - solar - generation in kW'),
    'dailyConsumption': Gauge('salicru_dailyConsumption', 'Daily - total - consumption (grid+solar) in kWh'),
    'powerDailyConsumption': Gauge('salicru_powerDailyConsumption', 'powerDailyConsumption = consumption in kW'),
    'export': Gauge('salicru_export', 'Daily - export - generation in kWh'),
    'import': Gauge('salicru_import', 'Daily - import - consumption in kWh'),
    'co2': Gauge('salicru_co2', 'CO2 compensation in kg'),
    'treeCompensation': Gauge('salicru_treeCompensation', 'Tree compensation'),
    'moneySavingByGeneration': Gauge('salicru_moneySavingByGeneration', 'moneySavingByGeneration'),
    'moneySavingCompensation': Gauge('salicru_moneySavingCompensation', 'moneySavingCompensation'),
    'battery': Gauge('salicru_battery', 'battery = 0'),
    'gridPower': Gauge('salicru_gridPower', 'Instant - grid import(+)/export(-) in kW'),
    'gridEnergy': Gauge('salicru_gridEnergy', 'gridEnergy = 0'),
    'profit': Gauge('salicru_profit', 'profit'),
    'outputPower': Gauge('salicru_outputPower', 'Instant - solar - generation in kW'),
    'autarkicFee': Gauge('salicru_autarkicFee', 'autarkicFee'),
    'selfConsumptionPercentage': Gauge('salicru_selfConsumptionPercentage', 'selfConsumptionPercentage'),
    'isUpdated': Gauge('salicru_isUpdated', 'isUpdated'),
    'isAnyDeviceOutdated': Gauge('salicru_isAnyDeviceOutdated', 'isAnyDeviceOutdated'),
    'connectStatus': Gauge('salicru_connectStatus', 'connectStatus'),
    'isZeroInjectionEnabled': Gauge('salicru_isZeroInjectionEnabled', 'isZeroInjectionEnabled'),
    'isZeroInjectionApplied': Gauge('salicru_isZeroInjectionApplied', 'isZeroInjectionApplied'),
}
PLANT_DATA = Info('plant_data', "Plant data")
#outputPower
GENERATION = Gauge('generated_kW', 'Solar generation in kW')
#gridPower
CONSUMPTION = Gauge('consumed_kW', 'Plant consumption in kW')

# Decorate function with metric.
@REQUEST_TIME.time()
def get_data(headers):
    """Get the data from salicru 'api'."""
    #TODO catch exception when connection fail due to dns or similar
    r = requests.get(url_data, headers=headers)
    if (r.status_code != 200):
        print('Get failed')
        if (r.status_code >= 400 and r.status_code < 500):
            print('Trying to reauth')
            time.sleep(1+random.random()*1)
            headers = login()
        else:
            print('Waiting a bit')
            time.sleep(5+random.random()*5)
        r = requests.get(url_data, headers=headers)

    if (r.status_code == 200):
        #print(r.json())
        print("fetch OK!")
        #print(r.json()['data']['lastUpdated'])
        #print(r.json()['data']['outputPower'])
        #print(r.json()['data']['gridPower'])
        #GENERATION.set(float(r.json()['data']['outputPower']))
        #CONSUMPTION.set(float(r.json()['data']['gridPower']))
        for key, value in r.json()['data'].items():
            if key in metrics:
                #print((key, value))
                if (metrics[key] == 'plant_data'):
                    metrics['plant_data'][key] = value
                else: 
                    #TODO handel None values
                    if value is None:
                        print(r.json())
                    else:
                        metrics[key].set(float(value))
        PLANT_DATA.info(metrics['plant_data'])

def login():
    """Do login and return header with auth"""
    r = requests.post(url_login, data=login_data)
    if (r.status_code == 200):
        headers = { 'Authorization': 'Bearer ' + r.json()['data']['token'] }
        print('Auth succeded')
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
    start_http_server(server_port)
    print('Server started at 0.0.0.0:' + str(server_port))

    # Get the the data
    while True:
        get_data(headers)
        time.sleep(30)
