import 'package:gateman/utils.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'models.dart';

SharedPreferences prefs;

class Database {
  Database() {}

  init() async {
    prefs = await SharedPreferences.getInstance();
  }

  void set service_ip(String text) {
    prefs.setString("service_ip", text);
  }

  String get service_ip {
    return prefs.getString("service_ip") ?? "";
  }

  void set password(String text) {
    prefs.setString("password", text);
  }

  String get password {
    return prefs.getString("password") ?? "";
  }

  void set doors_that_open(List<String> doors) {
    prefs.setStringList("doors_that_open", doors);
  }

  List<String> get doors_that_open {
    return prefs.getStringList("doors_that_open") ?? [];
  }

  Map<String, String> get english_to_chinese_door_name_dict {
    Map<String, String> map = {};
    String raw = prefs.getString("english_to_chinese_door_name_dict") ??
        Utils.json_dumps(map);
    return Map<String, String>.from(Utils.json_loads(raw));
  }

  void set english_to_chinese_door_name_dict(Map<String, String> object) {
    String text = Utils.json_dumps(object);
    prefs.setString("english_to_chinese_door_name_dict", text);
  }
}
