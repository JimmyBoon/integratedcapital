import time


def UserInterface(options):
    '''Prints a list of options and takes a user input.
    Params: options (list), list of strings to display as the options.
    Returns: (int), the option selected by the user.
    '''
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


def asyncTimer(func):
    '''Timer decorator: prints the time the function took to run for async'''
    async def wrapper_function(*args, **kwargs):
        start_time = time.time()
        await func(*args,  **kwargs)
        print(f"--- Process time: {(time.time() - start_time)} seconds ---")
    return wrapper_function


