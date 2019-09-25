import numpy as np 
import cv2
import datetime
import os
import time
import shutil

class Data:
    def get_time_string():
        return datetime.datetime.now().strftime("%I%M%m%d%Y")
    
    def check_and_create_dir(str):
        if not os.path.exists(str):
            os.makedirs(str)

    def add(i ,name, img):
        dir = "dataset/face_recognition/" + name + "/"
        Data.check_and_create_dir(dir)
        img_item = dir + str(i) + Data.get_time_string() +".png"
        cv2.imwrite(img_item, img)
    
    def del_temp():
        dir = "dataset/face_recognition/temp" 
        shutil.rmtree(dir, ignore_errors=True)

    def add_from_temp(name):
        dest = "dataset/face_recognition/" + name + "/"
        Data.check_and_create_dir(dest)
        source = 'dataset/face_recognition/temp/'
        files = os.listdir(source)

        for f in files:
            shutil.move(source+f, dest)
    
    
    def add_data(name):
        dir = "dataset/face_recognition" + name + "/"
        Data.check_and_create_dir(dir)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        cap = cv2.VideoCapture(0)
        timeout = time.time() + 10
        i=0
        while (time.time() <= timeout):
            #Capture frame 1 1
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) # This parameter will affect the quality of the detected face
            for (x, y, w, h) in faces: # Toa Do
                print(x, y, w, h)   
                roi_gray = gray[y:y+h, x:x+w] #(ycoordina_start, ycoordina_end)
                roi_color = frame[y:y+h, x:x+w]
                img_item = dir + str(i) + Data.get_time_string() +".png"
                cv2.imwrite(img_item, roi_gray)

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

    
