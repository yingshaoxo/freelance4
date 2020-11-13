package com.example.gateman


import androidx.annotation.NonNull
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

import darkmqtt.Darkmqtt

class MainActivity: FlutterActivity() {
    private val CHANNEL = "flutter_native_action"
    private lateinit var javaToolKit: JavaToolKit
    private lateinit var mqtt_service_thread: Thread

    override fun onContentChanged() {
        super.onContentChanged()
        javaToolKit = JavaToolKit(this.context);
    }

    override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler {
            call, result ->
            if (call.method == "getPlatformVersion") {
                result.success("Android ${android.os.Build.VERSION.RELEASE}")
            } else if (call.method == "openHotspotSettingPage") {
                javaToolKit.open_hotspot_setting_page()
                result.success("ok")
            } else if (call.method == "startMQTTService") {
                if (!this::mqtt_service_thread.isInitialized) {
                    mqtt_service_thread = Thread({
                        Darkmqtt.run()
                    })
                    mqtt_service_thread.isDaemon = true
                    mqtt_service_thread.start()
                } else {
                    if (!mqtt_service_thread.isAlive) {
                        mqtt_service_thread.start()
                    }
                }
            } else {
                result.notImplemented()
            }
        }
    }
}
