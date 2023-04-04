package com.example.application;

import android.content.Context;
import android.database.DataSetObserver;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListAdapter;
import android.widget.TextView;

import java.text.DecimalFormat;
import java.util.ArrayList;

public class WorkoutsListAdapter implements ListAdapter {
    ArrayList<Workout> workoutsList;
    Context context;

    public WorkoutsListAdapter(Context context, ArrayList<Workout> workoutsList) {
        this.workoutsList=workoutsList;
        this.context=context;
    }

    public boolean areAllItemsEnabled() {
        return false;
    }

    @Override
    public boolean isEnabled(int position) {
        return true;
    }
    @Override
    public void registerDataSetObserver(DataSetObserver observer) {
    }
    @Override
    public void unregisterDataSetObserver(DataSetObserver observer) {
    }
    @Override
    public int getCount() {
        return workoutsList.size();
    }
    @Override
    public Object getItem(int position) {
        return position;
    }
    @Override
    public long getItemId(int position) {
        return position;
    }
    @Override
    public boolean hasStableIds() {
        return false;
    }
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Workout currWorkout=workoutsList.get(position);
        if(convertView==null) {
            LayoutInflater layoutInflater = LayoutInflater.from(context);
            convertView=layoutInflater.inflate(R.layout.workout_item, null);
            convertView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                }
            });
            TextView workoutNum=convertView.findViewById(R.id.txt_workoutNum);
            TextView workoutName=convertView.findViewById(R.id.txt_workoutName);
            TextView workoutDate=convertView.findViewById(R.id.txt_workoutDate);
            TextView workoutScore=convertView.findViewById(R.id.txt_workoutScore);

            if (currWorkout.getUser_id() == -1){
                workoutNum.setText("");
                workoutName.setText("No workouts yet!");
                workoutDate.setText("");
                workoutScore.setText("");
            } else {
                workoutNum.setText(String.valueOf(position + 1));
                workoutName.setText(currWorkout.getExercise_name());
                workoutDate.setText(currWorkout.getDate());
                DecimalFormat df = new DecimalFormat("##.##");
                Double currScore = currWorkout.getScore() * 100;
                workoutScore.setText("Score: " + df.format(currScore) + "%");
            }



        }
        return convertView;
    }
    @Override
    public int getItemViewType(int position) {
        return position;
    }
    @Override
    public int getViewTypeCount() {
        return workoutsList.size();
    }
    @Override
    public boolean isEmpty() {
        return false;
    }
}
