#!/usr/bin/env python3
"""
github2dsj.py for 360i retrieves a raw dataset from GitHub and saves it to a file.
"""
import requests
from pathlib import Path
import base64
import json
import click
import sys

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

"""
github2dsj.py for 360i retrieves a raw dataset from GitHub and saves it to a file. It works with a the name of the 
dataset file to retrieve and a path to store the retrieved dataset. This program uses a config.ini file to maintain 
information about where and how to access the datasets in GitHub. To generalize this application, future versions 
may permit the config.ini content to be set via the command line or via environment variables.

Example Usage:
python github2dsj.py ie.json --path ./data
"""

@click.command(help="Retrieve a dataset from GitHub")
@click.version_option("0.1.0", prog_name="github2dsj")
@click.argument("file")
@click.option(
    "--path",
    default=Path.cwd(),
    type=click.Path(
        exists=True,
        file_okay=False,
        readable=True,
        path_type=Path,
    ),
    help="Path to store the retrieved dataset. Defaults to current directory."
)

def cli(file, path):
    """
    Retrieve a dataset from a specified GitHub repository and store it in a local directory.
    Writes the full path of the retrieved and stored file to standard output.
    :param file: Name of the dataset file to retrieve
    :param path: Local directory to store the retrieved dataset file
    """
    gh_path = __config.gh_repo_path_raw_data + file
    out_path = path.joinpath(file)
    github_get_file(__config.gh_user_name_raw_data, __config.gh_repo_name_raw_data, gh_path,
                    out_path, github_token=__config.gh_token_raw_data)
    sys.stdout.write(str(out_path.resolve()))
    sys.stdout.flush()

def github_get_file(username, repository_name, file_path, dataset_file_out, github_token=None):
    """
    Fetches a dataset from a specified GitHub repository and saves it to a local file.
    :param username: GitHub username of the repository owner.
    :param repository_name: Name of the GitHub repository.
    :param file_path: Path to the file within the repository.
    :param dataset_file_out: Path to the output file where the content will be saved.
    :param github_token: Optional authentication token for private repositories.
    :return: (dict) The decoded content of the file retrieved from the repository.
    """
    headers = {}
    if github_token:
        headers['Authorization'] = f"token {github_token}"
    url = f'https://api.github.com/repos/{username}/{repository_name}/contents/{file_path}'
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    file_data = r.json()
    if file_data['size'] > 1024 * 1024:
        # use GitHub blobs API for files larger than 1MB
        blob_url = f'https://api.github.com/repos/{username}/{repository_name}/git/blobs/{file_data["sha"]}'
        blob_response = requests.get(blob_url, headers=headers)
        blob_response.raise_for_status()
        blob_data = blob_response.json()
        file_content = base64.b64decode(blob_data["content"]).decode("utf-8")
    else:
        # use GitHub contents API for smaller files
        content_url = file_data['download_url']
        content_response = requests.get(content_url, headers=headers)
        content_response.raise_for_status()
        file_content = content_response.json()
    # save dataset to file
    with open(dataset_file_out, 'w') as f:
        json.dump(file_content, f, indent=2)
    return file_content


if __name__ == "__main__":
    cli()