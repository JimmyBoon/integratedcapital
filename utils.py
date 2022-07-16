def UserInterface(options):
    while True:
        print("Please select an option:")
        counter = 1
        for option in options:
            print(f"{counter}. {option}")
            counter += 1

        userInput = input()
        try:
            userSelection = int(userInput)
            if userSelection > 0 and userSelection <= len(options):
                return userSelection
            print("Invalid selection try again:")
            continue

        except:
            print("Invalid selection try again:")
            continue
