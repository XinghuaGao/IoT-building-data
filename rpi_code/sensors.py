
import Adafruit_DHT
import time
import datetime
import RPi.GPIO as GPIO
import threading
from mq import *

# Constants
DHT_PIN = 4
LIGHT_PIN = 19
SOUND_CHANNEL = 17
VIBRATION_CHANNEL = 16
PIR_PIN = 23
FLAME_CHANNEL = 12

# Initialize sensors
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_PIN, GPIO.IN)
GPIO.setup(SOUND_CHANNEL, GPIO.IN)
GPIO.setup(VIBRATION_CHANNEL, GPIO.IN)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(FLAME_CHANNEL, GPIO.IN)

dht_sensor = Adafruit_DHT.DHT11
sound_beat = 0
vibration_beat = 0
motion_beat = 0
flame_beat = 0
mq2 = None

# Sensor Callbacks
def sound_callback(sound_channel):
    global sound_beat
    sound_beat += 1

def vibration_callback(vibration_channel):
    global vibration_beat
    vibration_beat += 1

def flame_callback(flame_channel):
    global flame_beat
    flame_beat += 1

# Sensor Reading Start Functions
def start_reading(channel, callback):
    GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
    GPIO.add_event_callback(channel, callback)

def start_sound_reading():
    start_reading(SOUND_CHANNEL, sound_callback)

def start_vibration_reading():
    start_reading(VIBRATION_CHANNEL, vibration_callback)

def start_flame_reading():
    start_reading(FLAME_CHANNEL, flame_callback)

def start_mq2_reading():
    global mq2
    mq2 = MQ()

# Sensor Data Fetch Functions
def get_sensor_data(channel, beat):
    data = beat
    beat = 0
    return data

def get_temperature_humidity():
    while True:
        humidity, temperature = Adafruit_DHT.read(dht_sensor, DHT_PIN)
        if humidity is not None and temperature is not None:
            return temperature, humidity

def get_light():
    return GPIO.input(LIGHT_PIN)

def get_sound():
    return get_sensor_data(SOUND_CHANNEL, sound_beat)

def get_vibration():
    return get_sensor_data(VIBRATION_CHANNEL, vibration_beat)

def get_flame():
    return get_sensor_data(FLAME_CHANNEL, flame_beat)

def get_mq2_reading():
    global mq2
    reading = mq2.MQPercentage()
    return reading["SMOKE"], reading["CO"], reading["GAS_LPG"]

# Helper Functions
def get_date_time():
    date_time = str(datetime.datetime.now())
    return date_time

def get_id(rpi_id, room_id, date_time):
    row_id = date_time + "_" + rpi_id + "_" + room_id
    return row_id

def get_reading(rpi_id, room_id):
    date_time = get_date_time()
    row = dict()
    row['id'] = get_id(rpi_id, room_id, date_time)
    row['date_time'] = date_time
    row['rpi_id'] = rpi_id
    row['room_id'] = room_id
    row['temp'], row['humidity'] = get_temperature_humidity()
    row['light'] = get_light()
    row['sound'] = get_sound()
    row['flame'] = get_flame()
    row['vibration'] = get_vibration()
    row['motion'] = get_motion()
    row['smoke'], row['co'], row['lpg'] = get_mq2_reading()
    
    return row
