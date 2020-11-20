import 'dart:ffi';
import 'dart:typed_data';
import 'package:string_validator/string_validator.dart';
import 'package:typed_data/typed_data.dart' as typed;
import 'dart:convert';
import 'package:tcp_scanner/tcp_scanner.dart';
import 'dart:math';

class Utils {
  // Utility
  static typed.Uint8Buffer text_to_buffer(String text) {
    Uint8List data = utf8.encode(text);
    var dataBuffer = typed.Uint8Buffer();
    dataBuffer.addAll(data);
    return dataBuffer;
  }

  static String buffer_to_text(typed.Uint8Buffer buff) {
    String text = utf8.decode(Uint8List.view(buff.buffer, 0, buff.length));
    return text;
  }

  static Future<Void> sleep(int how_long) async {
    await new Future.delayed(Duration(seconds: how_long));
  }

  static Future<bool> is_port_open(String ip, int port) async {
    if (!isIP(ip, 4)) {
      return false;
    }

    ScanResult result = await TCPScanner(ip, [port]).scan();

    print('''
HTTP ports scan result
Host:          ${result.host}
Scanned ports: ${result.ports}
Open ports:    ${result.open}
Closed ports:  ${result.closed}
Elapsed time:  ${result.elapsed / 1000}s
''');

    if (result.open.contains(port)) {
      return true;
    } else {
      return false;
    }
  }

  static String getRandomString(int len) {
    var r = Random();
    const _chars = 'abcdefghijklmnopqrstuvwxyz';
    return List.generate(len, (index) => _chars[r.nextInt(_chars.length)])
        .join();
  }

  static String json_dumps(dynamic object) {
    return json.encode(object);
  }

  static dynamic json_loads(String text) {
    return json.decode(text);
  }
}
