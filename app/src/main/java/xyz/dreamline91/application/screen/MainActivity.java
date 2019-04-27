package xyz.dreamline91.application.screen;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.StrictMode;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import xyz.dreamline91.application.R;
import xyz.dreamline91.application.operator.ItemOperator;

public class MainActivity extends AppCompatActivity {

    private final int REQUEST_PERMISSION_CODE = 0;

    private ItemOperator itemOperator;



    private TextView textUpdateItem;
    void init(){
        setContentView(R.layout.activity_main);

        textUpdateItem = (TextView) findViewById(R.id.text_update_item);

        itemOperator = new ItemOperator(this);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        init();

        /* 권한 요청 */
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED)
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, REQUEST_PERMISSION_CODE);
    }
    @Override
    protected void onResume(){
        super.onResume();

        /* 종목 업데이트가 필요한 경우 */
        if(itemOperator.checkUpdateItem() == false){
            textUpdateItem.setText("Need update");
            itemOperator.updateItem();
        }
        /* 종목 업데이트가 필요 하지 않은 경우 */
        else {
            textUpdateItem.setText("Updated");
            itemOperator.updateItem();                  //디버깅 용도로 임시로 추가
        }
    }
}
