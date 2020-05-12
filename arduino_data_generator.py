import argparse
import random
import serial

from time import sleep


parser = argparse.ArgumentParser(
    description='Generate random temp and CO2 data to serial port'
)
parser.add_argument(
    '--co2',
    help='the mean value of generated co2 level',
    type=int,
    default=20
)
parser.add_argument(
    '--temp',
    help='the mean value of generated temp',
    type=int,
    default=30
)
parser.add_argument(
    '--port',
    help='the serial port used to send data',
    required=True
)
parser.add_argument(
    '--baud',
    help='the baud rate of the serial port',
    type=int,
    required=False,
    default=9600
)
parser.add_argument(
    '--range',
    help='the range of generated data',
    type=int,
    required=False,
    default=5
)

args = parser.parse_args()
co2_mean = args.co2
temp_mean = args.temp
gen_range = args.range
port = serial.Serial(args.port, args.baud)

def generate_random(mean, gen_range):
    min_val = mean - (gen_range//2)
    max_val = mean + (gen_range//2)
    return random.randint(min_val, max_val)

while(True):
    temp = generate_random(temp_mean, gen_range)
    co2 = generate_random(co2_mean, gen_range)
    msg = 'temp {} co2 {}\n'.format(temp, co2)
    msg = msg.encode('utf-8')

    port.write(msg)
    sleep(0.2)