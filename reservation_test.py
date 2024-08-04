import unittest
from unittest.mock import patch, mock_open, MagicMock
import reservation
import datetime


class TestReservationModule(unittest.TestCase):

    @patch('reservation.os.path.exists', return_value=False)
    def test_load_reservations_no_file(self, mock_exists):
        reservations = reservation.load_reservations()
        self.assertEqual(reservations, {})

    @patch('reservation.os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open,
           read_data='{"2023-01-01 09:00": [{"slot": 1, "username": "user1"}]}')
    def test_load_reservations_with_file(self, mock_open, mock_exists):
        reservations = reservation.load_reservations()
        self.assertEqual(reservations, {"2023-01-01 09:00": [{"slot": 1, "username": "user1"}]})

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_reservations(self, mock_json_dump, mock_open):
        reservations = {"2023-01-01 09:00": [{"slot": 1, "username": "user1"}]}
        reservation.save_reservations(reservations)
        mock_open.assert_called_once_with("reservations.json", 'w')
        mock_json_dump.assert_called_once_with(reservations, mock_open())

    def test_get_reservation_key(self):
        key = reservation.get_reservation_key("2023-01-01", "09:00")
        self.assertEqual(key, "2023-01-01 09:00")

    @patch('reservation.load_reservations', return_value={"2023-01-01 09:00": [{"slot": 1, "username": "user1"}]})
    def test_is_slot_reserved(self, mock_load_reservations):
        reservations = reservation.load_reservations()
        reserved = reservation.is_slot_reserved(reservations, "2023-01-01", "09:00", 1)
        self.assertTrue(reserved)

    @patch('reservation.load_reservations', return_value={})
    @patch('reservation.save_reservations')
    @patch('reservation.console.print')
    def test_make_reservation(self, mock_print, mock_save_reservations, mock_load_reservations):
        reservation.make_reservation("2023-01-01", "09:00", 1, "user1")
        mock_save_reservations.assert_called_once()
        mock_print.assert_called_once_with("[bold green]Reservation confirmed.[/bold green]")

    @patch('reservation.load_reservations', return_value={
        "2023-01-01 09:00": [{"slot": 1, "username": "user1"}, {"slot": 2, "username": "user2"},
                             {"slot": 3, "username": "user3"}]})
    @patch('reservation.show_menu', return_value=0)
    def test_slot_menu_no_available_slots(self, mock_show_menu, mock_load_reservations):
        with patch('reservation.console.print') as mock_print:
            with patch('reservation.datetime') as mock_datetime:
                mock_datetime.date.today.return_value = datetime.date(2023, 1, 1)
                mock_datetime.datetime.now.return_value = datetime.datetime(2023, 1, 1, 8, 0)
                mock_datetime.datetime.strptime.side_effect = lambda *args, **kwargs: datetime.datetime.strptime(*args,
                                                                                                                 **kwargs)
                reservation.slot_menu("2023-01-01", "09:00", "user1")
                mock_print.assert_called_once_with("[bold red]No available slots for this time.[/bold red]")

    @patch('reservation.Confirm.ask', return_value=True)
    @patch('reservation.make_reservation')
    @patch('reservation.console.print')
    def test_confirm_reservation_yes(self, mock_print, mock_make_reservation, mock_confirm_ask):
        reservation.confirm_reservation("2023-01-01", "09:00", 1, "user1")
        mock_make_reservation.assert_called_once_with("2023-01-01", "09:00", 1, "user1")
        mock_print.assert_not_called()

    @patch('reservation.Confirm.ask', return_value=False)
    @patch('reservation.console.print')
    def test_confirm_reservation_no(self, mock_print, mock_confirm_ask):
        reservation.confirm_reservation("2023-01-01", "09:00", 1, "user1")
        mock_print.assert_called_once_with("[bold yellow]Reservation cancelled.[/bold yellow]")


if __name__ == '__main__':
    unittest.main()
