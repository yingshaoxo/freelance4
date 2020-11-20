import 'dart:async';

import 'package:flutter/material.dart';
import 'package:gateman/utils.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:provider/provider.dart';
import 'package:flutter_staggered_grid_view/flutter_staggered_grid_view.dart';
import 'package:pinput/pin_put/pin_put.dart';

import 'models.dart';
import 'main.dart';
import 'mqtt_communication.dart';

class PagePassword extends StatefulWidget {
  @override
  _PagePasswordState createState() => _PagePasswordState();
}

class _PagePasswordState extends State<PagePassword> {
  PagePasswordModel pagePasswordModel;

  final TextEditingController _pinPutController = TextEditingController();
  final FocusNode _pinPutFocusNode = FocusNode();

  BoxDecoration get _pinPutDecoration {
    return BoxDecoration(
      border: Border.all(color: Colors.deepPurpleAccent),
      borderRadius: BorderRadius.circular(15.0),
    );
  }

  @override
  void didChangeDependencies() async {
    super.didChangeDependencies();
  }

  @override
  Widget build(BuildContext context) {
    var pageGatesModel = Provider.of<PageGatesModel>(context, listen: false);
    var pagePasswordModel =
        Provider.of<PagePasswordModel>(context, listen: false);

    _pinPutController.text = pagePasswordModel.password;

    return Center(
        child: SingleChildScrollView(
            child: Column(mainAxisSize: MainAxisSize.min, children: <Widget>[
      Container(
        color: Colors.white,
        margin: const EdgeInsets.all(20.0),
        padding: const EdgeInsets.all(20.0),
        child: PinPut(
          fieldsCount: 5,
          onSubmit: (String pin) {
            pagePasswordModel.password = pin;
          },
          focusNode: _pinPutFocusNode,
          controller: _pinPutController,
          submittedFieldDecoration: _pinPutDecoration.copyWith(
            borderRadius: BorderRadius.circular(20.0),
          ),
          selectedFieldDecoration: _pinPutDecoration,
          followingFieldDecoration: _pinPutDecoration.copyWith(
            borderRadius: BorderRadius.circular(5.0),
            border: Border.all(
              color: Colors.deepPurpleAccent.withOpacity(.5),
            ),
          ),
        ),
      ),
      const SizedBox(height: 30.0),
      const Divider(),
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: <Widget>[
          FlatButton(
            onPressed: () {
              _pinPutController.text = '';
              _pinPutFocusNode.unfocus();
            },
            child: const Text('重新输入'),
          ),
          FlatButton(
            onPressed: () {
              pagePasswordModel.password = _pinPutController.text;
              _pinPutFocusNode.unfocus();
            },
            child: const Text('确认设置'),
          ),
        ],
      )
    ])));
  }
}
