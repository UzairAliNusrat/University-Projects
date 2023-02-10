/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Course_Management_System;

import java.io.IOException;
import java.io.ObjectInput;
import java.io.ObjectOutput;
import java.io.Serializable;

/**
 *
 * @author Owner
 */
public abstract class User implements Serializable {
   
   protected String password;
   protected String ID;
   protected String UserType;
  
   
   public User(String pass, String UserID, String userType){
       
       password = pass;
       ID = UserID;
       UserType = userType;
   }
   
}
