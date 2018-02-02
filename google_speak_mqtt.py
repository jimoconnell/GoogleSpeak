#!/usr/bin/python
# -*- coding: utf-8 -*-
# Modified by @jimoconnell to add Google Say functionality via Home Assistant
# See: https://gist.github.com/jimoconnell/35d7a23a492ca5499c71b5465c6173df
# Original:
# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber using connect_srv method.

#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import requests



def on_connect(mqttc, obj, flags, rc):
    print("Connected to %s:%s" % (mqttc._host, mqttc._port))

def on_message(mqttc, obj, msg: object):
#    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    msg.payload = msg.payload.decode("utf-8")
    print(str(msg.payload))

    saymsg = str(msg.payload)
    data = "{\"entity_id\": \"media_player.studio_speaker\", \"message\": \"" + saymsg + "\"}"
    r = requests.post("http://your_homeassistant:8123/api/services/tts/google_say?api_password=YOUR_PASSWORD", data)
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
mqttc.connect_srv("mosquitto.org", 60)
mqttc.subscribe("jimoconnell/googlesay/messages", 0)

rc = 0
while rc == 0:
    rc = mqttc.loop()

print("rc: "+str(rc))


