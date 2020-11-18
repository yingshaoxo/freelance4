if "lvgl" not in dir():
    from ui_start import lvgl, TOUCH_READY

UI_READY = False

if TOUCH_READY:
    # text area
    if "text_area1" not in dir():
        text_area1 = lvgl.ta(lvgl.scr_act())
    text_area1.set_size(200, 100)
    #print(dir(lvgl.ALIGN))
    #ta1.align(lvgl.ALIGN.IN_TOP_MID, lvgl.ALIGN.CENTER, 0, 0)
    text_area1.align(None, lvgl.ALIGN.IN_TOP_MID, 0, 0)
    text_area1.set_cursor_type(lvgl.CURSOR.BLOCK)
    text_area1.set_text("nono")     # Set an initial text
    #print(dir(ta1))
    
    # button matrix
    """
    if "button_matrix1" not in dir():
        button_matrix1 = lvgl.btnm(lvgl.scr_act())
    btnm_map = ["1", "2", "3", "4", "5", "\n",
                "6", "7", "8", "9", "0", "\n",
                "OK", ".", "Delete", ""]
    button_matrix1.set_map(btnm_map)
    button_matrix1.set_btn_width(11, 2)        # Make "Action1" twice as wide as "Action2"
    button_matrix1.set_width(240)
    button_matrix1.set_height(150)
    button_matrix1.align(None, lvgl.ALIGN.IN_BOTTOM_MID, 0, 0)
    def button_matrix1_event_handler(obj, event):
        if event == lvgl.EVENT.VALUE_CHANGED:
            text = obj.get_active_btn_text()
            print("%s was pressed" % text)
            if text:
                if text == "Delete":
                    text_area1.set_text(text_area1.get_text()[:-1])
                elif text != "OK":
                    text_area1.set_text(text_area1.get_text() + text)
    button_matrix1.set_event_cb(button_matrix1_event_handler) #定义按钮事件回调函数
    """

    # keyboard
    if "keyboard1" not in dir():
        keyboard1 =lvgl.kb(lvgl.scr_act())
        keyboard1.set_cursor_manage(False)
        keyboard1.set_style(lvgl.kb.STYLE.BG,lvgl.style_transp_tight)
        keyboard1.set_ta(text_area1)
    keyboard1.align(None, lvgl.ALIGN.IN_BOTTOM_MID, 0, 0)
    def keyboard1_event_handler(obj, event):
        try:
            if event == lvgl.EVENT.APPLY:
                print("OK OK ..........")
            elif event == lvgl.EVENT.CANCEL:
                print("Cancel ..........")
            elif event == lvgl.EVENT.VALUE_CHANGED:
                obj.def_event_cb(event)
                #print(obj)
        except Exception as e:
            print(e)
    keyboard1.set_event_cb(keyboard1_event_handler) #定义按钮事件回调函数
    #print(dir(keyboard1))

    # label
    if "label1" not in dir():
        label1 = lvgl.label(lvgl.scr_act())
    mystyle = lvgl.style_t(lvgl.style_plain)
    mystyle.text.color = lvgl.color_hex(0xff0000) # text-colour, 0xRRGGBB
    label1.set_long_mode(lvgl.label.LONG.BREAK)     # Break the long lines
    label1.set_recolor(True)                      # Enable re-coloring by commands in the text
    label1.set_width(240)
    label1.set_align(lvgl.label.ALIGN.CENTER)       # Center aligned lines
    label1.align(None, lvgl.ALIGN.CENTER, 0, -30)
    label1.set_style(0, mystyle)
    label1.set_text("hi")

    """
    def abc():
        a = ta1.get_text().strip() != "" and SubscribeDict["password"] == ta1.get_text()
        b = GateName in SubscribeDict["doors_that_open"]
        
        if (a or b):
            label1.set_text("The door is open")
        else:
            label1.set_text("The door is close")
    UI_Logic = abc
    """

    UI_READY = True