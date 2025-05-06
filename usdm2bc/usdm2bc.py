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
EXTRACT_SOA_BC = """
    (
        $forceArray := function($v) {
            $type($v) = "array" ? $v : [$v]
        };
        $a := study.versions[].studyDesigns[].activities[].{
            "id": id,
            "name": name,
            "biomedicalConceptIds": biomedicalConceptIds
        };
        $b := study.versions[].studyDesigns[].biomedicalConcepts[].{
            "id": id,
            "concept": name,
            "type": reference ? (
                $contains(reference, "datasetspecializations") ? "Dataset Specialization" :
                $contains(reference, "biomedicalconcepts") ? "Biomedical Concept"
            ) : "Undefined",
            "code": code.standardCode.code,
            "decode": code.standardCode.decode,
            "dataElements": properties.name~>$join(", "),
            "dataTypes": properties.datatype.( $ = "" or $ = null ? "null" : $ )~>$join(", ")
        };

        $a.{
            "activityId": id,
            "activityName": name,
            "bc": $forceArray(
                $map(biomedicalConceptIds, function($id){
                    $b[id = $id].{
                        "usdmBcId": id,
                        "concept": concept,
                        "bcId": code,
                        "bcShortname": decode,
                        "bcType": type,
                        "dataElements": dataElements,
                        "dataTypes": dataTypes
                    }
                })
            )
        }
    )
"""

@click.command(help="Extract study BCs from an SDW USDM export file")
@click.version_option("0.1.0", prog_name="usdm2bc")
@click.argument("usdm_file")
@click.option(
    "--output",
    "-o",
    "output_file",
    help="Output file name. Defaults to usdm_bc.json in the data directory.",
    default=Path(__config.data_path).joinpath("usdm_bc.json"),
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
    jsonata_obj = jsonata.Jsonata(EXTRACT_SOA_BC)
    if verbose:
        click.echo(f"Querying {usdm_file} USDM export file for BCs...")
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
