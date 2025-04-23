
import json
import dataset as ds


class MetadataFile:
    def __init__(self, filename: str, dataset_metadata: ds.DatasetMetadata = None):
        """
        Reads and writes a metadata file that is part of a overall ndjson Dataset-JSON dataset. The DataFile class
        complements this by providing the data part of the dataset. They are maintained in separate files.
        :param filename: name of the metadata file
        :param dataset_metadata: a metadata object typically included when writing the metadata to file is desired
        """
        self.filename = filename
        self.metadata = dataset_metadata

    def get_metadata(self) -> ds.DatasetMetadata:
        """ return the metadata, if None then read it from the metadata file first """
        if self.metadata is None:
            self.read_file()
        return self.metadata

    def get_column_metadata(self) -> list:
        """ return the column metadata, if None then read it from the metadata file first """
        if self.metadata is None:
            self.read_file()
        return self.metadata["columns"]

    def get_metadata_json(self) -> dict:
        """ returns the metadata as JSON """
        if self.metadata is None:
            self.read_file()
        return self.metadata.model_dump(mode='json')

    def get_column_metadata_json(self) -> dict:
        """ returns the column metadata as JSON """
        if self.metadata is None:
            self.read_file()
        return self.metadata["columns"].model_dump(mode='json')

    def read_file(self) -> None:
        """ read the metadata file into a DatasetMetadata object """
        with open(self.filename) as f:
            json_line = json.loads(f.read())
            self.metadata = ds.DatasetMetadata(**json_line)

    def write_file(self, filename: str = None) -> None:
        """
        write the dataset metadata to its own file as JSON
        :param filename: optional filename to write to when not writing to the instance filename
        """
        if not filename:
            filename = self.filename
        with open(filename, mode='w') as f:
            f.write(f"{json.dumps(self.metadata.model_dump(mode='json', exclude_none=True))}\n")
            f.flush()

    def show_file(self) -> None:
        """ prints the metadata to stdout to aid in development and debugging """
        print(f"{self.metadata.model_dump(mode='json', exclude_none=True)}")
