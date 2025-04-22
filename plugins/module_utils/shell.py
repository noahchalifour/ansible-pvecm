import subprocess


def run_command(module, command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout, None
    except subprocess.CalledProcessError as err:
        module.fail_json(msg="Command failed: {0}".format(err.stderr))
    return "", None
