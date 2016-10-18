package com.drl.polylogue2;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.CountDownTimer;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.drl.polylogue2.models.Submission;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Date;

public class AnswerActivity extends AppCompatActivity {

    public static String LOG_TAG = "MAZI-ANSWER-ACTIVITY: ";
    private Logger Log;

    private Submission submission;

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

        initView();

    }

    private void initView() {
        //set message
        Intent intent = getIntent();
        if (intent.hasExtra("submission")) {
            submission = (Submission) intent.getSerializableExtra("submission");
            Log.debug(LOG_TAG + "New Intent with submission: " + submission.toString());

            TextView messageView = (TextView) findViewById(R.id.messageView);
            messageView.setText(submission.message);

            //set input focus
            findViewById(R.id.editText).requestFocus();

            //setup expiration time
            Date expiresAt = submission.getExpiresAt();
            startTimer(expiresAt.getTime() - new Date().getTime());
        }
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
        service.putExtra("submissionId", submission._id);
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

    private void startTimer(long timeRemaining) {

        final TextView timerText = (TextView) findViewById(R.id.timerView);

        new CountDownTimer(timeRemaining, 1000) {

            public void onTick(long millisUntilFinished) {
                timerText.setText("Question expires in " + millisUntilFinished / 1000 + " seconds.");
            }

            public void onFinish() {
                timerText.setText("Question expired");
            }
        }.start();
    }
}
