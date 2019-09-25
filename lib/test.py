from add_data import Add_data
from liveness_detector.liveness_training import Liveness_training
from label_training import Label_training
from face import Face

class Test:
    print("Option:")
    print("1. Add new data")
    print("2. Train liveness detector")
    print("3. Train face detector")
    option = input("Your option: ")
    if option == "1":
        name = input("Enter your name: ")
        Add_data.add(name)
    if option == "2":
        liveness = Liveness_training()
        liveness.train()
    if option == "3":
        Label_training.train()
    if option == "4":
        Face.check()

    


