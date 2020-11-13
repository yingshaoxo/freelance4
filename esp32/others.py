import network
import uurequests
#import urequests

def enable_ap():
    ap = network.WLAN(network.AP_IF) # 创捷一个AP热点接口
    ap.config(essid='ESP-AP') # 激活接口
    ap.config(password="yingshaoxo") # 设置热点允许连接数量
    ap.active(True)         # 设置AP的ESSID名称
    print("ap config:", ap.ifconfig())

def get_baidu():
    response = uurequests.get("http://baidu.com")
    print(response.content)