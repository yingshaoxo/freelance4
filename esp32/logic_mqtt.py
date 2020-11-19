import utility
from logic_database import database
from umqtt.simple import MQTTClient
from machine import Timer

GateName = "a"
CLIENT_ID = "client/" + GateName

def mqtt_timer1_callback(timer):
    #print("------------------")
    try:
        Client.check_msg()
    except Exception as e:
        print(e)
        Client.sock.close()
        Client.connect()
        mqtt_subscribe()
    mqtt_publish()
    UI_Logic()

class MyMQTT():
    def __init__(self):
        self.timer1 = Timer(-1)
        self.client = None

    def _timer1_callback(self, timer):
        #print("------------------")
        try:
            self.client.check_msg()
        except Exception as e:
            print(e)
            self.client.sock.close()
            self.client.connect()
            mqtt_subscribe()
        mqtt_publish()
        UI_Logic()

    def connect(self):
        self.client = MQTTClient(CLIENT_ID, database.get("service_ip"))
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

if __name__ == "__main__":
    import logic_main
    status = utility.is_port_open(database.get("service_ip"), 1883)
    print(status)
