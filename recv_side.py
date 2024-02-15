import random
import time
import json
from paho.mqtt import client as mqtt_client

broker = 'splavice.io'
port = 1883
client_id = f'fire-alarm-recv-{random.randint(0, 1000)}'

flag_connected = 0
TOPIC="splavice/fire/data/#"
n=1
first={}

def do_line(topic, payload):
    id=topic.split('/')[3];
    file1=f'rcvd_data_{id}.csv'

    with open(file1, 'a') as file:
        if file1 not in first:
            first[file1]=1
            out = 'topic,temp,co2,ir,date,time,fire-score'
            file.write(out + '\n')
        j = json.loads(payload)
        print(n, j)
        out = f'''{topic},{j['temp']},{j['co2']},{j['ir']},{j['time'].split(' ')[0]},{j['time'].split(' ')[1]},{j['fire-score']}'''
        # Write the data to the file
        file.write(out + '\n')
        file.flush()  # Flush the buffer to ensure data is written ij.ediately

        # Print the data to the console (optional)
        print(id, n, out)


def on_message(client, _t, msg):
    global n
    #if topic.startswith('s2m') and '/data' not in topic and not topic.endswith('stat'):
    do_line(msg.topic, msg.payload)
    n+=1


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker", broker)
            global flag_connected
            flag_connected = 1
            if TOPIC != "":
                client.subscribe(TOPIC)
                print("subscribed to {}".format(TOPIC))
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_disconnect(client, userdata, rc):
        global flag_connected
        flag_connected = 0
        print("Disconnected from MQTT Broker!")


    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    if flag_connected == 0:
        client.connect(broker, port)
    return client

client = connect_mqtt()
client.loop_forever()

