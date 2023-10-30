# Prometheus Salicru Exporter

It pulls data from the Salicru EQX-SUN API and exposes in [localhost:9887](http://localhost:9887)

Also handle Zero Injection mode automatically from OMIE prices

# Installation

```
git clone https://github.com/alejandroscf/prometheus_salicru_exporter
pip install prometheus-client
apt install at
```

# Configuration

```
cp config.py.sample config.py
vim config.py
```
You can find the plant ID in the URL of the [Salicru dashboard](https://eqx-sun.salicru.com). 

# Deployment

Run main.py

TODO: `systemd` unit file

# Automatic zero injection for Spain

File `calc_price.py` allow you to program zero injection when IDX price will be negative (you pay for injecting energy into the grid).

It takes tomorrow price from OMIE (Spanish Regulator) API, published at 13:00. Then procces it to calculate the aproximate selling price and program with `at` command to enable and disable inverter's zero injection mode.

Add a cron entry like this:
```
 15 15  *   *   *    /usr/src/prometheus_salicru_exporter/calc_price.py
```

# Sample Output

```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 383.0
python_gc_objects_collected_total{generation="1"} 0.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 51.0
python_gc_collections_total{generation="1"} 4.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="9",patchlevel="2",version="3.9.2"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 1.81628928e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.727936e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.64087232378e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0.53
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 6.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1024.0
# HELP request_processing_seconds Time spent processing request
# TYPE request_processing_seconds summary
request_processing_seconds_count 12.0
request_processing_seconds_sum 13.716022136854008
# HELP request_processing_seconds_created Time spent processing request
# TYPE request_processing_seconds_created gauge
request_processing_seconds_created 1.6408723258105247e+09
# HELP salicru_capacity Photovoltaic field power in kWp
# TYPE salicru_capacity gauge
salicru_capacity 5580.0
# HELP salicru_lastUpdated Timestamp of last update (NOT true)
# TYPE salicru_lastUpdated gauge
salicru_lastUpdated 1.64087266975e+012
# HELP salicru_lastEdit Timestamp of last modification
# TYPE salicru_lastEdit gauge
salicru_lastEdit 1.640519988058e+012
# HELP salicru_generation generation = 0
# TYPE salicru_generation gauge
salicru_generation 0.0
# HELP salicru_consumption Instant - plant - consumption in kW
# TYPE salicru_consumption gauge
salicru_consumption 0.648
# HELP salicru_selfConsumption Daily - self - consumption in kWh
# TYPE salicru_selfConsumption gauge
salicru_selfConsumption 8.19
# HELP salicru_dailyGeneration Daily - total - generation in kWh
# TYPE salicru_dailyGeneration gauge
salicru_dailyGeneration 10.28
# HELP salicru_powerDailyGeneration Instant - solar - generation in kW
# TYPE salicru_powerDailyGeneration gauge
salicru_powerDailyGeneration 1.609
# HELP salicru_dailyConsumption Daily - total - consumption (grid+solar) in kWh
# TYPE salicru_dailyConsumption gauge
salicru_dailyConsumption 16.279999999999998
# HELP salicru_powerDailyConsumption powerDailyConsumption = consumption in kW
# TYPE salicru_powerDailyConsumption gauge
salicru_powerDailyConsumption 0.648
# HELP salicru_export Daily - export - generation in kWh
# TYPE salicru_export gauge
salicru_export 2.09
# HELP salicru_import Daily - import - consumption in kWh
# TYPE salicru_import gauge
salicru_import 8.09
# HELP salicru_co2 CO2 compensation in kg
# TYPE salicru_co2 gauge
salicru_co2 4.02976
# HELP salicru_treeCompensation Tree compensation
# TYPE salicru_treeCompensation gauge
salicru_treeCompensation 0.0134668
# HELP salicru_moneySavingByGeneration moneySavingByGeneration
# TYPE salicru_moneySavingByGeneration gauge
salicru_moneySavingByGeneration 2.0147399999999998
# HELP salicru_moneySavingCompensation moneySavingCompensation
# TYPE salicru_moneySavingCompensation gauge
salicru_moneySavingCompensation 0.40337
# HELP salicru_battery battery = 0
# TYPE salicru_battery gauge
salicru_battery 0.0
# HELP salicru_gridPower Instant - grid import(+)/export(-) in kW
# TYPE salicru_gridPower gauge
salicru_gridPower -0.961
# HELP salicru_gridEnergy gridEnergy = 0
# TYPE salicru_gridEnergy gauge
salicru_gridEnergy 0.0
# HELP salicru_profit profit
# TYPE salicru_profit gauge
salicru_profit 0.0
# HELP salicru_outputPower Instant - solar - generation in kW
# TYPE salicru_outputPower gauge
salicru_outputPower 1.609
# HELP salicru_autarkicFee autarkicFee
# TYPE salicru_autarkicFee gauge
salicru_autarkicFee 0.6314496314496315
# HELP salicru_selfConsumptionPercentage selfConsumptionPercentage
# TYPE salicru_selfConsumptionPercentage gauge
salicru_selfConsumptionPercentage 0.503071253071253
# HELP salicru_isUpdated isUpdated
# TYPE salicru_isUpdated gauge
salicru_isUpdated 1.0
# HELP salicru_isAnyDeviceOutdated isAnyDeviceOutdated
# TYPE salicru_isAnyDeviceOutdated gauge
salicru_isAnyDeviceOutdated 0.0
# HELP salicru_connectStatus connectStatus
# TYPE salicru_connectStatus gauge
salicru_connectStatus 0.0
# HELP salicru_isZeroInjectionEnabled isZeroInjectionEnabled
# TYPE salicru_isZeroInjectionEnabled gauge
salicru_isZeroInjectionEnabled 0.0
# HELP salicru_isZeroInjectionApplied isZeroInjectionApplied
# TYPE salicru_isZeroInjectionApplied gauge
salicru_isZeroInjectionApplied 0.0
# HELP generated_kW Solar generation in kW
# TYPE generated_kW gauge
generated_kW 1.609
# HELP consumed_kW Plant consumption in kW
# TYPE consumed_kW gauge
consumed_kW -0.961
```

# Prometheus config

```
  - job_name: 'salicru_exporter'
    scrape_interval: "60s"
    static_configs:
      - targets: ['localhost:9887']
```

# Grafana dashboard

You can find the json source for a Grafana dasboard in [grafana.json](/grafana.json)

