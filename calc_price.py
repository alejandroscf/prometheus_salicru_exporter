#!/usr/bin/python3
import datetime
import requests
import os

omie_base_url = "https://www.omie.es/es/file-download?parents%5B0%5D=marginalpdbc&filename="
omie_file_prefix = "marginalpdbc_" 
omie_file_sufix = ".1" 
omie_file_2nd_sufix = ".2" 

dir_path = os.path.dirname(os.path.realpath(__file__))

sobrecoste_desvios = 0.00131
#Se deberia descargar de esios liquicomun pero no parece estar a priori, media aproximada
sobrecoste_banda_secundaria = 0.0025
sobrecoste_factor_potencia = 0
sobrecoste_coste_os = 0.00016
sobrecoste_bono_social = 0.00147
#factor_chanchullo = 0.0025
factor_chanchullo = 0.0
sobrecoste = sobrecoste_desvios + sobrecoste_banda_secundaria + sobrecoste_factor_potencia + sobrecoste_coste_os + sobrecoste_bono_social + factor_chanchullo

def get_omie_data(sufix=omie_file_sufix):

    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")

    omie_file = omie_file_prefix + tomorrow + sufix

    omie_url = omie_base_url + omie_file

    r = requests.get(omie_url)
    if (r.status_code != 200):
        print('Get failed')
        print(r.status_code)
        print('Waiting a bit')
        time.sleep(5+random.random()*5)
        r = requests.get(omie_url)

    if (r.status_code == 200):
        print("fetch OK!")
        prices = {} 
        #print(r.text)
        for line in r.text.split('\r\n'):
            #print(line)
            data = line.split(';')
            if not (data[0].strip() in ['MARGINALPDBC', '*', '']):
                #print(data)
                date = str(int(data[3])-1) + ':00' + ' ' + data[0] + '-' + data[1] + '-' + data[2]
                prices[date] =  float(data[5])/1000

        if len(prices) == 0 and sufix == omie_file_sufix:
            return get_omie_data(sufix=omie_file_2nd_sufix)
            
        return prices
    else:
        return None

def procces_data(omie_data):
    proc_data = {}
    for key, value in omie_data.items():
        proc_data[key] = omie_data[key] - sobrecoste
    return proc_data

def program_inverter(proc_data, threshold=0.0025):
    zero_inyection = False
    for hour, price in proc_data.items():
        new_zero_inyection = price < threshold
        
        print(hour + " " + str(price) + " " + str(int(new_zero_inyection)))
        if zero_inyection != new_zero_inyection:
            set_zero_inyection(new_zero_inyection, hour)
            zero_inyection = new_zero_inyection


def set_zero_inyection(status, hour):
    if status:
        command = "echo '" + dir_path + "/main.py --enable-zero-injection'|at " + hour
    else:
        command = "echo '" + dir_path + "/main.py --disable-zero-injection'|at " + hour 
    print(command)
    os.system(command)

omie_data = get_omie_data()
print(omie_data)
proc_data = procces_data(omie_data)
#print(proc_data)
program_inverter(proc_data)
