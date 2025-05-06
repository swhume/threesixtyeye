from lxml import etree
from pathlib import Path
import sys

SCRIPT_DIR = Path.cwd()
sys.path.append(str(SCRIPT_DIR))
from config.config import AppSettings as CFG

__config = CFG()

ODM_METADATA_FILE = Path(__config.data_path).joinpath("ie-odm.xml")
STYLESHEET_FILE = Path(__file__).parent.joinpath("crf_1_3_2.xsl")
OUTPUT_FILE = Path(__config.data_path).joinpath("odm_360i_cosa.html")


def transform_xml(xml_path, xsl_path, output_path=OUTPUT_FILE):
    """
    Transforms an XML file using an XSLT stylesheet.

    Args:
        xml_path (str): Path to the XML file.
        xsl_path (str): Path to the XSLT stylesheet file.
        output_path (str, optional): Path to save the transformed XML.
                                    If None, prints to console.
    """
    xml_tree = etree.parse(xml_path)
    xsl_tree = etree.parse(xsl_path)
    transform = etree.XSLT(xsl_tree)
    result_tree = transform(xml_tree)

    if output_path:
        with open(output_path, 'wb') as f:
            f.write(etree.tostring(result_tree, pretty_print=True))
    else:
        print(etree.tostring(result_tree, pretty_print=True).decode())


def main():
    transform_xml(ODM_METADATA_FILE, STYLESHEET_FILE, OUTPUT_FILE)

if __name__ == "__main__":
    main()
