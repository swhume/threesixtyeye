"""
Class representing Dataset-JSON v1.0 content
"""
import json

class DsjVersionOne:
    def __init__(self, data_file, dataset_name):
        self.data_file = data_file
        self.dataset = None
        self.variables = None
        self.data_types = None
        self.load_data()
        if "clinicalData" in self.dataset:
            self.dataset_type = "clinicalData"
        else:
            self.dataset_type = "referenceData"
        self.dataset_name = dataset_name
        self.dataset_oid = "IG." + dataset_name.upper()


    def load_data(self):
        with open(self.data_file, 'r') as f:
            self.dataset = json.loads(f.read())

    def get_study_oid(self):
        return self.dataset[self.dataset_type]["studyOID"]

    def get_mdv_oid(self):
        return self.dataset[self.dataset_type]["metaDataVersionOID"]

    def get_dataset_oid(self):
        return self.dataset_oid

    def get_dataset_name(self):
        return self.dataset_name

    def get_dataset_type(self):
        return self.dataset_type

    def get_creation_date_time(self):
        return self.dataset["creationDateTime"]

    def get_file_oid(self):
        return self.dataset.get("fileOID", None)

    def get_records(self):
        return self.dataset[self.dataset_type]["itemGroupData"][self.dataset_oid]["records"]

    def get_dataset_label(self):
        return self.dataset[self.dataset_type]["itemGroupData"][self.dataset_oid]["label"]

    def get_dataset_metadata(self) -> dict:
        ds_name = self.dataset[self.dataset_type]["itemGroupData"][self.dataset_oid]["name"]
        ds_label = self.dataset[self.dataset_type]["itemGroupData"][self.dataset_oid]["label"]
        return {"name": ds_name, "label": ds_label}

    def get_variable_metadata(self):
        variables = list(self.dataset[self.dataset_type]["itemGroupData"][self.dataset_oid]["items"])
        return variables

    def get_variables(self):
        dataset_attrs = list(self.dataset[self.dataset_type]["itemGroupData"].values())[0]
        variables = [var['OID'] for var in dataset_attrs['items']]
        return variables

    def get_data_rows(self):
        ig_oid = "IG." + self.dataset_name.upper()
        for row in self.dataset[self.dataset_type]["itemGroupData"][ig_oid]["itemData"]:
            yield row
