from ansible.module_utils import shell_utils


def get_cluster_name(module):
    # Run `pvecm status` to retrieve the cluster name
    command = "pvecm status"
    stdout, _ = shell_utils.run_command(module, command)

    # Extract the cluster name from the output
    for line in stdout.splitlines():
        if "Name:" in line:
            return line.split(":")[1].strip()  # Extract the cluster name
    return None
