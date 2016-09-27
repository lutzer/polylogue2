package com.drl.polylogue2;

import android.Manifest;
import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class MainActivity extends AppCompatActivity {

    public static String LOG_TAG = "MAZI-ACTIVTY: ";

    public static Logger Log;
    //static { BasicLogcatConfigurator.configureDefaultContext(); } // log to logcat

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Logging
        Log = LoggerFactory.getLogger(MainActivity.class);

        // start service
        Intent service = new Intent(MainActivity.this, ForegroundService.class);
        service.setAction(ForegroundService.ServiceAction.CONNECT);
        startService(service);

        Log.info(LOG_TAG + "Activity started");

        //Log.debug(LOG_TAG + "Internal files dir: " + this.getFilesDir().getAbsolutePath() );

        // debugging
        /*Thread.currentThread().setUncaughtExceptionHandler(new Thread.UncaughtExceptionHandler() {
            @Override
            public void uncaughtException(Thread thread, Throwable ex) {
                Log.error(MainActivity.LOG_TAG,ex.getMessage());

                ex.printStackTrace();

            }
        });*/

    }

    @Override
    protected void onDestroy() {
        Log.info(LOG_TAG + "Activity in onDestroy");
        super.onDestroy();

        Log.info(LOG_TAG + "Activity destroyed");
    }

    public void onButtonClicked(View view) {
        Button button = (Button) view;
        Intent service = new Intent(MainActivity.this, ForegroundService.class);
        service.putExtra("message", "Hello Websocket!");
        service.setAction(ForegroundService.ServiceAction.SEND_MESSSAGE);
        startService(service);
    }
}
