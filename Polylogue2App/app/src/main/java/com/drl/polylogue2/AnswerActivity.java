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
import android.widget.TextView;
import android.widget.Toast;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AnswerActivity extends AppCompatActivity {

    public static String LOG_TAG = "MAZI-ANSWER-ACTIVITY: ";
    private Logger Log;

    private String submissionId = "";

    private BroadcastReceiver mMessageReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            boolean msgDevilvered = intent.getBooleanExtra("msgDelivered", false);
            Log.debug(LOG_TAG + "Got return message from broadcast receiver, message delivered: " + msgDevilvered);
            onMessageDelivered(msgDevilvered);
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_answer);

        // broadcast manager to communicate with service
        LocalBroadcastManager.getInstance(this).registerReceiver(mMessageReceiver, new IntentFilter(ForegroundService.DELIVERED_BROADCAST));

        //logging
        Log = LoggerFactory.getLogger(ForegroundService.class);
        Log.debug(LOG_TAG + "Activity created");

        //set message
        if (this.getIntent().hasExtra("message")) {
            String message = this.getIntent().getStringExtra("message");
            TextView messageView = (TextView) findViewById(R.id.messageView);
            messageView.setText(message);
        }

        //set input focus
        findViewById(R.id.editText).requestFocus();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        // Unregister since the activity is about to be closed.
        LocalBroadcastManager.getInstance(this).unregisterReceiver(mMessageReceiver);
        Log.debug(LOG_TAG + "Activity destroyed");
    }

    public void onButtonClicked(View view) {

        EditText editText = (EditText)findViewById(R.id.editText);

        Intent service = new Intent(AnswerActivity.this, ForegroundService.class);
        service.putExtra("message", editText.getText().toString());
        //set message
        if (this.getIntent().hasExtra("id")) {
            String id = this.getIntent().getStringExtra("id");
            service.putExtra("id", id);
        }
        service.setAction(ForegroundService.ServiceAction.SEND_MESSSAGE);
        startService(service);
    }

    public void onMessageDelivered(boolean delivered) {
        if (delivered) {
            Toast.makeText(this, "Message succesfully sent.", Toast.LENGTH_LONG).show();
            finish();
        } else
            Toast.makeText(this, "ERROR: Message could not be sent. Check your internet connection and try again.", Toast.LENGTH_LONG).show();

    }
}
