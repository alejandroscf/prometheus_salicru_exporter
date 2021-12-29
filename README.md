# Prometheus Salicru Exporter

It pulls data from the Salicru EQX-SUN API and exposes in [localhost:9887](http://localhost:9887)

Still a WIP

# Installation

```
git clone https://github.com/alejandroscf/prometheus_salicru_exporter
pip install prometheus-client
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
process_virtual_memory_bytes 1.81522432e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.715648e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.64079678752e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0.6599999999999999
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 6.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1024.0
# HELP request_processing_seconds Time spent processing request
# TYPE request_processing_seconds summary
request_processing_seconds_count 16.0
request_processing_seconds_sum 17.604816008126363
# HELP request_processing_seconds_created Time spent processing request
# TYPE request_processing_seconds_created gauge
request_processing_seconds_created 1.6407967883901687e+09
# HELP generated_kW Solar generation in kW
# TYPE generated_kW gauge
generated_kW 1.358
# HELP consumed_kW Plant consumption in kW
# TYPE consumed_kW gauge
consumed_kW 0.399
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

