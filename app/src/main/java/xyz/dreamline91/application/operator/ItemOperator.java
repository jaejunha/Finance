package xyz.dreamline91.application.operator;

import android.content.Context;
import android.content.SharedPreferences;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Calendar;

import xyz.dreamline91.application.util.Error;

import static android.content.Context.MODE_PRIVATE;

/**
 * Created by jaejunha on 2019-04-20.
 */

public class ItemOperator {

    private Context context;

    private SharedPreferences preferences;
    private SharedPreferences.Editor editor;
    private Calendar cal;
    private int int_today;

    public ItemOperator(Context context){
        this.context = context;
    }

    public boolean checkUpdateItem(){
        preferences = context.getSharedPreferences("finance", MODE_PRIVATE);
        cal = Calendar.getInstance();
        int_today = cal.get(Calendar.YEAR) * 10000 + (cal.get(Calendar.MONTH)+1) * 100 + cal.get(Calendar.DATE);

        return int_today == preferences.getInt("update_item", 0);
    }

    public boolean updateItem(){
        editor = preferences.edit();
        editor.putInt("update_item", int_today);
        editor.commit();

        return true;
    }
    public boolean collectItem(int type, int page){

        try {
            String url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=" + type + "&page=" + page;

            URL obj = new URL(url);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setRequestProperty("Cookie", "field_list=12|0000801A;");

            BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String str;
            String strs[];

            int int_price;
            String str_code, str_title, str_changed, str_PER, str_ROE, str_PBR;

			/* skip first table */
            while ((str = br.readLine()).contains("</table") == false);
			/* skip first tr */
            while ((str = br.readLine()).contains("</tr") == false);

			/* loop tr */
            while(true) {
				/* skip first td */
                while ((str = br.readLine()).contains("</td") == false);

                for(int i=0;i<5;i++) {
                    while ((str = br.readLine()).contains("</td") == false);
                    while ((str = br.readLine()).contains("</td") == false);
					/* title */
                    if(str.contains("tltle")) {
                        strs = str.split("\"|<|>|=");
                        str_code = strs[6];
                        str_title = strs[11];
                    }
                    else
                        return false;
                    while ((str = br.readLine()).contains("</td") == false);
					/* price */
                    int_price = Integer.parseInt(str.split("<|>")[2].replace(",", ""));
                    while ((str = br.readLine()).contains("</td") == false);
                    while ((str = br.readLine()).contains("%") == false);
					/* changed */
                    if(str.contains("0.00"))
                        str_changed = "0.00%";
                    else
                        str_changed = str.replace("\t", "");
                    while ((str = br.readLine()).contains("</td") == false);
                    while ((str = br.readLine()).contains("</td") == false);
                    while ((str = br.readLine()).contains("</td") == false);
                    while ((str = br.readLine()).contains("</td") == false);
					/* PER */
                    str_PER = str.split("<|>")[2].replace(",", "");
                    while ((str = br.readLine()).contains("</td") == false);
					/* ROE */
                    str_ROE = str.split("<|>")[2].replace(",", "");
                    while ((str = br.readLine()).contains("</td") == false);
					/* PBR */
                    str_PBR = str.split("<|>")[2].replace(",", "");
                    while ((str = br.readLine()).contains("</td") == false);
                    //map_raw.put(str_title, new ItemOperator(str_code, int_price, str_changed, str_PER, str_ROE, str_PBR));
                }

				/* skip blank */
                while ((str = br.readLine()).contains("</tr") == false);
                while ((str = br.readLine()).contains("</tr") == false);
                while ((str = br.readLine()).contains("</tr") == false);
            }

        } catch (NullPointerException e) {
        } catch(Exception e) {
            Error.logError(e);
            return true;
        }
        return false;
    }

    public boolean loadItem(){
        return true;
    }
}
