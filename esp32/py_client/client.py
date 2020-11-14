import paho.mqtt.publish as publish

def get_gateway_ip():
    import netifaces
    return netifaces.gateways()['default'][netifaces.AF_INET][0]

print(get_gateway_ip())

publish.single("password", "whateverpassword", hostname=get_gateway_ip(), client_id="client/d")
