# Ansible Collection - noahchalifour.pvecm

[![Ansible Galaxy](https://img.shields.io/badge/galaxy-noahchalifour.pvecm-blue.svg)](https://galaxy.ansible.com/noahchalifour/pvecm)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

An Ansible collection for managing Proxmox VE Cluster Manager (pvecm) configurations and operations.

## Overview

This collection provides roles and modules to help automate the deployment, configuration, and management of Proxmox VE clusters using Ansible. It simplifies common tasks such as cluster creation, node addition/removal, and configuration management.

## Requirements

- Ansible 2.9 or newer
- Proxmox VE 6.x or newer
- SSH access to Proxmox nodes with appropriate privileges

## Installation

```bash
ansible-galaxy collection install noahchalifour.pvecm
```

Or include in your `requirements.yml`:

```yaml
collections:
  - name: noahchalifour.pvecm
```

## Roles

### pvecm.cluster

Creates and configures a Proxmox VE cluster.

### pvecm.node

Adds or removes nodes from an existing Proxmox VE cluster.

## Usage Examples

### Creating a new cluster

```yaml
- hosts: proxmox_master
  collections:
    - noahchalifour.pvecm
  tasks:
    - name: Create the new cluster
      noahchalifour.pvecm.node:
        name: cluster-name

- hosts: proxmox_nodes
  collections:
    - noahchalifour.pvecm
  tasks:
    - name: Join the cluster
      noahchalifour.pvecm.node:
        cluster: cluster-name
        leader: leader-hostname
```

### Adding a node to an existing cluster

```yaml
- hosts: new_proxmox_node
  collections:
    - noahchalifour.pvecm
  tasks:
    - name: Join an existing cluster
      noahchalifour.pvecm.node:
        cluster: cluster-name
        leader: leader-hostname
```

## Configuration Options

See the documentation for each role for detailed configuration options.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Noah Chalifour

