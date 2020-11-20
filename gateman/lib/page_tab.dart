import 'package:flutter/material.dart';
import 'package:gateman/page_password.dart';
import 'package:gateman/utils.dart';
import 'package:provider/provider.dart';
import 'package:google_nav_bar/google_nav_bar.dart';
import 'package:flutter_beautiful_popup/main.dart';

import 'services.dart';
import 'models.dart';
import 'main.dart';
import 'mqtt_communication.dart';
import 'page_gates.dart';
import 'page_password.dart';

class PageTabs extends StatefulWidget {
  PageTabs({
    Key key,
  }) : super(key: key);

  @override
  _PageTabsState createState() => _PageTabsState();
}

class _PageTabsState extends State<PageTabs> {
  static List<Widget> _widgetOptions = <Widget>[
    PageGates(),
    PagePassword(),
  ];

  @override
  void didChangeDependencies() async {
    FlutterNativeAction.startMQTTService();
    await Utils.sleep(1);
    await MyMQTT.connect();
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    final appModel = Provider.of<AppModel>(context, listen: false);
    final pageGatesModel = Provider.of<PageGatesModel>(context, listen: false);

    final popup = BeautifulPopup(
      context: context,
      template: TemplateSuccess,
    );

    return Consumer<PageTabsModel>(builder: (context, pageTabModel, child) {
      return Scaffold(
        appBar: AppBar(
          title: const Text(TITLE),
        ),
        floatingActionButton: FloatingActionButton(
          onPressed: () async {
            //MyMQTT.publish("gate_name", "ok");
            //await MyMQTT.ping();
            pageGatesModel.add_a_gate(Utils.getRandomString(8));
          },
          child: Icon(Icons.send),
          backgroundColor: Colors.green,
        ),
        drawer: Drawer(
          child: ListView(
            // Important: Remove any padding from the ListView.
            padding: EdgeInsets.zero,
            children: <Widget>[
              DrawerHeader(
                child: Center(child: Text('')),
                decoration: BoxDecoration(
                  color: Colors.blue,
                ),
              ),
              ListTile(
                title: Text('门牌绑定'),
                onTap: () async {
                  pageGatesModel.name_binding_mode = true;
                  Navigator.pop(context);
                },
              ),
              ListTile(
                title: Text('设置'),
                onTap: () async {
                  if (!await MyMQTT.is_service_avaliable()) {
                    appModel.service_ip = "";
                    appModel.current_page = "page_check_service";
                  } else {
                    popup.show(
                      title: '注意',
                      content: Center(child: Text("你不需要设置什么，服务器运行正常。")),
                      actions: [
                        popup.button(
                          label: '好的',
                          onPressed: () async {
                            Navigator.pop(context);
                          },
                        ),
                      ],
                    );
                  }
                },
              ),
              ListTile(
                title: Opacity(
                  opacity: .01,
                  child: const Text('Author'),
                ),
                onTap: () async {
                  popup.show(
                    title: 'yingshaoxo@gmail.com',
                    content: Center(
                        child: Image(image: AssetImage('assets/me.jpg'))),
                    actions: [
                      popup.button(
                        label: 'OK',
                        onPressed: () async {
                          Navigator.pop(context);
                        },
                      ),
                    ],
                  );
                },
              ),
            ],
          ), // Populate the Drawer in the next step.
        ),
        body: Center(
          child: _widgetOptions.elementAt(pageTabModel.tab_index),
        ),
        bottomNavigationBar: Container(
          decoration: BoxDecoration(color: Colors.white, boxShadow: [
            BoxShadow(blurRadius: 2, color: Colors.black.withOpacity(.1))
          ]),
          child: SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
              child: GNav(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  gap: 0,
                  activeColor: Colors.white,
                  iconSize: 32,
                  padding: EdgeInsets.symmetric(horizontal: 40, vertical: 5),
                  duration: Duration(milliseconds: 800),
                  //tabBackgroundColor: Colors.grey[400],
                  tabBackgroundColor: Colors.blue,
                  //backgroundColor: Colors.purple,
                  color: Colors.blue,
                  tabs: [
                    GButton(
                      //borderRadius: BorderRadius.all(Radius.circular(5)),
                      icon: Icons.apartment,
                      text: '开关控制',
                    ),
                    GButton(
                      //borderRadius: BorderRadius.all(Radius.circular(5)),
                      icon: Icons.vpn_key,
                      text: '密码设置',
                    ),
                  ],
                  selectedIndex: pageTabModel.tab_index,
                  onTabChange: (index) {
                    pageTabModel.tab_index = index;
                  }),
            ),
          ),
        ),
      );
    });
  }
}
