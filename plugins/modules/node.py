from ansible.module_utils import shell_utils
from ansible.module_utils import cluster_utils


DOCUMENTATION = """
---
module: node
short_description: Manage a Proxmox cluster node
description:
    - This module is used to manage nodes in a Proxmox cluster
options:
    leader:
        description:
            - The hostname of the cluster leader.
        required: true
        type: str
    cluster:
        description:
            - The name of the Proxmox cluster.
        required: true
        type: str
author:
    - Noah Chalifour (@noahchalifour)
"""


def join_cluster(module, hostname):
    ssh_keyscan_command = f"ssh-keyscan -H {hostname} >> ~/.ssh/known_hosts"
    shell_utils.run_command(module, ssh_keyscan_command)

    join_command = f"pvecm add {hostname}"
    stdout, _ = shell_utils.run_command(module, join_command)

    module.exit_json(
        changed=True, msg="Node joined the cluster successfully.", stdout=stdout
    )


def main():
    module_args = dict(
        leader=dict(type="str", required=True), cluster=dict(type="str", required=True)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    cluster_name = module.params["cluster"]
    leader_hostname = module.params["leader"]

    # Check if already part of the cluster
    if cluster_name == cluster_utils.get_cluster_name(module):
        module.exit_json(changed=False, msg="Node already associated with cluster.")

    # Join the cluster
    join_cluster(module, leader_hostname)


if __name__ == "__main__":
    main()
