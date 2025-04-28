from ansible_collections.noahchalifour.pvecm.plugins.module_utils import shell_utils


def get_cluster_name(module):
    # Run `pvecm status` to retrieve the cluster name
    command = "pvecm status"
    stdout, stderr = shell_utils.run_command(module, command, fail_on_error=False)

    # Extract the cluster name from the output
    for line in stdout.splitlines():
        if "Name:" in line:
            return line.split(":")[1].strip()  # Extract the cluster name

    return None


def create_cluster(module, cluster_name):
    command = f"pvecm create {cluster_name}"
    stdout, _ = shell_utils.run_command(module, command)
    module.exit_json(changed=True, msg="Cluster created successfully.", stdout=stdout)


def join_cluster(module, hostname):
    join_command = f"pvecm add {hostname} --use_ssh"
    stdout, _ = shell_utils.run_command(module, join_command)
    module.exit_json(
        changed=True, msg="Node joined cluster successfully.", stdout=stdout
    )
