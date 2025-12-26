import random
import sys

# ---------------------------------------------
# Helper Functions
# ---------------------------------------------
def wait():
    input("\nPress ENTER to continue...")

# ---------------------------------------------
# LEVEL 1 — BASIC
# ---------------------------------------------
def level_1():
    print("\n=== LEVEL 1: BASIC ===")

    # Exercise 1
    name = input("1) What's your name? ")
    print(f"Hello, {name}!")

    print("\n2) Printing numbers 1–10:")
    for i in range(1, 11):
        print(i, end=" ")

    wait()

    # Exercise 2 — Swap variables
    print("\n3) Swap two variables (you choose numbers)")
    a = int(input("Enter a: "))
    b = int(input("Enter b: "))
    print(f"Before swap → a={a}, b={b}")
    a, b = b, a
    print(f"After swap  → a={a}, b={b}")

    wait()

    # Exercise 3 — Even or odd
    num = int(input("\n4) Enter a number to check even/odd: "))
    if num % 2 == 0:
        print("It's even.")
    else:
        print("It's odd.")

    wait()

    # Exercise 4 — Multiplication table
    print("\n5) Multiplication table")
    n = int(input("Enter a number: "))
    for i in range(1, 11):
        print(f"{n} × {i} = {n * i}")

    print("\n🎉 LEVEL 1 COMPLETE!")
    wait()


# ---------------------------------------------
# LEVEL 2 — INTERMEDIATE
# ---------------------------------------------
def level_2():
    print("\n=== LEVEL 2: INTERMEDIATE ===")

    # Exercise 1 — Largest in a list
    print("\n1) Finding largest number in a list...")
    nums = [random.randint(1, 50) for _ in range(10)]
    print("List:", nums)
    print("Largest number:", max(nums))

    wait()

    # Exercise 2 — Word count
    print("\n2) Word counting")
    sentence = input("Enter a sentence: ").lower().split()
    counts = {}
    for word in sentence:
        counts[word] = counts.get(word, 0) + 1
    print("Word counts:", counts)

    wait()

    # Exercise 3 — Guess the number game
    print("\n3) Guess the number (1–50)")
    secret = random.randint(1, 50)
    attempts = 0

    while True:
        guess = int(input("Your guess: "))
        attempts += 1
        if guess == secret:
            print(f"Correct! You guessed it in {attempts} attempts!")
            break
        elif guess < secret:
            print("Higher!")
        else:
            print("Lower!")

    print("\n🎉 LEVEL 2 COMPLETE!")
    wait()


# ---------------------------------------------
# LEVEL 3 — ADVANCED
# ---------------------------------------------
def level_3():
    print("\n=== LEVEL 3: ADVANCED ===")

    # Exercise 1 — Fibonacci using recursion
    print("\n1) Fibonacci using recursion")

    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    n = int(input("Enter n: "))
    print(f"fib({n}) = {fib(n)}")

    wait()

    # Exercise 2 — Bubble sort
    print("\n2) Bubble Sort demonstration")
    arr = [random.randint(1, 100) for _ in range(8)]
    print("Unsorted:", arr)

    for i in range(len(arr)):
        for j in range(len(arr) - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    print("Sorted:  ", arr)

    wait()

    # Exercise 3 — Simple OOP
    print("\n3) Car Class Example")

    class Car:
        def __init__(self, brand, model):
            self.brand = brand
            self.model = model
            self.speed = 0

        def accelerate(self):
            self.speed += 10
            print(f"{self.brand} {self.model} speed: {self.speed}")

        def brake(self):
            self.speed = max(0, self.speed - 10)
            print(f"{self.brand} {self.model} speed: {self.speed}")

    car = Car("Tesla", "Model S")
    car.accelerate()
    car.accelerate()
    car.brake()

    print("\n🎉 LEVEL 3 COMPLETE!")
    wait()


# ---------------------------------------------
# MAIN GAME LOOP
# ---------------------------------------------
def main():
    while True:
        print("\n=====================================")
        print("     🐍 Python Training Game 🕹️")
        print("=====================================")
        print("1) Start Level 1 (Basic)")
        print("2) Start Level 2 (Intermediate)")
        print("3) Start Level 3 (Advanced)")
        print("4) Exit Game")

        choice = input("\nChoose an option: ")

        if choice == "1":
            level_1()
        elif choice == "2":
            level_2()
        elif choice == "3":
            level_3()
        elif choice == "4":
            print("\nGoodbye! Keep practicing Python! 🚀")
            sys.exit()
        else:
            print("Invalid choice! Try again.")

# Run game
main()
