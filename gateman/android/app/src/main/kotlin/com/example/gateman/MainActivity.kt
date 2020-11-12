package com.example.gateman


import android.app.Activity
import android.content.Context
import androidx.annotation.RequiresApi
import android.os.Build
import androidx.annotation.NonNull
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.embedding.engine.plugins.FlutterPlugin
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import io.flutter.embedding.engine.plugins.activity.ActivityPluginBinding
import io.flutter.plugin.common.MethodChannel.MethodCallHandler
import io.flutter.plugin.common.MethodChannel.Result

import com.example.gateman.Toolkt

class MainActivity: FlutterActivity() {
    private val CHANNEL = "flutter_native_action"
    private lateinit var toolkt: Toolkt

    override fun onContentChanged() {
        super.onContentChanged()
        toolkt = Toolkt(this.context) ;
    }

    override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler {
            call, result ->
            if (call.method == "getPlatformVersion") {
                result.success("Android ${android.os.Build.VERSION.RELEASE}")
            } else if (call.method == "openHotspotSettingPage") {
                toolkt.open_hotspot_setting_page()
                result.success("ok")
            } else {
                result.notImplemented()
            }
        }
    }
}
