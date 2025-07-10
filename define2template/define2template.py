import odmlib.define_loader as OL
import odmlib.loader as LD
import template_define as TD
import odmlib.odm_parser as P
import xmlschema as XSD
import os
import sys
import click
from pathlib import Path
import study, standards, datasets, variables, value_level as valuelevel, where_clauses as whereclauses, codelists
import dictionaries, methods, comments, documents

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

SECTIONS = ["Study", "Standards", "Datasets", "Variables", "ValueLevel", "WhereClauses", "CodeLists", "Dictionaries",
              "Methods", "Comments", "Documents"]
TEMPLATE_FILE = "define-lzzt-template.json"


@click.command(help="Generate Define-XML JSON template from a Define-XML file.")
@click.version_option("0.0.1", prog_name="define2template")
@click.option(
    "-d",
    "--define",
    "define_file",
    default=Path(__config.data_path).joinpath("define-msg.xml"),
    help="The path to the define.xml input file",
    type = click.Path(
        exists=False,
        file_okay=True,
        readable=True,
        path_type=Path
    ),
)
@click.option(
    "-t",
    "--template",
    "template_file",
    default=Path(__config.data_path).joinpath(TEMPLATE_FILE),
    help="The path to the JSON template file",
    type = click.Path(
        exists=False,
        file_okay=True,
        readable=True,
        path_type=Path
    ),
)

def cli(define_file: Path, template_file: Path, verbose: bool = False):
    d2t = Define2Template(define_file, template_file, "en", verbose)
    d2t.create()


class Define2Template:
    """ generate a metadata template JSON file from a Define-XML v2.1 file """
    def __init__(self, define_file, template_file, language="en", verbose: bool = False):
        self.define_file = define_file
        self.template_file = template_file
        self.lang = language
        self.acrf = ""
        self.verbose = verbose

    def create(self):
        loader = LD.ODMLoader(OL.XMLDefineLoader(model_package="define_2_1", ns_uri="http://www.cdisc.org/ns/def/v2.1"))
        loader.open_odm_document(self.define_file)
        mdv_odmlib = loader.MetaDataVersion()
        study_odmlib = loader.Study()
        self._set_acrf(mdv_odmlib)
        # ws_files = []
        templates = []
        for section in SECTIONS:
            if section == "Study":
                ws = eval(section.lower() + "." + section + "(study_odmlib, mdv_odmlib, self.lang, self.acrf)")
            else:
                ws = eval(section.lower() + "." + section + "(mdv_odmlib)")
            ws.extract()
            templates.append(ws.get_template())
        self._write_template(templates)

    def _set_acrf(self, mdv):
        if mdv.AnnotatedCRF.DocumentRef:
            self.acrf = mdv.AnnotatedCRF.DocumentRef.leafID
        else:
            for leaf in mdv.leaf:
                if leaf.title and "annotated" in leaf.title._content.lower():
                    self.acrf = leaf.ID
                    break

    def _write_template(self, templates):
        td = TD.TemplateFile(templates, self.template_file, SECTIONS)
        td.create()

class DefineValidator:
    """ Define-XML schema validation """
    def __init__(self, schema, define_file):
        """
        :param schema: str - the path and filename for the Define-XML schema
        :param define_file: str - the path and filename for the Define-XML to validate
        """
        self.schema_file = schema
        self.define_file = define_file

    def validate(self):
        """" execute the schema validation and report the results """
        validator = P.ODMSchemaValidator(self.schema_file)
        try:
            validator.validate_file(self.define_file)
            print("define-XML schema validation completed successfully...")
        except XSD.validators.exceptions.XMLSchemaChildrenValidationError as ve:
            print(f"schema validation errors: {ve}")

    def _check_file_existence(self):
        """ throw an error if the schema of Define-XML file cannot be found """
        if not os.path.isfile(self.schema_file):
            raise ValueError("The schema validate flag is set, but the schema file cannot be found.")
        if not os.path.isfile(self.define_file):
            raise ValueError("The define-xml file cannot be found.")


if __name__ == "__main__":
    cli()
