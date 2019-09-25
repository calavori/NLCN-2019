#test thoi chua chinh thuc


import numpy as np 
import cv2 
import pickle
class Face:
    def check():
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("dataset/face_model/trainner.yml")
        labels = {"person_name": 1}
        with open("dataset/face_model/labels.pickle", 'rb') as f: #wb writing bytes, f file
            og_labels = pickle.load(f)
            labels = {v:k for k,v in og_labels.items()}

        cap = cv2.VideoCapture(0)
        while (True):
            #Capture frame 1 1
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) # This parameter will affect the quality of the detected face
            for (x, y, w, h) in faces: # Toa Do
                print(x, y, w, h)   
                roi_gray = gray[y:y+h, x:x+w] #(ycoordina_start, ycoordina_end)
                roi_color = frame[y:y+h, x:x+w]
                id_, conf = recognizer.predict(roi_gray)
                if conf>=45 and conf <=85:
                    print(id_)
                    print(labels[id_])
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    name = labels[id_]
                    color = (255, 255, 255)
                    stroke= 2
                    cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                img_item = "images/id_.png"
                cv2.imwrite(img_item, roi_gray)

                color = (102, 255, 102) #BGR 0-255
                stroke = 1
                end_cord_x = x + w #chieu  ngang
                end_cord_y = y + h  #chieu cao
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke) #Tạo khung

        # eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=10) # This parameter will affect the quality of the detected face
            #for (x, y, w, h) in eyes: # Toa Do
            # print(x, y, w, h)   
            # roi_gray = gray[y:y+h, x:x+w] #(ycoordina_start, ycoordina_end)
            # roi_color = frame[y:y+h, x:x+w]

            # color = (255, 255, 102) #BGR 0-255
                #stroke = 1
                #end_cord_x = x + w #chieu  ngang
                #end_cord_y = y + h  #chieu cao
            # cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke) #Tạo khung
            #Result display
            cv2.imshow('frame', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()