import unittest
import subprocess
from unittest.mock import patch, MagicMock, call

from ansible_collections.noahchalifour.pvecm.plugins.module_utils import cluster_utils


class TestClusterUtils(unittest.TestCase):
    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.shell_utils.run_command"
    )
    def test_get_cluster_name_success(self, mock_run_command):
        """Test successful retrieval of cluster name"""
        # Mock the output of pvecm status command
        mock_run_command.return_value = (
            "Cluster information\n"
            "-------------------\n"
            "Name: test-cluster\n"
            "Config Version: 3\n"
            "Transport: knet\n"
            "Secure auth: on\n",
            "",
        )

        # Create a mock module
        mock_module = MagicMock()

        # Call the function
        result = cluster_utils.get_cluster_name(mock_module)

        # Verify the result
        self.assertEqual(result, "test-cluster")

        # Verify run_command was called with correct arguments
        mock_run_command.assert_called_once_with(mock_module, "pvecm status")

    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.shell_utils.run_command"
    )
    def test_get_cluster_name_no_name(self, mock_run_command):
        """Test when cluster name is not found in the output"""
        # Mock output without a Name field
        mock_run_command.return_value = (
            "Cluster information\n"
            "-------------------\n"
            "Config Version: 3\n"
            "Transport: knet\n"
            "Secure auth: on\n",
            "",
        )

        # Create a mock module
        mock_module = MagicMock()

        # Call the function
        result = cluster_utils.get_cluster_name(mock_module)

        # Verify the result is None when no name is found
        self.assertIsNone(result)

    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.shell_utils.run_command"
    )
    def test_get_cluster_name_empty_output(self, mock_run_command):
        """Test with empty command output"""
        # Mock empty output
        mock_run_command.return_value = ("", "")

        # Create a mock module
        mock_module = MagicMock()

        # Call the function
        result = cluster_utils.get_cluster_name(mock_module)

        # Verify the result is None for empty output
        self.assertIsNone(result)

    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.shell_utils.run_command"
    )
    def test_create_cluster_success(self, mock_run_command):
        """Test create_cluster function with successful execution"""
        module = MagicMock()

        # Mock run_command to return success
        mock_run_command.return_value = ("Cluster created successfully", "")

        # Call create_cluster
        cluster_utils.create_cluster(module, "test-cluster")

        # Verify run_command was called with correct arguments
        mock_run_command.assert_called_once_with(module, "pvecm create test-cluster")

        # Verify exit_json was called with correct arguments
        module.exit_json.assert_called_once_with(
            changed=True,
            msg="Cluster created successfully.",
            stdout="Cluster created successfully",
        )

    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.shell_utils.subprocess.run"
    )
    def test_create_cluster_failure(self, mock_run_command):
        """Test create_cluster function with command failure"""
        # Mock the module
        module = MagicMock()
        module.fail_json.side_effect = SystemExit(1)

        # Mock run_command to return error
        mock_run_command.side_effect = subprocess.CalledProcessError(
            1, "", "", "Failed to create cluster"
        )

        # Call create_cluster
        with self.assertRaises(SystemExit):
            cluster_utils.create_cluster(module, "test-cluster")

        # Verify fail_json was called with correct arguments
        module.fail_json.assert_called_once_with(
            msg="Command failed: Failed to create cluster"
        )

    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.shell_utils.run_command"
    )
    def test_join_cluster_success(self, mock_run_command):
        """Test join_cluster function with successful execution"""
        # Mock run_command to return success
        mock_run_command.return_value = ("Node joined cluster successfully", "")

        # Create module mock
        module = MagicMock()
        module.params = {"hostname": "192.168.1.100"}

        # Call join_cluster
        cluster_utils.join_cluster(module, "192.168.1.100")

        # Verify run_command was called with correct arguments
        mock_run_command.assert_has_calls(
            [
                call(module, "ssh-keyscan -H 192.168.1.100 >> ~/.ssh/known_hosts"),
                call(module, "pvecm add 192.168.1.100 --use_ssh"),
            ]
        )

        # Verify exit_json was called with correct arguments
        module.exit_json.assert_called_once_with(
            changed=True,
            msg="Node joined cluster successfully.",
            stdout="Node joined cluster successfully",
        )

    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.shell_utils.subprocess.run"
    )
    def test_join_cluster_failure(self, mock_run_command):
        """Test join_cluster function with command failure"""
        # Mock run_command to return error
        mock_run_command.side_effect = subprocess.CalledProcessError(
            1, "", "", "Failed to join cluster"
        )

        # Create module mock
        module = MagicMock()
        module.params = {"hostname": "192.168.1.100"}
        module.fail_json.side_effect = SystemExit(1)

        # Call join_cluster
        with self.assertRaises(SystemExit):
            cluster_utils.join_cluster(module, "192.168.1.100")

        # Verify fail_json was called with correct arguments
        module.fail_json.assert_called_once_with(
            msg="Command failed: Failed to join cluster"
        )
