/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Course_Management_System;

 
import java.awt.Desktop;
 
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
 
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
 

/**
 *
 * @author Owner
 */
public class Student extends User implements Serializable {
    protected ArrayList<Course> studentCourses = new ArrayList();
    
    
    public Student(String pass, String UserID, String userType){
        super(pass, UserID, userType);    
    }
    
    public void AccessResources(String resourceName) throws Exception{
        File file = new File(  "C:\\Users\\Owner\\Desktop\\" + resourceName);
             if(Desktop.isDesktopSupported()){
            Desktop.getDesktop().open(file);
           }  
    }
    
    public boolean SubmitAssignment(String CourseName, String AssignmentName,String attachmentName)throws Exception{
         boolean successful = false;
        
                     File f1 = new File(ID + CourseName);
                     File file = new File(ID + CourseName + "/" +  AssignmentName + ".dat");
                     if(f1.exists()){
                          if(!file.exists()){
                               FileOutputStream fstream = new FileOutputStream(file);
                         DataOutputStream datastream = new DataOutputStream(fstream);
                         datastream.writeUTF("Submitted");
                         fstream.close();
                         datastream.close();
                        successful = true;
                          }
                           
                             
                     }
                     else{
                         if(!f1.exists()){
                             f1.mkdir();
                             
                             FileOutputStream fstream = new FileOutputStream(file);
                         DataOutputStream datastream = new DataOutputStream(fstream);
                         datastream.writeUTF("Submitted");
                         fstream.close();
                         datastream.close();
                          successful = true;
                         }
                     }
                     File file1 = new File(CourseName + "Submission");
                     File file2 = new File(CourseName + "Submission" + "/" +AssignmentName);
                     File file3 = new File(CourseName + "Submission" + "/" +AssignmentName + "/" + ID);
                     File file4 = new File(CourseName + "Submission" + "/" +AssignmentName + "/" + ID + "/" + "attachment.dat");
                    
                     file1.mkdir();
                     file2.mkdir();
                     file3.mkdir();
                     if(!file4.exists()){
                         FileOutputStream fstream = new FileOutputStream(file4);
                             DataOutputStream dstream = new DataOutputStream(fstream);
                             dstream.writeUTF(attachmentName);
                             fstream.close();
                             dstream.close();
                     }
                      
        return successful;
        
    }

    
    public ArrayList<Assignment> AccessAssignment(String CourseName) throws Exception{
        File file = new File("CourseAssignment.dat");
        HashMap<String,ArrayList<Assignment>> map = new HashMap();
        ArrayList<Assignment> array1 = new ArrayList();
        if(file.exists()){
            FileInputStream instream = new FileInputStream(file);
            ObjectInputStream obstream = new ObjectInputStream(instream);
            map = (HashMap<String,ArrayList<Assignment>>)obstream.readObject();
            instream.close();
            obstream.close();
            if(map.containsKey(CourseName)){
                array1 = map.get(CourseName);
            }
        }
        return array1;
    }
    
}
