from ansible.module_utils.basic import AnsibleModule
from ansible_collections.noahchalifour.pvecm.plugins.module_utils import shell_utils
from ansible_collections.noahchalifour.pvecm.plugins.module_utils import cluster_utils


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
    cluster_utils.join_cluster(module, leader_hostname)

    module.exit_json(changed=True, msg=f"Successfully joined cluster '{cluster_name}'")


if __name__ == "__main__":
    main()
