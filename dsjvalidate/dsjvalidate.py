#!/usr/bin/env python3
"""
Validates a Dataset-JSON v1.1 NDJSON dataset. Uses LinkML model in dataset-ndjson.yaml to validate.
Requires the dataset file name and path as an input.
"""
from linkml.validator import validate
import ndjson
from pathlib import Path
import click
import sys

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

@click.command(help="Validate a DSJ v1.1 NDJSON dataset")
@click.version_option("0.0.1", prog_name="dsjvalidate")
@click.option(
    "-f",
    "--file",
    help="Path with filename to the dataset file to be validated."
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Puts the program into verbose mode to display additional messages",
)

def cli(file: str, verbose: bool) -> None:
    """
    Validates a Dataset-JSON v1.1 NDJSON dataset
    :param file: Path to the dataset file to be validated.
    :return: Outputs the absolute path of the updated dataset file to
        standard output after conversion.
    """
    if not file:
        file = get_file_from_stdin(verbose)

    file = Path(file)
    validate_dataset(file, verbose)
    # sends the full path and filename to standard out to support chaining
    sys.stdout.write(str(file.resolve()))
    sys.stdout.flush()


def get_file_from_stdin(verbose: bool) -> str:
    """
    Reads a single line of input from the stdin and returns it as a string
    :return: the filename and path as a string
    """
    file = ""
    try:
        for line in sys.stdin:
            file = line.strip()
    except BrokenPipeError:
        click.echo("Error: Input pipe closed unexpectedly.", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)
    if file and verbose:
        click.echo(f"Starting validation of {file}...", err=False)
    return file


def validate_dataset(dataset_filename, verbose, batch_size=100) -> None:
    """
    Runs the Dataset-JSON v1.1 NDJSON validation.
    :param dataset_filename: path and filename of the dataset to be validated.
    :param verbose: boolean verbose mode flag
    :param batch_size: how many dataset rows to validate at a time
    """
    with open(dataset_filename, mode='r', encoding='utf-8') as f:
        invalid_lines = []
        reader = ndjson.reader(f)
        batch = []
        for line_num, json_line in enumerate(reader, 1):
            if line_num == 1:
                # validate the first line, the metadata line, separately
                report = validate(json_line,
                                  schema=str(__config.ndjson_linkml),
                                  target_class="DatasetMetadata")
                if report.results:
                    invalid_lines.append(line_num)
                    for result in report.results:
                        print(result.message)
            else:
                # collect rows into a batch
                batch.append(json_line)
                if len(batch) >= batch_size:
                    invalid_lines.extend(validate_batch(batch, line_num - batch_size + 1))
                    batch = []
        if batch:
            invalid_lines.extend(validate_batch(batch, line_num - batch_size + 1))

        if not invalid_lines and verbose:
            click.echo(f"The DSJ NDJSON file {dataset_filename} is valid!", err=False)
        elif invalid_lines:
            sys.stderr.write(f"The following DSJ NDJSON lines from file {dataset_filename} are invalid {invalid_lines}")


def validate_batch(batch, start_line_num):
    """
    Validates a batch of Dataset-JSON records against the LinkML model and returns a list of invalid
    line numbers.
    :param batch: The batch of Dataset-JSON records to be validated
    :param start_line_num: The starting line number of the batch in the source dataset
    :return: list of integers with the line numbers of invalid rows starting from the start_line_num
    """
    invalid_lines = []
    data_row = {"rows": batch}  # LinkML expects a list in 'rows'
    # yaml_model_file = Path(__file__).parent.joinpath("dataset-ndjson.yaml")
    report = validate(data_row, schema=str(__config.ndjson_linkml), target_class="RowData")
    if report.results:
        for result in report.results:
            print(result.message)
        invalid_lines.extend(range(start_line_num, start_line_num + len(batch)))
    return invalid_lines


if __name__ == '__main__':
    cli()
