/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Course_Management_System;

import java.io.File;
import java.io.FileInputStream;
 
import java.io.ObjectInputStream;
 
import java.io.Serializable;
 
import java.util.Vector;
 

/**
 *
 * @author Owner
 */
public class Course implements Serializable {
   
    protected String CourseName;
    protected String TimeSlot;
    protected Vector<Student> studentarray = new Vector();
    protected Vector<Teacher> teacherarray = new Vector();
    
    
    public Course(String courseName, String timing){
         CourseName = courseName;
         TimeSlot = timing;
    }
    
    public Vector<Student> getStudents() throws Exception{
        File file = new File(CourseName + "Students.dat");
        FileInputStream instream = new FileInputStream(file);
        ObjectInputStream obstream = new ObjectInputStream(instream);
        studentarray = (Vector<Student>)obstream.readObject();
        instream.close();
        obstream.close();
        return studentarray;
    }
    
    public Vector<Teacher> getTeachers() throws Exception{
         File file = new File(CourseName + "Teachers.dat");
        FileInputStream instream = new FileInputStream(file);
        ObjectInputStream obstream = new ObjectInputStream(instream);
        teacherarray = (Vector<Teacher>)obstream.readObject();
        instream.close();
        obstream.close();
        return teacherarray;
    }
    
}
