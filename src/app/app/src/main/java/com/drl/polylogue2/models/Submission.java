package com.drl.polylogue2.models;

import com.drl.polylogue2.MainActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.Serializable;
import java.sql.Time;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

/**
 * Created by lutz on 10/10/16.
 */
public class Submission implements Serializable {

    public String message = "";
    public String createdAt = "";
    public boolean expired = false;
    public String expiresAt = "";
    public int boxId = -1;
    public String _id = null;

    private static String LOG_TAG = "SUBMISSION_MODEL: ";

    public Submission(JSONObject json) {

        try {
            message = json.getString("message");
            createdAt = json.getString("createdAt");
            expired = Boolean.parseBoolean(json.getString("expired"));
            expiresAt = json.getString("expiresAt");
            boxId = Integer.parseInt(json.getString("boxId"));
            _id = json.getString("_id");

        } catch (JSONException e) {
            MainActivity.Log.error(LOG_TAG + "Error parsing json: " + e.getMessage());
            e.printStackTrace();
        }
    }

    public Date getExpiresAt() {
        return parseDateString(expiresAt);
    }

    @Override
    public String toString() {
        return  "\n_id:" + _id +
                "\nMessage:" + message +
                "\ncreatedAt:" + createdAt +
                "\nexpired:" + expired +
                "\nexpiresAt:" + expiresAt +
                "\nboxId:" + boxId;
    }

    private Date parseDateString(String dateString) {

        SimpleDateFormat form = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
        form.setTimeZone(TimeZone.getTimeZone("UTC"));
        try {
            return form.parse(dateString);
        } catch (ParseException e) {
            MainActivity.Log.error(LOG_TAG + "Error parsing date: " + e.getMessage());
            e.printStackTrace();
        }
        return null;
    }
}
