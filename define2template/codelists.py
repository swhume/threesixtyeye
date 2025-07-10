class CodeLists:
    def __init__(self, odmlib_mdv):
        self.mdv = odmlib_mdv
        self.templates = []

    def extract(self):
        for cl in self.mdv.CodeList:
            if cl.EnumeratedItem:
                self._write_enumerated_item_row(cl)
            elif cl.CodeListItem:
                self._write_code_list_item_row(cl)

    def _write_enumerated_item_row(self, cl):
        attr = self._conditional_codelist_content(cl)
        for ei in cl.EnumeratedItem:
            metadata = {}
            metadata["oid"] = cl.OID
            metadata["name"] = cl.Name
            metadata["cl_c_code"] = attr["cl_c_code"]
            metadata["dataType"] = cl.DataType
            if ei.OrderNumber:
                metadata["order"] = ei.OrderNumber
            metadata["term"] = ei.CodedValue
            if ei.Alias:
                metadata["nci_term_code"] = ei.Alias[0].Name
            metadata["decoded_value"] = ""
            if "comment_oid" in attr:
                metadata["comment"] = attr["comment_oid"]
            if "is_non_std" in attr:
                metadata["isNonStandard"] = attr["is_non_std"]
            if "standard_oid" in attr:
                metadata["standardOid"] = attr["standard_oid"]
            self.templates.append(metadata)

    def _write_code_list_item_row(self, cl):
        attr = self._conditional_codelist_content(cl)
        for cli in cl.CodeListItem:
            metadata = {}
            decode = cli.Decode.TranslatedText[0]._content
            metadata["oid"] = cl.OID
            metadata["name"] = cl.Name
            metadata["cl_c_code"] = attr["cl_c_code"]
            metadata["dataType"] = cl.DataType
            if cli.OrderNumber:
                metadata["order"] = cli.OrderNumber
            metadata["term"] = cli.CodedValue
            if cli.Alias:
                metadata["nci_term_code"] = cli.Alias[0].Name
            if decode:
                metadata["decoded_value"] = decode
            if "comment_oid" in attr:
                metadata["comment"] = attr["comment_oid"]
            if "is_non_std" in attr:
                metadata["isNonStandard"] = attr["is_non_std"]
            if "standard_oid" in attr:
                metadata["standardOid"] = attr["standard_oid"]
            self.templates.append(metadata)

    def _conditional_codelist_content(self ,cl):
        attr = {"cl_c_code": ""}
        if cl.Alias:
            attr["cl_c_code"] = cl.Alias[0].Name
        if cl.CommentOID:
            attr["comment_oid"] = cl.CommentOID
        if cl.IsNonStandard:
            attr["is_non_std"] = cl.IsNonStandard
        if cl.StandardOID:
            attr["standard_oid"] = cl.StandardOID
        return attr

    def get_template(self):
        return self.templates