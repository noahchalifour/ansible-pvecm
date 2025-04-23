#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from unittest.mock import patch, MagicMock


mock_module = MagicMock()
mock_module.params = {"cluster": "test-cluster", "leader": "leader-host"}
mock_module.exit_json.side_effect = SystemExit(0)


with patch("ansible.module_utils.basic.AnsibleModule", return_value=mock_module):
    from ansible_collections.noahchalifour.pvecm.plugins.modules import node


class TestNodeModule:
    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.get_cluster_name"
    )
    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.join_cluster"
    )
    def test_main_join_cluster(self, mock_join_cluster, mock_get_cluster_name):
        """Test main function when node needs to join a cluster"""
        # Mock get_cluster_name to return None (not in a cluster)
        mock_get_cluster_name.return_value = None

        # Call main function
        with pytest.raises(SystemExit):
            node.main()

        # Verify join_cluster was called with correct arguments
        mock_join_cluster.assert_called_once_with(mock_module, "leader-host")
        mock_get_cluster_name.assert_called_once_with(mock_module)
        mock_module.exit_json.assert_called_once_with(
            changed=True, msg="Successfully joined cluster 'test-cluster'"
        )

    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.get_cluster_name"
    )
    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.join_cluster"
    )
    def test_main_already_in_cluster(self, mock_join_cluster, mock_get_cluster_name):
        """Test main function when already in the requested cluster"""
        # Mock get_cluster_name to return the same cluster name
        mock_get_cluster_name.return_value = "test-cluster"

        # Call main function
        with pytest.raises(SystemExit):
            node.main()

        # Verify exit_json was called with correct arguments
        mock_module.exit_json.assert_called_once_with(
            changed=False, msg="Node already associated with cluster."
        )

        # Verify join_cluster was not called
        mock_join_cluster.assert_not_called()

    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.get_cluster_name"
    )
    @patch(
        "ansible_collections.noahchalifour.pvecm.plugins.module_utils.cluster_utils.join_cluster"
    )
    def test_main_different_cluster(self, mock_join_cluster, mock_get_cluster_name):
        """Test main function when already in a different cluster"""
        # Mock get_cluster_name to return a different cluster name
        mock_get_cluster_name.return_value = "other-cluster"

        # Call main function
        with pytest.raises(SystemExit):
            node.main()

        # Verify join_cluster was called with correct arguments
        mock_join_cluster.assert_called_once_with(mock_module, "leader-host")
        mock_module.exit_json.assert_called_once_with(
            changed=True, msg="Successfully joined cluster 'test-cluster'"
        )
