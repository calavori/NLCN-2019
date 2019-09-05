from add_data import Add_data

class Test:
    print("Option:")
    print("1. Add new data")
    option = input("Your option: ")
    if option == "1":
        name = input("Enter your name: ")
        Add_data.add(name)
    


