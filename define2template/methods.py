class Methods:
    def __init__(self, odmlib_mdv):
        self.mdv = odmlib_mdv
        self.templates = []

    def extract(self):
        for md in self.mdv.MethodDef:
            metadata = {}
            description = " ".join(md.Description.TranslatedText[0]._content.split())
            metadata["oid"] = md.OID
            metadata["name"] = md.Name
            metadata["type"] = md.Type
            metadata["description"] = description
            if md.FormalExpression:
                metadata["context"] = md.FormalExpression[0].Context
                metadata["code"] = md.FormalExpression[0]._content
            if md.DocumentRef:
                metadata["leaf_id"] = md.DocumentRef[0].leafID
                metadata["page_refs"] = md.DocumentRef[0].PDFPageRef[0].PageRefs
            self.templates.append(metadata)

    def get_template(self):
        return self.templates