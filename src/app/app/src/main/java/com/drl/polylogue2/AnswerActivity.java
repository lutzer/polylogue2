package com.drl.polylogue2;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.CountDownTimer;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.InputFilter;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.TextUtils;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.drl.polylogue2.models.Question;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Date;
import java.util.regex.Pattern;

public class AnswerActivity extends AppCompatActivity {

    public static String LOG_TAG = "MAZI-ANSWER-ACTIVITY: ";
    private Logger Log;

    private Question question;

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
        if (intent.hasExtra("question")) {
            question = (Question) intent.getSerializableExtra("question");
            Log.debug(LOG_TAG + "New Intent with question: " + question.toString());

            TextView messageView = (TextView) findViewById(R.id.messageView);
            messageView.setText(question.question);

            //set input focus
            EditText editText = (EditText)findViewById(R.id.editText);
            editText.requestFocus();

            //set input filter to only allow asci
            InputFilter asciFilter = new InputFilter() {

                @Override
                public CharSequence filter(CharSequence source, int start, int end, Spanned dest, int dstart, int dend) {

                    boolean keepOriginal = true;
                    StringBuilder sb = new StringBuilder(end - start);
                    for (int i = start; i < end; i++) {
                        char c = source.charAt(i);
                        if (isCharAllowed(c)) // put your condition here
                            sb.append(c);
                        else
                            keepOriginal = false;
                    }
                    if (keepOriginal)
                        return null;
                    else {
                        if (source instanceof Spanned) {
                            SpannableString sp = new SpannableString(sb);
                            TextUtils.copySpansFrom((Spanned) source, start, sb.length(), null, sp, 0);
                            return sp;
                        } else {
                            return sb;
                        }
                    }
                }

                private boolean isCharAllowed(char c) {
                    return Pattern.matches("[\\x1f-\\x80]", Character.toString(c));
                }

            };
            editText.setFilters(new InputFilter[] { asciFilter });

                    //setup expiration time
            Date expiresAt = question.getExpiresAt();
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
        service.putExtra("questionId", question._id);
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
