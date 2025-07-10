class Dictionaries:
    def __init__(self, odmlib_mdv):
        self.mdv = odmlib_mdv
        self.templates = []

    def extract(self):
        for cl in self.mdv.CodeList:
            if cl.ExternalCodeList.Dictionary:
                ext_cl = cl.ExternalCodeList
                metadata = {}
                metadata["oid"] = cl.OID
                metadata["name"] = cl.Name
                metadata["dataType"] = cl.DataType
                metadata["dictionary"] = ext_cl.Dictionary
                if ext_cl.Version:
                    metadata["version"] = ext_cl.Version

    def get_template(self):
        return self.templates