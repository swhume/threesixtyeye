import sys
from pathlib import Path
import click
import odmlib.odm_loader as OL
import odmlib.ns_registry as NS

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

@click.command(help="Read an OSB extended ODM file.")
@click.version_option("0.0.1", prog_name="odmlib_osb")
@click.option(
    "-f",
    "--file",
    "odm_file",
    default=Path(__config.data_path).joinpath("osb").joinpath("osb_vs_crf.xml"),
    help="The path to the OSB ODM file.",
    type = click.Path(
        exists=True,
        file_okay=True,
        readable=True,
        path_type=Path
    ),
)

def cli(odm_file: Path):
    odm = load_osb_odm(odm_file)
    print(f"Study OID is {odm.Study[0].OID}")
    print(f"Study Name is {odm.Study[0].GlobalVariables.StudyName}")
    print(f"Study Description is {odm.Study[0].GlobalVariables.StudyDescription}")
    print(f"Protocol Name is {odm.Study[0].GlobalVariables.ProtocolName}")

def load_osb_odm(odm_file: Path):
    model_package = "osb_odm_1_0"
    loader = OL.XMLODMLoader(model_package=model_package, ns_uri="http://www.cdisc.org/ns/osb-xml/v1.0", local_model=True)
    ns = NS.NamespaceRegistry(prefix="osb", uri="http://www.cdisc.org/ns/osb-xml/v1.0")
    loader.create_document(odm_file, ns)
    odm = loader.load_odm()
    return odm

if __name__ == "__main__":
    odm = cli()
