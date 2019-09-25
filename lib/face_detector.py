#test thoi chua chinh thuc
import numpy as np 
import cv2 
import pickle
from data import Data
class Face_detector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {"person_name": 1}
        self.cap = cv2.VideoCapture(0)

    def detect(self):
        self.recognizer.read("dataset/face_model/trainner.yml")
        with open("dataset/face_model/labels.pickle", 'rb') as f: #wb writing bytes, f file
            og_labels = pickle.load(f)
            self.labels = {v:k for k,v in og_labels.items()}
        i = 0
        while (True):
            #Capture frame 1 1
            ret, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) # This parameter will affect the quality of the detected face
            for (x, y, w, h) in faces: # Toa Do
                print(x, y, w, h)   
                roi_gray = gray[y:y+h, x:x+w] #(ycoordina_start, ycoordina_end)
                roi_color = frame[y:y+h, x:x+w]
                id_, conf = self.recognizer.predict(roi_gray)
                if conf>=45 and conf <=85:
                    print(id_)
                    print(self.labels[id_])
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    name = self.labels[id_]
                    color = (255, 255, 255)
                    stroke= 2
                    cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                Data.add(i, 'temp', roi_gray)

                self.display(frame, x, y, w, h)
            i+=1

            cv2.imshow('frame', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
                
        self.cap.release()
        cv2.destroyAllWindows()






    def display(self, frame, x, y, w, h):
        color = (102, 255, 102) #BGR 0-255
        stroke = 1
        end_cord_x = x + w #chieu  ngang
        end_cord_y = y + h  #chieu cao
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke) #Tạo khung

