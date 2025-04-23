# Plugins for noahchalifour.pvecm Collection

This directory contains plugins that extend the functionality of the noahchalifour.pvecm collection for managing Proxmox VE clusters.

## Plugin Types

The collection may include the following types of plugins:

### Modules

Custom modules for interacting with Proxmox VE's cluster management functionality:

- `pvecm_*`: Modules for managing Proxmox cluster configurations

### Module Utils

Shared utility code used by the collection's modules:

- Common functions for interacting with the Proxmox API
- Helper utilities for parsing and validating Proxmox cluster configurations

### Action Plugins

Action plugins that may provide additional functionality when executing modules.

## Usage

Plugins in this collection are automatically available when you install the collection:

```bash
ansible-galaxy collection install noahchalifour.pvecm
```

You can then use the modules in your playbooks:

```yaml
- name: Example using a pvecm module
  noahchalifour.pvecm.module_name:
    param1: value1
    param2: value2
```

## Development

When adding new plugins:

1. Place them in the appropriate subdirectory based on plugin type
2. Include proper documentation using Ansible's documentation format
3. Add tests to verify plugin functionality

For more information on Ansible plugins, see the [Ansible Plugin Documentation](https://docs.ansible.com/ansible-core/latest/plugins/plugins.html).
