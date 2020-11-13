import paho.mqtt.publish as publish

def get_gateway_ip():
    #return "127.0.0.1"
    import netifaces
    return netifaces.gateways()['default'][netifaces.AF_INET][0]

print(get_gateway_ip())

publish.single("abc", "boo", hostname=get_gateway_ip())
