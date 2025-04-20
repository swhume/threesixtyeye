import subprocess
from pathlib import Path
import sys
import click

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

def github2dsj(input_value):
    """
    Creates and configures the command to execute the `github2dsj` script
    :param input_value: Command-line inputs into the script
    :return: The command (as a list) to run the "github2dsj.py" script
    """
    data_dir = Path(__file__).parent.joinpath("data")
    command = Path(__file__).parent.joinpath("github2dsj").joinpath("github2dsj.py")
    cmd = [__config.python_command, str(command), "ie.json", "--path", str(data_dir)]
    return cmd

def dsjupversion(input_value):
    """
    Creates and configures the command to execute the `dsjupversion` script
    :param input_value: Command-line inputs into the script
    :return: The command (as a list) to run the `dsjupversion.py` script
    """
    command = Path(__file__).parent.joinpath("dsjupversion").joinpath("dsjupversion.py")
    cmd = [__config.python_command, str(command), "-f" + input_value.strip()]
    return cmd

def dsjvalidate(input_value):
    """
    Creates and configures the command to execute the `dsjvalidate` script
    :param input_value: Command-line inputs into the script
    :return: The command (as a list) to run the `dsjvalidate.py` script
    """
    command = Path(__file__).parent.joinpath("dsjvalidate").joinpath("dsjvalidate.py")
    cmd = [__config.python_command, str(command), "-f" + input_value]
    return cmd

def dsj2api(input_value):
    """
    Creates and configures the command to execute the `dsj2api` script
    :param input_value: Command-line inputs into the script
    :return: The command (as a list) to run the `dsj2api.py` script
    """
    command = Path(__file__).parent.joinpath("dsj2api").joinpath("dsj2api.py")
    cmd = [__config.python_command, str(command), "-f" + input_value, "-u" + __config.base_url,
           "-k" + __config.api_key]
    return cmd

def cdisc_pipeline(command, verbose=False):
    """
    Executes a command line process using the specified command and captures its output.
    Provides an alternative to running these scripts on the command line directly.

    :param command: The command to execute and its arguments as a list of strings
    :param verbose: Enable verbose logging of the script while running
    """
    try:
        returned_value = subprocess.run(command, check=True, timeout=60, capture_output=True)
        if verbose:
            print(f"\nCommand {command} completed successfully with return value\n{returned_value.stdout.decode('utf-8')}.")
        return returned_value.stdout.decode('utf-8').strip()
    except FileNotFoundError as exc:
        print(
            f"Command {command} failed because the process "
            f"could not be found.\n{exc}"
        )
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(
            f"Command {command} failed because the process "
            f"did not return a successful return code.\n{exc.stderr.decode('utf-8')}"
        )
        sys.exit(1)
    except subprocess.TimeoutExpired as exc:
        print(f"Command {command} timed out.\n {exc}")
        sys.exit(1)

@click.command(help="Run a CDISC 360i pipeline using subprocess")
@click.version_option("0.0.1", prog_name="360i")
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Puts the program into verbose mode to display additional messages",
)

def cli(verbose):
    """
    Runs a 360i pipeline by invoking a series of subprocess commands in sequence.
    :param verbose: Boolean flag. Enables verbose mode to display additional messages
    """
    return_value = ""
    command_funcs = [github2dsj, dsjupversion, dsjvalidate, dsj2api]
    for command in command_funcs:
        if verbose:
            print(f"Running command with input: {return_value}")

        return_value = cdisc_pipeline(command(return_value), verbose)

        if verbose:
            print(f"Command returned value: {return_value}")


if __name__ == "__main__":
    cli()