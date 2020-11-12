package com.example.gateman;

import android.content.Context;
import android.content.Intent;

import static androidx.core.content.ContextCompat.startActivity;

public class Toolkt {
    private Context context;

    Toolkt(Context context) {
        this.context = context;
    }

    public void open_hotspot_setting_page() {
        Intent tetherSettings = new Intent();
        tetherSettings.setClassName("com.android.settings", "com.android.settings.TetherSettings");
        startActivity(context, tetherSettings, null);
    }
}
