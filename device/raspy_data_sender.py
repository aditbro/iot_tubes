import argparse
import paho.mqtt.client as mqtt
import serial
import threading

parser = argparse.ArgumentParser(
    description='Parse data from arduino via serial port'
)
parser.add_argument(
    '--port',
    help='Receiving serial port',
    required=True
)
parser.add_argument(
    '--baud',
    help='serial port baud rate',
    required=False,
    default=9600
)
parser.add_argument(
    '--id',
    help='client id',
    required=False,
    default=1
)

def subscribe_alert_topic(client, userdata, flags, rc):
    alert_topic = '/dev/{}/alert'.format(client_id)
    client.subscribe(alert_topic)

def alert(client, userdata, message):
    msg = message.payload.decode("utf-8")
    print('ALERT! ALERT! ALERT!')
    print(msg)

def alert_thread():
    client.loop_forever()

args = parser.parse_args()
client_id = str(args.id)
client = mqtt.Client(client_id=client_id)
client.username_pw_set('ayoti', password='test')
client.on_connect = subscribe_alert_topic
client.on_message = alert
client.connect('localhost')

alt_thrd = threading.Thread(target=alert_thread)
alt_thrd.start()


topic = '/dev/{}/sensor_data'.format(client_id)
serial_port = serial.Serial(args.port, args.baud)
while(True):
    sensor_data = serial_port.readline()
    sensor_data = sensor_data.decode('ascii')
    msg = str({
        'temp': sensor_data.split()[1],
        'co2': sensor_data.split()[3]  
    })

    # print(msg, topic)
    client.publish(topic, msg)
