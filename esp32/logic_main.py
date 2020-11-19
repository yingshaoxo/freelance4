import utility
import ui_page
from logic_database import database
import logic_wifi

if ui_page.TOUCH_READY:
    print(database.dict)
    if database.get("reset", default_value="true") == "true":
        ui_page.swich_page(ui_page.PAGENAMES.set_wifi_name)
        while (not ui_page.was_OK_button_pressed()):
            pass
        database.set("ssid", ui_page.get_text_area_text()) 
        ui_page.cancel_OK_state()

        ui_page.swich_page(ui_page.PAGENAMES.set_wifi_password)
        while (not ui_page.was_OK_button_pressed()):
            pass
        database.set("password", ui_page.get_text_area_text()) 
        ui_page.cancel_OK_state()

        ui_page.swich_page(ui_page.PAGENAMES.set_service_ip_address)
        while (not ui_page.was_OK_button_pressed()):
            pass
        database.set("service_ip", ui_page.get_text_area_text()) 
        ui_page.cancel_OK_state()

        database.set("reset", "false")
        database.commit()
        utility.reboot()
    else:
        ui_page.swich_page(ui_page.PAGENAMES.only_label)
        ui_page.set_label_text("connecting...")

        logic_wifi.is_wifi_ok()

        """
        print("we got all info that we need")
        ui_page.swich_page(ui_page.PAGENAMES.verify_password)
        while 1:
            while (not ui_page.was_OK_button_pressed()):
                pass
            text = ui_page.get_text_area_text()
            if text == "1900":
                database.reset()
                utility.reboot()
        """