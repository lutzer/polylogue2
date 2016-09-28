package com.drl.polylogue2;

import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

import com.drl.polylogue2.utils.AlarmReceiver;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Calendar;


public class MainActivity extends AppCompatActivity {

    public static String LOG_TAG = "MAZI-ACTIVTY: ";

    public static Logger Log;

    private BroadcastReceiver mMessageReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            Log.debug(LOG_TAG + "Got return message from broadcast receiver, connected to socket.");
            onSocketConnected();
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Logging
        Log = LoggerFactory.getLogger(MainActivity.class);

        // broadcast manager to communicate with service
        LocalBroadcastManager.getInstance(this).registerReceiver(mMessageReceiver, new IntentFilter(ForegroundService.CONNECTED_BROADCAST));

        // start service
        Intent service = new Intent(MainActivity.this, ForegroundService.class);
        service.setAction(ForegroundService.ServiceAction.CONNECT);
        startService(service);


        Log.debug(LOG_TAG + "Activity started");

    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        // Unregister since the activity is about to be closed.
        LocalBroadcastManager.getInstance(this).unregisterReceiver(mMessageReceiver);
    }

    public void onButtonClicked(View view) {
        finish();
    }

    private void onSocketConnected() {
        findViewById(R.id.spinner).setVisibility(View.GONE);
        findViewById(R.id.invisibleLayout).setVisibility(View.VISIBLE);
    }
}
