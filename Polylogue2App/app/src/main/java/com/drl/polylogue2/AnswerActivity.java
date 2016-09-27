package com.drl.polylogue2;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AnswerActivity extends AppCompatActivity {

    public static String LOG_TAG = "MAZI-ANSWER-ACTIVITY: ";
    private Logger Log;

    private BroadcastReceiver mMessageReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            boolean msgDevilvered = intent.getBooleanExtra("msgDelivered", false);
            Log.debug(LOG_TAG + "Got return message from broadcast receiver, message delivered: " + msgDevilvered);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_answer);

        // broadcast manager to communicate with service
        LocalBroadcastManager.getInstance(this).registerReceiver(mMessageReceiver, new IntentFilter(ForegroundService.SERVICE_NAME));

        //logging
        Log = LoggerFactory.getLogger(ForegroundService.class);
    }

    @Override
    protected void onDestroy() {
        Log.info(LOG_TAG + "Activity in onDestroy");
        // Unregister since the activity is about to be closed.
        LocalBroadcastManager.getInstance(this).unregisterReceiver(mMessageReceiver);
        super.onDestroy();

        Log.info(LOG_TAG + "Activity destroyed");
    }

    public void onButtonClicked(View view) {

        EditText editText = (EditText)findViewById(R.id.editText);

        Intent service = new Intent(AnswerActivity.this, ForegroundService.class);
        service.putExtra("message", editText.getText().toString());
        service.setAction(ForegroundService.ServiceAction.SEND_MESSSAGE);
        startService(service);
    }
}
