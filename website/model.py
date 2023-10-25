from _ast import Pass

import mysql.connector
from app import connection
from flask import session
from werkzeug.security import generate_password_hash,check_password_hash
import hashlib
import os
class UserModel:
    def __init__(self,connection):
        self.connection=connection
        # self.secret_key=secret_key

    def add_user(self,User_Name,Email,Password):
        cursor=self.connection.cursor()
        Password=Password.encode()
        data=hashlib.sha256(Password).hexdigest()
        # hashpass=generate_password_hash(Password).encode()
        insert_qry="INSERT INTO users(User_Name,Email,Password) VALUES (%s,%s,%s)"
        cursor.execute(insert_qry,(User_Name,Email,data))
        self.connection.commit()
        cursor.close()

    def get_user(self,Email):
        cursor=self.connection.cursor()

        select_qry="SELECT User_Name,Email,Password FROM users WHERE Email= '%s'"
        cursor.execute(select_qry,(Email))
        user=cursor.fetchone()
        cursor.close()
        return user

    def edit_user(self,Email,User_Name,Profile_Img,Bio):
        cursor=self.connection.cursor()
        qry="UPDATE users SET User_Name = %s, Profile_Img = %s, Bio = %s WHERE Email = %s"
        try:
            cursor.execute(qry,(User_Name,Profile_Img,Bio,Email))
            self.connection.commit()
            if cursor.rowcount >0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error updating user data: {str(e)}")
            self.connection.rollback()
            return False  # Error occurred while updating
        finally:
            cursor.close()

    def validate_pass(self,Email,Password):
        cursor = self.connection.cursor()
        # cur=connection.cursor()
        print("pass",Password)
        entered_hashed_password = hashlib.sha256((Password).encode()).hexdigest()
        print(entered_hashed_password)
        select_qry = "SELECT * FROM users WHERE Email=%s AND Password=%s"
        cursor.execute(select_qry, (Email,entered_hashed_password))
        user = cursor.fetchone()
        print(user)
        cursor.close()

        if user:

            if user[3] == entered_hashed_password:
                return user
        return None

class Pin:
    def __init__(self, connection):
        self.connection = connection

    def addPin(self,User_Id,Title,Img_URL):
        cursor=self.connection.cursor()
        # User_Id=session.get('uid')
        # print(User_Id)
        insert_qry="INSERT INTO pins(User_Id,Description,Title,IMG_URL) VALUES (%s,%s,%s,%s)"
        cursor.execute(insert_qry,(User_Id," ",Title,Img_URL))
        self.connection.commit()
        cursor.close()

    def RecentPins(self):
        cur=self.connection.cursor()
        cur.execute("SELECT IMG_URL FROM pins ORDER BY Pin_Date DESC LIMIT 3")
        recent_pins=cur.fetchall()
        filename = [os.path.basename(path[0]) for path in recent_pins]
        print(filename)
        return recent_pins
