import matplotlib.pyplot as plt
from calc import calculate, substitute


def plot(expression):
    x_vals = range(-100, 100)
    y_vals = []
    skip = None
    try:
        for x in x_vals:
            skip = x
            y_vals.append(substitute(expression, x))
    # cant divide by zero so remove this x from values and try again.
    except ZeroDivisionError:
        y_vals = []
        x_vals = [x for x in x_vals if x != skip]
        for x in x_vals:
            y_vals.append(substitute(expression, x))

    plt.plot(x_vals, y_vals)
    plt.title("y=" + expression)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


if __name__ == '__main__':
    print("Enter an expression or equation ('q' to quit)")
    user_input = input("> ")
    while user_input != "q":

        stripped = "".join(user_input.split())

        if stripped[:2] == "y=":
            plot(stripped[2:])

        else:  # default to normal calculator operation from main.py
            try:
                value = calculate(user_input)
            except ZeroDivisionError:
                value = None
            print("> " + str(value if value is not None else "error"))

        user_input = input("> ")
