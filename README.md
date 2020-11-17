# freelance4
We use flutter as the mqtt hotspot server, pyboard esp32 as clients.

It's a gate control system.

1. server can control the openness of two gates.
2. server can change the password of two gates.
3. user can open the gates if they input the right password.

It should happend under WIFI or LocalAreaNetwork.

It should has authorization. 

* The MQTT service server IP is given as a const value.
* The WIFI name and password are given as constants.

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

## discussion

### q&a 1
#### question
1. 手机APP的界面能不能更直观一点，因为学校实验管理员一般都是退休的大爷。对这个英文不懂。

2. 门牌号是动态添加，就是要自己随意输入，

3. 整个系统的逻辑是没有问题了，不过我觉得我是不是得买开发板买两套过去。因为实验室有很多个，一个实验室对应一个控制板，所以，开发的时候用两个板会比较好些。

4. APP的界面，我需要装到手机上之后再去确定要修改哪些地方，因为不实际操作我也不确定会有哪些问题。

5. 为什么用的是热点而不是开WLAN?

6. 那个3.3V继电器模块是用来连接电控锁的。
#### answer
1. 这个在手机APP上没有问题

2. 设备名在单片机上预先设定(一串英文)，但可以在手机APP上给它绑定一个中文名字

3. 暂时不需要(因为除了单片机的程序，其他部分都是用编译语言写的，几乎不出错。而且以我现在的构架能力也不会出错。)

4. 这个没什么问题，是个人就会用

5. 因为这样方便单片机找到手机app的服务器地址，因为网关即地址。（同时自建热点更纯净，没有防火墙。据我所知，学校的WIFI网络在你不登陆之前，是不互通的，防火墙会过滤掉一切ip包。要想在学校的网络用，需要让网络管理员不过滤 1883 tcp 端口。）

6. 你给我发了继电器模块？我没仔细看，不知道包裹里有没有

### q&a 2
#### question
那如果用热点的话，信号怎么样？能不能穿墙？

我这个门禁系统设计的目的就是为了能在办公室开实验室的门。

#### answer

不怎么样、不能穿墙。


___

我们可以回忆一下小米智能设备是怎么连上网的

首先，你用蓝牙把APP和设备相连，APP把WiFi名和密码告诉设备。

情况1，APP把一个远程的需要连外网的mqtt服务器地址告诉了设备

情况2，APP把安卓设备的IP地址告诉了设备（本地mqtt服务器

设备连上WiFi，连上Mqtt服务器，物联网成功！


可见，设备本身不会主动扫描端口，因为那增加了软件的复杂度和不稳定因素。

它需要别人告诉它一个MQTT服务器IP地址。

### q&a 3
#### question
这个问题有解吗？

#### answer
有

一般来讲，学校的网络，只需要账号和密码就能登陆

如果能对那个网页进行抓包，就可以通过访问一个网页进行网络登陆

你恰好有学校的WiFi账号和密码

单片机连上网后，就让它用我闲置的云服务器（MQTT服务器）

这样的话就不单纯是一个局域网程序了，这是真物联网

### q&a 4
#### question
其实你要是一早说你要“装b”

那我就不搞局域网了

不过局域网挺好玩的

#### answer
这是什么话啊？

这不是装，是要考虑到这个系统的实际使用情况。

因为在申请这个大创的时候，写的系统设计的目的就是为了，可以让实验室管理员在他自己的办公室里面打开多个实训室，而不用整栋楼上下到处跑着去开门。

为了节省人力啊！

不然如果管理员直接在实验室门口开门，那设计这个系统就没有意义，直接拿钥匙去一个一个门的打开就好了。

> 暗示，热点那一套不靠谱，还是需要连到更大的局域网

### q&a 5
#### question
那目前如果我在家里的网络能完成吗？

这整个系统是我自己的一个设计，至于最后是不是真的拿来在学校用，是不确定的。

但是我要把基本的功能都实现，要考虑到使用环境。

#### answer
条件1

这个问题最困难的地方不是实现系统

而是怎么让学校的网络更开放一点

至少开一个1883端口

___


条件2

还有，如果是学校局域网的话

至少整个学校要有一台固定ip的服务器电脑，这样才能运行mqtt service 程序


___



只要条件1和条件2满足，整个系统想怎么设计怎么设计，完全没有压力


___



现在的问题是你都没有。你想不通过满足条件达到目的。

那就强行做。

___

条件1绕过方法：
http GET or POST 强行登录学校网络

条件2代替方案：
用自己的云服务器，代替学校那台局域网设备

### q&a 6
#### question
这个系统只是我自己的设计，如果说真的要用到学校的实验室管理，肯定是要让学校开1883端口。所以，现在先不考虑使用环境是学校的局域网。

在家庭网络条件下是否可以实现，如果可以，就在家庭无线网的条件下开发这个系统。

这样有没有问题？

#### answer
没有难度。

你只需要在路由器设置界面192.168.1.1，绑定手机的mac和ip地址即可，这样我们的 mqtt server 的IP地址就固定了。

这样，环境就搭好了，不需要热点，纯WiFi。

### q&a 7
#### question
这两天我一直在想通信安全的事情（没写代码

发现这个项目做不了（理想环境当然可以，但真实世界是有黑客的）

https://kknews.cc/zh-hk/tech/3op8eay.html

黑客会对信息进行篡改，在我们这个例子里，就是他可以随意的开启或关闭任意一个实验室的门，并偷走里面的东西。

解决方案1：服务器加ssl。

解决方案2：通信加密。

限制1：ssl无法在局域网部署。ssl一般配置在有外部网络的服务器。它让网站自带加密功能，防偷窥、防篡改。如果在局域网搞这个，服务器和客户端都得有密匙文件，都得进行配置，都得有相应的软件，很明显micropython没有，全世界任意一款单片机也没有。（https://www.jianshu.com/p/c191db193a9c

限制2：通信加密在单片机上无法实现。因为单片机没有那么大的内存和计算力做加解密。它们最多做了一个AES模块，而这个模块只能处理16个字符(128bit)，多一个不行，少一个也不行，实属鸡肋产品。(AES is a block cipher, it works on 16-byte (128-bit) blocks. AES, on its own, can't work with data smaller or bigger than 16 bytes. Smaller data needs to be padded until they're 16 bytes, and larger data needs to be split into 16-byte blocks (and, of course, padded when needed*)



所以之前用热点也是有这个安全考虑在里面：小局域网里面没有坏人。

#### answer
不要考虑的太复杂，在理想环境下做就可以了，再说外面的人也进不来学校，学校的学生也没有这么厉害的黑客。

另外学校还到处都有监控。

不用考虑的太复杂了，把基本的东西考虑到就可以了。

## comments
### about android mqtt service or broker
用手机做服务器会停止服务，并中断网络

一旦你切换程序并且关屏，就断了


不过这不影响我们的程序，我之前设计的时候，就假定我们的服务器会经常断线


而且这个设计和服务器没什么关系，mqtt服务器只是一个中介平台，用作消息转发。不管是在安卓上，还是在Linux或者Windows电脑上，程序都不会变。（这个服务器跨平台可用


重点是处理安卓软件和单片机之间的关系，完成既定的信息交换