if "lvgl" not in dir():
    import lvgl

if "disp" not in dir():
    import ujson
    import os

    #LCD ili9341初始化
    from ili9341 import ili9341
    from xpt2046 import xpt2046

    TFT_IS_PORTRAIT =1 #竖屏：1 ，横屏：0 ；
    TOUCH_READY = 0 #用于检测触摸屏是否已经校准过；

    disp = ili9341(
        miso=12,
        mosi=13,
        clk=14,
        cs=15,
        dc=21,
        rst=33,
        power=50,  #硬件不支持，随便配一个参数
        backlight=51, #硬件不支持，随便配一个参数
        backlight_on= 1,
        power_on= 1,
        width=240 if TFT_IS_PORTRAIT else 320,
        height=320 if TFT_IS_PORTRAIT else 240,
        rot=ili9341.PORTRAIT if TFT_IS_PORTRAIT else ili9341.LANDSCAPE #垂直方向PORTRAIT ；水平方向：LANDSCAPE
    )

    #触摸屏设置校准
    TOUCH_CS = 2  #触摸屏CS片选引脚
    TOUCH_INTERRUPT=0 #横屏

    if TFT_IS_PORTRAIT:
        TOUCH_CALI_FILE = "touch_cali_PORTRAIT.json" #保存为竖屏触摸参数
    else:
        TOUCH_CALI_FILE = "touch_cali_LANDSCAPE.json" #保存为横屏触摸参数

    #从没做过触摸校准
    if TOUCH_CALI_FILE not in os.listdir():
        touch = xpt2046(
            cs=TOUCH_CS,
            transpose=TFT_IS_PORTRAIT,
        )

        from touch_cali import TouchCali

        touch_cali = TouchCali(touch, TOUCH_CALI_FILE)
        touch_cali.start()

    #已经做过触摸校准，直接调用触摸参数文件
    else:
        with open(TOUCH_CALI_FILE, 'r') as f:
            param = ujson.load(f)
            touch_x0 = param['cal_x0']
            touch_x1 = param['cal_x1']
            touch_y0 = param['cal_y0']
            touch_y1 = param['cal_y1']

        touch = xpt2046(
            cs=TOUCH_CS,
            transpose=TFT_IS_PORTRAIT,
            cal_x0=touch_x0,
            cal_x1=touch_x1,
            cal_y0=touch_y0,
            cal_y1=touch_y1,
        )

        TOUCH_READY = 1 #表示已经配置好触摸参数