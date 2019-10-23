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
        print("7. Add data for liveness detector")
        print("8. Test liveness detector")
        print("9. Test edit dataset")
        print("10. Test delete dataset")
        option = input("Your option: ")
        if option == "1":
            id = input("Enter your id: ")
            name = input("Enter your name: ")
            data = Data()
            data.addDb_student(id, name)
            data.add_data(id, name)
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
        if option == '7':
            o = input("1 for real, 2 for fake: ")
            if o == '1':
                Data.addLiveData('real')
            elif o == '2':
                Data.addLiveData('fake')
        if option == '8':
            face_detector = Face_detector()
            face_detector.liveness_test()
        if option == '9':
            id = input("enter student id: ")
            data = Data()
            data.edit_data(id)
        if option == '10':
            id = input("enter student id: ")
            data = Data()
            data.del_data(id)
        
        if option == 'q':
            break


        


