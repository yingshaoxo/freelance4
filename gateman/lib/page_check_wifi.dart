import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_nav_bar/google_nav_bar.dart';
import 'package:gateman/services.dart';
import 'package:wifi_iot/wifi_iot.dart';

import 'models.dart';
import 'main.dart';

class PageCheckWiFi extends StatefulWidget {
  @override
  _PageCheckWiFiState createState() => _PageCheckWiFiState();
}

class _PageCheckWiFiState extends State<PageCheckWiFi> {
  @override
  void didChangeDependencies() async {
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    final appModel = Provider.of<AppModel>(context, listen: false);

    var text = '''
    你需要连接上WIFI才能使用本软件！
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
              text,
              textAlign: TextAlign.center,
            ),
            SizedBox(
              height: 50,
            ),
            ButtonBar(
              alignment: MainAxisAlignment.spaceEvenly,
              children: [
                FlatButton(
                  child: Text(
                    "已经连好了",
                    style: TextStyle(fontSize: 15.0),
                  ),
                  onPressed: () async {
                    appModel.current_page = "page_check_service";
                  },
                  minWidth: 100,
                  color: Colors.grey,
                  textColor: Colors.white,
                  padding: EdgeInsets.all(8.0),
                ),
                FlatButton(
                  child: Text(
                    "前往设定",
                    style: TextStyle(fontSize: 15.0),
                  ),
                  onPressed: () async {
                    await FlutterNativeAction.openWiFiSettingPage();
                  },
                  minWidth: 100,
                  color: Colors.blue,
                  textColor: Colors.white,
                  padding: EdgeInsets.all(8.0),
                  splashColor: Colors.blueAccent,
                )
              ],
            )
          ],
        )));
  }
}
