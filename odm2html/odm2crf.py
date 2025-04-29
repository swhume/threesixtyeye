"""
odm2crf uses the Dominate library to generate ODM CRFs from ODM v1.3.2 XML.
"""
from dominate import document
from dominate.tags import *
from pathlib import Path
import os
import sys
import click
from odmlib import odm_loader as OL, loader as LO

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

DEFAULT_OUTPUT_FILE = Path(__config.data_path).joinpath("odm_360i_crf.html")

@click.command(help="Convert a ODM v1.3.2 CRF Metadata to HTML")
@click.version_option("0.1.0", prog_name="odm2crf")
@click.argument("odm_file")
@click.option(
    "--output",
    "-o",
    "output_file",
    metavar="FILE",
    help="Output file name. Defaults to odm_360i_crf.html in the data directory.",
    default=DEFAULT_OUTPUT_FILE,
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

def cli(odm_file: str, output_file: str, verbose: bool = False):
    doc = create_crf_html(odm_file, verbose)
    write_html_doc(doc, output_file, verbose)


def create_crf_html(odm_file, verbose):
    loader = LO.ODMLoader(OL.XMLODMLoader())
    loader.open_odm_document(odm_file)
    odm = loader.load_odm()
    study = loader.Study()
    if verbose:
        click.echo(f"Generating HTML CRF from {odm_file}")

    # Create HTML document
    doc = document(title='360i ODM CRF View')

    with doc.head:
        # Add some basic styling
        style('''
            body { font-family: Arial, sans-serif; margin: 20px; }
            .form-section { margin: 20px 0; padding: 10px; border: 1px solid #ccc; }
            .item-group { margin: 10px 0; padding: 5px; background-color: #f9f9f9; }
            .item { margin: 5px 0; }
            label { display: inline-block; min-width: 200px; }
        ''')

    with doc.body:
        h1('360i ODM CRFs')
        with div(cls='study-section'):
            h2(f'Study: {study.GlobalVariables.StudyName}')

            # Process MetaDataVersion
            mdv = study.MetaDataVersion[0]
            with div(cls='metadata-version'):
                h3(f'Metadata Version: {mdv.Name}')
                form_def = mdv.FormDef[0]
                with div(cls='form-section'):
                    h5(f'Form: {form_def.Description.TranslatedText[0]._content}')

                    # Process ItemGroups
                    for ig_ref in form_def.ItemGroupRef:
                        ig_def = mdv.find("ItemGroupDef", "OID", ig_ref.ItemGroupOID),
                        if ig_def:
                            with div(cls='item-group'):
                                h5(f'{ig_def[0].Name}')

                                # Process Items
                                for item_ref in ig_def[0].ItemRef:
                                    item_def = mdv.find("ItemDef", "OID", item_ref.ItemOID)
                                    # if item_def:
                                    with div(cls='item'):
                                        label(f"{item_def.Question.TranslatedText[0]._content}")
                                        if item_def.CodeListRef:
                                            cl = mdv.find("CodeList", "OID", item_def.CodeListRef.CodeListOID),
                                            options_list = gen_codelist_items(cl[0])
                                            with select(name=cl[0].Name):
                                                for opt in options_list:
                                                    option(opt[0], value=opt[1])
                                        else:
                                            input_(type='text',
                                                   name=item_def.OID,
                                                   placeholder=item_def.Name)
                                        for alias in item_def.Alias:
                                            if alias.Context == "CDASH" or alias.Context == "SDTM":
                                                input_(type="text",
                                                       name=item_def.OID + "." + alias.Context,
                                                       placeholder=alias.Context + ": " + alias.Name,
                                                       style="background-color: LightYellow; border: 1px solid #ccc;")
    return doc


def write_html_doc(doc, output_file_path, verbose=False):
    if verbose:
        click.echo(f"Writing HTML CRF to {output_file_path}")
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(str(doc))

def gen_codelist_items(cl) -> list:
    options_list = []
    if cl.EnumeratedItem:
        for ei in cl.EnumeratedItem:
            options_list.append([ei.CodedValue, ei.CodedValue])
    elif cl.CodeListItem:
        for cli in cl.CodeListItem:
            options_list.append([cli.Decode.TranslatedText[0]._content, cli.CodedValue])
    return options_list

if __name__ == "__main__":
    cli()