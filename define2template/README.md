# Define Template Schema

This repository contains a LinkML schema for representing clinical study data definitions in the CDISC Define-XML format. The schema is based on the JSON structure in `define-lzzt-template.json` and provides a comprehensive model for representing study metadata, datasets, variables, codelists, and other components of clinical study data definitions.

## Schema Overview

The schema defines the following main classes:

- **DefineTemplate**: Root class representing the entire define-lzzt-template structure
- **Study**: Basic study information
- **Standard**: Standard definition used in the study
- **Dataset**: Dataset definition
- **Variable**: Variable definition
- **WhereClause**: Where clause definition
- **CodeListItem**: Code list item definition
- **Method**: Method definition
- **Comment**: Comment definition
- **Document**: Document reference

Each class has a set of attributes with appropriate types, constraints, and relationships to other classes. The schema also defines enumerations for controlled vocabularies like data types, standard types, dataset classes, variable roles, and comparator types.

## Usage

### Validating JSON Data

You can use the schema to validate JSON data against the schema using the LinkML validator:

```bash
linkml-validate -s define_template.yaml -C DefineTemplate data.json
```

### Generating Other Formats

You can use the schema to generate other formats like JSON Schema, ShEx, OWL, etc.:

```bash
gen-json-schema define_template.yaml > define_template.schema.json
gen-shex define_template.yaml > define_template.shex
gen-owl define_template.yaml > define_template.owl
```

### Programmatic Usage

You can use the schema programmatically in Python:

```python
from linkml_runtime.loaders import json_loader
from linkml_runtime.dumpers import json_dumper

# Load data from JSON
data = json_loader.load("data.json", "DefineTemplate", "define_template.yaml")

# Modify data
data.study.studyName = "New Study Name"

# Save data to JSON
json_dumper.dump(data, "new_data.json")
```

## Example

Here's a simple example of a clinical study data definition that conforms to the schema:

```yaml
study:
  studyName: "CDISCPILOT01"
  studyDescription: "Study Data Tabulation Model Metadata Submission Guidelines Sample Study"
  protocolName: "CDISCPILOT01"
  language: "en"
  annotatedCRF: "LF.acrf"
standards:
  - oid: "STD.1"
    name: "STDTMIG"
    type: "IG"
    publishingSet: ""
    version: "3.3"
    status: "Final"
    comment: "COM.ST1"
datasets:
  - oid: "IG.DM"
    name: "DM"
    description: "Demographics"
    class: "SPECIAL PURPOSE"
    structure: "One record per subject"
    purpose: "Tabulation"
    repeating: "No"
    referenceData: "No"
    standardOid: "STD.1"
variables:
  - oid: "IT.DM.STUDYID"
    order: 1
    dataset: "DM"
    name: "DM"
    variable: "STUDYID"
    label: "Study Identifier"
    dataType: "text"
    length: 12
    mandatory: "Yes"
    role: "Identifier"
```

## Installation

To use this schema, you need to install LinkML:

```bash
pip install linkml
```

## References

- [LinkML Documentation](https://linkml.io/linkml/)
- [CDISC Define-XML](https://www.cdisc.org/standards/data-exchange/define-xml)