#!/usr/bin/env python3

import requests
import json
import sys
import os
from pathlib import Path
import click
from graphviz.backend.viewing import view_windows

import dataset as DS

from ndjsonlib.dataset_name import DatasetName
from ndjsonlib.ndjson_data_file import NdjsonDataFile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

@click.command(help="Posts Dataset-JSON NDJSON dataset to the Dataset-JSON API")
@click.version_option("0.0.1", prog_name="dsj2api")
@click.option(
    "-f",
    "--file"
)
@click.option(
    "-s",
    "--study",
    default=__config.study_oid,
    help="The Study OID for the datasets"
)
@click.option(
"-u",
    "--url",
    default=__config.base_url,
    help="DSJ API base URL"
)
@click.option(
    "-k",
    "--apikey",
    default=__config.api_key,
    help="DSJ API key needed to post or modify a dataset via the API."
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Puts the program into verbose mode to display additional messages",
)


def cli(file: str, study: str, url: str, apikey: str, verbose: bool = False):
    if verbose:
        click.echo(f"Study OID is {study} and API Key is {apikey}")
    if not file:
        file = get_file_from_stdin()

    file = Path(file)
    dataset_metadata = load_dataset_metadata(file)
    if verbose:
        click.echo(f"Dataset Metadata is {dataset_metadata}")
    create_study(dataset_metadata, study, url, apikey, verbose)
    load_dataset(dataset_metadata, file, study, url, apikey, verbose)
    sys.stdout.write(str(file.resolve()))
    sys.stdout.flush()
    sys.stdout = None

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


def load_dataset_metadata(file):
    with open(file, mode='r', encoding='utf-8') as f:
        metadata_line = f.readline()
    dataset_metadata = DS.DatasetMetadata(**json.loads(metadata_line))
    return dataset_metadata

def load_dataset(dataset_metadata, file, study_oid, base_url, api_key, verbose: bool = False):
    dsn = DatasetName(directory=file.parent, dataset_name=dataset_metadata.name)
    jf = NdjsonDataFile(ds_name=dsn.get_ds_name(), directory=dsn.get_path(), chunk_size=1000)
    jf.read_dataset()
    dataset = ndjson2json(jf)
    ds = requests.post(url=f"{base_url}studies/{study_oid}/datasets",
                       headers={"Content-Type": "application/json", "api-key": api_key},
                       data=json.dumps(dataset))
    if ds.status_code != requests.codes.created:
        if ds.status_code == requests.codes.conflict:
            if verbose:
                click.echo(f"Dataset {dataset_metadata.name} exists for Study OID {study_oid}. "
                           f"Skipping creation of dataset resource.")
            update_dataset(dataset_metadata, dataset, study_oid, dataset_metadata.itemGroupOID, base_url,
                           api_key, verbose)
        else:
            if verbose:
                click.echo(f"ERROR: unable to post dataset resource to API ({ds.status_code})", err=True)
            ds.raise_for_status()

def update_dataset(dataset_metadata, dataset, study_oid, item_group_oid, base_url, api_key, verbose: bool = False):
    ds = requests.put(url=f"{base_url}studies/{study_oid}/datasets/{item_group_oid}",
                             headers={"Content-Type": "application/json", "api-key": api_key},
                             data=json.dumps(dataset))
    if ds.status_code != requests.codes.ok:
        if verbose:
            click.echo(f"ERROR: unable to update dataset using API ({ds.status_code})", err=True)
        ds.raise_for_status()
    else:
        if verbose:
            click.echo(f"Updated dataset {dataset_metadata.name} for Study OID {study_oid}.")


def ndjson2json(jf):
    dataset = jf.metadata
    dataset["rows"] = jf.rows
    return dataset


def create_study(dataset_metadata: DS.DatasetMetadata, study: str, base_url: str, apikey: str, verbose: bool = False):
    if does_study_exist(study, base_url, apikey, verbose):
        if verbose:
            click.echo(f"Study exists for Study OID {study}. Skipping creation of study resource.")
        return

    study_resource = {
        "studyOID": dataset_metadata.studyOID,
        "name": dataset_metadata.name,
        "label": dataset_metadata.label,
        "standards": ["sdtmig"],
        "href": f"{base_url}studies/{study}"
    }
    study = requests.post(url=f"{base_url}studies", headers={"Content-Type": "application/json", "api-key": apikey},
                          data=json.dumps(study_resource))
    if study.status_code != requests.codes.created:
        if study.status_code == requests.codes.conflict:
            if verbose:
                click.echo(f"Study already exists for Study OID {study}. Skipping study creation.")
        else:
            if verbose:
                click.echo(f"ERROR: unable to post study resource to API. Status code = {study.status_code}", err=True)
            study.raise_for_status()

def does_study_exist(study_oid: str, base_url: str, apikey: str, verbose: bool = False) -> bool:
    study_url = f"{base_url}studies/{study_oid}"
    study = requests.get(f"{base_url}studies/{study_oid}", headers={"api-key": apikey})
    if study.status_code == requests.codes.ok:
        if verbose:
            click.echo(f"Study exists for Study OID {study_oid}. Skipping creation of study resource.")
        return True
    else:
        if verbose:
            click.echo(f"Study not found for Study OID {study_oid} with status code {study.status_code} and url {study_url}.")
        return False


if __name__ == "__main__":
    cli()

