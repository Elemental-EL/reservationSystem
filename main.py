import sys

import user
import reservation


def main_menu(username):
    """gives you the option to navigate through the app."""
    print("1. My Reservations")
    print("2. Available Reservations")
    print("3. Log Out")
    choice = input("Choose an option: ")
    if choice == '1':
        reservation.my_reservations(username)
    elif choice == '2':
        reservation.available_reservations(username)
    elif choice == '3':
        main()


def main():
    while True:
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        choice0 = input("Choose an option: ")

        if choice0 == '1':
            username = user.sign_up()
            if username:
                main_menu(username)
        elif choice0 == '2':
            username = user.log_in()
            if username:
                main_menu(username)
        elif choice0 == '3':
            sys.exit()
        else:
            print("Invalid input, please try again.")


if __name__ == "__main__":
    main()
