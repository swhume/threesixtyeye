import json
from pathlib import Path
import sys
import click
import ndjsonlib.models.dataset as DS

@click.command(help="Given a JSON Dataset-JSON shell dataset path and file, this program write NDJSON to stdout.")
@click.version_option("0.0.1", prog_name="shell2ndjson")
@click.argument(
    "shell_dataset_file",
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path
    ),
)

def cli(shell_dataset_file: Path):
    if shell_dataset_file.exists() and shell_dataset_file.is_file() and shell_dataset_file.suffix == ".json":
        dataset = read_dsj_dataset(shell_dataset_file)
        write_dataset(dataset)
    else:
        click.echo(f"JSON dataset shell file: {str(shell_dataset_file)} not found", err=True)
        raise SystemExit(1)


def write_dataset(dsj_metadata: dict) -> None:
    """
    Given a dataset shell represented as a dictionary, this function writes the dataset
    to stdout as NDJSON
    Parameters:
      dsj_metadata (dict): Dictionary containing the dataset and column metadata
    """
    dataset_metadata = DS.DatasetMetadata(**dsj_metadata)
    sys.stdout.write(f"{json.dumps(dataset_metadata.model_dump(mode='json', exclude_none=True))}\n")

def read_dsj_dataset(dsj_filename: Path) -> dict:
    """
    Reads a JSON shell dataset and return its content as a Python object
    Parameters:
      dsj_filename (str): The path to the JSON dataset file that needs to be read.
      verbose (bool): A flag to enable verbose output
    Returns:
      dataset shell as a dictionary
    """
    with open(str(dsj_filename)) as f:
        dataset = json.load(f)
    return dataset


if __name__ == "__main__":
    cli()
