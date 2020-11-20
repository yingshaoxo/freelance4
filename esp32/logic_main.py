import utility
import ui_page
from logic_database import database, StoreKey
import logic_wifi
import logic_mqtt

if ui_page.TOUCH_READY:
    print(database.dict)
    if database.get(StoreKey.reset, default_value="true") == "true":
        ui_page.swich_page(ui_page.PAGENAMES.set_device_name)
        while (not ui_page.was_OK_button_pressed()):
            pass
        database.set(StoreKey.device_name, ui_page.get_text_area_text()) 
        ui_page.cancel_OK_state()

        ui_page.swich_page(ui_page.PAGENAMES.set_wifi_name)
        while (not ui_page.was_OK_button_pressed()):
            pass
        database.set(StoreKey.ssid, ui_page.get_text_area_text()) 
        ui_page.cancel_OK_state()

        ui_page.swich_page(ui_page.PAGENAMES.set_wifi_password)
        while (not ui_page.was_OK_button_pressed()):
            pass
        database.set(StoreKey.password, ui_page.get_text_area_text()) 
        ui_page.cancel_OK_state()

        ui_page.swich_page(ui_page.PAGENAMES.set_service_ip_address)
        while (not ui_page.was_OK_button_pressed()):
            pass
        database.set(StoreKey.service_ip, ui_page.get_text_area_text()) 
        ui_page.cancel_OK_state()

        database.set(StoreKey.reset, "false")
        database.commit()
        utility.reboot()
    else:
        ui_page.swich_page(ui_page.PAGENAMES.only_label)
        ui_page.set_label_text("connecting...")

        logic_wifi.is_wifi_ok()

        utility.sleep(0.1)
        logic_mqtt.update_info()
        utility.sleep(1)
        print("info updated")
        logic_mqtt.mqtt_connect()
        utility.sleep(1)
        print("mqtt connected")

        print("we got all info that we need")
        ui_page.swich_page(ui_page.PAGENAMES.verify_password)
        utility.sleep(2)
        def abc():
            condition = logic_mqtt.GateName in logic_mqtt.SubscribeDict["doors_that_open"]
            if (condition):
                ui_page.set_label_text("The door is open")
            else:
                ui_page.set_label_text("The door is close")
        logic_mqtt.UI_Logic = abc
        while 1:
            ui_page.set_text_area_text("")
            ui_page.cancel_OK_state()
            while (not ui_page.was_OK_button_pressed()):
                pass
            text = ui_page.get_text_area_text()

            if text == "1900":
                database.set("reset", "true")
                database.commit()
                utility.reboot()
            
            if text == logic_mqtt.SubscribeDict["password"]:
                logic_mqtt.restart_mqtt_timer(delay=3)
                ui_page.set_label_text("The door is open")
                print("open door with password")