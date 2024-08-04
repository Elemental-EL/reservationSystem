import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
import user
import reservation

console = Console(color_system="windows")


def main_menu(username):
    """gives you the option to navigate through the app."""
    options = ["My reservations", "Available reservations", "Exit"]
    choice = reservation.show_menu(options, title="[bold blue]Main Menu[/bold blue]")
    if choice == 0:
        reservation.view_reservations(username)
    elif choice == 1:
        reservation.available_reservations(username)
    elif choice == 2:
        main()


def main():
    while True:
        options = ["Sign Up", "Log In", "Exit"]
        choice = reservation.show_menu(options, title="[bold blue]Welcome Menu[/bold blue]")

        if choice == 0:
            username = user.sign_up()
            if username:
                main_menu(username)
        elif choice == 1:
            username = user.log_in()
            if username:
                main_menu(username)
        elif choice == 2:
            sys.exit()


if __name__ == "__main__":
    main()
