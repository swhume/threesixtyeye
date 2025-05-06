"""
ti2ie.py generates an ODM v1.3.2 CRF from the TI content extracted from the USDM study design

TODO load global variables and other template metadata from an external source
"""
import sys
from pathlib import Path

import click
import json
import datetime
import odmlib.odm_1_3_2.model as ODM

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()
@click.command(help="Extract study BCs from an SDW USDM export file")
@click.version_option("0.1.0", prog_name="usdm2bc")
@click.argument("ti_file")
@click.option(
    "--output",
    "-o",
    "output_file",
    help="ODM output file name. Defaults to ie-ti.xml in the data directory.",
    default=Path(__config.data_path).joinpath("ie-ti.xml"),
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

def cli(ti_file, output_file, verbose: bool = False):
    if verbose:
        print(f"Generating the IE {output_file} from TI {ti_file}...")
    with open(ti_file, 'r', encoding='utf-8') as f:
        ti = json.load(f)
    gen_odm_doc(ti, output_file, verbose)

def add_form(root, ig_list: list, ti: dict, verbose: bool = False) -> None:
        fd = ODM.FormDef(OID="F.IE", Name="Inclusion/Exclusion Criteria Not Met", Repeating="No")
        fd.Description = ODM.Description()
        fd.Description.TranslatedText.append(ODM.TranslatedText(_content="IE - Inclusion/Exclusion Criteria Not Met", lang="en"))
        for order, ig in enumerate(ig_list, 1):
            fd.ItemGroupRef.append(ODM.ItemGroupRef(ItemGroupOID=ig, Mandatory="No", OrderNumber=order))
        root.Study[0].MetaDataVersion[0].FormDef.append(fd)

def add_item_groups(root: ODM.ODM, ig_list: list, verbose: bool = False) -> None:
    item_group = None
    for ig in ig_list:
        if ig == "IG.Common":
            item_group = ODM.ItemGroupDef(OID=ig, Name="Common Keys", Repeating="No")
            add_ig_common_items(item_group)
        elif ig == "IG.IE.Header":
            item_group = ODM.ItemGroupDef(OID=ig, Name="Inclusion/Exclusion Criteria Assessment", Repeating="No")
            add_ig_header_items(item_group)
        elif ig == "IG.IE.IENotMet":
            item_group = ODM.ItemGroupDef(OID=ig, Name="Inclusion/Exclusion Criteria Not Met", Repeating="Yes")
            add_ig_ienotmet_items(item_group)
        root.Study[0].MetaDataVersion[0].ItemGroupDef.append(item_group)


def add_ig_ienotmet_items(item_group: ODM.ItemGroupDef) -> None:
    item_group.ItemRef.append(ODM.ItemRef(ItemOID="IT.IECAT", Mandatory="No", OrderNumber=1))
    item_group.ItemRef.append(ODM.ItemRef(ItemOID="IT.IETESTCD", Mandatory="No", OrderNumber=2))


def add_ig_header_items(item_group: ODM.ItemGroupDef) -> None:
    item_group.ItemRef.append(ODM.ItemRef(ItemOID="IT.IEYN", Mandatory="No", OrderNumber=1))
    item_group.ItemRef.append(ODM.ItemRef(ItemOID="IT.IEDAT", Mandatory="No", OrderNumber=2))


def add_ig_common_items(item_group: ODM.ItemGroupDef) -> None:
    item_group.ItemRef.append(ODM.ItemRef(ItemOID="IT.STUDYID", Mandatory="No", OrderNumber=1))
    item_group.ItemRef.append(ODM.ItemRef(ItemOID="IT.SITEID", Mandatory="No", OrderNumber=2))
    item_group.ItemRef.append(ODM.ItemRef(ItemOID="IT.SUBJID", Mandatory="No", OrderNumber=3))
    item_group.ItemRef.append(ODM.ItemRef(ItemOID="IT.VISIT", Mandatory="No", OrderNumber=4))
    item_group.ItemRef.append(ODM.ItemRef(ItemOID="IT.VISITDAT", Mandatory="No", OrderNumber=5))


def add_itd_common_items(root: ODM.ODM, verbose: bool = False) -> None:
    # STUDYID
    itd = ODM.ItemDef(OID="IT.STUDYID", Name="STUDYID", DataType="text", Length=20)
    itd.Description = ODM.Description()
    itd.Description.TranslatedText.append(ODM.TranslatedText(_content="Study Identifier", lang="en"))
    itd.Question = ODM.Question()
    itd.Question.TranslatedText.append(ODM.TranslatedText(_content="What is the study identifier?", lang="en"))
    itd.Alias.append(ODM.Alias(Name="IE.STUDYID", Context="CDASH"))
    itd.Alias.append(ODM.Alias(Name="IE.STUDYID", Context="SDTM"))
    root.Study[0].MetaDataVersion[0].ItemDef.append(itd)
    # SITEID
    itd = ODM.ItemDef(OID="IT.SITEID", Name="SITEID", DataType="text", Length=20)
    itd.Description = ODM.Description()
    itd.Description.TranslatedText.append(ODM.TranslatedText(_content="Study Site Identifier", lang="en"))
    itd.Question = ODM.Question()
    itd.Question.TranslatedText.append(ODM.TranslatedText(_content="What is the site identifier?", lang="en"))
    itd.Alias.append(ODM.Alias(Name="IE.SITEID", Context="CDASH"))
    itd.Alias.append(ODM.Alias(Name="IE.SITEID", Context="SDTM"))
    root.Study[0].MetaDataVersion[0].ItemDef.append(itd)
    # SUBJID
    itd = ODM.ItemDef(OID="IT.SUBJID", Name="SUBJID", DataType="text", Length=20)
    itd.Description = ODM.Description()
    itd.Description.TranslatedText.append(ODM.TranslatedText(_content="Subject Identifier", lang="en"))
    itd.Question = ODM.Question()
    itd.Question.TranslatedText.append(ODM.TranslatedText(_content="What is the subject identifier?", lang="en"))
    itd.Alias.append(ODM.Alias(Name="IE.SUBJID", Context="CDASH"))
    itd.Alias.append(ODM.Alias(Name="IE.SUBJID", Context="SDTM"))
    root.Study[0].MetaDataVersion[0].ItemDef.append(itd)
    # VISIT
    itd = ODM.ItemDef(OID="IT.VISIT", Name="VISIT", DataType="text", Length=20)
    itd.Description = ODM.Description()
    itd.Description.TranslatedText.append(ODM.TranslatedText(_content="Visit Name", lang="en"))
    itd.Question = ODM.Question()
    itd.Question.TranslatedText.append(ODM.TranslatedText(_content="What is the visit name?", lang="en"))
    itd.Alias.append(ODM.Alias(Name="IE.VISIT", Context="CDASH"))
    itd.Alias.append(ODM.Alias(Name="IE.VISIT", Context="SDTM"))
    root.Study[0].MetaDataVersion[0].ItemDef.append(itd)
    # VISDAT
    itd = ODM.ItemDef(OID="IT.VISITDAT", Name="VISITDAT", DataType="text", Length=20)
    itd.Description = ODM.Description()
    itd.Description.TranslatedText.append(ODM.TranslatedText(_content="Visit Date", lang="en"))
    itd.Question = ODM.Question()
    itd.Question.TranslatedText.append(ODM.TranslatedText(_content="What is the visit date?", lang="en"))
    itd.Alias.append(ODM.Alias(Name="IE.VISITDAT", Context="CDASH"))
    itd.Alias.append(ODM.Alias(Name="IE.VISITDAT", Context="SDTM"))
    root.Study[0].MetaDataVersion[0].ItemDef.append(itd)

def add_itd_header_items(root: ODM.ODM, verbose: bool = False) -> None:
    # IEYN
    itd = ODM.ItemDef(OID="IT.IEYN", Name="IEYN", DataType="text", Length=3)
    itd.Description = ODM.Description()
    itd.Description.TranslatedText.append(ODM.TranslatedText(_content="IE Yes/No", lang="en"))
    itd.Question = ODM.Question()
    itd.Question.TranslatedText.append(ODM.TranslatedText(_content="Were all eligibility criteria met?", lang="en"))
    itd.CodeListRef = ODM.CodeListRef(CodeListOID="CL.NY")
    itd.Alias.append(ODM.Alias(Name="Met Criteria", Context="prompt"))
    itd.Alias.append(ODM.Alias(Name="IE.IEYN", Context="CDASH"))
    itd.Alias.append(ODM.Alias(Name="NOT SUBMITTED", Context="SDTM"))
    root.Study[0].MetaDataVersion[0].ItemDef.append(itd)
    # IEDAT
    itd = ODM.ItemDef(OID="IT.IEDAT", Name="IEDAT", DataType="date")
    itd.Description = ODM.Description()
    itd.Description.TranslatedText.append(ODM.TranslatedText(_content="IE Date", lang="en"))
    itd.Question = ODM.Question()
    itd.Question.TranslatedText.append(ODM.TranslatedText(_content="Eligibility criteria assessment date?", lang="en"))
    itd.Alias.append(ODM.Alias(Name="Date", Context="prompt"))
    itd.Alias.append(ODM.Alias(Name="IE.IEDAT", Context="CDASH"))
    itd.Alias.append(ODM.Alias(Name="IE.IEDAT", Context="SDTM"))
    root.Study[0].MetaDataVersion[0].ItemDef.append(itd)

def add_itd_ienotmet_items(root: ODM.ODM, verbose: bool = False) -> None:
    # IECAT
    itd = ODM.ItemDef(OID="IT.IECAT", Name="IECAT", DataType="text", Length=15)
    itd.Description = ODM.Description()
    itd.Description.TranslatedText.append(ODM.TranslatedText(_content="IECAT", lang="en"))
    itd.Question = ODM.Question()
    itd.Question.TranslatedText.append(ODM.TranslatedText(_content="What was the category of the criterion?", lang="en"))
    itd.CodeListRef = ODM.CodeListRef(CodeListOID="CL.IECAT")
    itd.Alias.append(ODM.Alias(Name="Criteria Type", Context="prompt"))
    itd.Alias.append(ODM.Alias(Name="IE.IECAT", Context="CDASH"))
    itd.Alias.append(ODM.Alias(Name="IE.IECAT", Context="SDTM"))
    root.Study[0].MetaDataVersion[0].ItemDef.append(itd)
    # IETESTCD
    itd = ODM.ItemDef(OID="IT.IETESTCD", Name="IETESTCD", DataType="text", Length=35)
    itd.Description = ODM.Description()
    itd.Description.TranslatedText.append(ODM.TranslatedText(_content="IETESTCD", lang="en"))
    itd.Question = ODM.Question()
    itd.Question.TranslatedText.append(ODM.TranslatedText(_content="Inclusion criteria not met or exclusion criterion met?", lang="en"))
    itd.CodeListRef = ODM.CodeListRef(CodeListOID="CL.IETESTCD")
    itd.Alias.append(ODM.Alias(Name="Exception Criterion", Context="prompt"))
    itd.Alias.append(ODM.Alias(Name="IE.IETESTCD", Context="CDASH"))
    itd.Alias.append(ODM.Alias(Name="IE.IETESTCD", Context="SDTM"))
    root.Study[0].MetaDataVersion[0].ItemDef.append(itd)


def add_items(root, verbose: bool = False) -> None:
    add_itd_common_items(root, verbose)
    add_itd_header_items(root, verbose)
    add_itd_ienotmet_items(root, verbose)

def add_cl_ny(root, verbose: bool = False,):
    cl = ODM.CodeList(OID="CL.NY", Name="No Yes Response Only", DataType="text")
    cli = ODM.CodeListItem(CodedValue="N", OrderNumber=1)
    cli.Decode = ODM.Decode()
    cli.Decode.TranslatedText.append(ODM.TranslatedText(_content="No", lang="en"))
    cl.CodeListItem.append(cli)
    cli = ODM.CodeListItem(CodedValue="Y", OrderNumber=2)
    cli.Decode = ODM.Decode()
    cli.Decode.TranslatedText.append(ODM.TranslatedText(_content="Yes", lang="en"))
    cl.CodeListItem.append(cli)
    cl.Alias.append(ODM.Alias(Name="C66742", Context="nci:ExtCodeID"))
    root.Study[0].MetaDataVersion[0].CodeList.append(cl)


def add_cl_cat(root, ti, verbose: bool = False):
    cl_cat_set = {cat["IECAT"] for cat in ti}
    cl = ODM.CodeList(OID="CL.IECAT", Name="Inclusion/Exclusion Category", DataType="text")
    for i, cat in enumerate(cl_cat_set, 1):
        cli = ODM.CodeListItem(CodedValue=cat, OrderNumber=i)
        cli.Decode = ODM.Decode()
        cli.Decode.TranslatedText.append(ODM.TranslatedText(_content=cat.upper(), lang="en"))
        cl.CodeListItem.append(cli)
    cl.Alias.append(ODM.Alias(Name="C66797", Context="nci:ExtCodeID"))
    root.Study[0].MetaDataVersion[0].CodeList.append(cl)

def add_cl_testcd(root, ti, verbose: bool = False):
    cl_testcd_list = [(test["IETESTCD"], test["IETEST"]) for test in ti]
    cl = ODM.CodeList(OID="CL.IETESTCD", Name="Inclusion/Exclusion Criteria", DataType="text")
    for i, test in enumerate(cl_testcd_list, 1):
        cli = ODM.CodeListItem(CodedValue=test[0], OrderNumber=i)
        cli.Decode = ODM.Decode()
        cli.Decode.TranslatedText.append(ODM.TranslatedText(_content=test[1], lang="en"))
        cl.CodeListItem.append(cli)
    root.Study[0].MetaDataVersion[0].CodeList.append(cl)

def add_codelists(root, ti, verbose) -> None:
    add_cl_ny(root, verbose)
    add_cl_cat(root, ti, verbose)
    add_cl_testcd(root, ti, verbose)

def gen_odm_doc(ti, odm_filename, verbose: bool = False) -> None:
    root = create_root()
    root.Study.append(ODM.Study(OID=__config.study_oid))
    # create the global variables
    root.Study[0].GlobalVariables = ODM.GlobalVariables()
    root.Study[0].GlobalVariables.StudyName = ODM.StudyName(_content="360i-lzzt-ie")
    root.Study[0].GlobalVariables.StudyDescription = ODM.StudyDescription(_content="360i LZZT IE CRF")
    root.Study[0].GlobalVariables.ProtocolName = ODM.ProtocolName(_content="360i LZZT")
    # create the MetaDataVersion
    root.Study[0].MetaDataVersion.append(ODM.MetaDataVersion(OID="MDV.360i.IE.CRF", Name="360i IE CRF")),
    ig_list = ["IG.Common", "IG.IE.Header", "IG.IE.IENotMet"]
    add_form(root, ig_list, ti, verbose)
    add_item_groups(root, ig_list, verbose)
    add_items(root, verbose)
    add_codelists(root, ti, verbose)
    root.write_xml(odm_filename)

def create_root():
    date_time = set_datetime()
    root = {"FileOID": "ODM.360i.LZZT.Metadata.IE",
            "Granularity": "Metadata",
            "AsOfDateTime": date_time,
            "CreationDateTime": date_time,
            "ODMVersion": "1.3.2",
            "Originator": "ODMLIB",
            "SourceSystem": "ODMLIB",
            "SourceSystemVersion": "0.1",
            "FileType": "Snapshot"}
    root = ODM.ODM(**root)
    return root

def set_datetime():
    """return the current datetime in ISO 8601 format"""
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=datetime.timezone.utc).isoformat()


if __name__ == "__main__":
    cli()
