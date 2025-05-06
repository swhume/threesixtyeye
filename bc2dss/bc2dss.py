import sys
from pathlib import Path
from cdisc_library_client import CDISCLibraryClient
import json
import click

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

@click.command(help="Use study BCs to retrieve the associated Dataset Specializations from the Library API.")
@click.version_option("0.1.0", prog_name="bc2dss")
@click.argument("usdm_bc_file")
@click.option(
    "--output",
    "-o",
    "output_file",
    help="Output file name. Defaults to dss_cdash.json in the data directory.",
    default=Path(__config.data_path).joinpath("soa_dss.json"),
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

def cli(usdm_bc_file, output_file, verbose: bool = False):
    # open usdm_bc_file, find BCs, use BCs to look-up DSSs, write DSS to a JSON file using BC ID as the key
    soa_dss = []
    with open(usdm_bc_file, 'r', encoding='utf-8') as f:
        soa_bc = json.load(f)
    for activity in soa_bc:
        if not activity["bc"]:
            if verbose:
                print(f"No BCs found for Activity {activity['activityName']} ({activity['activityId']})")
            continue
        for bc in activity["bc"]:
           soa_dss.append(get_dss_using_bc(bc, activity["activityId"]))
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(soa_dss, f, indent=2)

def get_dss_using_bc(bc, activity_id):
    bc_id = bc["bcId"]
    client = CDISCLibraryClient(api_key=__config.clib_api_key)
    # all_dss = client.get_sdtm_latest_sdtm_datasetspecializations("v2")
    bc_dss = client.get_biomedicalconcept_latest_datasetspecializations(version="v2", biomedicalconcept=bc_id)
    bc_dss["activityId"] = activity_id
    bc_dss["bcId"] = bc_id
    bc_dss["bcShortname"] = bc["bcShortname"]
    # print(f"the SYSBP DSS from the API: {bc_dss}")
    return bc_dss


if __name__ == "__main__":
    cli()
