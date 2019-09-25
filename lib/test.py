from add_data import Add_data
from liveness_detector.liveness_training import Liveness_training

class Test:
    print("Option:")
    print("1. Add new data")
    print("2. Train liveness detector")
    option = input("Your option: ")
    if option == "1":
        name = input("Enter your name: ")
        Add_data.add(name)
    if option == "2":
        liveness = Liveness_training()
        liveness.train()

    


