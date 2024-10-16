#!/usr/bin/python
# -*- coding: utf-8 -*-


from ansible.module_utils.basic import AnsibleModule
import socket
import subprocess


DOCUMENTATION = '''
---
module: create_or_join
short_description: Manage Proxmox cluster creation and node joining
description:
    - This module checks if a Proxmox cluster is already configured and either creates a new one or joins an existing one.
options:
    name:
        description:
            - The name of the Proxmox cluster.
        required: true
        type: str
    leader_hostname:
        description:
            - The hostname of the leader node to join the cluster.
        required: true
        type: str
    use_ssh:
        description:
            - Whether to use SSH when joining the cluster.
        required: false
        type: bool
        default: false
author:
    - Noah Chalifour (@noahchalifour)
'''


def run_command(module, command):
    try:
        result = subprocess.run(command, 
                                shell=True, 
                                check=True,
                                text=True,
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
        return result.stdout, None
    except subprocess.CalledProcessError as err:
        module.fail_json(msg="Command failed: {0}".format(err.stderr))


def add_arguments(cmd, args: dict):
    updated_cmd = cmd

    for k, v in args.items():
        # Handle booleans
        if isinstance(v, bool):
            if not v:
                continue
            updated_cmd += f' {k}'

        # Rest of arguments
        updated_cmd += f' {k} {v}'

    return updated_cmd


def get_cluster_name(module):
    # Run `pvecm status` to retrieve the cluster name
    command = "pvecm status"
    stdout, _ = run_command(module, command)
    
    # Extract the cluster name from the output
    for line in stdout.splitlines():
        if "Name:" in line:
            return line.split(":")[1].strip()  # Extract the cluster name
    return None


def create_cluster(module, cluster_name):
    command = f"pvecm create {cluster_name}"
    stdout, _ = run_command(module, command)
    module.exit_json(changed=True, msg="Cluster created successfully.", stdout=stdout)


def join_cluster(module, hostname, options: dict):
    use_ssh = options.get('--use_ssh')

    if use_ssh:
        ssh_keyscan_command = f"ssh-keyscan -H {hostname} >> ~/.ssh/known_hosts"
        run_command(module, ssh_keyscan_command)

    join_command = f"pvecm add {hostname}"
    join_command = add_arguments(join_command, options)

    stdout, _ = run_command(module, join_command)
    module.exit_json(changed=True, msg="Node joined the cluster successfully.", stdout=stdout)


def main():
    module_args = dict(
        name=dict(type='str', required=True),
        leader_hostname=dict(type='str', required=True),
        use_ssh=dict(type='bool', required=False, default=False)
    )
    
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    cluster_name = module.params['name']
    leader_hostname = module.params.get('leader_hostname')
    use_ssh = module.params.get('use_ssh')

    # Check if already part of the cluster
    if cluster_name == get_cluster_name(module):
        module.exit_json(changed=False, msg="Node already associated with cluster.")

    # Create cluster if hostname equals leader_hostname
    if leader_hostname == socket.gethostname():
        create_cluster(module, cluster_name)
    else:
        # Otherwise join cluster
        join_cluster(module, leader_hostname, {
            '--use_ssh': use_ssh,
        })


if __name__ == '__main__':
    main()
