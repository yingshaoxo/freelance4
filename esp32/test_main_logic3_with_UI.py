import network
from time import sleep
from umqtt.simple import MQTTClient
from machine import Timer
import ujson

WIFI_SSID = "Hello World"
WIFI_PASSWORD = "yingshaoxo"
SERVICE_IP = "192.168.49.182"

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

UI_Logic = lambda : 1

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
    #SERVICE_IP = ifconfig[2]

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
    UI_Logic()

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

import lvgl as lv

try:
    print(disp)
except:
    import ujson

    #LCD ili9341初始化
    from ili9341 import ili9341
    from xpt2046 import xpt2046

    TFT_IS_PORTRAIT =1 #竖屏：1 ，横屏：0 ；
    TOUCH_READY = 0 #用于检测触摸屏是否已经校准过；

    disp = ili9341(
        miso=12,
        mosi=13,
        clk=14,
        cs=15,
        dc=21,
        rst=33,
        power=50,  #硬件不支持，随便配一个参数
        backlight=51, #硬件不支持，随便配一个参数
        backlight_on= 1,
        power_on= 1,
        width=240 if TFT_IS_PORTRAIT else 320,
        height=320 if TFT_IS_PORTRAIT else 240,
        rot=ili9341.PORTRAIT if TFT_IS_PORTRAIT else ili9341.LANDSCAPE #垂直方向PORTRAIT ；水平方向：LANDSCAPE
    )

    #触摸屏设置校准
    TOUCH_CS = 2  #触摸屏CS片选引脚
    TOUCH_INTERRUPT=0 #横屏

    if TFT_IS_PORTRAIT:
        TOUCH_CALI_FILE = "touch_cali_PORTRAIT.json" #保存为竖屏触摸参数
    else:
        TOUCH_CALI_FILE = "touch_cali_LANDSCAPE.json" #保存为横屏触摸参数

    #从没做过触摸校准
    if TOUCH_CALI_FILE not in uos.listdir():
        touch = xpt2046(
            cs=TOUCH_CS,
            transpose=TFT_IS_PORTRAIT,
        )

        from touch_cali import TouchCali

        touch_cali = TouchCali(touch, TOUCH_CALI_FILE)
        touch_cali.start()

    #已经做过触摸校准，直接调用触摸参数文件
    else:
        with open(TOUCH_CALI_FILE, 'r') as f:
            param = ujson.load(f)
            touch_x0 = param['cal_x0']
            touch_x1 = param['cal_x1']
            touch_y0 = param['cal_y0']
            touch_y1 = param['cal_y1']

        touch = xpt2046(
            cs=TOUCH_CS,
            transpose=TFT_IS_PORTRAIT,
            cal_x0=touch_x0,
            cal_x1=touch_x1,
            cal_y0=touch_y0,
            cal_y1=touch_y1,
        )

        TOUCH_READY = 1 #表示已经配置好触摸参数


if TOUCH_READY:
    # text area
    ta1 = lv.ta(lv.scr_act())
    ta1.set_size(200, 100)
    #print(dir(lv.ALIGN))
    #ta1.align(lv.ALIGN.IN_TOP_MID, lv.ALIGN.CENTER, 0, 0)
    ta1.align(None, lv.ALIGN.IN_TOP_MID, 0, 0)
    ta1.set_cursor_type(lv.CURSOR.BLOCK)
    ta1.set_text("")     # Set an initial text
    #print(dir(ta1))
    
    # keypad
    btnm_map = ["1", "2", "3", "4", "5", "\n",
                "6", "7", "8", "9", "0", "\n",
                "OK", "Delete", ""]
    btnm1 = lv.btnm(lv.scr_act())
    btnm1.set_map(btnm_map)
    btnm1.set_btn_width(11, 2)        # Make "Action1" twice as wide as "Action2"
    btnm1.set_width(240)
    btnm1.set_height(150)
    btnm1.align(None, lv.ALIGN.IN_BOTTOM_MID, 0, 0)
    def event_handler(obj, event):
        if event == lv.EVENT.VALUE_CHANGED:
            text = obj.get_active_btn_text()
            print("%s was pressed" % text)
            if text == "Delete":
                ta1.set_text(ta1.get_text()[:-1])
            elif text != "OK":
                ta1.set_text(ta1.get_text() + text)
    btnm1.set_event_cb(event_handler) #定义按钮事件回调函数

    # label
    mystyle = lv.style_t(lv.style_plain)
    mystyle.text.color = lv.color_hex(0xff0000) # text-colour, 0xRRGGBB
    label1 = lv.label(lv.scr_act())
    label1.set_long_mode(lv.label.LONG.BREAK)     # Break the long lines
    label1.set_recolor(True)                      # Enable re-coloring by commands in the text
    label1.set_width(240)
    label1.set_align(lv.label.ALIGN.CENTER)       # Center aligned lines
    label1.align(None, lv.ALIGN.CENTER, 0, -30)
    label1.set_style(0, mystyle)
    label1.set_text("hi")

    def abc():
        a = ta1.get_text().strip() != "" and SubscribeDict["password"] == ta1.get_text()
        b = GateName in SubscribeDict["doors_that_open"]
        
        if (a or b):
            label1.set_text("The door is open")
        else:
            label1.set_text("The door is close")


    UI_Logic = abc

    do_wifi_connect()
    sleep(0.1)
    mqtt_connect()