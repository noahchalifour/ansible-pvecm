import subprocess


def run_command(module, command, fail_on_error: bool = True):
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
        if fail_on_error:
            module.fail_json(msg="Command failed: {0}".format(err.stderr))
    return "", None
