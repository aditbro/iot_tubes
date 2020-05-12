## How to run the simulation

### Make sure to resolve any required dependency before running

### Running communication stack
1. download and run mqtt server e.g. mosquitto and make sure it runs on port 1883
2. download prometheus server, copy the prometheus.yml and other yaml files from prometheus_config to the same folder as the prometheus binary and run it
3. download alertmanager, copy the alertmanager.yml from alertmanager_config and copy it to the same folder as alertmanager binary then run it

### Running device simulation
1. create a pair of connected COM port (might use socat for linux or vspd for windows)
2. run device/arduino_data_generator.py, use --help or -h to see the configuration option
3. run device/raspy_data_sender.py
NB: arduino and raspy baud rate must be the same

### Running application
1. run application/server_data_exporter.py