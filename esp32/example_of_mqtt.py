import network
from time import sleep
from umqtt.simple import MQTTClient
from machine import Timer

WIFI_SSID = "gateman"
WIFI_PASSWORD = "123456789"
SERVICE_IP = ""

try:
    if client:
        client.disconnect()
except Exception:
    client = None

try:
    mqtt_timer.deinit()
except Exception:
    mqtt_timer = None

def do_wifi_connect():
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
    return ifconfig

def mqtt_init():
    global client
    if client == None:
        client = MQTTClient("client/f", SERVICE_IP)
        client.connect()

def mqtt_publish():
    client.publish(b"password", b"hello")

def MQTT_Rev(tim):
    if client:
        client.check_msg()

def mqtt_callback(topic, msg):
    print("topic:", topic)
    print("msg:", msg)

def mqtt_listen(*topics):
    global client
    global mqtt_timer

    client.set_callback(mqtt_callback)

    client.connect()

    for topic in topics:
        client.subscribe(topic)

    if mqtt_timer != None:
        mqtt_timer.deinit()
    mqtt_timer = Timer(-1)
    mqtt_timer.init(period=1000, mode=Timer.PERIODIC,callback=MQTT_Rev)
    print("start to listeing...")

if __name__ == '__main__':
    _,_,gateway,_ = do_wifi_connect()
    sleep(1)
    mqtt_init()
    #mqtt_publish()
    mqtt_listen(b"password")