# Make Your *Google Home* Speak

This document outlines how to have your Google Home or other Google Cast device speak a string, using [IFTTT](https://ifttt.com/), CURL, MQTT, or Python.

Like a well-behaved child, your [Google Home](https://store.google.com/product/google_home) speaks only when spoken to. 
This is the preferred way to have it behave for most people, but if you're like me, you want to push its capabilities and have it do things for which it was not designed. 

Perhaps you want to have Google announce something like: ***“The temperature upstairs has reached 90 degrees Fahrenheit!” **or perhaps** “Someone just placed an order for $53.99 on your e-commerce store!”***
Sadly, this functionality is not available out of the box with the Google Home, even when you add in IFTTT.

It *is* possible to have your Google Home speak, but it takes a bit of work, as well some kind of home server, such as a Raspberry Pi, Linux box, or Windows or Mac.  (It needs to be on the same network as your Google Home, so using a cloud server won't work.)  To make this work with IFTTT, the server will need to be accessible from the Internet.

It relies upon [Home Assistant, ](https://home-assistant.io/)the excellent home automation platform that will run on as little as a [$10 Raspberry Pi Zero](https://home-assistant.io/blog/2017/05/01/home-assistant-on-raspberry-pi-zero-in-30-minutes/).  (Installing Home Assistant is outside the scope of this document and well-documented [elsewhere](https://home-assistant.io/blog/2017/05/01/home-assistant-on-raspberry-pi-zero-in-30-minutes/).)

In your configuration.yaml file, you enable the following:

`media_player: 
 - platform: cast 
tts: 
 - platform: google `

(The Media Player component will discover any Google Homes on your network.  “TTS” is text-to-speech.)

Home Assistant also has a RESTful API.  We will use this to do the heavy lifting.

## Via IFTTT:

*Note:*
*To use IFTTT, you must have a publicly-accessible URL for Home Assistant.*
 
Create your trigger, the “If THIS” condition that you want to listen for. 
For 

```
[http://YOUR_HOMEASSISTANT:8123/api/services/tts/google_say?api_password=YOUR_PASSWORD](http://your_homeassistant:8123/api/services/tts/google_say?api_password=YOUR_PASSWORD)
```

```
POST
```

```
Application/JSON
```

```
{"entity_id": "media_player.studio_speaker", "message": "Hello World!"}
```

## Via Python

```
import requests

#N.B.: Escape the quotes in your JSON with slashes: \"
data = "{\"entity_id\": \"media_player.studio_speaker\", \"message\": \"Hello World!\"}"

r = requests.post("http://your_homeassistant:8123/api/services/tts/google_say?api_password=YOUR_PASSWORD", data)

print(r.text) #TEXT/HTML
print(r.status_code, r.reason) #HTTP
```

## Via CURL

```

curl --request POST \
  --url 'http://your_homeassistant:8123/api/services/tts/google_say?api_password=YOUR_PASSWORD' \
  --header 'Content-Type: application/x-www-form-urlencoded' 
  --form 'data={"entity_id": "media_player.studio_speaker", "message": "Hello World!" }'
  
```

## Via MQTT

It occurred to me that it might be useful to have MQTT as a very flexible and dynamic way to send commands to your Google Homes and Cast devices.  I grabbed a sample Python/PAHO script and tweaked it a little to listen to a custom channel and send any message received to Home Assistant to be announced via Google TTS.

This method would also make it trivial to send messages to an unlimited number of Home Assistant installs, in different locations, on different networks.

Save the following code as a script, use pip to install pahoo-mqtt and requests:

```
sudo pip install paho-mqtt requests
```

The script will keep running until you close the session, kill it, or it encounters an error. (Accented characters or other non-standard english will cause it to choke.  Fixing this is a #todo )

(See the section after the script for the mosquitto command for *sending* the message.)

```
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


```

To fire it from the command line, install the 'mosquitto-clients' package and run:
```

mosquitto_pub -h test.mosquitto.org -t "jimoconnell/googlesay/foo" -m "Hokey Smokes! It worked\!"   

```

