/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Course_Management_System;

import java.io.File;
import java.io.FileInputStream;
 
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Vector;

/**
 *
 * @author Owner
 */
public class Administrator extends User implements Serializable{
    
    
    public Administrator(String pass, String UserID, String userType){
        super(pass, UserID, userType);
    }
    
    public boolean AddStudentCourse(String CourseName, String timings,String studentID)throws Exception{
        boolean successful = false;
        Course a = new Course(CourseName, timings);
        HashMap<String,ArrayList<Course>> map = new HashMap();
        Vector<User> vect = new Vector();
       
            File file = new File("UserDetails.dat");
            
                FileInputStream fl = new FileInputStream(file);
                ObjectInputStream ob = new ObjectInputStream(fl);
                vect = (Vector<User>)ob.readObject();
                fl.close();
                ob.close();
                for(int i = 0;i < vect.size();i++){
                    User user = vect.get(i);
                    if(user.ID.equals(studentID) && user.UserType.equals("Student")){
                        Student st = (Student)user;
                        File file2 = new File("Courses.dat");
                        Vector<Course> courseArr = new Vector();
                        if(file2.exists()){
                             FileInputStream f2 = new FileInputStream(file2);
                             ObjectInputStream obstream = new ObjectInputStream(f2);
                              courseArr = (Vector<Course>)obstream.readObject();
                             f2.close();
                             obstream.close();
                            boolean containsCourse = false;
                             for(int j = 0; j < courseArr.size();j++){ 
                                if(courseArr.get(j).CourseName.equals(CourseName)){
                                         containsCourse = true;
                                }      
                             }
                             if(!containsCourse){
                                 courseArr.add(a);
                                 FileOutputStream instream = new FileOutputStream(file2);
                             ObjectOutputStream ostream = new ObjectOutputStream(instream);
                             ostream.writeObject(courseArr);
                             instream.close();
                             ostream.close();
                             }
                        }
                        else{
                            if(!file2.exists()){
                                courseArr.add(a);
                                FileOutputStream instream = new FileOutputStream(file2);
                             ObjectOutputStream ostream = new ObjectOutputStream(instream);
                             ostream.writeObject(courseArr);
                             instream.close();
                             ostream.close();
                            }
                        }
                        File file1 = new File(CourseName + "Students.dat");
                        if(file1.exists()){
                             FileInputStream f2 = new FileInputStream(file1);
                             ObjectInputStream obstream = new ObjectInputStream(f2);
                             a.studentarray = (Vector<Student>)obstream.readObject();
                             f2.close();
                             obstream.close();
                             a.studentarray.add(st);
                             FileOutputStream instream = new FileOutputStream(file1);
                             ObjectOutputStream ostream = new ObjectOutputStream(instream);
                             ostream.writeObject(a.studentarray);
                             instream.close();
                             ostream.close();
                        }
                        else{
                            FileOutputStream instream = new FileOutputStream(file1);
                             ObjectOutputStream ostream = new ObjectOutputStream(instream);
                             a.studentarray.add(st);
                             ostream.writeObject(a.studentarray);
                             instream.close();
                             ostream.close();
                        }
                        File b = new File("StudentCourse.dat");
                        if(b.exists()){
                             FileInputStream f2 = new FileInputStream(b);
                             ObjectInputStream obstream = new ObjectInputStream(f2);
                             map = (HashMap<String,ArrayList<Course>>)obstream.readObject();
                             f2.close();
                             obstream.close();
                             if(map.containsKey(st.ID)){
                                 st.studentCourses = map.get(st.ID);
                                   for(int j = 0;j < st.studentCourses.size();j++){
                                       if(st.studentCourses.get(j).CourseName.equals(CourseName)){
                                         throw new Exception("Student Already Has This Course");  
                                       }
                                   }
                                 st.studentCourses.add(a);
                                 map.put(st.ID,st.studentCourses);
                                 FileOutputStream fst = new FileOutputStream(b);
                                 ObjectOutputStream ost = new ObjectOutputStream(fst);
                                 ost.writeObject(map);
                                 fst.close();
                                 ost.close();
                                 successful = true;
                                 break;
                             }
                             else{
                                 if(!map.containsKey(st.ID)){
                                     st.studentCourses.add(a);
                                     map.put(st.ID,st.studentCourses);
                                     FileOutputStream f = new FileOutputStream(b);
                                     ObjectOutputStream outstream = new ObjectOutputStream(f);
                                     outstream.writeObject(map);
                                     f.close();
                                     outstream.close();
                                     successful = true;
                                     break;
                                 }
                             } 
                        }
                        else{
                            if(!b.exists()){
                                st.studentCourses.add(a);
                                map.put(st.ID, st.studentCourses);
                                FileOutputStream stream = new FileOutputStream(b);
                                ObjectOutputStream bstream = new ObjectOutputStream(stream);
                                bstream.writeObject(map);
                                stream.close();
                                bstream.close();
                                successful = true;
                                break;
                            }
                        }
                    }
                }
                if(!successful){
                    throw new Exception("Student ID is Incorrect");
                }
          
        return successful;
    }
   
    /**
     *
     * @param studentID
     * @param CourseName
     * @return
     * @throws Exception
     */
    public boolean DeleteStudentCourse(String studentID,String CourseName)throws Exception  {
       boolean successful = false;
        boolean courseFound = false; 
        boolean isStudent = false;
        Vector<User> vector2 = new Vector();
        HashMap<String,ArrayList<Course>> mp = new HashMap();
        File a = new File("UserDetails.dat");
        if(a.exists()){
            FileInputStream instream = new FileInputStream(a);
            ObjectInputStream obstream = new ObjectInputStream(instream);
            
            vector2 = (Vector<User>)obstream.readObject();
            instream.close();
            obstream.close();
            for(int i = 0; i < vector2.size(); i++){
                User user1 = vector2.get(i);
                if(user1.ID.equals(studentID) && user1.UserType.equals("Student")){
                    Student st = (Student)user1;
                    isStudent = true;
                    File file1 = new File(CourseName + "Students.dat");
                    if(file1.exists()){
                         FileInputStream f = new FileInputStream(file1);
                        ObjectInputStream ob = new ObjectInputStream(f);
                        Vector<Student> arrayStud = (Vector<Student>)ob.readObject();
                        f.close();
                        ob.close();
                        for(int j = 0;j < arrayStud.size();j++){
                            if(arrayStud.get(j).ID.equals(st.ID)){
                                arrayStud.remove(j);
                                FileOutputStream fstream = new FileOutputStream(file1);
                               ObjectOutputStream objstream = new ObjectOutputStream(fstream);
                               objstream.writeObject(arrayStud);
                               fstream.close();
                               objstream.close();
                               break;
                            }
                        }
                    }
                    File file = new File("StudentCourse.dat");
                    if(file.exists()){
                        FileInputStream f = new FileInputStream(file);
                        ObjectInputStream ob = new ObjectInputStream(f);
                       mp = (HashMap<String,ArrayList<Course>>)ob.readObject();
                       f.close();
                       ob.close();
                       if(mp.containsKey(st.ID)){
                            st.studentCourses = mp.get(st.ID);
                       for(int z = 0;z < st.studentCourses.size();z++){
                           if(st.studentCourses.get(z).CourseName.equals(CourseName)){
                               courseFound = true;
                                   st.studentCourses.remove(z);
                               mp.put(st.ID,st.studentCourses);
                               FileOutputStream fstream = new FileOutputStream(file);
                               ObjectOutputStream objstream = new ObjectOutputStream(fstream);
                               objstream.writeObject(mp);
                               fstream.close();
                               objstream.close();
                               successful = true;
                               break;   
                           }
                       }
                       }
                       
                       if(successful){
                           break;
                       }
                              
                    }
                }
            }
            if(!isStudent){
                throw new Exception("Student ID is Incorrect");
            }
            if(!courseFound){
                throw new Exception("The specified Student Does Not Have This Course");
            }
                          
        }
        return successful;
    }
   
   public boolean assignTeacherCourse(String teacherID, String CourseName,String timing) throws Exception{
       boolean successful = false;
       Course a = new Course(CourseName,timing);
       Vector<User> vec = new Vector();
       HashMap<String,ArrayList<Course>> map = new HashMap();
       File f1 = new File("UserDetails.dat");
       
       if(f1.exists()){
           FileInputStream f = new FileInputStream(f1);
           ObjectInputStream ob = new ObjectInputStream(f);
           vec = (Vector<User>)ob.readObject();
           f.close();
           ob.close();
           for(int i = 0;i < vec.size();i++){
               User user = vec.get(i);
               if(user.ID.equals(teacherID) && user.UserType.equals("Teacher")){
                   Teacher teacher = (Teacher)user;
                   File file2 = new File("Courses.dat");
                        Vector<Course> courseArr = new Vector();
                        if(file2.exists()){
                             FileInputStream f2 = new FileInputStream(file2);
                             ObjectInputStream obstream = new ObjectInputStream(f2);
                              courseArr = (Vector<Course>)obstream.readObject();
                             f2.close();
                             obstream.close();
                            boolean containsCourse = false;
                             for(int j = 0; j < courseArr.size();j++){ 
                                if(courseArr.get(j).CourseName.equals(CourseName)){
                                         containsCourse = true;
                                }      
                             }
                             if(!containsCourse){
                                 courseArr.add(a);
                                 FileOutputStream instream = new FileOutputStream(file2);
                             ObjectOutputStream ostream = new ObjectOutputStream(instream);
                             ostream.writeObject(courseArr);
                             instream.close();
                             ostream.close();
                             }
                        }
                        else{
                            if(!file2.exists()){
                                courseArr.add(a);
                                FileOutputStream instream = new FileOutputStream(file2);
                             ObjectOutputStream ostream = new ObjectOutputStream(instream);
                             ostream.writeObject(courseArr);
                             instream.close();
                             ostream.close();
                            }
                        }
                   File file = new File(CourseName + "Teachers.dat");
                   if(file.exists()){
                       FileInputStream instream = new FileInputStream(file);
                       ObjectInputStream objstream = new ObjectInputStream(instream);
                       a.teacherarray = (Vector<Teacher>)objstream.readObject();
                       instream.close();
                       objstream.close();
                       a.teacherarray.add(teacher);
                       FileOutputStream outstream = new FileOutputStream(file);
                       ObjectOutputStream obstream = new ObjectOutputStream(outstream);
                       obstream.writeObject(a.teacherarray);
                       outstream.close();
                       obstream.close();
                   }
                   else{
                       FileOutputStream fstream = new FileOutputStream(file);
                       ObjectOutputStream Ostream = new ObjectOutputStream(fstream);
                       a.teacherarray.add(teacher);
                       Ostream.writeObject(a.teacherarray);
                       fstream.close();
                       Ostream.close();
                   }
                   File file1 = new File("TeacherCourse.dat");
                   if(file1.exists()){
                       FileInputStream instream = new FileInputStream(file1);
                       ObjectInputStream objstream = new ObjectInputStream(instream);
                       map = (HashMap<String,ArrayList<Course>>)objstream.readObject();
                       instream.close();
                       objstream.close();
                       if(map.containsKey(teacher.ID)){
                           teacher.ArrayCourse = map.get(teacher.ID);
                           for(int j = 0;j < teacher.ArrayCourse.size();j++){
                               if(teacher.ArrayCourse.get(j).CourseName.equals(CourseName)){
                                   throw new Exception("Teacher Already Has This Course");
                               }
                           }
                           teacher.ArrayCourse.add(a);
                           map.put(teacher.ID, teacher.ArrayCourse);
                           FileOutputStream fl = new FileOutputStream(file1);
                           ObjectOutputStream obj = new ObjectOutputStream(fl);
                           obj.writeObject(map);
                           fl.close();
                           obj.close();
                           successful = true;
                           break;
                       }
                       else{
                           if(!map.containsKey(teacher.ID)){
                               teacher.ArrayCourse.add(a);
                               map.put(teacher.ID, teacher.ArrayCourse);
                               FileOutputStream filestream = new FileOutputStream(file1);
                               ObjectOutputStream objectstream = new ObjectOutputStream(filestream);
                                 objectstream.writeObject(map);
                                 filestream.close();
                                 objectstream.close();
                                 successful = true;
                                 break;
                            }
                       }
                   }
                   else{
                       if(!file1.exists()){
                           teacher.ArrayCourse.add(a);
                           map.put(teacher.ID, teacher.ArrayCourse);
                           FileOutputStream FileStream = new FileOutputStream(file1);
                           ObjectOutputStream ObjectStream = new ObjectOutputStream(FileStream);
                           ObjectStream.writeObject(map);
                           FileStream.close();
                           ObjectStream.close();
                           successful = true;
                           break;
                       }
                   }
                   
               }
           }
           if(!successful){
               throw new Exception("Teacher ID is Incorrect");
           }
       }
       return successful;
   }
   
   public boolean DeleteTeacherCourse(String teacherID,String CourseName) throws Exception{
       boolean successful = false;
        boolean courseFound = false; 
        boolean isTeacher = false;
        Vector<User> vector2 = new Vector();
        HashMap<String,ArrayList<Course>> mp = new HashMap();
        File a = new File("UserDetails.dat");
        if(a.exists()){
            FileInputStream instream = new FileInputStream(a);
            ObjectInputStream obstream = new ObjectInputStream(instream);
            
            vector2 = (Vector<User>)obstream.readObject();
            instream.close();
            obstream.close();
            for(int i = 0; i < vector2.size(); i++){
                User user1 = vector2.get(i);
                if(user1.ID.equals(teacherID) && user1.UserType.equals("Teacher")){
                    Teacher teacher = (Teacher)user1;
                    isTeacher = true;
                    File fl = new File(CourseName + "Teachers.dat");
                    if(fl.exists()){
                        FileInputStream f = new FileInputStream(fl);
                        ObjectInputStream ob = new ObjectInputStream(f);
                        Vector<Teacher> teacherArr = (Vector<Teacher>) ob.readObject();
                        f.close();
                        ob.close();
                        for(int j = 0;j < teacherArr.size();j++){
                            if(teacherArr.get(j).ID.equals(teacher.ID)){
                                teacherArr.remove(j);
                                FileOutputStream stream  = new FileOutputStream(fl);
                                ObjectOutputStream objstream = new ObjectOutputStream(stream);
                                objstream.writeObject(teacherArr);
                                stream.close();
                                objstream.close();
                                break;
                            }
                        }
                    }
                    File file = new File("TeacherCourse.dat");
                    if(file.exists()){
                        FileInputStream f = new FileInputStream(file);
                        ObjectInputStream ob = new ObjectInputStream(f);
                       mp = (HashMap<String,ArrayList<Course>>)ob.readObject();
                       f.close();
                       ob.close();
                       if(mp.containsKey(teacher.ID)){
                            teacher.ArrayCourse = mp.get(teacher.ID);
                       for(int z = 0;z < teacher.ArrayCourse.size();z++){
                           if(teacher.ArrayCourse.get(z).CourseName.equals(CourseName)){
                               courseFound = true;
                                   teacher.ArrayCourse.remove(z);
                               mp.put(teacher.ID,teacher.ArrayCourse);
                               FileOutputStream fstream = new FileOutputStream(file);
                               ObjectOutputStream objstream = new ObjectOutputStream(fstream);
                               objstream.writeObject(mp);
                               fstream.close();
                               objstream.close();
                               successful = true;
                               break;   
                           }
                       }
                       }
                       
                       if(successful){
                           break;
                       }
                              
                    }
                }
            }
            if(!isTeacher){
                throw new Exception("Teacher ID is Incorrect");
            }
            if(!courseFound){
                throw new Exception("The specified Teacher Does Not Have This Course");
            }
                          
        }
        return successful;
   }
    
}
