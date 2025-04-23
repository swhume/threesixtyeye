"""
define2shell.py takes an ItemGroupDef OID and the path to the define.xml to generate a Dataset-JSON shell file.
A Dataset-JSON shell contains only the metadata in the JSON format.

A future version may include:
- An option to generate Dataset-JSON as JSON or NDJSON
- An option to generate all the datasets included in the Define-XML (removed from this version to KISS)
- Process Define-XML v2.1 in addition to v2.0 (odmlib supports both)

The define.xml used for this was retrieved from the same source as the raw CDASH Dataset-JSON datasets.
The define.xml needed some updates to make it valid, including adding a ProtocolName and commenting out invalid
Origin Types.
"""
from pathlib import Path
import dataset as ds
import datetime
import json
import sys
import click
import odmlib.define_loader as OL
import odmlib.loader as LD

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

@click.command(help="Generates a Dataset-JSON shell (metadata only) from a define.xml and ItemGroupDef OID.")
@click.version_option("0.0.1", prog_name="define2shell")
@click.option(
    "-o",
    "--oid",
    help = "The OID of the Dataset-JSON file to generate"
)
@click.option(
    "-p",
    "--path",
    default=__config.data_path,
    help="The path to the define.xml and datasets"
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Puts the program into verbose mode to display additional messages",
)

def cli(oid: str, path: str, verbose: bool = False):
    """
    CLI for generating a Dataset-JSON shell (metadata only) from a define.xml file
    and an ItemGroupDef OID.
    Parameters:
      oid (str): The OID of the Dataset-JSON file to generate
      path (str): The path to the folder containing define.xml and datasets files
      verbose (bool): Flag to enable verbose output with additional messages
    """
    loader = LD.ODMLoader(OL.XMLDefineLoader())
    loader.open_odm_document(Path(path).joinpath("define.xml"))
    study = loader.Study()
    mdv = loader.MetaDataVersion()
    ig = mdv.find("ItemGroupDef", "OID", oid.upper())
    study_oid = get_study_oid(study)
    datasets(study_oid, mdv, ig)


def dataset_metadata(study_oid, mdv, ig):
    """
    Generates and returns metadata for the dataset.
    Parameters:
      study_oid (str): The identifier of the study.
      mdv (object): The metadata version object containing its attributes.
      ig (object): The item group object containing its attributes.
    Returns:
      dict: A dictionary containing the generated dataset metadata.
    """
    ds_metadata = {}
    ds_metadata["datasetJSONCreationDateTime"] = datetime.datetime.now(datetime.timezone.utc)
    ds_metadata["datasetJSONVersion"] = "1.1.0"
    ds_metadata["fileOID"] = "360i.dataset.sdtm." + ig.Name
    ds_metadata["originator"] = "360i"
    if __config.source_system_name and __config.source_system_version:
        source_system = {}
        source_system["name"] = __config.source_system_name
        source_system["version"] = __config.source_system_version
        ds_metadata["sourceSystem"] = source_system
    ds_metadata["studyOID"] = study_oid
    ds_metadata["metaDataVersionOID"] = mdv.OID
    ds_metadata["itemGroupOID"] = ig.OID
    ds_metadata["records"] = 0
    ds_metadata["name"] = ig.Name
    ds_metadata["label"] = ig.Description.TranslatedText[0]._content
    ds_metadata["columns"] = []
    return ds_metadata

def datasets(study_oid, mdv, ig, verbose=False):
    """
    Generates dataset metadata and saves it as a JSON file.
    Parameters:
      study_oid (str): The identifier of the study from which metadata is extracted.
      mdv: The metadata object containing definitions and references for items and item groups.
      ig: The item group object used for generating the dataset metadata.
      verbose (bool): Flag indicating if detailed column metadata should be output to the console.
    """
    ds_metadata = dataset_metadata(study_oid, mdv, ig)
    if verbose:
        click.echo(ds_metadata)
    dataset = ds.DatasetMetadata(**ds_metadata)
    for ir in ig.ItemRef:
        col_metadata = {}
        itd = mdv.find("ItemDef", "OID", ir.ItemOID)
        col_metadata["itemOID"] = itd.OID
        col_metadata["name"] = itd.Name
        col_metadata["label"] = itd.Description.TranslatedText[0]._content
        data_type, target_data_type = get_data_types(itd.DataType, mdv.StandardName, itd.DisplayFormat)
        col_metadata["dataType"] = data_type
        if target_data_type:
            col_metadata["targetDataType"] = target_data_type
        if itd.Length:
            col_metadata["length"] = itd.Length
        if itd.DisplayFormat:
            col_metadata["displayFormat"] = itd.DisplayFormat
        if ir.KeySequence:
            col_metadata["keySequence"] = ir.KeySequence
        if verbose:
            click.echo(col_metadata)
        column = ds.Column(**col_metadata)
        dataset.columns.append(column)
    dataset_name = ig.Name + ".json"
    dataset_file = Path(__config.data_path).joinpath("shells").joinpath(dataset_name)
    with open(dataset_file, "w") as f:
        json.dump(dataset.model_dump(mode='json', exclude_none=True), f, indent=2)


def get_data_types(define_datatype: str, standard_name: str = None, display_format: str = None):
    """
    Determines and returns the appropriate data types for a given input based on
    various conditions such as the defined data type, standard name, and display
    format.
    Parameters:
      define_datatype (str): The data type being defined (e.g., "text", "integer").
      standard_name (str, optional): Name of the standard in the define.xml.
      display_format (str, optional): A SAS format string that specifies the display style
    Returns:
      tuple: A 2-tuple containing: the resulting data type and the resulting target data type
    """
    data_type = ""
    target_data_type = ""
    if define_datatype == "text":
        data_type = "string"
    elif define_datatype == "decimal":
        data_type = define_datatype
        target_data_type = define_datatype
    elif "adam" in standard_name.lower() and define_datatype == "integer" and "date9" in display_format.lower():
        # assume this means that we're dealing with an integer date variable
        data_type = "datetime"
        target_data_type = "integer"
    elif "adam" in standard_name.lower() and define_datatype == "integer" and "datetime19." in display_format.lower():
        # assume this means that we're dealing with an integer date variable
        data_type = "datetime"
        target_data_type = "integer"
    else:
        data_type = define_datatype
    return data_type, target_data_type


def get_study_oid(study):
    """
    Retrieves the study OID either from the configuration or the provided study object.
    Parameters:
      study (object): odmlib study object from which the OID may be retrieved
    Returns:
      str: The retrieved study OID from either the configuration or the study object.
    """
    if __config.study_oid:
        return __config.study_oid
    else:
        return study.OID


if __name__ == "__main__":
    cli()
