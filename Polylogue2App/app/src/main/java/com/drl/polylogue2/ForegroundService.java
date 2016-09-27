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

import java.io.UnsupportedEncodingException;

import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketException;
import de.tavendo.autobahn.WebSocketHandler;

/**
 * Created by lutz on 26/09/16.
 */
public class ForegroundService extends Service {

    public static String SERVICE_NAME = "mazi-service";
    public static int NOTIFICATION_ID = 101;
    public final String WEBSOCKET_URL = "ws://echo.websocket.org";
    public final int CONNECTION_CHECK_INTERVAL = 10000;

    private Logger Log;
    private static String LOG_TAG = "MAZI-SERVICE: ";

    public interface ServiceAction {
        public String CONNECT = "connect";
        public String SEND_MESSSAGE = "Send Message";
    }


    private final WebSocketConnection socket = new WebSocketConnection();

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
                Intent retIntent = new Intent(SERVICE_NAME);
                retIntent.putExtra("msgDelivered", msgDelivered);
                LocalBroadcastManager.getInstance(this).sendBroadcast(retIntent);

            }
        }

        // keep service running until stopped
        return Service.START_STICKY;
    }

    private void showNotification(String action, int messageId, String message) {

        Log.debug(LOG_TAG + "show notifiation");

        Intent notificationIntent = new Intent(this, AnswerActivity.class);
        notificationIntent.setAction(action);
        PendingIntent resultPendingIntent =
            PendingIntent.getActivity(this, 0, notificationIntent, PendingIntent.FLAG_UPDATE_CURRENT );


        Uri notificationSound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        NotificationCompat.Builder mBuilder =
            new NotificationCompat.Builder(this)
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

    @Override
    public void onDestroy() {
        Log.debug(LOG_TAG + "In onDestroy");
        super.onDestroy();
        if (socket.isConnected())
            socket.disconnect();
        connectionTimer.removeCallbacksAndMessages(null);
        Log.info(LOG_TAG + "Service stopped");
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    public boolean sendMessage(String submissionId, String message) {

        byte[] payload = "{}".getBytes();

        try {

            JSONObject json = new JSONObject();
            json.put("_id", submissionId);
            json.put("message", message);
            payload  = json.toString().getBytes("UTF-8");
        } catch (JSONException e) {
            Log.error(e.getMessage());
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            Log.error(e.getMessage());
            e.printStackTrace();
        }

        if (socket.isConnected()) {
            socket.sendRawTextMessage(payload);
            return true;
        }
        return false;
    }

    public void connectWebsocket() {

        if (!socket.isConnected()) {

            Log.debug(LOG_TAG + "Connecting to socket.");

            try {

                socket.connect(WEBSOCKET_URL, new WebSocketHandler() {

                    @Override
                    public void onOpen() {
                        Log.info(LOG_TAG + "Status: Connected to " + WEBSOCKET_URL);
                    }

                    @Override
                    public void onTextMessage(String payload) {

                        JSONObject json;

                        try {
                            json = new JSONObject(payload);
                        } catch (JSONException e) {
                            Log.error(e.getMessage());
                            e.printStackTrace();
                            return;
                        }

                        try {
                            Log.info(LOG_TAG + "Received message: " + json.toString());
                            showNotification("Message Received", NOTIFICATION_ID, json.getString("message"));
                        } catch (JSONException e) {
                            Log.error(e.getMessage());
                            e.printStackTrace();
                        }

                    }

                    @Override
                    public void onClose(int code, String reason) {
                        Log.info(LOG_TAG + "Connection lost.");
                    }

                });

            } catch (WebSocketException e) {
                Log.error(LOG_TAG + e.toString());
            }
        }


    }

}
