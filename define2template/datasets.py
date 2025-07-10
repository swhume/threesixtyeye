class Datasets:
    def __init__(self, odmlib_mdv):
        self.mdv = odmlib_mdv
        self.template = []

    def extract(self):
        for ig in self.mdv.ItemGroupDef:
            metadata = {}
            metadata["oid"] = ig.OID
            metadata["name"] = ig.Name
            metadata["description"] = ig.Description.TranslatedText[0]._content
            metadata["class"] = ig.Class.Name
            metadata["structure"] = ig.Structure
            metadata["purpose"] = ig.Purpose
            metadata["repeating"] = ig.Repeating
            metadata["referenceData"] = ig.IsReferenceData
            if ig.CommentOID:
                metadata["comment"] = ig.CommentOID
            if ig.IsNonStandard:
                metadata["isNonStandard"] = ig.IsNonStandard
            metadata["standardOid"] = ig.StandardOID
            self.template.append(metadata)

    def get_template(self):
        return self.template