#test thoi chua chinh thuc
import numpy as np 
import cv2 
import pickle
from data import Data
from keras.models import load_model
from keras.preprocessing.image import img_to_array

class Face_detector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {"person_name": 1}
        self.cap = cv2.VideoCapture(0)

    def detect(self):
        # load the liveness detector model and label encoder from disk
        print("[INFO] loading liveness detector...")
        live_model = load_model('dataset/liveness_model/liveness.model')
        le = pickle.loads(open('dataset/liveness_model/livenesspickle.le', "rb").read())

        # load face detect model
        self.recognizer.read("dataset/face_model/trainner.yml")
        with open("dataset/face_model/labels.pickle", 'rb') as f: #wb writing bytes, f file
            og_labels = pickle.load(f)
            self.labels = {v:k for k,v in og_labels.items()}
        i = 0
        while (True):
            #Capture frame 1 1
            ret, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5,minSize=(150,150)) # This parameter will affect the quality of the detected face
            for (x, y, w, h) in faces: # Toa Do
                print(x, y, w, h)   
                roi_gray = gray[y:y+h, x:x+w] #(ycoordina_start, ycoordina_end)
                roi_color = frame[y:y+h, x:x+w]
                
                # Detect liveness
                face = cv2.resize(roi_color, (32, 32))
                face = face.astype("float") / 255.0
                face = img_to_array(face)
                face = np.expand_dims(face, axis=0)
                preds = live_model.predict(face)[0]
                j = np.argmax(preds)
                live_label = le.classes_[j]

                # Recognize face
                id_, conf = self.recognizer.predict(roi_gray)
                if conf>=30 and conf <=50:
                    if(live_label == 'dataset/liveness_detector/real'):
                        print(id_)
                        print(self.labels[id_])
                        name = self.labels[id_]
                    else:
                        print('fake')
                        name = 'fake'
                # Data.add(i, 'temp', roi_gray)
                else:
                    print('Unknown')
                    name = 'Unknown'
                font = cv2.FONT_HERSHEY_SIMPLEX
                color = (255, 255, 255)
                stroke= 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

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


            

            