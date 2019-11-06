import numpy as np 
import cv2
import datetime
import os
import time
import shutil
import mysql.connector

class Data:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="linhkiet_2291998",
            database="project"
            )
        self.cursor = self.mydb.cursor()
    
    def __del__(self):
        self.mydb.close()

    def get_time_string(self):
        return datetime.datetime.now().strftime("%I%M%m%d%Y")
    
    def check_and_create_dir(self,str):
        if not os.path.exists(str):
            os.makedirs(str)

    # def add(self, i ,name, img):
    #     dir = "dataset/face_recognition/" + name + "/"
    #     Data.check_and_create_dir(dir)
    #     img_item = dir + str(i) + Data.get_time_string() +".png"
    #     cv2.imwrite(img_item, img)
    
    def del_old(self, f_name):
        dir = "dataset/face_recognition/" + f_name
        os.remove(dir)

    # def add_from_temp(self, name):
    #     dest = "dataset/face_recognition/" + name + "/"
    #     Data.check_and_create_dir(dest)
    #     source = 'dataset/face_recognition/temp/'
    #     files = os.listdir(source)

    #     for f in files:
    #         shutil.move(source+f, dest)
    
    
    def add_data(self, s_id):
        dir = "dataset/face_recognition/" 
        self.check_and_create_dir(dir)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        list_img = []

        cap = cv2.VideoCapture(0)
        i=0
        while i<150:
            #Capture frame 1 1
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5,minSize=(150,150)) # This parameter will affect the quality of the detected face
            for (x, y, w, h) in faces: # Toa Do
                print(x, y, w, h)   
                roi_color = frame[y:y+h, x:x+w]
                pic_id = str(i) + self.get_time_string()
                img_item = dir + pic_id +".png"
                cv2.imwrite(img_item, roi_color)
                list_img.append(pic_id)
                i+=1

                color = (102, 255, 102) #BGR 0-255
                stroke = 1
                end_cord_x = x + w #chieu  ngang
                end_cord_y = y + h  #chieu cao
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke) #Tạo khung
            #Result display
            cv2.imshow('frame', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
            

        cap.release()
        cv2.destroyAllWindows()
        self.save_image_to_db(list_img, s_id)
        
        
    def save_image_to_db(self, list, s_id):
        for i in list:
            self.addDb_dataset(i, s_id)

    def edit_data(self,s_id):
        old = self.getDb_dataset_id(s_id)
        self.add_data(s_id)
        for i in old:
            self.delDb_dataset(i)
            self.del_old(i + '.png')

    def del_data(self, s_id):
        data = self.getDb_dataset_id(s_id)
        for i in data:
            self.delDb_dataset(i)
            self.del_old(i + '.png')
        self.delDb_student(s_id)


    def addLiveData(self, name):
        dir = "dataset/liveness_detector/" + name + "/"
        self.check_and_create_dir(dir)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        cap = cv2.VideoCapture(0)
        i=0
        while 1:
            #Capture frame 1 1
            ret, frame = cap.read()
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=5,minSize=(120,120)) # This parameter will affect the quality of the detected face
            for (x, y, w, h) in faces: # Toa Do
                print(x, y, w, h)   
                roi_color = frame[y:y+h, x:x+w]
                img_item = dir + str(i) + self.get_time_string() +".png"
                cv2.imwrite(img_item, roi_color)

                color = (102, 255, 102) #BGR 0-255
                stroke = 1
                end_cord_x = x + w #chieu  ngang
                end_cord_y = y + h  #chieu cao
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke) #Tạo khung
            #Result display
            cv2.imshow('frame', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
            i+=1

        cap.release()
        cv2.destroyAllWindows()

    def addDb_dataset(self, pic_id, s_id):
        query = 'insert into `dataset` values(%s, %s)'
        val = (pic_id, s_id)
        self.cursor.execute(query, val)
        self.mydb.commit()

    def addDb_student(self, s_id, name):
        querry = 'insert into `students` values(%s, %s)'
        val = (s_id, name)
        self.cursor.execute(querry, val)
        self.mydb.commit()

    def delDb_dataset(self, id):
        query = 'delete from `dataset` where id = %s'
        val = (id,)
        self.cursor.execute(query, val)
        self.mydb.commit()

    def getDb_dataset_id(self, s_id):
        list = []
        query = 'select id from `dataset` where s_id = %s'
        val = (s_id,)
        self.cursor.execute(query, val)
        result = self.cursor.fetchall()
        for x in result:
            list.append(x[0])
        return list
    
    def delDb_student(self, id):
        query = 'delete from `students` where id = %s'
        val = (id,)
        self.cursor.execute(query, val)
        self.mydb.commit()

    def getDb_dataset_sid(self, id):
        query = 'select s_id from `dataset` where id = %s'
        val = (id,)
        self.cursor.execute(query, val)
        result = self.cursor.fetchone()
        return result[0]

    def getDb_students_name(self, id):
        query = 'select name from `student` where id = %s'
        val = (id,)
        self.cursor.execute(query, val)
        result = self.cursor.fetchone()
        return result[0]

    def getDb_attendace(self, date):
        list = []
        query = "call attendList(%s);"
        val = (date,)
        self.cursor.execute(query, val)
        result = self.cursor.fetchall()
        for x in result:
            y = ( x[0], x[1], x[2], str(x[3]), x[4] )
            list.append(y)
        return list






        





        
        
        


    
