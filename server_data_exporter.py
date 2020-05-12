import argparse
import json
import paho.mqtt.client as mqtt
import threading
import yaml

from flask import Flask

metrics_data = {}

def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8")
    msg = json.loads(msg.replace("'", '"'))
    topic = message.topic
    dev_id = topic.split('/')[2]
    metrics = {'temp': msg['temp'], 'co2': msg['co2']}
    metrics_data[dev_id] = metrics
    

def load_yaml(filepath):
    f_data = ''
    with open(filepath, 'r') as f:
        f_data = f.read()
    
    return yaml.load(f_data, Loader=yaml.Loader)

def load_devices_data(filepath):
    devices_data = load_yaml(filepath)
    devices = []
    for device in devices_data['devices']:
        devices.append({
            'name': device['name'],
            'sensor_topic': device['sensor_topic'],
            'alert_topic': device['alert_topic']
        })

    return devices

def init_mqtt_connection(host, port):
    client = mqtt.Client()
    client.username_pw_set('ayoti', password='test')
    client.connect('localhost', port=port)
    client.on_message = on_message
    client.on_connect = subscribe_devices_sensor_topic

    return client

def mqtt_thread(host, port):
    client = init_mqtt_connection(host, port)
    client.loop_forever()

def subscribe_devices_sensor_topic(client, userdata, flags, rc):
    devices = load_devices_data('devices.yaml')
    for device in devices:
        client.subscribe(device['sensor_topic'])

app = Flask(__name__)

@app.route('/metrics')
def show_metrics():
    temp_data = '# HELP temperature_device_data the detected temperature of the device\n'
    temp_data += '# TYPE temperature_device_data gauge\n'
    temp_data += '# UNIT temperature_device_data celsius\n'
    co2_data = '# HELP co2_device_data the detected temperature of the device\n'
    co2_data += '# TYPE co2_device_data gauge\n'
    co2_data += '# UNIT co2_device_data percent\n'
    
    for key in metrics_data:
        temp = metrics_data[key]['temp']
        co2 = metrics_data[key]['co2']

        temp_data += 'temperature_device_data_celcius{%s="%s"} %s.0\n' % ('id', key, temp)
        co2_data += 'co2_device_data_percent{%s="%s"} %s.0\n' % ('id', key, co2)

    return co2_data + temp_data

if __name__=='__main__':
    mqtt_thread = threading.Thread(target=mqtt_thread, args=('localhost', 1883))
    mqtt_thread.start()
    app.run('0.0.0.0', port=8000)