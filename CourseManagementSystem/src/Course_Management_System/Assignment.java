/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Course_Management_System;

import java.io.DataOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;

/**
 *
 * @author Owner
 */
public class Assignment implements Serializable {
    
   protected String assignmentName;
    protected String DueDate;
    protected int AssignmentMarks;
    
    protected String attachment;
    protected String dueTime;
    protected String CourseName;
   
    
    public Assignment(String Coursename,String name, String duedate, int outOfmarks,String timeDue){
        assignmentName = name;
        DueDate = duedate;
        AssignmentMarks = outOfmarks;
        dueTime = timeDue;
        CourseName = Coursename;
    }
    
    public void changeDeadline(String newDueDate){
        DueDate = newDueDate;
    }
    
    public void ADDattachment(String filename) throws Exception{
        File f1 = new File(CourseName);
        File file = new File(CourseName+"/"+CourseName + assignmentName + ".dat");
         if(!f1.exists()){
             f1.mkdir();
             attachment = filename;
             FileOutputStream fstream = new FileOutputStream(file);
             DataOutputStream obstream = new DataOutputStream(fstream);
             obstream.writeUTF(attachment);
             fstream.close();
             obstream.close();
         }
         else{
             if(f1.exists()){
                 attachment = filename;
             FileOutputStream fstream = new FileOutputStream(file);
             DataOutputStream obstream = new DataOutputStream(fstream);
             obstream.writeUTF(attachment);
             fstream.close();
             obstream.close();
             }
         }     
          
    }
}
