from data import Data
from liveness_detector.liveness_training import Liveness_training
from label_training import Label_training
from face_detector import Face_detector

class Test:
    while(True):
        print("Option:")
        print("1. Add new data")
        print("2. Train liveness detector")
        print("3. Train face detector")
        print("4. Face detector")
        print("5. Add data from temp folder")
        print("6. Delete temp folder")
        option = input("Your option: ")
        if option == "1":
            name = input("Enter your name: ")
            Data.add_data(name)
        if option == "2":
            liveness = Liveness_training()
            liveness.train()
        if option == "3":
            Label_training.train()
        if option == "4":
            face_detector = Face_detector()
            face_detector.detect()
        if option == '5':
            name = input('Input name: ')
            Data.add_from_temp(name)
        if option == '6':
            Data.del_temp()
        if option == 'q':
            break


        


