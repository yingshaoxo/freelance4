import network

WIFI_SSID = "gateman"
WIFI_PASSWORD = "123456789"

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

if __name__ == '__main__':
    _,_,gateway,_ = do_wifi_connect()