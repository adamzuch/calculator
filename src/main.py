from calc import calculate


if __name__ == '__main__':
    print("Enter an expression ('q' to quit)")
    user_input = input("> ")
    while user_input != "q":
        try:
            value = calculate(user_input)
        except ZeroDivisionError:
            value = None
        print("> " + str(value if value is not None else "error"))
        user_input = input("> ")
