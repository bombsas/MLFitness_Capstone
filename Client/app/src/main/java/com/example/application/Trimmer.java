package com.example.application;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class Trimmer extends AppCompatActivity {
    private static final int STORAGE_PERMISSION_CODE = 150;
    Button pickvideo;
    final int Requestcode = 149;
    ProgressBar progressBar;
    public static   final String VideoUri = "VideoUri";

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trimmer);
        pickvideo = findViewById(R.id.pick_video);
        progressBar=findViewById(R.id.progress_bar);
        pickvideo.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {

                if (ContextCompat.checkSelfPermission(Trimmer.this, Manifest.permission.READ_EXTERNAL_STORAGE) +
                        ContextCompat.checkSelfPermission(Trimmer.this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED) {
                    //Toast.makeText(Trimmer.this, "You have already granted this permission!",
                    //Toast.LENGTH_SHORT).show();
                    Database.loadAllVideos(getApplicationContext(), new MycompleteListener() {
                        @Override
                        public void OnSuccess() {
                            progressBar.setVisibility(View.VISIBLE);
                            startActivity(new Intent(getApplicationContext(),LoadAllExistingVideos.class));
                            finish();
                        }
                        @Override
                        public void OnFailure() {
                            //Get a toaster if this happens
                        }
                    });
                } else {
                    requestStoragePermission();
                }
                finish();
            }
        });
    }

    private void requestStoragePermission() {
        if (ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.READ_EXTERNAL_STORAGE) &&
                ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)) {
            new AlertDialog.Builder(this)
                    .setTitle("Permission needed")
                    .setMessage("Please give permissions to see video,upload and download videos")
                    .setPositiveButton("ok", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            ActivityCompat.requestPermissions(Trimmer.this,
                                    new String[]{Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
                        }
                    })
                    .setNegativeButton("cancel", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            dialog.dismiss();
                        }
                    })
                    .create().show();
        } else {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.WRITE_EXTERNAL_STORAGE}, STORAGE_PERMISSION_CODE);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == Requestcode && resultCode == RESULT_OK) {
            Uri uri = data.getData();
            Intent intent = new Intent(getApplicationContext(), TrimVideoActivty.class);
            intent.putExtra(VideoUri, uri.toString());
            startActivity(intent);
            finish();
        }
    }
}