import utility
from logic_database import database
import network
import utime
import usocket


def is_wifi_ok():
    print(database.dict)
    if (not database.exists("ssid")) or (not database.exists("password")):
        return False
    else:
        ssid = database.get("ssid") 
        password = database.get("password")

        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(ssid, password)
            start_time = utime.ticks_ms()
            while not sta_if.isconnected():
                now = utime.ticks_ms()
                diff = utime.ticks_diff(now, start_time)
                if diff >  5000:
                    return False
            ifconfig = sta_if.ifconfig()
            print("""network config: 
                IP address:  {}
                subnet mask: {}
                gateway: {} 
                DNS server: {}""".format(*ifconfig))
            return True

def is_port_open(ip:str, port:str):
    s = usocket.socket()
    try:
        s.connect(usocket.getaddrinfo(ip, port, 0, usocket.SOCK_STREAM)[0][-1])
        s.close()
        return True
    except OSError:
        return False

if __name__ == "__main__":
    pass
