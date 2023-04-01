package com.example.application;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.Environment;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.material.navigation.NavigationView;
import com.squareup.picasso.Picasso;

public class TraineeProfile extends AppCompatActivity{

    DrawerLayout drawerLayout;
    NavigationView navigationView;
    ActionBarDrawerToggle drawerToggle;

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {

        if (drawerToggle.onOptionsItemSelected(item)) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trainee_profile);

        //Set objects in the page
        //Once db is implemented change from test/example cases to the version that get the data from the db

        //Init fields in xml
        TextView trainee_profile_username_textview = (TextView) findViewById(R.id.userNameTraineeProfile);
        TextView trainee_profile_email_textview = (TextView) findViewById(R.id.userEmailTraineeProfile);

        ImageView userProfilePicture = (ImageView) findViewById(R.id.profile_picture);

        //Assigns values to the fields in the xml
        //String trainee_profile_username = user.getUsername();
        String trainee_profile_username = SocketFunctions.user.getUserName();
        trainee_profile_username_textview.setText(trainee_profile_username);
        //String trainee_profile_email = user.getEmail();
        String trainee_profile_email = SocketFunctions.user.getEmail();
        trainee_profile_email_textview.setText(trainee_profile_email);

        //Check line to get from db
        try{
            if(SocketFunctions.user.hasPfp()){
                userProfilePicture.setImageBitmap(SocketFunctions.user.getPfp());
            }else{
                Picasso.get().load("http://162.246.157.128/MLFitness/pfps/"+ SocketFunctions.user.getId() +".jpg").into(userProfilePicture);
                Drawable pfp = userProfilePicture.getDrawable();
                SocketFunctions.user.setPfp(Bitmap.createBitmap(pfp.getIntrinsicWidth(), pfp.getIntrinsicHeight(), Bitmap.Config.ARGB_8888));
            }
        }catch (Exception e){
            int trainee_profile_image = R.drawable.ic_baseline_tag_faces_24;
            userProfilePicture.setImageResource(trainee_profile_image);
        }

        drawerLayout = findViewById(R.id.drawer_layout);
        navigationView = findViewById(R.id.nav_view);
        drawerToggle = new ActionBarDrawerToggle(this, drawerLayout, R.string.open, R.string.close);
        drawerLayout.addDrawerListener(drawerToggle);
        drawerToggle.syncState();
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        if (SocketFunctions.user.isTrainer() == false) {
            String name = SocketFunctions.user.getName();
            TextView textView = findViewById(R.id.TraineeProfileTitle);
            textView.setText(name);
            navigationView.getMenu().findItem(R.id.trainers).setVisible(true);
            navigationView.getMenu().findItem(R.id.trainees).setVisible(false);
        }
        else{
            navigationView.getMenu().findItem(R.id.trainers).setVisible(false);
            navigationView.getMenu().findItem(R.id.trainees).setVisible(true);

        }
        invalidateOptionsMenu();
        invalidateMenu();
        navigationView.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {

                switch (item.getItemId()) {
                    case R.id.home: {
                        //Go to homepage
                        Intent i = new Intent(getApplicationContext(), TraineeHomePage.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.workouts: {
                        //Go to workouts
                        Intent i = new Intent(getApplicationContext(), TraineeWorkouts.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.message: {
                        //Go to message
                        Intent i = new Intent(getApplicationContext(), TraineeMessages.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        //finish();
                        drawerLayout.closeDrawer(GravityCompat.START);
                        break;
                    }
                    case R.id.setting: {
                        //Go to setting
                        Intent i = new Intent(getApplicationContext(), TraineeSettings.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.trainees: {
                        //Go to trainees
                        Intent i = new Intent(getApplicationContext(), TrainerTraineeProfile.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.trainers:{
                        Intent i = new Intent(getApplicationContext(), TraineeTrainerProfile.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.friends: {
                        //Go to friends
                        Intent i = new Intent(getApplicationContext(), FriendsPage.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.profile: {
                        //Already selected
                        if(SocketFunctions.user.isTrainer()){
                            Intent i = new Intent(getApplicationContext(), TraineeProfile.class);
                            i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                            startActivity(i);
                            finish();
                            break;
                        }else {
                            drawerLayout.closeDrawer(GravityCompat.START);
                        }
                        break;
                    }
                    case R.id.logout: {
                        //Add a confirmation pop up

                        //Once completed logout/remove locally stored user cred

                        //End all activities and go to welcome screen
                        Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                        startActivity(intent);
                        break;
                    }
                    default: {
                        drawerLayout.closeDrawer(GravityCompat.START);
                    }
                }
                return false;
            }
        });
    }

    public void goToEdit(View view) {
        Intent i;
        i = new Intent(getApplicationContext(), TraineeEditProfile.class);
        startActivity(i);
        finish();
    }

    public void moreWorkouts(View view) {
        Intent i;
        i = new Intent(getApplicationContext(), TraineeWorkouts.class);
        startActivity(i);
        finish();
    }

    public void moreAwards(View view) {
        Intent i;
        i = new Intent(getApplicationContext(), TraineeEditProfile.class);
        startActivity(i);
        finish();
    }

    @Override
    public void onBackPressed() {

        if (drawerLayout.isDrawerOpen(GravityCompat.START)) {
            drawerLayout.closeDrawer(GravityCompat.START);
        } else {
            //Go to homepage
            Intent i = new Intent(getApplicationContext(), TraineeHomePage.class);
            i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
            startActivity(i);
            finish();
            super.onBackPressed();
        }
    }
}