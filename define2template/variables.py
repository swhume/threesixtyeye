class Variables:
    def __init__(self, odmlib_mdv):
        self.mdv = odmlib_mdv
        self.templates = []

    def extract(self):
        for ig in self.mdv.ItemGroupDef:
            dataset = ig.Name
            for ir in ig.ItemRef:
                # assumes all ItemDefs are referenced by an ItemRef
                metadata = {}
                ird = self._load_item_ref(ir)
                idd = self._load_item_def(ir.ItemOID)
                metadata['oid'] = idd["OID"]
                metadata['order'] = ird["Order"]
                metadata['dataset'] = dataset
                metadata['name'] = ig.Name
                metadata['variable'] = idd["Variable"]
                metadata['label'] = idd["Label"]
                metadata['dataType'] = idd["Data Type"]
                metadata['length'] = idd["Length"]
                metadata['significantDigits'] = idd["Significant Digits"]
                metadata['format'] = idd["Format"]
                metadata['keySequence'] = ird["KeySequence"]
                metadata['mandatory'] = ird["Mandatory"]
                if "CodeList" in idd:
                    metadata['codelist'] = idd["Codelist"]
                if "Valuelist" in idd:
                    metadata['value_list'] = idd["Valuelist"]
                if "Origin Type" in idd:
                    metadata['originType'] = idd["Origin Type"]
                if "Origin Source" in idd:
                    metadata['originSrc'] = idd["Origin Source"]
                if "Pages" in idd:
                    metadata['pages'] = idd["Pages"]
                if "Method" in ird:
                    metadata['method'] = ird["Method"]
                if "Predecessor" in idd:
                    metadata['predecessor'] = idd["Predecessor"]
                if "Role" in ird:
                    metadata['role'] = ird["Role"]
                if "Comment" in idd:
                    metadata['comment'] = idd["Comment"]
                if "IsNonStandard" in ird:
                    metadata['isNonStandard'] = ird["IsNonStandard"]
                if "StandardOID" in ird:
                    metadata['hasNoData'] = ird["HasNoData"]
                self.templates.append(metadata)

    def _load_item_ref(self, ir):
        ird = {}
        ird["Order"] = ir.OrderNumber
        ird["Mandatory"] = ir.Mandatory
        ird["KeySequence"] = ir.KeySequence
        ird["Method"] = ir.MethodOID
        ird["Role"] = ir.Role
        if ir.IsNonStandard:
            ird["IsNonStandard"] = ir.IsNonStandard
        if ir.HasNoData:
            ird["HasNoData"] = ir.HasNoData
        return ird

    def _load_item_def(self, item_oid):
        idd = {}
        it = self.mdv.find("ItemDef", "OID", item_oid)
        idd["OID"] = item_oid
        idd["Variable"] = it.Name
        idd["Data Type"] = it.DataType
        idd["Length"] = it.Length
        idd["Significant Digits"] = it.SignificantDigits
        idd["Format"] = it.DisplayFormat
        idd["Label"] = " ".join(it.Description.TranslatedText[0]._content.split())
        if it.CodeListRef:
            idd["Codelist"] = it.CodeListRef.CodeListOID
        if it.ValueListRef:
            idd["Valuelist"] = it.ValueListRef.ValueListOID
        # TODO add support for multiple Origins
        if it.Origin:
            idd["Origin Type"] = it.Origin[0].Type
        if it.Origin and it.Origin[0].Source:
            idd["Origin Source"] = it.Origin[0].Source
        if it.Origin and it.Origin[0].DocumentRef and it.Origin[0].DocumentRef[0].PDFPageRef:
            idd["Pages"] = it.Origin[0].DocumentRef[0].PDFPageRef[0].PageRefs
        if it.Origin and it.Origin[0].Type == "Predecessor":
            idd["Predecessor"] = it.Origin[0].Description.TranslatedText[0]._content
        if it.CommentOID:
            idd["Comment"] = it.CommentOID
        return idd

    def get_template(self):
        return self.templates