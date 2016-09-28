package com.drl.polylogue2;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Handler;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.support.v4.app.NotificationCompat;
import android.support.v4.content.LocalBroadcastManager;


import org.json.JSONException;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.URISyntaxException;

import com.github.nkzawa.emitter.Emitter;
import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;

/**
 * Created by lutz on 26/09/16.
 */
public class ForegroundService extends Service {

    public static String WEBSOCKET_URL = "http://192.168.1.4:8081";
    public static int NOTIFICATION_ID = 101;
    public final int CONNECTION_CHECK_INTERVAL = 10000;

    public static String DELIVERED_BROADCAST = "delivered-broadcast";
    public static String CONNECTED_BROADCAST = "connected-broadcast";

    private Logger Log;
    private static String LOG_TAG = "MAZI-SERVICE: ";

    public interface ServiceAction {
        public String CONNECT = "connect";
        public String SEND_MESSSAGE = "Send Message";
    }

    private Socket socket;

    private Emitter.Listener onNewSubmission = new Emitter.Listener() {

        @Override
        public void call(Object... args) {

            JSONObject json = new JSONObject();

            try {
                json = (JSONObject) args[0];
            } catch (Exception e) {
                Log.error(e.getMessage());
                return;
            }

            Log.info(LOG_TAG + "Received Submission: " + json.toString());

            try {
                showNotification("Message Received",NOTIFICATION_ID,json.getString("message"));
            } catch (JSONException e) {
                Log.error(e.getMessage());
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

    // timer checks the connection every few seconds
    private Handler connectionTimer = new Handler();
    private Runnable connectionChecker = new Runnable() {

        @Override
        public void run() {
            try {
                connectWebsocket();
            } finally {
                connectionTimer.postDelayed(connectionChecker, CONNECTION_CHECK_INTERVAL);
            }
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

        Log.info(LOG_TAG + "Service created");
        connectionChecker.run();

    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.info(LOG_TAG + "received command");

        if (intent != null) {

            if (intent.getAction().equals(ServiceAction.SEND_MESSSAGE)) {

                String message = intent.getStringExtra("message");

                // send message to server
                boolean msgDelivered = sendMessage("290480-324ß-fake-id", message);

                //answer to activity
                Intent retIntent = new Intent(DELIVERED_BROADCAST);
                retIntent.putExtra("msgDelivered", msgDelivered);
                LocalBroadcastManager.getInstance(this).sendBroadcast(retIntent);

            } else if (intent.getAction().equals(ServiceAction.CONNECT)) {

                if (socket.connected()) {
                    //answer that socket is connected
                    Intent retIntent = new Intent(CONNECTED_BROADCAST);
                    LocalBroadcastManager.getInstance(this).sendBroadcast(retIntent);
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
        connectionTimer.removeCallbacksAndMessages(null);
        Log.info(LOG_TAG + "Service stopped");
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    public boolean sendMessage(String submissionId, String message) {

        JSONObject json = new JSONObject();

        try {
            json.put("_id", submissionId);
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
            Log.info(LOG_TAG + "Connecting to socket: " + getResources().getString(R.string.websocketUrl));
            socket.connect();
        }
    }

    private void showNotification(String action, int messageId, String message) {

        Log.debug(LOG_TAG + "showing notifiation");

        Intent notificationIntent = new Intent(this, AnswerActivity.class);
        notificationIntent.setAction(action);
        PendingIntent resultPendingIntent =
            PendingIntent.getActivity(this, 0, notificationIntent, PendingIntent.FLAG_UPDATE_CURRENT );


        Uri notificationSound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(this)
            .setSound(notificationSound)
                .setSmallIcon(R.drawable.message)
            .setContentTitle(action)
            .setContentText(message)
                .setContentIntent(resultPendingIntent)
            .setAutoCancel(true);

        // Gets an instance of the NotificationManager service
        NotificationManager mNotifyMgr = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        // Builds the notification and issues it.
        mNotifyMgr.notify(messageId, mBuilder.build());
    }

}
