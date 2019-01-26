package com.example.androidcontroller;

import android.annotation.SuppressLint;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

import io.github.controlwear.virtual.joystick.android.JoystickView;

public class MainActivity extends AppCompatActivity {

//    Screen Drawing Elements
    TextView strengthVal,angleVal;
    EditText ipAddEdit;
    Button setIPbtn;


//    Connection Vars
    boolean isIpSet=false;
    Socket myAppSocket = null;
    public static String IpAddress;
    public static int wifiModulePort = 0;
    public static String MESSAGE="";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        assignIds();
        setClickListeners();

        JoystickView joystick = (JoystickView) findViewById(R.id.joycon);
        joystick.setOnMoveListener(new JoystickView.OnMoveListener() {
            @Override
            public void onMove(int angle, int strength) {
//                Log.i("JOYCONS","Strength:"+Integer.toString(strength)+" , Angle:"+Integer.toString(angle));
                strengthVal.setText(Integer.toString(strength)+"%");
                angleVal.setText(Integer.toString(angle)+"°");

                MESSAGE = Integer.toString(strength) + "," + Integer.toString(angle);

                if(isIpSet) {
                    Socket_AsyncTask cmd_increase_servo = new Socket_AsyncTask();
                    cmd_increase_servo.execute();
                }
                else
                {
//                    Toast.makeText(MainActivity.this, "Ip-Address is Not Set", Toast.LENGTH_SHORT).show();
                }
            }
        });

    }


    void assignIds()
    {
        strengthVal = (TextView)findViewById(R.id.strengthVal);
        angleVal = (TextView)findViewById(R.id.angleVal);
        ipAddEdit = (EditText)findViewById(R.id.ipEditText);
        setIPbtn = (Button)findViewById(R.id.setIP);
    }

    void setClickListeners()
    {
        setIPbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String Complexip = ipAddEdit.getText().toString();
                String RawIp = Complexip.split(":")[0];
                int port = Integer.parseInt(Complexip.split(":")[1]);
                setIPAddress(RawIp,port);
                ipAddEdit.clearFocus();
            }
        });


    }

    void setIPAddress(String ip,int port)
    {
        isIpSet=true;
        IpAddress =  ip;
        wifiModulePort=port;
        Log.i("JOYCONS","IP_Address is set to :" + IpAddress+" , Port:"+Integer.toString(port));
    }

}


class Socket_AsyncTask extends AsyncTask<Void,Void,Void>
{
    Socket socket;

    @Override
    protected Void doInBackground(Void... params){
        try{
            InetAddress inetAddress = InetAddress.getByName(MainActivity.IpAddress);
            socket = new java.net.Socket(inetAddress,MainActivity.wifiModulePort);
            DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());
            dataOutputStream.writeBytes(MainActivity.MESSAGE);
            dataOutputStream.close();
            socket.close();
        }catch (UnknownHostException e){e.printStackTrace();}catch (IOException e){e.printStackTrace();}
        return null;
    }
}
