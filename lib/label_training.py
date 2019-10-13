import os
from PIL import Image
import numpy as np
import cv2
import pickle
#The endswith() method returns True if the string ends with the specified value, otherwise False.
class Label_training:
  def train():
    image_dir = "dataset/face_recognition/"

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    y_labels = []
    x_train = []

    for root, dirs, files in os.walk(image_dir):
        if (dirs != 'dataset/face_recognition/fake' and dir != 'dataset/face_recognition/real' ):
            for file in files:
                    if file.endswith("png") or file.endswith("jpg"):
                        path = os.path.join(root, file)
                        label = os.path.basename(root).replace(" ", "-").lower()
                        print(label, path)
                        if not label in label_ids:
                            label_ids[label] = current_id
                            current_id += 1
                        id_ = label_ids[label]
                        print(label_ids)
                        #y_labels.append(label) #number
                        #x_train.append(path) # verify image, turn Numy array
                        pil_image = Image.open(path).convert("L") #grayscale
                        size = (550, 550)
                        final_image = pil_image.resize(size, Image.ANTIALIAS)            
                        image_array = np.array(pil_image, "uint8")
                        print(image_array)
                        x_train.append(image_array)
                        y_labels.append(id_)
    print(y_labels)
    print(x_train)
    with open("dataset/face_model/labels.pickle", 'wb') as f: #wb writing bytes, f file
        pickle.dump(label_ids, f)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("dataset/face_model/trainner.yml")