package com.drl.polylogue2.utils;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.support.v4.content.WakefulBroadcastReceiver;
import android.util.Log;

import com.drl.polylogue2.ForegroundService;

/**
 * Created by lutz on 28/09/16.
 */
// keeps service awake
public class AlarmReceiver extends WakefulBroadcastReceiver
{
    @Override
    public void onReceive(Context context, Intent intent)
    {

        Intent service = new Intent(context, ForegroundService.class);
        service.setAction(ForegroundService.ServiceAction.CONNECT);
        context.startService(service);

        Log.d("ALARM-RECEIVER", "called.");
    }
}
