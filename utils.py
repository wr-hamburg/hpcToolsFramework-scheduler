import subprocess

def run_command(command: str):
    """Runs a command.

    Args:
        command (str): Command to run.

    Returns:
        _type_: Result of the query if existing.
    """
    result = subprocess.check_output(command, shell=True)
    result = result[:-1].decode('ascii')
    return result


def parse_Popen(popen_output): ##todo in util 
    popen_output = popen_output.split("\"")
    popen_output = list(filter(("\n").__ne__, popen_output))
    popen_output = list(filter(("").__ne__, popen_output))

    return popen_output
