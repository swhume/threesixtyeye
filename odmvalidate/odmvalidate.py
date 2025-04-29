"""
odmvalidate.py

An alternative command-line option that can validate ODM
`xmllint --schema yourxsd.xsd yourxml.xml --noout`
"""

import click
import sys
from pathlib import Path
from odmlib import odm_parser as P
import xmlschema as XSD
import os

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

ODM_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'ie-odm.xml')
SCHEMA_FILE = os.path.join(os.sep, 'home', 'sam', 'standards', 'odm1_3_2', 'ODM1-3-2.xsd')

@click.command(help="Validate an ODM file")
@click.version_option("0.1.0", prog_name="odmvalidate")
@click.argument("odm_file")
@click.option(
    "--version",
    default="1.3.2",
    help="Path to store the retrieved dataset. Defaults to current directory."
)
@click.option(
    "--schema",
    default=SCHEMA_FILE,
    type=click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
    help="Path and filename of the ODM schema file."
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Puts the program into verbose mode to display additional messages",
)

def cli(odm_file: str, version: str , schema: Path, verbose: bool = False):
    validate_odm_xml_file(odm_file, schema, verbose)
    sys.stdout.write(str(odm_file))
    sys.stdout.flush()

def validate_odm_xml_file(odm_file, schema_file, verbose):
    validator = P.ODMSchemaValidator(schema_file)
    try:
        validator.validate_file(odm_file)
    except XSD.validators.exceptions.XMLSchemaChildrenValidationError as ve:
        print(f"schema validation errors: {ve}")
    else:
        if verbose:
            print("ODM XML schema validation completed successfully...")

if __name__ == "__main__":
    cli()