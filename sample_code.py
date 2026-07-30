def used_function():
    print("This function is actually used.")

def unused_function():
    print("Nobody calls this function anywhere!")

def main():
    used_function()

if __name__ == "__main__":
    main()
