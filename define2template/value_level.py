class ValueLevel:
    def __init__(self, odmlib_mdv):
        self.mdv = odmlib_mdv
        self.templates = []

    def extract(self):
        for vl in self.mdv.ValueListDef:
            dataset = self._get_dataset_name(vl.OID)
            for ir in vl.ItemRef:
                # assumes all ItemDefs are referenced by an ItemRef
                metadata = {}
                ird = self._load_item_ref(ir)
                idd = self._load_item_def(ir.ItemOID)
                metadata["oid"] = vl.OID
                metadata["order"] = ird["Order"]
                metadata["dataset"] = dataset
                metadata["variable"] = idd["Variable"]
                metadata["itemOid"] = ir.ItemOID
                metadata["whereClause"] = ird["Where Clause"]
                metadata["dataType"] = idd["Data Type"]
                metadata["length"] = idd["Length"]
                metadata["significantDigits"] = idd["Significant Digits"]
                metadata["format"] = idd["Format"]
                metadata["mandatory"] = ird["Mandatory"]
                metadata["codelist"] = idd["Codelist"]
                metadata["originType"] = idd["Origin Type"]
                metadata["originSource"] = idd["Origin Source"]
                metadata["pages"] = idd["Pages"]
                metadata["method"] = ird["Method"]
                metadata["predecessor"] = idd["Predecessor"]
                metadata["comment"] = idd["Comment"]
                self.templates.append(metadata)

    def _get_dataset_name(self, vl_oid):
        for item in self.mdv.ItemDef:
            if item.ValueListRef and item.ValueListRef.ValueListOID == vl_oid:
                for igd in self.mdv.ItemGroupDef:
                    ir = igd.find("ItemRef", "ItemOID", item.OID)
                    if ir:
                        return igd.Name
        raise ValueError(f"Dataset for ValueListDef {vl_oid} not found in the Define-XML file")


    def _load_item_ref(self, ir):
        ird = {}
        ird["Order"] = ir.OrderNumber
        ird["Mandatory"] = ir.Mandatory
        ird["Method"] = ir.MethodOID
        ird["Where Clause"] = self._get_where_clause_oid(ir)
        return ird

    def _load_item_def(self, item_oid):
        idd = {}
        it = self.mdv.find("ItemDef", "OID", item_oid)
        idd["Variable"] = it.Name
        idd["Data Type"] = it.DataType
        idd["Length"] = it.Length
        idd["Significant Digits"] = it.SignificantDigits
        idd["Format"] = it.DisplayFormat
        idd["Codelist"] = it.CodeListRef.CodeListOID if it.CodeListRef else ""
        # TODO add support for multiple Origins
        idd["Origin Type"] = it.Origin[0].Type if it.Origin else ""
        idd["Origin Source"] = it.Origin[0].Source if it.Origin and it.Origin[0].Source else ""
        idd["Pages"] = it.Origin[0].DocumentRef[0].PDFPageRef[0].PageRefs \
            if it.Origin and it.Origin[0].DocumentRef and it.Origin[0].DocumentRef[0].PDFPageRef else ""
        idd["Predecessor"] = it.Origin[0].Description.TranslatedText[0]._content \
            if it.Origin and it.Origin[0].Type == "Predecessor" else ""
        idd["Comment"] = it.CommentOID if it.CommentOID else ""
        return idd

    def _get_where_clause_oid(self, item):
        wc_oids = []
        for wc in item.WhereClauseRef:
            wc_oids.append(wc.WhereClauseOID)
        return "'".join(wc_oids)

    def get_template(self):
        return self.templates