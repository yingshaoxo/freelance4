import 'package:flutter/material.dart';
import 'package:gateman/mqtt_communication.dart';
import 'dart:convert';

import 'main.dart';

class AppModel extends ChangeNotifier {
  String _service_ip = "";
  String _current_page = "page_check_wifi";

  AppModel() {
    _service_ip = database.service_ip;
  }

  String get service_ip {
    return _service_ip;
  }

  set service_ip(String ip) {
    if (ip != this._service_ip) {
      this._service_ip = ip;
      database.service_ip = ip;
      notifyListeners();
    }
  }

  String get current_page {
    return this._current_page;
  }

  set current_page(String value) {
    if (value != this._current_page) {
      this._current_page = value;
      notifyListeners();
    }
  }
}

class PageCheckWiFiModel extends ChangeNotifier {
  PageCheckWiFiModel() {}
}

class PageCheckServiceModel extends ChangeNotifier {
  final textController = TextEditingController();

  PageCheckServiceModel() {}
}

class PageTabsModel extends ChangeNotifier {
  int _tabIndex = 0;

  PageTabsModel() {}

  int get tab_index {
    return _tabIndex;
  }

  void set tab_index(int value) {
    if (value != _tabIndex) {
      _tabIndex = value;
      notifyListeners();
    }
  }
}

class PageGatesModel extends ChangeNotifier {
  List<String> _gates_list = [];
  List<String> _doors_that_open = [];
  bool _name_binding_mode = false;
  Map<String, String> _english_to_chinese_door_name_dict = {};
  final textController = TextEditingController();

  PageGatesModel() {
    _doors_that_open = database.doors_that_open;
    _english_to_chinese_door_name_dict =
        database.english_to_chinese_door_name_dict;
  }

  bool get name_binding_mode {
    return _name_binding_mode;
  }

  void set name_binding_mode(bool value) {
    if (value != _name_binding_mode) {
      _name_binding_mode = value;
      notifyListeners();
    }
  }

  bool binding_name_exists(String key) {
    return _english_to_chinese_door_name_dict.containsKey(key);
  }

  void add_binding_name(String english, String chinese) {
    _english_to_chinese_door_name_dict.update(
      english,
      (existingValue) => chinese,
      ifAbsent: () => chinese,
    );
    database.english_to_chinese_door_name_dict =
        _english_to_chinese_door_name_dict;
    notifyListeners();
  }

  Map<String, String> get english_to_chinese_door_name_dict {
    return _english_to_chinese_door_name_dict;
  }

  List<String> get gates_list {
    return _gates_list;
  }

  List<String> get doors_that_open {
    return _doors_that_open;
  }

  bool add_a_gate(String gate) {
    if (!_gates_list.contains(gate)) {
      _gates_list.add(gate);
      notifyListeners();
      return true;
    }
    return false;
  }

  void open_a_door(String gate) {
    if (_gates_list.contains(gate)) {
      _doors_that_open.add(gate);
      database.doors_that_open = _doors_that_open;
      notifyListeners();
    }
  }

  void close_a_door(String gate) {
    if (_gates_list.contains(gate)) {
      if (_doors_that_open.contains(gate)) {
        _doors_that_open.remove(gate);
        database.doors_that_open = _doors_that_open;
        notifyListeners();
      }
    }
  }

  bool is_door_open(String gate) {
    if (_gates_list.contains(gate)) {
      if (_doors_that_open.contains(gate)) {
        return true;
      }
    }
    return false;
  }

  void send_open_doors_info_out() {
    MyMQTT.publish("doors_that_open", jsonEncode(_doors_that_open));
  }
}

class PagePasswordModel extends ChangeNotifier {
  String _password = "";

  PagePasswordModel() {
    _password = database.password;
  }

  String get password {
    return _password;
  }

  void set password(String value) {
    if (value != _password) {
      _password = value;
      database.password = _password;
    }
    send_password_info_out();
  }

  void send_password_info_out() {
    MyMQTT.publish("password", _password);
  }
}
