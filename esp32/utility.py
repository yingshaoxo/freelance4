import network

def encode(text: str):
    return text.encode("utf-8")

def decode(bytes_: bytes):
    return bytes_.decode("utf-8")

def connect_wifi(ssid: str, password: str):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    ifconfig = sta_if.ifconfig()
    print("""network config: 
        IP address:  {}
        subnet mask: {}
        gateway: {} 
        DNS server: {}""".format(*ifconfig))