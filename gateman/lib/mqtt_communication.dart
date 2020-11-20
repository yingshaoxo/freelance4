import 'dart:async';
import 'package:gateman/database.dart';
import 'package:gateman/main.dart';
import 'package:mqtt_client/mqtt_server_client.dart';
import 'package:mqtt_client/mqtt_client.dart';
import 'utils.dart';
import 'package:wifi/wifi.dart';
import 'package:ping_discover_network/ping_discover_network.dart';
import 'package:tcp_scanner/tcp_scanner.dart';

MqttServerClient client = null;

class MyMQTT {
  static Future<void> connect() async {
    // Create and connect the client
    final url = database.service_ip; // The google iot-core MQTT bridge server
    print(url);
    const port = 1883; // You can also use 8883 if you so wish
    // The client id is a path to your device, example given below, note this contravenes the 23 character client id length
    // from the MQTT specification, the mqtt_client allows this, if exceeded and logging is turned on  a warning is given.
    const clientId = 'client/controller';
    // User name is not used and can be set to anything, it is needed because the password field contains the encoded JWT token for the device
    client = MqttServerClient(url, clientId);
    // Set the port
    client.port = port;
    // Set secure
    client.secure = false;
    client.setProtocolV311();
    // logging if you wish
    client.logging(on: true);
    client.autoReconnect = true;
    await client.connect();
  }

  static Future<bool> is_service_avaliable() async {
    return await Utils.is_port_open(database.service_ip, 1883);
  }

  static Future<void> make_sure_it_is_connected() async {
    while (client == null) {
      await Utils.sleep(1);
    }
    while (client.connectionStatus.state != MqttConnectionState.connected) {
      await Utils.sleep(1);
    }
  }

  static void publish(String topic, String content) {
    client.publishMessage(
        topic, MqttQos.exactlyOnce, Utils.text_to_buffer(content));
  }

  static void subscribe(String topic) {
    client.subscribe(topic, MqttQos.exactlyOnce);
  }

  static set_callback_for_a_topic(String topic, Function(String) handler) {
    client.updates.listen((List<MqttReceivedMessage<MqttMessage>> c) {
      c.forEach((c) {
        final MqttPublishMessage recMess = c.payload;
        //final pt = MqttPublishPayload.bytesToStringAsString(recMess.payload.message);
        final text = Utils.buffer_to_text(recMess.payload.message);
        print('topic is <${c.topic}>, payload is <-- $text -->');
        if (c.topic == topic) {
          handler(text);
        }
      });
    });
  }
}
