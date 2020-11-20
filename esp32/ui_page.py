from logic_database import database, StoreKey

if "lvgl" not in dir():
    from ui_make import TOUCH_READY, lvgl, text_area1, label1 , button_matrix1, keyboard1, UI_STATES
if "utility" not in dir():
    import utility

class PAGENAMES:
    set_device_name = "set_device_name"
    set_wifi_name = "set_wifi_name"
    set_wifi_password = "set_wifi_password"
    set_service_ip_address = "set_service_ip_address"
    verify_password = "verify_password"
    only_label = "only_label"


def set_text_area_text(text:str):
    return text_area1.set_text(text)

def get_text_area_text():
    return text_area1.get_text().strip()

def was_OK_button_pressed():
    global UI_STATES
    return UI_STATES["OK"] == True

def cancel_OK_state():
    global UI_STATES
    UI_STATES["OK"] = False

def set_label_text(text: str):
    label1.set_text(text)

def swich_page(page_name: str):
    text_area1.set_text("")
    if (page_name == PAGENAMES.set_device_name):
        label1.set_text("Please input your device name")     # Set an initial text
        utility.show_widget(text_area1, True)
        utility.show_widget(button_matrix1, False)
        utility.show_widget(keyboard1, True)
        if (database.exists(StoreKey.device_name)):
            set_text_area_text(database.get(StoreKey.device_name))
    elif (page_name == PAGENAMES.set_wifi_name):
        label1.set_text("Please input your WiFi name")     # Set an initial text
        utility.show_widget(text_area1, True)
        utility.show_widget(button_matrix1, False)
        utility.show_widget(keyboard1, True)
        if (database.exists(StoreKey.ssid)):
            set_text_area_text(database.get(StoreKey.ssid))
    elif (page_name == PAGENAMES.set_wifi_password):
        label1.set_text("Please input your WiFi password")     # Set an initial text
        utility.show_widget(text_area1, True)
        utility.show_widget(button_matrix1, False)
        utility.show_widget(keyboard1, True)
        if (database.exists(StoreKey.password)):
            set_text_area_text(database.get(StoreKey.password))
    elif (page_name == PAGENAMES.set_service_ip_address):
        label1.set_text("Please input your server IP address")     # Set an initial text
        utility.show_widget(text_area1, True)
        utility.show_widget(button_matrix1, False)
        utility.show_widget(keyboard1, True)
        if (database.exists(StoreKey.service_ip)):
            set_text_area_text(database.get(StoreKey.service_ip))
    elif (page_name == PAGENAMES.verify_password):
        label1.set_text("Please input your passwrod to open the door")     # Set an initial text
        utility.show_widget(text_area1, True)
        utility.show_widget(button_matrix1, True)
        utility.show_widget(keyboard1, False)
    elif (page_name == PAGENAMES.only_label):
        label1.set_text("")     # Set an initial text
        utility.show_widget(text_area1, False)
        utility.show_widget(button_matrix1, False)
        utility.show_widget(keyboard1, False)


#swich_page(PAGENAMES.set_service_ip_address)
#swich_page("set_wifi_password")