#!/usr/bin/python
# -*- coding: utf-8 -*-


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import shell_utils
from ansible.module_utils import cluster_utils


DOCUMENTATION = """
---
module: cluster
short_description: Manage a Proxmox cluster
description:
    - This module is used to create/delete Proxmox clusters using the pvecm tool.
options:
    name:
        description:
            - The name of the Proxmox cluster.
        required: true
        type: str
author:
    - Noah Chalifour (@noahchalifour)
"""


def create_cluster(module, cluster_name):
    command = f"pvecm create {cluster_name}"
    stdout, _ = shell_utils.run_command(module, command)
    module.exit_json(changed=True, msg="Cluster created successfully.", stdout=stdout)


def main():
    module_args = dict(name=dict(type="str", required=True))

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    cluster_name = module.params["name"]

    # Check if already part of the cluster
    if cluster_name == cluster_utils.get_cluster_name(module):
        module.exit_json(changed=False, msg="Node already associated with cluster.")

    # Create cluster
    create_cluster(module, cluster_name)


if __name__ == "__main__":
    main()
