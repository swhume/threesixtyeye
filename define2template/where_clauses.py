class WhereClauses:
    def __init__(self, odmlib_mdv):
        self.mdv = odmlib_mdv
        self.templates = []

    def extract(self):
        for wc in self.mdv.WhereClauseDef:
            metadata = {}
            comment_oid = ""
            if wc.CommentOID:
                comment_oid = wc.CommentOID
            for rc in wc.RangeCheck:
                dataset = self._get_dataset_name(rc.ItemOID)
                variable_name = self._get_variable_name(rc.ItemOID)
                value = self._load_check_values(rc)
                # TODO fix the multiple level RC with join
                metadata["oid"] = wc.OID
                metadata["dataset"] = dataset
                metadata["variable"] = variable_name
                metadata["comparator"] = rc.Comparator
                metadata["value"] = value
                metadata["comment"] = comment_oid
                self.templates.append(metadata)

    def _get_dataset_name(self, item_oid):
        for igd in self.mdv.ItemGroupDef:
            ir = igd.find("ItemRef", "ItemOID", item_oid)
            if ir:
                return igd.Name
        raise ValueError(f"Dataset for ItemRef {item_oid} not found in the Define-XML file")

    def _get_variable_name(self, item_oid):
        item = self.mdv.find("ItemDef", "OID", item_oid)
        if item:
            return item.Name
        else:
            raise ValueError(f"ItemDef for ItemRef {item_oid} not found in the Define-XML file")

    def _load_check_values(self, rc):
        check_values = []
        for cv in rc.CheckValue:
            if cv._content:
                check_values.append(cv._content)
            else:
                check_values.append("")
        return ",".join(check_values)

    def get_template(self):
        return self.templates