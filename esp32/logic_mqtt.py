import ujson
import utility
from logic_database import database, StoreKey
from umqtt.simple import MQTTClient
from machine import Timer

if "Client" not in dir():
    GateName = None
    CLIENT_ID = None
    SERVICE_IP = None
    PublishDict = {}
    SubscribeDict = {}

    Client = None
    UI_Logic = lambda : 1

    MQTT_Timer = Timer(-1)


def update_info():
    global GateName
    global CLIENT_ID
    global SERVICE_IP
    global PublishDict
    global SubscribeDict

    GateName = database.get(StoreKey.device_name)
    CLIENT_ID = "client/" + GateName
    SERVICE_IP = database.get(StoreKey.service_ip)

    PublishDict = {
        "gate_name": GateName,
    }

    SubscribeDict = {
        "doors_that_open": [],
        "password": "",
    }

def mqtt_publish():
    print("publish:", PublishDict)
    for key, value in PublishDict.items():
        Client.publish(utility.encode(key), utility.encode(value))

def mqtt_subscribe():
    print("subscribe:", SubscribeDict)
    for topic in SubscribeDict.keys():
        topic = utility.encode(topic)
        Client.subscribe(topic)

def mqtt_callback(topic, msg):
    global SubscribeDict

    print("subscribe_callback:", SubscribeDict)

    topic = utility.decode(topic)
    msg = utility.decode(msg)
    if (topic == "password"):
        SubscribeDict["password"] = msg
    if (topic == "doors_that_open"):
        SubscribeDict["doors_that_open"] = ujson.loads(msg)

    print('---------')
    print("topic:", topic)
    print("msg:", msg)

def mqtt_timer_callback(timer):
    print("------------------")
    try:
        Client.check_msg()
    except Exception as e:
        print(e)
        Client.sock.close()
        Client.connect()
        mqtt_subscribe()
        utility.sleep(0.5)
        mqtt_publish()
    UI_Logic()

def mqtt_connect():
    global Client
    global MQTT_Timer

    Client = MQTTClient(CLIENT_ID, SERVICE_IP)
    Client.set_callback(mqtt_callback)

    while 1:
        try:
            Client.connect(clean_session=True)
            break
        except Exception as e:
            print(e)
            if "sock" in dir(Client):
                Client.sock.close()
            utility.sleep(1)

    mqtt_subscribe()
    utility.sleep(1)
    mqtt_publish()

    MQTT_Timer.init(mode=Timer.PERIODIC, period=1000, callback=mqtt_timer_callback)
    print("start to listeing...")

def restart_mqtt_timer(delay:int):
    global MQTT_Timer
    MQTT_Timer.deinit()
    utility.sleep(delay)
    MQTT_Timer.init(mode=Timer.PERIODIC, period=1000, callback=mqtt_timer_callback)

if __name__ == "__main__":
    import logic_main
    status = utility.is_port_open(database.get("service_ip"), 1883)
    print(status)
