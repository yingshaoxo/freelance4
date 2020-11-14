import paho.mqtt.client as mqtt

def get_gateway_ip():
    import netifaces
    ip =  netifaces.gateways()['default'][netifaces.AF_INET][0]
    print(ip)
    return ip

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("password")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(client_id="client/c")
client.on_connect = on_connect
client.on_message = on_message

client.connect(get_gateway_ip(), 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
