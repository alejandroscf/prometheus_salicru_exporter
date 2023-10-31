#!/usr/bin/python3
from prometheus_client import start_http_server, Summary, Gauge, Info
import random
import time
import requests
import config
import sys
#import json

# Credentials
login_data={"email":config.username,"password":config.password,"appVersion":"web"}

#url_base='https://eqx-sun.salicru.comi/api'
#url_base='https://new-equinox.salicru.com'
url_base='https://equinox.salicru.com/api'
#url_base='http://34.160.181.48/api'

#url_login='https://eqx-sun.salicru.com/api/users/login'
#url_login='https://new-equinox.salicru.com/users/login'
url_login = url_base + '/users/login'

#url_data='https://eqx-sun.salicru.com/api/plants/'+config.plant
#url_data='https://new-equinox.salicru.com/plants/'+config.new_plant+'/realTime'
url_data = url_base + '/plants/' + config.new_plant + '/realTime'

url_config = url_base + '/plants/' + config.new_plant

glob = {}
glob['isZeroInjectionEnabled'] = None
glob['isZeroInjectionApplied'] = None

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
    'powerDailyConsumption': Gauge('salicru_powerDailyConsumption', 'Instant - load - consumption in kW'),
    'powerSelfConsumption': Gauge('salicru_powerSelfConsumption', 'powerSelfConsumption = powerDailyConsumption'),
    #'export': Gauge('salicru_export', 'Daily - export - generation in kWh'),
    'exportEnergy': Gauge('salicru_exportEnergy', 'Daily - export - generation in kWh'),
    #'import': Gauge('salicru_import', 'Daily - import - consumption in kWh'),
    'importEnergy': Gauge('salicru_importEnergy', 'Daily - import - consumption in kWh'),
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
    #print("headers")
    #print(headers)
    """Get the data from salicru 'api'."""
    #TODO catch exception when connection fail due to dns or similar
    r = requests.get(url_data, headers=headers)
    if (r.status_code != 200):
        print('Get failed')
        print(r.status_code)
        if (r.status_code >= 400 and r.status_code < 500):
            print('Trying to reauth')
            time.sleep(1+random.random()*1)
            headers['Authorization'] = login()['Authorization']
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
        for key, value in r.json().items():
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
                    if key == 'isZeroInjectionApplied':
                        glob['isZeroInjectionApplied'] = value
                    elif key == 'isZeroInjectionEnabled':
                        glob['isZeroInjectionEnabled'] = value
        #TODO get this data from another get
        #PLANT_DATA.info(metrics['plant_data'])
    else:
        print('Get failed')
        print(r.status_code)

def setZeroInjection(headers, status=False):
    """Set inverter to Zero Injection mode"""
    print('Setting Zero Injection mode to ' + str(int(status)))
    payload = { 'isZeroInjectionEnabled' : status }
    #print("Headers: ")
    #print(headers)
    headers['Content-Type'] = 'application/json'
    r = requests.patch(url_config, json=payload, headers=headers)
    if (r.status_code != 200):
        print('Patch failed')
        print(r.status_code)
        if (r.status_code >= 400 and r.status_code < 500):
            print('Trying to reauth')
            time.sleep(1+random.random()*1)
            headers['Authorization'] = login()['Authorization']
        else:
            print('Waiting a bit')
            time.sleep(5+random.random()*5)
        r = requests.patch(url_config, payload, headers=headers)

    if (r.status_code == 200):
        #print(r.json())
        print("patch OK!")
    else:
        print('Patch failed')
        print(r.status_code)

def ensureZeroInjection(headers):
    #print("iz0enable")
    #print(glob['isZeroInjectionEnabled'])
    #print("iz0applie")
    #print(glob['isZeroInjectionApplied'])
    #print("headers")
    #print(headers)
    if glob['isZeroInjectionApplied'] != glob['isZeroInjectionEnabled'] :
        print('Mode not applied')
        setZeroInjection(headers,glob['isZeroInjectionEnabled'])
    

def login():
    """Do login and return header with auth"""
    r = requests.post(url_login, json=login_data)
    if (r.status_code == 200):
        headers = { 'Authorization': 'Bearer ' + r.json()['token'] }
        print('Auth succeded')
        #print(headers)
        return headers
    else:
        print('Auth failed')
        print(r)
        return None
        
def usage():
    print("Usage: " + sys.argv[0] + "[option]")
    print("   --server                 (default) Start server to monitor")
    print("   --enable-zero-injection  Enable Zero Injection and exit")
    print("   --disable-zero-injection Disable Zero Injection and exit")
    print("   --help                   Print this help and exit")
    print()
    
if __name__ == '__main__':
    headers = login()
    while (headers == None):
        # API refresh freq = 2 min
        time.sleep(60+random.random()*5)
        headers = login()

    if len(sys.argv[1:]) > 0:
        args = sys.argv[1:]
#        match args[0]:
#            case "-s":
#                pass
#            case "--enable-zero-injection"
#                setZeroInjection(headers, status=True)
#                exit()
#            case "--disable-zero-injection"
#                setZeroInjection(headers, status=False)
#                exit()
        if args[0] == "--server":
            pass
        elif args[0] == "--enable-zero-injection":
            setZeroInjection(headers, status=True)
            exit()
        elif args[0] == "--disable-zero-injection":
            setZeroInjection(headers, status=False)
            exit()
        elif args[0] == "--help":
            usage()
            exit()
            
#    setZeroInjection(headers, status=False)
#    exit()

    # Start up the server to expose the metrics.
    start_http_server(server_port)
    print('Server started at 0.0.0.0:' + str(server_port))

    # Get the the data
    while True:
        get_data(headers)
        ensureZeroInjection(headers)
        time.sleep(30)
