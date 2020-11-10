package xyz.dreamline91.application.util;

import android.os.Environment;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Created by jaejunha on 2019-04-20.
 */

public class Error {
    public static void logError(Exception ex){
        File file = new File(Environment.getExternalStorageDirectory().getAbsolutePath() + "/Finance");
        if(!file.exists())
            file.mkdir();

        ex.printStackTrace();
        StringWriter sw = new StringWriter();
        ex.printStackTrace(new PrintWriter(sw));
        String str_error = sw.toString();

        try {
            Date date = new Date(System.currentTimeMillis());
            String str_time = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(date);
            BufferedWriter bw = new BufferedWriter(new FileWriter(file+"/" + str_time + ".txt", true));
            bw.append(str_time + "\n");
            bw.append(str_error);
            bw.newLine();
            bw.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
