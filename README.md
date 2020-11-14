# freelance4
We use flutter as the mqtt hotspot server, pyboard esp32 as clients.

It's a gate control system.

1. server can control the openness of two gates.
2. server can change the password of two gates.
3. user can open the gates if they input the right password.

## android 
### flutter
It renders a beautiful GUI.

https://flutter.dev

* wifi_iot: ^0.1.1
* provider: ^4.3.2+2
* google_nav_bar: ^3.1.0
* permission_handler: ^5.0.1+1

### Native Kotlin/Java Plugin for flutter
https://flutter.dev/docs/development/platform-integration/platform-channels

https://flutter.dev/docs/development/packages-and-plugins/developing-packages

### Go binding for android development
https://yingshaoxo.blogspot.com/2019/04/golang-for-android-development.html

### MQTT service or broker
https://yingshaoxo.blogspot.com/2020/11/what-is-mqtt.html

https://github.com/DrmagicE/gmqtt

There is indeed have more choices that you can get:
* https://github.com/eclipse/paho.mqtt.golang
* https://github.com/fhmq/hmq
* https://github.com/goiiot/libmqtt
* https://github.com/alsm/hrotti

### Dart backgound process or threading
https://stackoverflow.com/questions/46505528/how-to-initialize-a-thread-in-kotlin

https://stackoverflow.com/questions/46505528/how-to-initialize-a-thread-in-kotlin

There has more on the dart side, but I have no interests on them:
* https://buildflutter.com/flutter-threading-isolates-future-async-and-await/
* https://medium.com/@danielkao/%E5%B9%BB%E6%BB%85-%E6%98%AF%E6%88%90%E9%95%B7%E7%9A%84%E9%96%8B%E5%A7%8B-flutter-%E7%9A%84-async-%E8%88%87-isolate-2f87321a7ba8
* https://github.com/fluttercommunity/flutter_workmanager
* https://github.com/transistorsoft/flutter_background_fetch
* https://github.com/michael-cheung-thebus/foreground_service

## esp32
### firmware update
https://github.com/lvgl/lv_micropython

```bash
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -fm dio -z 0x1000 firmware_idf3_generic_spiram.bin
```

https://yingshaoxo.blogspot.com/2020/11/how-to-update-pyborad-firmware.html

### wifi connection
```python
import network

WIFI_SSID = "gateman"
WIFI_PASSWORD = "123456789"

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    while not sta_if.isconnected():
        pass

print("""network config: 
    IP address:  {}
    subnet mask: {}
    gateway: {} 
    DNS server: {}""".format(*sta_if.ifconfig()))
```

* http://docs.micropython.org/en/latest/esp32/quickref.html#networking
* http://docs.micropython.org/en/latest/library/network.html#module-network

### hotspot(AP, Access Point) setting
```python
ap = network.WLAN(network.AP_IF) # 创捷一个AP热点接口
ap.config(essid='ESP-AP') # 激活接口
ap.config(password="yingshaoxo") # 设置热点允许连接数量
ap.active(True)         # 设置AP的ESSID名称
print("ap config:", ap.ifconfig())
```

### http requests
```python
import uurequests

response = uurequests.get("http://baidu.com")
print(response.content)
```

https://github.com/pfalcon/pycopy-lib/tree/master/uurequests

### mqtt client
Basically, you got two actions available.

One is `publish`.

Another is `subscribe`.

If we want to send some message out to others, we need to use `publish`.

If we want to just receive messages from others, we use `subscribe`.

```python
from umqtt.simple import MQTTClient

#IP=$(/sbin/ip route | awk '/default/ { print $3 }')
#mosquitto_sub -h $IP -i "client/b" -t "a_topic"

c = MQTTClient("clients/a", SERVICE_IP)
c.connect()
c.publish(b"a_topic", b"hello")
c.disconnect()
```

```python
import time
from umqtt.simple import MQTTClient

#IP=$(/sbin/ip route | awk '/default/ { print $3 }')
#mosquitto_pub -h $IP -i "client/a" -t "a_topic" -m "hello"

# Received messages from subscriptions will be delivered to this callback
def callback(topic, msg):
    print((topic, msg))

c = MQTTClient("clients/b", server)
c.set_callback(callback)
c.connect()
c.subscribe(b"a_topic")
while True:
    if True:
        # Blocking wait for message
        c.wait_msg()
    else:
        # Non-blocking wait for message
        c.check_msg()
        # Then need to sleep to avoid 100% CPU usage (in a real
        # app other useful actions would be performed instead)
        time.sleep(1)

c.disconnect()
```

* You can't receive a topic before you subscribe to it.
* You won't receive anything if you don't call `client.check_msg()` or `client.wait_msg()`.
* You may need a timer to execute the `check_msg()` function since you can't use threading in micropython.

https://github.com/pfalcon/pycopy-lib/tree/master/umqtt.simple

### gui: LVGL
https://github.com/lvgl/lv_micropython
