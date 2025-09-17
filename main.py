from paho.mqtt.client import Client as MQTTClient
from esterownik import Esterownik
import time

mqtt = MQTTClient()
esterownik = Esterownik('192.168.1.137', 'admin', 'admin')

mqtt.connect('192.168.1.30', 1883)

mqtt.loop_start()

while True:
    status = esterownik.get_status()

    messages = {
            'mode': status.mode,
            'blower': 'ON' if status.blower_enabled else 'OFF',
            'feeder': 'ON' if status.feeder_enabled else 'OFF',
            'pump_domestic_water': 'ON' if status.pump_domestic_water_enabled else 'OFF',
            'pump_technic_water': 'ON' if status.pump_technic_water_a_enabled else 'OFF',
            'temperature/exhaust': status.temperatures.exhaust,
            'temperature/domestic_water': status.temperatures.domestic_water,
            'temperature/technic_water_input': status.temperatures.technic_water_input,
            'temperature/technic_water_output': status.temperatures.technic_water_output,
            'temperature/feeder': status.temperatures.feeder,
            'temperature/outdoor': status.temperatures.outdoor,
        }

    for topic, payload in messages.items():
        mqtt.publish(f'esterownik_test/{topic}', payload)

    time.sleep(5)

mqtt.loop_stop()

