import user


def main():
    while True:
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            user.sign_up()
        elif choice == '2':
            user.log_in()
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
