# Proxmox Cluster Node

This role configures a Proxmox VE node to join an existing cluster. It handles the necessary steps to add a node to a Proxmox cluster that has already been initialized with a leader node.

## Requirements

- Proxmox VE 7.x or higher installed on the target node
- Network connectivity between the node and the cluster leader
- SSH access to the Proxmox node with sudo/root privileges
- The cluster leader must be already set up and running

## Role Variables

| Variable | Description | Required | Default |
|----------|-------------|:--------:|:-------:|
| `cluster_name` | Name of the Proxmox cluster to join | yes | - |
| `leader_hostname` | Hostname or IP address of the cluster leader node | yes | - |

## Dependencies

None. This role is designed to work independently, but it assumes that a cluster leader has already been set up.

## Example Playbook

```yaml
- hosts: proxmox_nodes
  become: true
  roles:
    - role: noahchalifour.pvecm.node
      vars:
        cluster_name: "pve-cluster"
        leader_hostname: "pve-leader.example.com"
```

## Notes

- This role only handles joining nodes to an existing cluster. It does not set up the initial cluster leader.
- The target node will be rebooted if necessary to complete the cluster join operation.
- Ensure that hostnames can be resolved between all nodes in the cluster.
- Make sure the Proxmox cluster network is properly configured before adding nodes.

## License

MIT

## Author Information

Noah Chalifour
