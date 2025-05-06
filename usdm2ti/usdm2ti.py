import sys
from pathlib import Path
import click
import json
import jsonata

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

# from Anthony's notebook
EXTRACT_SDTM_TI = """
    study.versions[versionIdentifier=$studyVersionId].criteria[].{
        "STUDYID": $$.study.name,
        "DOMAIN": "TI",
        "IETESTCD": name,
        "IETEST": label,
        "IECAT": category.decode
    }
"""

@click.command(help="Extract study BCs from an SDW USDM export file")
@click.version_option("0.1.0", prog_name="usdm2bc")
@click.argument("usdm_file")
@click.option(
    "--output",
    "-o",
    "output_file",
    help="Output file name. Defaults to ti.json in the data directory.",
    default=Path(__config.data_path).joinpath("ti.json"),
    type=click.Path(
        exists=False,
        file_okay=True,
        readable=True,
        path_type=Path,
    ),
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Puts the program into verbose mode to display additional messages",
)

def cli(usdm_file, output_file, verbose: bool = False):
    jsonata_obj = jsonata.Jsonata(EXTRACT_SDTM_TI)
    jsonata_obj.assign("studyVersionId", "2")
    with open(usdm_file, 'r', encoding='utf-8') as f:
        usdm_export = json.load(f)
    # Evaluate the expression against the data
    result = jsonata_obj.evaluate(usdm_export)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    if verbose:
        click.echo(f"Wrote study BCs to {output_file}...")

if __name__ == "__main__":
    cli()
