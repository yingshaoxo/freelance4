import network
from time import sleep
from umqtt.simple import MQTTClient
from machine import Timer
import ujson

WIFI_SSID = "gateman"
WIFI_PASSWORD = "123456789"
SERVICE_IP = ""

GateName = "a"
CLIENT_ID = "client/" + GateName

PublishDict = {
    "gate_name": GateName,
}

SubscribeDict = {
    "doors_that_open": [],
    "password": ""
}


def free_client():
    global Client
    try:
        #Client.disconnect()
        pass
    except Exception as e:
        pass

def free_timer():
    global MQTT_Timer
    try:
        MQTT_Timer.deinit()
    except Exception as e:
        pass

free_client()
free_timer()
Client = None
MQTT_Timer = Timer(-1)

def encode(text: str):
    return text.encode("utf-8")

def decode(bytes_: bytes):
    return bytes_.decode("utf-8")

def do_wifi_connect():
    global WIFI_SSID
    global WIFI_PASSWORD
    global SERVICE_IP
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    ifconfig = sta_if.ifconfig()
    print("""network config: 
        IP address:  {}
        subnet mask: {}
        gateway: {} 
        DNS server: {}""".format(*ifconfig))
    SERVICE_IP = ifconfig[2]

def mqtt_publish():
    global PublishDict
    global Client
    for key, value in PublishDict.items():
        Client.publish(encode(key), encode(value))

def mqtt_subscribe():
    global SubscribeDict
    global Client
    for topic in SubscribeDict.keys():
        topic = encode(topic)
        Client.subscribe(topic)

def mqtt_callback(topic, msg):
    global SubscribeDict

    topic = decode(topic)
    msg = decode(msg)
    if (topic == "password"):
        SubscribeDict["password"] = msg
    if (topic == "doors_that_open"):
        SubscribeDict["doors_that_open"] = ujson.loads(msg)

    print('---------')
    print("topic:", topic)
    print("msg:", msg)

def mqtt_timer_callback(timer):
    #print("------------------")
    try:
        Client.check_msg()
    except Exception as e:
        print(e)
        Client.sock.close()
        Client.connect()
        mqtt_subscribe()
    mqtt_publish()

def mqtt_connect():
    global CLIENT_ID
    global SERVICE_IP

    global MQTT_Timer
    global Client

    Client = MQTTClient(CLIENT_ID, SERVICE_IP)
    Client.set_callback(mqtt_callback)

    while 1:
        try:
            Client.connect(clean_session=True)
            break
        except Exception as e:
            print(e)

    mqtt_subscribe()

    MQTT_Timer.init(mode=Timer.PERIODIC, period=1000, callback=mqtt_timer_callback)
    print("start to listeing...")


if __name__ == '__main__':
    do_wifi_connect()
    sleep(1)
    mqtt_connect()