import network
import machine
import uos
import usocket

def encode(text: str):
    return text.encode("utf-8")

def decode(bytes_: bytes):
    return bytes_.decode("utf-8")

def show_widget(widget, hidden: bool):
    widget.set_hidden(not hidden)

def reboot():
    machine.reset()
    #machine.soft_reset()

def remove_a_file(path: str):
    uos.remove(path)

def is_port_open(ip:str, port:str):
    s = usocket.socket()
    try:
        s.connect(usocket.getaddrinfo(ip, port, 0, usocket.SOCK_STREAM)[0][-1])
        s.close()
        return True
    except OSError:
        return False