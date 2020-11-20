import 'package:flutter/material.dart';
import 'package:gateman/mqtt_communication.dart';
import 'package:gateman/page_check%20service.dart';
import 'package:gateman/services.dart';
import 'package:provider/provider.dart';
import 'package:wifi_iot/wifi_iot.dart';
import 'package:permission_handler/permission_handler.dart';

import 'models.dart';
import 'page_check_wifi.dart';
import "page_tab.dart";
import 'database.dart';

const String TITLE = "智能守卫";
Database database;

Future<void> main(List<String> args) async {
  WidgetsFlutterBinding.ensureInitialized();

  Map<Permission, PermissionStatus> statuses = await [
    Permission.locationWhenInUse,
  ].request();
  //print(statuses[Permission.locationWhenInUse]);

  database = Database();
  await database.init();

  runApp(MultiProvider(
    providers: [
      ChangeNotifierProvider(create: (context) => AppModel()),
      ChangeNotifierProvider(create: (context) => PageCheckWiFiModel()),
      ChangeNotifierProvider(create: (context) => PageCheckServiceModel()),
      ChangeNotifierProvider(create: (context) => PageTabsModel()),
      ChangeNotifierProvider(create: (context) => PageGatesModel()),
      ChangeNotifierProvider(create: (context) => PagePasswordModel()),
    ],
    child: MaterialApp(
      title: TITLE,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyApp(),
    ),
  ));
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  AppModel appModel;

  @override
  void didChangeDependencies() async {
    bool isWiFiConnected = await WiFiForIoTPlugin.isConnected();
    print("wifi status: ${isWiFiConnected}");

    String target = appModel.current_page;
    if (isWiFiConnected) {
      if (appModel.service_ip == "") {
        final isServiceAvaliable = await MyMQTT.is_service_avaliable();
        if (isServiceAvaliable) {
          target = "page_tab";
        } else {
          target = "page_check_service";
        }
      } else {
        target = "page_tab";
      }
    } else {
      target = "page_check_wifi";
    }
    appModel.current_page = target;

    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    appModel = Provider.of<AppModel>(context, listen: true);

    print(appModel.current_page);

    if (appModel.current_page == "page_check_wifi") {
      return PageCheckWiFi();
    } else if (appModel.current_page == "page_check_service") {
      return PageCheckService();
    } else if (appModel.current_page == "page_tab") {
      return PageTabs();
    }
  }
}
