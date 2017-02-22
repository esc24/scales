#!/usr/bin/env python

import socket
import time

from hx711 import HX711
from oled import OledDisplay
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

# Raspberry Pi pin configuration:
# HX711 pins
DATA_PIN = 9
CLOCK_PIN = 11

# MQTT
MQTT_HOSTNAME = 'netbook.local'
MQTT_TOPIC = 'restfulobs/weight'
MQTT_THRESH = 1.0  # Publish anything greather than +\- threshold


def main():
    hx = HX711(DATA_PIN, CLOCK_PIN)
    # Calibrate based on experiments with 1, 2, and 4 kg of water.
    hx.reference_unit = 21666.0

    hx.reset()
    hx.tare()

    disp = OledDisplay()

    # Set up connection to MQTT server to publish data.
    client = mqtt.Client()
    try:
	client.connect(MQTT_HOSTNAME)
    except socket.gaierror as e:
        print('Cannot connect to MQTT broker: {}'.format(e))
        client = None
    else:
        client.loop_start()  # context mgr is an option here

    # Main event loop
    while True:
        try:
            val = hx.get_weight(5)
            msg = '{:.1f} kg'.format(val)
            # Workaround to avoid negative zero
            if msg == '-0.0 kg':
                msg = '0.0 kg'
            disp.display(msg)
            #publish.single(MQTT_TOPIC, val, hostname=MQTT_HOSTNAME)
            if client is not None and abs(val) > MQTT_THRESH:
                client.publish(MQTT_TOPIC, val)
            print(val)
            hx.power_down()
            hx.power_up()
            time.sleep(0.2)
        except KeyboardInterrupt:
            disp.display('Bye...')
            time.sleep(1)
            disp.clear()
            break


if __name__ == '__main__':
    main()
