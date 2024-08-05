import unittest
from unittest.mock import patch, MagicMock
import report
import json


class TestReportModule(unittest.TestCase):

    @patch("report.os.path.exists", return_value=False)
    def test_load_reservations_file_not_exist(self, mock_exists):
        result = report.load_reservations()
        self.assertEqual(result, {})

    @patch("report.os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=unittest.mock.mock_open,
           read_data='{"2024-08-04 10:00": [{"username": "test_user"}]}')
    def test_load_reservations_file_exist(self, mock_open, mock_exists):
        result = report.load_reservations()
        expected = {"2024-08-04 10:00": [{"username": "test_user"}]}
        self.assertEqual(result, expected)

    def test_get_most_booked_days_and_times(self):
        reservations = {
            "2024-08-04 10:00": [{"username": "user1"}, {"username": "user2"}],
            "2024-08-04 11:00": [{"username": "user1"}],
            "2024-08-05 10:00": [{"username": "user1"}],
        }
        most_common_days, most_common_times, most_common_weekly_times = report.get_most_booked_days_and_times(
            reservations)

        expected_days = [("Sunday", 3), ("Monday", 1)]
        expected_times = [("10:00", 3), ("11:00", 1)]
        expected_weekly_times = [(("Sunday", "10:00"), 2), (("Sunday", "11:00"), 1), (("Monday", "10:00"), 1)]

        self.assertEqual(most_common_days, expected_days)
        self.assertEqual(most_common_times, expected_times)
        self.assertEqual(most_common_weekly_times, expected_weekly_times)

    @patch("report.console.print")
    def test_show_report_no_reservations(self, mock_print):
        report.show_report([], [], [], "1")
        mock_print.assert_any_call("[bold red]No reservations found.[/bold red]")

    @patch("report.console.print")
    def test_show_report_with_data(self, mock_print):
        most_common_days = [("Monday", 5)]
        most_common_times = [("10:00", 5)]
        most_common_weekly_times = [(("Monday", "10:00"), 5)]

        report.show_report(most_common_days, most_common_times, most_common_weekly_times, "1")
        report.show_report(most_common_days, most_common_times, most_common_weekly_times, "2")
        report.show_report(most_common_days, most_common_times, most_common_weekly_times, "3")

        self.assertTrue(mock_print.called)

    @patch("report.load_reservations", return_value={"2024-08-04 10:00": [{"username": "test_user"}]})
    @patch("report.get_most_booked_days_and_times", return_value=([], [], []))
    @patch("report.show_report")
    @patch("report.Prompt.ask", side_effect=["4"])
    def test_generate_report(self, mock_ask, mock_show_report, mock_get_most_booked_days_and_times,
                             mock_load_reservations):
        report.generate_report()
        mock_load_reservations.assert_called_once()
        mock_get_most_booked_days_and_times.assert_called_once()
        mock_show_report.assert_not_called()

    @patch("report.load_reservations", return_value={"2024-08-04 10:00": [{"username": "test_user"}]})
    @patch("report.get_most_booked_days_and_times", return_value=([], [], []))
    @patch("report.show_report")
    @patch("report.Prompt.ask", side_effect=["1", "4"])
    def test_generate_report_with_report_type(self, mock_ask, mock_show_report, mock_get_most_booked_days_and_times,
                                              mock_load_reservations):
        report.generate_report()
        mock_load_reservations.assert_called_once()
        mock_get_most_booked_days_and_times.assert_called_once()
        mock_show_report.assert_called_once()


if __name__ == "__main__":
    unittest.main()
