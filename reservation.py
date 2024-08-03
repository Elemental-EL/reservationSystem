import json
import os
import datetime

import main

TIME_SLOTS = ["09:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00", "23:00"]


def load_reservations():
    """Loads the reservations that have been made until now."""
    if not os.path.exists("reservations.json"):
        return {}
    with open("reservations.json", 'r') as file:
        return json.load(file)


def save_reservations(reservations):
    """Saves the reservations with the new changes made to them."""
    with open("reservations.json", 'w') as file:
        json.dump(reservations, file)


def get_reservation_key(date, time):
    """Gets the reservation key for the given date and time."""
    return f"{date} {time}"


def is_slot_reserved(reservations, date, time, slot):
    """Checks if the given slot is reserved for the given date and time."""
    key = get_reservation_key(date, time)
    return key in reservations and any(reservation['slot'] == slot for reservation in reservations[key])


def make_reservation(date, time, slot, username):
    """Creates a new reservation for the given date and time and slot."""
    reservations = load_reservations()
    key = get_reservation_key(date, time)
    if key not in reservations:
        reservations[key] = []
    reservations[key].append({'slot': slot, 'username': username})
    save_reservations(reservations)
    print("Reservation confirmed.")


def show_menu(options):
    """Enumerates the options of each menu and returns the index of the chosen option."""
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    choice = int(input("Choose an option: ")) - 1
    return choice


def time_menu(date, username):
    """Checks for the available times for the given date and shows them."""
    reservations = load_reservations()
    today = datetime.date.today()
    current_time = datetime.datetime.now().time()
    options = [
        time for time in TIME_SLOTS
        if not all(is_slot_reserved(reservations, date, time, slot) for slot in range(1, 4)) and
           (date != today.isoformat() or datetime.datetime.strptime(time, "%H:%M").time() > current_time)
    ]
    if not options:
        print("No available times for this date.")
        return

    options.append("Back")
    choice = show_menu(options)
    if choice == len(options) - 1:
        return
    selected_time = options[choice]
    slot_menu(date, selected_time, username)


def slot_menu(date, time, username):
    """Checks for the available slots for the given date and time and shows them."""
    reservations = load_reservations()
    options = [f"Slot {i}" for i in range(1, 4) if not is_slot_reserved(reservations, date, time, i)]
    if not options:
        print("No available slots for this time.")
        return

    options.append("Back")
    choice = show_menu(options)
    if choice == len(options) - 1:
        return
    selected_slot = int(options[choice].split()[1])

    confirm_reservation(date, time, selected_slot, username)


def confirm_reservation(date, time, selected_slot, username):
    """Double checks for the users decision and finalizes the reservation if the input is yes."""
    confirmation = input(f"Do you want to reserve {date} at {time}, Slot {selected_slot}? (yes/no): ")
    if confirmation.lower() == 'yes':
        make_reservation(date, time, selected_slot, username)
    elif confirmation.lower() == 'no':
        print("Reservation cancelled.")
    else:
        print("Invalid input, please try again.")
        confirm_reservation(date, time, selected_slot, username)


def available_reservations(username):
    """Creates a menu with available dates for reservation with the option to navigate between each week and
    selecting the desired dated."""
    reservations = load_reservations()
    today = datetime.date.today()
    start_date = today
    while True:
        options = []
        for i in range(7):
            date = start_date + datetime.timedelta(days=i)
            current_time = datetime.datetime.now().time()
            available_times = [
                time for time in TIME_SLOTS
                if not all(is_slot_reserved(reservations, date.isoformat(), time, slot) for slot in range(1, 4)) and
                   (date != today or datetime.datetime.strptime(time, "%H:%M").time() > current_time)
            ]
            if available_times:
                options.append(f"{date} ({date.strftime('%A')})")
        options.append("Next week")
        if start_date > today:
            options.append("Previous week")
        options.append("Exit")

        choice = show_menu(options)
        if choice == len(options) - 1:
            main.main_menu(username)
        elif choice == len(options) - 2 and start_date > today:
            start_date -= datetime.timedelta(days=7)
        elif choice == len(options) - 3 and start_date > today:
            start_date += datetime.timedelta(days=7)
        elif choice == len(options) - 2 and start_date <= today:
            start_date += datetime.timedelta(days=7)
        else:
            selected_date = start_date + datetime.timedelta(days=choice)
            time_menu(selected_date.isoformat(), username)


def my_reservations(username):
    reservations = load_reservations()
    user_reservations = [res for res in reservations.keys() if reservations[res]['username'] == username]

    if not user_reservations:
        print("You have no reservations.")
    else:
        print("My Reservations:")
        for res in user_reservations:
            print(f"- {res}: {reservations[res]['details']}")
