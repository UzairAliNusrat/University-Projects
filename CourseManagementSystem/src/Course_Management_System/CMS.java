/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Course_Management_System;

 import java.io.*;
import java.io.FileOutputStream;
import java.util.Vector;
 
public class CMS {
     
    private File file = new File("UserDetails.dat");
    
     
    public boolean SignUp(String pass, String UserID, String userType){
        boolean signUp = false;
        Vector<User> vector1 = new Vector(); 
        if(file.exists()){
            try{
            FileInputStream fstream = new FileInputStream(file);
      ObjectInputStream inputFile = new ObjectInputStream(fstream);   
      vector1 = (Vector<User>)inputFile.readObject();
      fstream.close();
      inputFile.close();
        }
        catch(Exception e){
            e.getMessage();
        }
            try{
                 FileOutputStream Outstream = new FileOutputStream(file);
        ObjectOutputStream outputFile = new ObjectOutputStream(Outstream);
        
         if(userType == "Student"){
            User a = new Student(pass, UserID, userType);
            vector1.add(a);
            outputFile.writeObject(vector1);
            signUp = true;
             Outstream.close();
        outputFile.close();
        }
        else{
            if(userType == "Teacher"){
                User a = new Teacher(pass, UserID, userType);
                vector1.add(a);
                outputFile.writeObject(vector1);
                signUp = true;
             Outstream.close();
        outputFile.close();
            }
            else{
                if(userType == "Administrator"){
                    User a = new Administrator(pass, UserID, userType);
                    vector1.add(a);
                    outputFile.writeObject(vector1);
                    signUp = true;
             Outstream.close();
        outputFile.close();
            }
        }
            }
            }
             catch(Exception e){
                 e.getMessage();
             }
        }
        else{
            if(!file.exists()){
                try{
                    FileOutputStream Outstream = new FileOutputStream(file);
        ObjectOutputStream outputFile = new ObjectOutputStream(Outstream);
               if(userType == "Student"){
            User a = new Student(pass, UserID, userType);
            vector1.add(a);
            outputFile.writeObject(vector1);
            signUp = true;
             Outstream.close();
        outputFile.close();
        }
        else{
            if(userType == "Teacher"){
                User a = new Teacher(pass, UserID, userType);
                vector1.add(a);
                outputFile.writeObject(vector1);
                signUp = true;
             Outstream.close();
        outputFile.close();
            }
            else{
                if(userType == "Administrator"){
                    User a = new Administrator(pass, UserID, userType);
                    vector1.add(a);
                    outputFile.writeObject(vector1);
                    signUp = true;
             Outstream.close();
        outputFile.close();
            }
        }
            }
                }
                catch(Exception e){
                    e.getMessage();
                }
            }
        }
         return signUp;
     }
     
     public boolean LogIn(String pass, String UserID, String userType)throws Exception{ 
      //boolean endOfFile = false;  
      boolean  logIn = false;
      FileInputStream fstream = new FileInputStream(file);
      ObjectInputStream inputFile = new ObjectInputStream(fstream); 
      Vector<User> vector2 = new Vector();
      vector2 = (Vector<User>)inputFile.readObject();
      fstream.close();
      inputFile.close();
      
      for(int i = 0;i < vector2.size();i++){
          if((vector2.get(i)).password.equals(pass) && (vector2.get(i)).ID.equals(UserID) && (vector2.get(i)).UserType.equals(userType))
          {
              logIn = true;
              break;
      }
     
     }
       return logIn;
    }
}
      
     

    
  
