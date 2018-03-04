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
(Code removed, see updated source at: https://github.com/jimoconnell/GoogleSpeak/blob/master/google_speak_mqtt.py )
```

To fire it from the command line, install the 'mosquitto-clients' package and run:
```

mosquitto_pub -h test.mosquitto.org -t "jimoconnell/googlesay/foo" -m "Hokey Smokes! It worked\!"   

```

