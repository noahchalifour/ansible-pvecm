import subprocess
import unittest
from unittest import mock

from ansible.module_utils.basic import AnsibleModule

from plugins.module_utils.shell_utils import run_command


class TestShellUtils(unittest.TestCase):
    """Test cases for shell_utils module"""

    def setUp(self):
        """Set up test fixtures"""
        self.module = mock.MagicMock(spec=AnsibleModule)

    @mock.patch("subprocess.run")
    def test_run_command_success(self, mock_run):
        """Test run_command with successful execution"""
        # Setup mock
        mock_process = mock.MagicMock()
        mock_process.stdout = "command output"
        mock_run.return_value = mock_process

        # Call function
        stdout, stderr = run_command(self.module, "test command")

        # Assertions
        mock_run.assert_called_once_with(
            "test command",
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(stdout, "command output")
        self.assertIsNone(stderr)
        self.module.fail_json.assert_not_called()

    @mock.patch("subprocess.run")
    def test_run_command_failure(self, mock_run):
        """Test run_command with failed execution"""
        # Setup mock to raise CalledProcessError
        error = subprocess.CalledProcessError(1, "test command")
        error.stderr = "error message"
        mock_run.side_effect = error

        # Call function
        stdout, stderr = run_command(self.module, "test command")

        # Assertions
        mock_run.assert_called_once_with(
            "test command",
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.module.fail_json.assert_called_once_with(
            msg="Command failed: error message"
        )
        self.assertEqual(stdout, "")
        self.assertIsNone(stderr)

    @mock.patch("subprocess.run")
    def test_run_command_with_empty_command(self, mock_run):
        """Test run_command with empty command"""
        # Setup mock
        mock_process = mock.MagicMock()
        mock_process.stdout = ""
        mock_run.return_value = mock_process

        # Call function
        stdout, stderr = run_command(self.module, "")

        # Assertions
        mock_run.assert_called_once_with(
            "",
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(stdout, "")
        self.assertIsNone(stderr)
        self.module.fail_json.assert_not_called()
