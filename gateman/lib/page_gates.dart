import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:gateman/utils.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:provider/provider.dart';
import 'package:flutter_beautiful_popup/main.dart';

import 'models.dart';
import 'main.dart';
import 'mqtt_communication.dart';

class PageGates extends StatefulWidget {
  @override
  _PageGatesState createState() => _PageGatesState();
}

class _PageGatesState extends State<PageGates> {
  PageGatesModel pageGatesModel;
  PagePasswordModel pagePasswordModel;

  @override
  void didChangeDependencies() async {
    await MyMQTT.make_sure_it_is_connected();
    MyMQTT.subscribe("gate_name");
    MyMQTT.set_callback_for_a_topic("gate_name", (String text) {
      print("haha, the new gate is: ${text}");
      if (pageGatesModel.add_a_gate(text)) {
        pageGatesModel.send_open_doors_info_out();
        pagePasswordModel.send_password_info_out();
      }
    });

    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    pageGatesModel = Provider.of<PageGatesModel>(context, listen: true);
    pagePasswordModel = Provider.of<PagePasswordModel>(context, listen: false);

    final width = MediaQuery.of(context).size.width;
    final height = MediaQuery.of(context).size.height;

    final popup = BeautifulPopup(
      context: context,
      template: TemplateSuccess,
    );

    final onTapFunction = (gate, door_state) {
      if (pageGatesModel.name_binding_mode) {
        popup.show(
          title: '清输入门牌号',
          content: Center(
              child: TextFormField(
                  controller: pageGatesModel.textController,
                  textAlign: TextAlign.center,
                  autofocus: true,
                  decoration: InputDecoration(),
                  style: TextStyle(color: Colors.red))),
          actions: [
            popup.button(
              label: '完成',
              onPressed: () {
                pageGatesModel.add_binding_name(
                    gate, pageGatesModel.textController.text);
                Navigator.pop(context);
              },
            ),
          ],
          // bool barrierDismissible = false,
          // Widget close,
        );
      } else {
        if (door_state) {
          pageGatesModel.close_a_door(gate);
        } else {
          pageGatesModel.open_a_door(gate);
        }
        pageGatesModel.send_open_doors_info_out();
      }
    };

    return Padding(
        padding: EdgeInsets.all(width * 0.15),
        child: Container(
            child: Center(
          child: Column(
            children: [
              pageGatesModel.name_binding_mode
                  ? Expanded(
                      flex: 1,
                      child: GestureDetector(
                        child: Text("点我退出编辑模式"),
                        onTap: () async {
                          pageGatesModel.name_binding_mode = false;
                        },
                      ))
                  : Expanded(
                      flex: 0,
                      child: Container(),
                    ),
              Expanded(
                flex: 12,
                child: Center(
                  child: ListView(
                    // Create a grid with 2 columns. If you change the scrollDirection to
                    // horizontal, this produces 2 rows.
                    shrinkWrap: true,
                    // Generate 100 widgets that display their index in the List.
                    children: List.generate(pageGatesModel.gates_list.length,
                        (index) {
                      final gate = pageGatesModel.gates_list[index];
                      String chinese_gate = "";
                      if (pageGatesModel.binding_name_exists(gate)) {
                        chinese_gate = pageGatesModel
                            .english_to_chinese_door_name_dict[gate];
                      } else {
                        chinese_gate = gate;
                      }
                      final door_state = pageGatesModel.is_door_open(gate);
                      return Container(
                        height: 0.08 * height,
                        child: ListTile(
                          title: Text(
                            '${chinese_gate}',
                            style: TextStyle(
                                color: Colors.black, fontSize: width * 0.05),
                          ),
                          trailing: CupertinoSwitch(
                            value: door_state,
                            onChanged: (bool value) {
                              onTapFunction(gate, door_state);
                            },
                          ),
                          onTap: () {
                            onTapFunction(gate, door_state);
                          },
                        ),
                      );
                    }),
                  ),
                ),
              ),
            ],
          ),
        )));
  }
}
