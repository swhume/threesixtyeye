# shell2ndjson

The `shell2ndjson.py` filter reads in a Dataset-JSON v1.1 JSON shell dataset, converts it to an NDJSON 
representation, and writes the NDJSON to stdout.

A Dataset-JSON shell is a dataset that contains only the Dataset-JSON metadata.

NDJSON is supported by the Dataset-JSON standard. ND stands for newline delimited. NDJSON Dataset-JSON datasets
include all the metadata in the first line of the dataset.

## Example Usage

```
python3 shell2ndjson/shell2ndjson.py data/shells/IE.json > data/shells/IE.ndjson
```