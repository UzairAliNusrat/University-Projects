/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Course_Management_System;

import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.HashMap;
import javax.swing.JOptionPane;

/**
 *
 * @author Owner
 */
public class Teacher extends User  implements Serializable{
    protected ArrayList<Course> ArrayCourse = new ArrayList();
    protected ArrayList<String> Courseresources = new ArrayList();
           
    public Teacher(String pass, String UserID, String userType){
        super(pass, UserID, userType);
    }
    
    public boolean AddResources(String CourseName,String filename)throws Exception{
        boolean successful = false;
        File f1 = new File(CourseName + "resources");
        File file = new File(CourseName + "resources" + "/" + "resources.dat");
        if(f1.exists()){
            if(file.exists()){
            FileInputStream instream = new FileInputStream(file);
            ObjectInputStream datastream = new ObjectInputStream(instream); 
            Courseresources = (ArrayList<String>)datastream.readObject();
            instream.close();
            datastream.close();
            Courseresources.add(filename);
            FileOutputStream fstream = new FileOutputStream(file);
            ObjectOutputStream obstream = new ObjectOutputStream(fstream);
            obstream.writeObject(Courseresources);
            fstream.close();
            obstream.close();
            successful = true;
        }
        }
         
        else{
            if(!f1.exists()){
                f1.mkdir();
                 if(!file.exists()){
                Courseresources.add(filename);
            FileOutputStream fstream = new FileOutputStream(file);
            ObjectOutputStream obstream = new ObjectOutputStream(fstream);
            obstream.writeObject(Courseresources);
            fstream.close();
            obstream.close();
            successful = true;
            }
            }
        }
        return successful;
    }
     
    
    public boolean PostAssignment(String CourseName ,String Assignname, String duedate, int outOfmarks,String timeDue ,String Attachment)throws Exception{ 
        boolean successful = false;
        ArrayList<Assignment> array = new ArrayList();
        Assignment assignment = new Assignment(CourseName,Assignname,duedate,outOfmarks,timeDue);
         HashMap<String,ArrayList<Assignment>> map = new HashMap();
         File file = new File("CourseAssignment.dat");
         if(file.exists()){
             FileInputStream instream = new FileInputStream(file);
             ObjectInputStream obstream = new ObjectInputStream(instream);
             map = (HashMap<String,ArrayList<Assignment>>)obstream.readObject();
             instream.close();
             obstream.close();
             if(map.containsKey(assignment.CourseName)){
                 array = map.get(assignment.CourseName);
                 array.add(assignment);
                 map.put(assignment.CourseName, array);
                 assignment.ADDattachment(Attachment);
                 FileOutputStream outstream = new FileOutputStream(file);
                 ObjectOutputStream objstream = new ObjectOutputStream(outstream);
                 objstream.writeObject(map);
                 outstream.close();
                 objstream.close();
                 successful = true;
             }
             else{
                 if(!map.containsKey(assignment.CourseName)){
                     array.add(assignment);
                     map.put(assignment.CourseName, array);
                     assignment.ADDattachment(Attachment);
                     FileOutputStream fstream = new FileOutputStream(file);
                     ObjectOutputStream ostream = new ObjectOutputStream(fstream);
                     ostream.writeObject(map);
                     fstream.close();
                     ostream.close();
                     successful = true;
                 }
             }
         }
         else{
             if(!file.exists()){
                 array.add(assignment);
                 map.put(assignment.CourseName, array);
                 assignment.ADDattachment(Attachment);
                 FileOutputStream stream = new FileOutputStream(file);
                 ObjectOutputStream objectStream = new ObjectOutputStream(stream);
                 objectStream.writeObject(map);
                 stream.close();
                 objectStream.close();
                 successful = true;
             }
         }
         return successful;
    }  
}
