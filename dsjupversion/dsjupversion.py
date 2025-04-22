#!/usr/bin/env python3
"""
dsjupversion.py for 360i converts a Dataset-JSON v1.0 raw dataset to Dataset-JSON NDJSON v1.1.

Example usage:
python3 dsjupversion.py -f /path/to/dataset.json
"""
from pathlib import Path
import sys
import shutil
import click

from ndjsonlib.json_data_file import JsonDataFile
import ndjsonlib.metadata_file as MF
import ndjsonlib.data_file as DF
import ndjsonlib.dataset_name as DN
from dsjversionone import DsjVersionOne
import dataset as DS

@click.command(help="Convert a DSJ v1.0 dataset to v1.1 in NDJSON")
@click.version_option("0.0.1", prog_name="dsjupversion")
@click.option("-f", "--file")

def cli(file: str):
    """
    Convert a DSJ v1.0 dataset to v1.1 NDJSON. It backs up the original dataset file before processing,
    then loads, processes, and updates the file to the desired version. The updated file path is written to
    standard output upon successful conversion.
    :param file: Path to the dataset file to be converted.
    :return: Writes the absolute path of the updated dataset file to standard output after conversion.
    """
    if not file:
        file = get_file_from_stdin()
    file = Path(file)
    copy_original_file(file)
    dsj10 = load_original_dataset(file)
    upversioned_filename = upversion_dataset(dsj10, file)
    sys.stdout.write(upversioned_filename)
    sys.stdout.flush()

def get_file_from_stdin() -> str:
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
    return file

def upversion_dataset(dsj10, file):
    """
    Updates the original v1.0 dataset by loading its metadata and data content,
    saving that content as data and metadata NDJSON files, and then writing them
    out as one complete Dataset-JSON v1.1 NDJSON dataset file.
    :param dsj10: The Dataset-JSON v1.0 object containing the data to be updated.
    :param file: The full path or filename of the dataset.
    """
    dsn = DN.DatasetName(full_name=str(file))
    load_dsj_metadata(dsj10, dsn)
    load_dsj_data(dsj10, dsn)
    dn = DN.DatasetName(full_name=str(file))
    jdf = JsonDataFile(ds_name=dn.get_ds_name(), directory=dn.get_path(), chunk_size=1000)
    jdf.write_full_dataset_from_files()
    return dn.get_full_dataset_filename()

def load_dsj_data(dsj10, dsn):
    """
    Loads data from the original dataset and writes it into an NDJSON data file.
    :param dsj10: A data source object that loads and provides access to the original dataset
    :param dsn: An object that provides the filenames for the data file, metadata file, and full dataset
    """
    dsj_dataset = []
    for row in dsj10.get_data_rows():
        dsj_dataset.append(row)
    df = DF.DataFile(filename=dsn.get_data_filename() , chunk_size=1000,
                     row_data=DS.RowData(rows=dsj_dataset))
    df.write_file()

def load_dsj_metadata(dsj10, dsn):
    """
    Loads the metadata from the original dataset, processes the metadata, and writes it to an
    NDJSON metadata dataset file.
    :param dsj10: An object containing the original dataset metadata and data.
    :param dsn: An object containing the data, metadata, and full dataset filenames
    """
    dsj_metadata = DS.DatasetMetadata(
        datasetJSONCreationDateTime=dsj10.get_creation_date_time(),
        datasetJSONVersion="1.1.0",
        fileOID=dsj10.get_file_oid(),
        dbLastModifiedDateTime=None,
        originator="360i",
        sourceSystem=None,
        studyOID=dsj10.get_study_oid(),
        metaDataVersionOID=dsj10.get_mdv_oid(),
        metaDataRef=None,
        itemGroupOID=dsj10.get_dataset_oid(),
        records=dsj10.get_records(),
        name=dsj10.get_dataset_name(),
        label=dsj10.get_dataset_label(),
        columns=get_column_metadata(dsj10)
    )
    mf = MF.MetadataFile(dsn.get_metadata_filename(), dataset_metadata=dsj_metadata)
    mf.write_file()

def get_column_metadata(dsj10):
    """
    Loads the metadata for each column in the original dataset
    :param dsj10: An object that loads and provides access to the original dataset metadata and data
    :return: A list of DS.Column objects providing detailed column metadata
    :rtype: list[DS.Column]
    """
    column_metadata = []
    for column in dsj10.get_variable_metadata():
        dsj_column = DS.Column(
            itemOID=column["OID"],
            name=column["name"],
            label=column["label"],
            dataType=column["type"],
            targetDataType=None,
            length=column.get("length", None),
            displayFormat=column.get("displayFormat", None),
            keySequence=column.get("keySequence", None),
        )
        column_metadata.append(dsj_column)
    return column_metadata

def load_original_dataset(file):
    """
    Loads the original dataset into a DSJ v1.0 object
    :param file: Input file and path used to load the object
    :return: An instance of `DsjVersionOne` with the original dataset loaded
    :rtype: DsjVersionOne
    """
    dsj10 = DsjVersionOne(data_file=file, dataset_name=file.stem)
    return dsj10

def copy_original_file(file):
    """
    Copies the original file and appends a version suffix to its name
    to create a backup.
    :param file: The original file to be copied. It must be a `Path` object
    """
    backup_file = file.parent.joinpath(file.stem + "_1_0" + file.suffix)
    try:
        shutil.copy(str(file), str(backup_file))
    except PermissionError as pe:
        print(f"Write permission denied for backup file {backup_file}.")
    except Exception as ex:
        print(f"Error backing up original dataset: {ex} \n")


if __name__ == "__main__":
    cli()
