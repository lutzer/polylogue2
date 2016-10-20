package com.drl.polylogue2;

import android.app.AlarmManager;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.support.v4.app.NotificationCompat;
import android.support.v4.content.LocalBroadcastManager;


import org.json.JSONException;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.URISyntaxException;
import java.util.ArrayList;

import com.drl.polylogue2.models.Submission;
import com.drl.polylogue2.utils.AlarmReceiver;
import com.github.nkzawa.emitter.Emitter;
import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;

/**
 * Created by lutz on 26/09/16.
 */
public class ForegroundService extends Service {

    //public static String WEBSOCKET_URL = "http://lu-re.de:8090";
    public static String WEBSOCKET_URL = "http://192.168.1.5:8090";
    public static int NOTIFICATION_ID = 101;
    public final int CONNECTION_CHECK_INTERVAL = 5000;

    public static String DELIVERED_BROADCAST = "delivered-broadcast";
    public static String CONNECTED_BROADCAST = "connected-broadcast";

    private Logger Log;
    private static String LOG_TAG = "MAZI-SERVICE: ";

    public interface ServiceAction {
        String CONNECT = "connect";
        String SEND_MESSSAGE = "Send Message";
        String CHECK_CONNECT = "check connection";
    }

    private Socket socket;
    ArrayList<String> fetchedSubmissions;

    private Emitter.Listener onNewSubmission = new Emitter.Listener() {

        @Override
        public void call(Object... args) {

            Submission submission;

            try {
                JSONObject json = (JSONObject) args[0];
                submission = new Submission(json);
            } catch (Exception e) {
                Log.error(e.getMessage());
                return;
            }

            // check if message already displayed
            if (!fetchedSubmissions.contains(submission._id)) {
                Log.info(LOG_TAG + "Received Submission: " + submission.toString());
                showNotification("New Polylogue Question", submission);
                fetchedSubmissions.add(submission._id);
            }
        }
    };

    private Emitter.Listener onSocketConnected = new Emitter.Listener() {

        @Override
        public void call(Object... args) {

            Log.info(LOG_TAG + "Socket Connected");

            //answer to activity
            Intent retIntent = new Intent(CONNECTED_BROADCAST);
            LocalBroadcastManager.getInstance(getApplicationContext()).sendBroadcast(retIntent);

        }
    };

    @Override
    public void onCreate() {
        super.onCreate();

        //logging
        Log = LoggerFactory.getLogger(ForegroundService.class);

        try {
            socket = IO.socket(WEBSOCKET_URL);
            socket.on("submission:new",onNewSubmission);
            socket.on("connected", onSocketConnected);

        } catch (URISyntaxException e) {
            Log.error(LOG_TAG + e.getMessage());
        }

        fetchedSubmissions = new ArrayList();

        Log.info(LOG_TAG + "Service created");

        connectWebsocket();

        keepServiceAlive();

    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {

        if (intent != null) {

            Log.debug(LOG_TAG + "received command: "  + intent.getAction());

            if (intent.getAction().equals(ServiceAction.SEND_MESSSAGE)) {

                String message = intent.getStringExtra("message");
                String submissionId = intent.getStringExtra("submissionId");

                // send message to server
                boolean msgDelivered = sendMessage(submissionId, message);

                //answer to activity
                Intent retIntent = new Intent(DELIVERED_BROADCAST);
                retIntent.putExtra("msgDelivered", msgDelivered);
                LocalBroadcastManager.getInstance(this).sendBroadcast(retIntent);

            } else if (intent.getAction().equals(ServiceAction.CHECK_CONNECT)) {

                if (socket.connected()) {
                    //answer that socket is connected
                    onSocketConnected.call();
                }

            } else if (intent.getAction().equals(ServiceAction.CONNECT)) {

                if (!socket.connected()) {
                    connectWebsocket();
                }
            }
        }

        // keep service running until stopped
        return Service.START_STICKY;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.debug(LOG_TAG + "In onDestroy");

        if (socket != null && socket.connected()) {
            socket.disconnect();
            socket.off("submission:new", onNewSubmission);
            socket.off("connected", onSocketConnected);
        }

        //TODO: cancel alarmmanager
        //connectionTimer.removeCallbacksAndMessages(null);
        Log.info(LOG_TAG + "Service stopped");
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }


    //keeps service running even if screen turned off
    public void keepServiceAlive() {

        Intent myAlarm = new Intent(getApplicationContext(), AlarmReceiver.class);
        PendingIntent recurringAlarm = PendingIntent.getBroadcast(getApplicationContext(), 0, myAlarm, PendingIntent.FLAG_CANCEL_CURRENT);
        AlarmManager alarms = (AlarmManager) this.getSystemService(Context.ALARM_SERVICE);
        alarms.setRepeating(AlarmManager.RTC_WAKEUP, System.currentTimeMillis(),
                CONNECTION_CHECK_INTERVAL, recurringAlarm);
    }

    public boolean sendMessage(String submissionId, String message) {

        JSONObject json = new JSONObject();

        try {
            json.put("submissionId", submissionId);
            json.put("message", message);
        } catch (JSONException e) {
            Log.error(e.getMessage());
            e.printStackTrace();
        }

        if (socket != null && socket.connected()) {
            socket.emit("message:new",json);
            return true;
        }
        return false;
    }

    public void connectWebsocket() {

        if (socket != null && !socket.connected()) {
            Log.info(LOG_TAG + "Connecting to socket: " + WEBSOCKET_URL);
            socket.connect();
        }
    }

    private void showNotification(String action, Submission submission) {

        // do not notify for a submission twice

        Log.debug(LOG_TAG + "showing notifiation");

        Intent notificationIntent = new Intent(this, AnswerActivity.class);
        notificationIntent.addFlags(Intent.FLAG_ACTIVITY_MULTIPLE_TASK); // start new activity
        notificationIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        notificationIntent.setAction(action);
        notificationIntent.putExtra("submission", submission);
        PendingIntent resultPendingIntent =
            PendingIntent.getActivity(this, submission.boxId, notificationIntent, PendingIntent.FLAG_UPDATE_CURRENT);


        Uri notificationSound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(this)
            .setSound(notificationSound)
            .setSmallIcon(R.drawable.message)
            .setContentTitle(action)
            .setContentText(submission.message)
            .setContentIntent(resultPendingIntent)
            .setAutoCancel(true);

        // Gets an instance of the NotificationManager service
        NotificationManager mNotifyMgr = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        // Builds the notification and issues it.
        mNotifyMgr.notify(submission.boxId, mBuilder.build());
    }

}