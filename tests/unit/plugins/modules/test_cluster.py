#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock


mock_module = MagicMock()
mock_module.exit_json.side_effect = SystemExit(0)
mock_module.params = {"name": "test-cluster"}


with patch("ansible.module_utils.basic.AnsibleModule", return_value=mock_module):
    from ansible_collections.noahchalifour.pvecm.plugins.modules import cluster


class TestClusterModule:
    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.get_cluster_name"
    )
    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.create_cluster"
    )
    def test_main_create_cluster(self, mock_create_cluster, mock_get_cluster_name):
        """Test main function when cluster needs to be created"""
        # Mock get_cluster_name to return None (not in a cluster)
        mock_get_cluster_name.return_value = None

        # Call main function
        with pytest.raises(SystemExit):
            cluster.main()

        # Verify create_cluster was called with correct arguments
        mock_create_cluster.assert_called_once_with(mock_module, "test-cluster")
        mock_get_cluster_name.assert_called_once_with(mock_module)
        mock_module.exit_json.assert_called_once_with(
            changed=True, msg="Created new cluster"
        )

    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.get_cluster_name"
    )
    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.create_cluster"
    )
    def test_main_already_in_cluster(self, mock_create_cluster, mock_get_cluster_name):
        """Test main function when already in the requested cluster"""
        # Mock get_cluster_name to return the same cluster name
        mock_get_cluster_name.return_value = "test-cluster"

        with patch(
            "ansible.module_utils.basic.AnsibleModule", return_value=mock_module
        ):
            # Call main function
            with pytest.raises(SystemExit):
                cluster.main()

            # Verify exit_json was called with correct arguments
            mock_module.exit_json.assert_called_once_with(
                changed=False, msg="Node already associated with cluster."
            )

            # Verify create_cluster was not called
            mock_create_cluster.assert_not_called()

    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.get_cluster_name"
    )
    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.create_cluster"
    )
    def test_main_different_cluster(self, mock_create_cluster, mock_get_cluster_name):
        """Test main function when already in a different cluster"""
        # Mock get_cluster_name to return a different cluster name
        mock_get_cluster_name.return_value = "other-cluster"

        with patch(
            "ansible.module_utils.basic.AnsibleModule", return_value=mock_module
        ):
            # Call main function
            with pytest.raises(SystemExit):
                cluster.main()

        # Verify create_cluster was called with correct arguments
        mock_create_cluster.assert_called_once_with(mock_module, "test-cluster")
