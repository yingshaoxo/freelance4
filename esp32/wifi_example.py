import network
from time import sleep
from umqtt.simple import MQTTClient

WIFI_SSID = "gateman"
WIFI_PASSWORD = "123456789"
SERVICE_IP = ""

def do_wifi_connect():
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
    return ifconfig

def mqtt_publish():
    # Test reception e.g. with:
    # mosquitto_sub -t foo_topic
    c = MQTTClient("umqtt_client", SERVICE_IP)
    c.connect()
    c.publish(b"foo_topic", b"hello")
    c.disconnect()

if __name__ == '__main__':
    _,_,gateway,_ = do_wifi_connect()
    SERVICE_IP = gateway
    sleep(1)
    mqtt_publish()