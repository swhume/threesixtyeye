class Comments:
    def __init__(self, odmlib_mdv):
        self.mdv = odmlib_mdv
        self.templates = []

    def extract(self):
        for com in self.mdv.CommentDef:
            metadata = {}
            comment = " ".join(com.Description.TranslatedText[0]._content.split())
            metadata["oid"] = com.OID
            metadata["comment"] = comment
            if com.DocumentRef:
                metadata["leaf_id"] = com.DocumentRef[0].leafID
                if com.DocumentRef[0].PDFPageRef:
                    metadata["page_refs"] = com.DocumentRef[0].PDFPageRef[0].PageRefs
            self.templates.append(metadata)

    def get_template(self):
        return self.templates