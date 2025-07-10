class Standards:
    def __init__(self, odmlib_mdv):
        self.mdv = odmlib_mdv
        self.template = []

    def extract(self):
        for std in self.mdv.Standards.Standard:
            metadata = {}
            metadata["oid"] = std.OID
            metadata["name"] = std.Name
            metadata["type"] = std.Type
            if std.PublishingSet:
                metadata["publishingSet"] = std.PublishingSet
            metadata["version"] = std.Version
            if std.Status:
                metadata["status"] = std.Status
            if std.CommentOID:
                metadata["comment"] = std.CommentOID
            self.template.append(metadata)

    def get_template(self):
        return self.template