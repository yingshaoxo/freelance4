# freelance4
We use flutter as the mqtt hotspot server, pyboard esp32 as clients.

It's a gate control system.

1. server can control the openness of two gates.
2. server can change the password of two gates.
3. user can open the gates if they input the right password.

## server
### techs
* https://github.com/alternadom/WiFiFlutter
* https://pub.dev/packages/mqtt_client

## client
### techs
* http://docs.micropython.org/en/latest/esp32/quickref.html#networking
* https://github.com/peterhinch/micropython-mqtt

## esp32
### firmware update
https://github.com/lvgl/lv_micropython

```bash
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -fm dio -z 0x1000 firmware_idf3_generic_spiram.bin
```

https://yingshaoxo.blogspot.com/2020/11/how-to-update-pyborad-firmware.html
