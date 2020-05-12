import argparse
import paho.mqtt.client as mqtt
import serial

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

args = parser.parse_args()
serial_port = serial.Serial(args.port, args.baud)

client_id = str(1)
topic = '/dev/{}/sensor_data'.format(client_id)
client = mqtt.Client(client_id=client_id)
client.username_pw_set('ayoti', password='test')
client.connect('localhost')

while(True):
    sensor_data = serial_port.readline()
    sensor_data = sensor_data.decode('ascii')
    msg = str({
        'temp': sensor_data.split()[1],
        'co2': sensor_data.split()[3]  
    })
    print(msg, topic)

    client.publish(topic, msg)
