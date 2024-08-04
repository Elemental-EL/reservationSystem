import unittest
from unittest.mock import patch, mock_open, MagicMock
import bcrypt
import json
import os
from user import User, load_users, save_users, is_valid_password, validate_input, sign_up, log_in, validate_name


class TestUserModule(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    def test_load_users(self, mock_file):
        result = load_users()
        self.assertEqual(result, {})
        mock_file.assert_called_once_with('users.json', 'r')

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_users(self, mock_json_dump, mock_file):
        users = {
            'test_user': {'username': 'test_user', 'password': 'hashed_pw', 'first_name': 'Test', 'last_name': 'User'}}
        save_users(users)
        mock_file.assert_called_once_with('users.json', 'w')
        mock_json_dump.assert_called_once_with(users, mock_file())

    def test_is_valid_password(self):
        self.assertTrue(is_valid_password('Password123'))
        self.assertFalse(is_valid_password('short1'))
        self.assertFalse(is_valid_password('longpasswordwithoutdigits'))
        self.assertFalse(is_valid_password('12345678'))

    @patch("user.console.print")
    def test_validate_input(self, mock_console_print):
        self.assertTrue(validate_input("Username", "valid_username"))
        self.assertFalse(validate_input("Username", ""))
        mock_console_print.assert_called_with("[red]Username cannot be empty.[/red]")

    def test_validate_name(self):
        self.assertTrue(validate_name("John Doe"))
        self.assertTrue(validate_name("Jane"))
        self.assertFalse(validate_name("John123"))
        self.assertFalse(validate_name("John@Doe"))
        self.assertFalse(validate_name("John-Doe"))

    @patch("user.load_users", return_value={})
    @patch("user.save_users")
    @patch("rich.prompt.Prompt.ask", side_effect=['new_user', 'Password123', 'Test', 'User'])
    @patch("user.console.print")
    def test_sign_up(self, mock_console_print, mock_prompt, mock_save_users, mock_load_users):
        username = sign_up()
        self.assertEqual(username, 'new_user')
        mock_console_print.assert_any_call("[bold green]Sign up successful![/bold green]")
        mock_save_users.assert_called_once()
        args, kwargs = mock_save_users.call_args
        self.assertIn('new_user', args[0])
        saved_user = args[0]['new_user']
        self.assertTrue(bcrypt.checkpw('Password123'.encode('utf-8'), saved_user['password'].encode('utf-8')))

    @patch("user.load_users")
    @patch("rich.prompt.Prompt.ask", side_effect=['new_user', 'Password123'])
    @patch("rich.console.Console.print")
    def test_log_in_success(self, mock_print, mock_prompt, mock_load_users):
        mock_load_users.return_value = {
            'new_user': {
                'username': 'new_user',
                'password': bcrypt.hashpw('Password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                'first_name': 'Test',
                'last_name': 'User'
            }
        }
        username = log_in()
        self.assertEqual(username, 'new_user')
        mock_print.assert_any_call("[bold green]Login successful![/bold green]")

    @patch("user.load_users")
    @patch("rich.prompt.Prompt.ask", side_effect=['new_user', 'WrongPassword'])
    @patch("rich.console.Console.print")
    @patch("rich.prompt.Confirm.ask", return_value=False)
    def test_log_in_failure(self, mock_confirm, mock_print, mock_prompt, mock_load_users):
        mock_load_users.return_value = {
            'new_user': {
                'username': 'new_user',
                'password': bcrypt.hashpw('Password123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                'first_name': 'Test',
                'last_name': 'User'
            }
        }
        username = log_in()
        self.assertIsNone(username)
        mock_print.assert_any_call("[red]Invalid username or password.[/red]")


if __name__ == '__main__':
    unittest.main()
