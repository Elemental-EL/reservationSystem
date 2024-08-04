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


def view_reservations(username):
    """Lets the user choose which reservation they want to view."""
    while True:
        options = ["History of reservations", "Current reservations", "Back"]
        choice = show_menu(options)
        if choice == 0:
            show_reservations(username, past=True)
        elif choice == 1:
            show_reservations(username, past=False)
        elif choice == 2:
            main.main_menu(username)


def show_reservations(username, past):
    """Views the reservations made by the user."""
    reservations = load_reservations()
    today = datetime.datetime.now()
    user_reservations = []

    for key, slots in reservations.items():
        for reservation in slots:
            if reservation['username'] == username:
                reservation_time = datetime.datetime.strptime(key, "%Y-%m-%d %H:%M")
                if (past and reservation_time < today) or (not past and reservation_time >= today):
                    user_reservations.append((reservation_time, reservation['slot']))

    if not user_reservations:
        print("No reservations found.")
        main.main_menu(username)

    user_reservations.sort()
    for idx, (res_time, slot) in enumerate(user_reservations, 1):
        print(f"{idx}. {res_time.strftime('%Y-%m-%d %H:%M')} - Slot {slot}")

    if past:
        input("Press Enter to go back.")
    else:
        options = [f"Cancel reservation {idx}" for idx in range(1, len(user_reservations) + 1)]
        options.append("Back")
        choice = show_menu(options)
        if choice == len(options) - 1:
            main.main_menu(username)
        confirm_cancellation(username, user_reservations[choice])


def confirm_cancellation(username, reservation):
    """Double checks for the users decision and finalizes the cancellation if the input is yes."""
    confirmation = input(f"Are you sure you want to cancel this reservation? (yes/no): ")
    if confirmation.lower() == 'yes':
        cancel_reservation(username, reservation)
    elif confirmation.lower() == 'no':
        print("Cancellation aborted.")
    else:
        print("Invalid input, please try again.")
        confirm_cancellation(username, reservation)


def cancel_reservation(username, reservation):
    """Cancels the reservation selected by the user."""
    reservations = load_reservations()
    key = reservation[0].strftime("%Y-%m-%d %H:%M")
    slot = reservation[1]

    if key in reservations:
        reservations[key] = [res for res in reservations[key] if
                             not (res['slot'] == slot and res['username'] == username)]
        if not reservations[key]:
            del reservations[key]
        save_reservations(reservations)
        print("Reservation cancelled.")
    else:
        print("Reservation not found.")
