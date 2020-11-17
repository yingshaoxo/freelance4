package com.example.gateman;

import android.content.Context;
import android.content.Intent;

import static android.provider.Settings.ACTION_WIFI_SETTINGS;
import static androidx.core.content.ContextCompat.startActivity;

public class JavaToolKit {
    private Context context;

    JavaToolKit(Context context) {
        this.context = context;
    }

    public void open_hotspot_setting_page() {
        Intent tetherSettings = new Intent();
        tetherSettings.setClassName("com.android.settings", "com.android.settings.TetherSettings");
        startActivity(context, tetherSettings, null);
    }

    public void open_wifi_setting_page() {
        startActivity(context, new Intent(android.provider.Settings.ACTION_WIFI_SETTINGS), null);
    }
}
