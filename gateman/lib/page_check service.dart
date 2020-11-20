import 'package:flushbar/flushbar.dart';
import 'package:flutter/material.dart';
import 'package:gateman/utils.dart';
import 'package:provider/provider.dart';
import 'package:google_nav_bar/google_nav_bar.dart';
import 'package:gateman/services.dart';
import 'package:string_validator/string_validator.dart';
import 'package:wifi_iot/wifi_iot.dart';

import 'models.dart';
import 'main.dart';
import 'mqtt_communication.dart';

class PageCheckService extends StatefulWidget {
  @override
  _PageCheckServiceState createState() => _PageCheckServiceState();
}

class _PageCheckServiceState extends State<PageCheckService> {
  AppModel appModel;

  String device_ip = "";
  String wifi_name = "";

  @override
  void didChangeDependencies() async {
    device_ip = await WiFiForIoTPlugin.getIP();

    print(device_ip);

    setState(() {
      device_ip = device_ip;
    });

    FlutterNativeAction.startMQTTService();

    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    final appModel = Provider.of<AppModel>(context, listen: false);
    final pageCheckServiceModel =
        Provider.of<PageCheckServiceModel>(context, listen: true);

    final width = MediaQuery.of(context).size.width;
    final height = MediaQuery.of(context).size.height;

    var text = '''
    当前安卓手机IP地址: ${device_ip}
    ''';
    // 注意，你的WIFI供应商需要开放 `到某一MQTT服务器的1883TCP端口` 。
    text = text.trim();

    return Scaffold(
        appBar: AppBar(
          title: const Text(TITLE),
        ),
        body: Center(
            child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              "在这儿输入你的服务器IP地址:",
              textAlign: TextAlign.center,
            ),
            Container(
              width: width * 0.6,
              child: TextFormField(
                  controller: pageCheckServiceModel.textController,
                  textAlign: TextAlign.center,
                  autofocus: true,
                  decoration: InputDecoration(),
                  style: TextStyle(color: Colors.red)),
            ),
            SizedBox(
              height: height * 0.05,
            ),
            Text(
              text,
              textAlign: TextAlign.center,
            ),
            SizedBox(
              height: height * 0.03,
            ),
            ButtonBar(
              alignment: MainAxisAlignment.spaceEvenly,
              children: [
                FlatButton(
                  child: Text(
                    "好了",
                    style: TextStyle(fontSize: 15.0),
                  ),
                  onPressed: () async {
                    final text = pageCheckServiceModel.textController.text;
                    if (isIP(text)) {
                      if (await Utils.is_port_open(text, 1883)) {
                        appModel.service_ip = text;
                        appModel.current_page = "page_tab";
                      } else {
                        Flushbar(
                          title: "注意",
                          message: "你给的IP地址我连接不上，你是不是输错了，或者服务器没有启动？",
                          duration: Duration(seconds: 3),
                          backgroundColor: Colors.red,
                        )..show(context);
                      }
                    } else {
                      Flushbar(
                        title: "注意",
                        message: "你需要输入一个正确的IP地址",
                        duration: Duration(seconds: 3),
                        backgroundColor: Colors.blueAccent,
                      )..show(context);
                    }
                  },
                  minWidth: 100,
                  color: Colors.blue[400],
                  textColor: Colors.white,
                  padding: EdgeInsets.all(8.0),
                ),
              ],
            )
          ],
        )));
  }
}
