import unittest
from unittest.mock import patch, MagicMock

from main import main, main_menu


class TestMainAppFunctions(unittest.TestCase):

    @patch('user.sign_up')
    @patch('user.log_in')
    @patch('main.main_menu')
    def test_sign_up(self, mock_main_menu, mock_log_in, mock_sign_up):
        mock_sign_up.return_value = 'test_user'
        with patch('builtins.input', side_effect=['1', '3']):
            with self.assertRaises(SystemExit):
                main()
        mock_sign_up.assert_called_once()
        mock_main_menu.assert_called_once_with('test_user')

    @patch('user.sign_up')
    @patch('user.log_in')
    @patch('main.main_menu')
    def test_log_in(self, mock_main_menu, mock_log_in, mock_sign_up):
        mock_log_in.return_value = 'test_user'
        with patch('builtins.input', side_effect=['2', '3']):
            with self.assertRaises(SystemExit):
                main()
        mock_log_in.assert_called_once()
        mock_main_menu.assert_called_once_with('test_user')

    def test_exit(self):
        with patch('builtins.input', side_effect=['3']):
            with self.assertRaises(SystemExit):
                main()

    @patch('reservation.view_reservations')
    @patch('reservation.available_reservations')
    @patch('report.report_menu')
    def test_main_menu_view_reservations(self, mock_report_menu, mock_available_reservations, mock_view_reservations):
        with patch('builtins.input', side_effect=['1']):
            main_menu('test_user')
        mock_view_reservations.assert_called_once_with('test_user')

    @patch('reservation.view_reservations')
    @patch('reservation.available_reservations')
    @patch('report.report_menu')
    def test_main_menu_available_reservations(self, mock_report_menu, mock_available_reservations,
                                              mock_view_reservations):
        with patch('builtins.input', side_effect=['2']):
            main_menu('test_user')
        mock_available_reservations.assert_called_once_with('test_user')

    @patch('reservation.view_reservations')
    @patch('reservation.available_reservations')
    @patch('report.report_menu')
    def test_main_menu_report_menu(self, mock_report_menu, mock_available_reservations, mock_view_reservations):
        with patch('builtins.input', side_effect=['3']):
            main_menu('test_user')
        mock_report_menu.assert_called_once_with('test_user')

    @patch('user.sign_up')
    @patch('user.log_in')
    @patch('main.main_menu')
    def test_invalid_input(self, mock_main_menu, mock_log_in, mock_sign_up):
        mock_sign_up.return_value = 'test_user'
        with patch('builtins.input', side_effect=['4', '1', '3']):
            with self.assertRaises(SystemExit):
                main()
        mock_sign_up.assert_called_once()
        mock_main_menu.assert_called_once_with('test_user')


if __name__ == '__main__':
    unittest.main()
