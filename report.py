import json
import os
from collections import Counter
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from datetime import datetime

import main
import reservation

console = Console()


def load_reservations():
    """Loads the reservations that have been made until now."""
    if not os.path.exists("reservations.json"):
        return {}
    with open("reservations.json", 'r') as file:
        return json.load(file)


def get_most_booked_days_and_times(reservations, username=None):
    """Gets the most booked days of the week and their times of the day."""
    day_counter = Counter()
    time_counter = Counter()
    weekly_time_counter = Counter()

    for key, slots in reservations.items():
        date_str, time_str = key.split()
        day_of_week = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
        for res in slots:
            if username is None or res['username'] == username:
                day_counter[day_of_week] += 1
                time_counter[time_str] += 1
                weekly_time_counter[(day_of_week, time_str)] += 1

    most_common_days = day_counter.most_common(5)
    most_common_times = time_counter.most_common(5)
    most_common_weekly_times = weekly_time_counter.most_common(5)

    return most_common_days, most_common_times, most_common_weekly_times


def show_report(most_common_days, most_common_times, most_common_weekly_times, report_type, title="Reservation Report"):
    """Displays the report relative to the report type."""
    console.print(f"[bold blue]{title}[/bold blue]", justify="center")

    if report_type == "1":
        if not most_common_days:
            console.print("[bold red]No reservations found.[/bold red]")
            return
        day_table = Table(title="Most Booked Days of the Week", show_header=True, header_style="bold magenta")
        day_table.add_column("Day", style="cyan", no_wrap=True)
        day_table.add_column("Number of Bookings", justify="right", style="green")

        for day, count in most_common_days:
            day_table.add_row(day, str(count))

        console.print(day_table)

    elif report_type == "2":
        if not most_common_times:
            console.print("[bold red]No reservations found.[/bold red]")
            return
        time_table = Table(title="Most Booked Times of the Day", show_header=True, header_style="bold magenta")
        time_table.add_column("Time", style="cyan", no_wrap=True)
        time_table.add_column("Number of Bookings", justify="right", style="green")

        for time, count in most_common_times:
            time_table.add_row(time, str(count))

        console.print(time_table)

    elif report_type == "3":
        if not most_common_weekly_times:
            console.print("[bold red]No reservations found.[/bold red]")
            return
        weekly_time_table = Table(title="Most Specifically Booked Weekly Times", show_header=True, header_style="bold magenta")
        weekly_time_table.add_column("Day and Time", style="cyan", no_wrap=True)
        weekly_time_table.add_column("Number of Bookings", justify="right", style="green")

        for (day, time), count in most_common_weekly_times:
            weekly_time_table.add_row(f"{day} at {time}", str(count))

        console.print(weekly_time_table)


def generate_report(username=None):
    """Generates the report for either all users or the specified user."""
    reservations = load_reservations()
    most_common_days, most_common_times, most_common_weekly_times = get_most_booked_days_and_times(reservations, username)

    title = "Reservation Report for All Users" if username is None else f"Reservation Report for {username}"

    report_options = ["Most Booked Days of the Week", "Most Booked Times of the Day", "Most Booked Weekly Times", "Back"]
    report_choices = {str(i): option for i, option in enumerate(report_options, start=1)}

    while True:
        console.print("[bold blue]Choose report type[/bold blue]")
        for key, value in report_choices.items():
            console.print(f"{key}. {value}")

        report_type = Prompt.ask("Choose report type", choices=list(report_choices.keys()), default="4")

        if report_type == "4":
            break

        show_report(most_common_days, most_common_times, most_common_weekly_times, report_type, title)


def report_menu(username):
    """Gives you the option to view reservation reports."""
    while True:
        options = ["All Users", "My Reservations", "Back"]
        choice = reservation.show_menu(options, title="[bold blue]Reservation Report Menu[/bold blue]")
        if choice == 0:
            generate_report()
        elif choice == 1:
            generate_report(username)
        elif choice == 2:
            main.main_menu(username)
