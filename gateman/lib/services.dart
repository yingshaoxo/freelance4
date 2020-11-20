import 'package:flutter/services.dart';

class FlutterNativeAction {
  static const MethodChannel _channel =
      const MethodChannel('flutter_native_action');

  static Future<String> get platformVersion async {
    final String version = await _channel.invokeMethod('getPlatformVersion');
    return version;
  }

  static Future<void> openHotspotSettingPage() async {
    await _channel.invokeMethod('openHotspotSettingPage');
  }

  static Future<void> openWiFiSettingPage() async {
    await _channel.invokeMethod('openWiFiSettingPage');
  }

  static Future<void> startMQTTService() async {
    await _channel.invokeMethod('startMQTTService');
  }
}
