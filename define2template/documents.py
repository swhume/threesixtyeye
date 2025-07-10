class Documents:
    def __init__(self, odmlib_mdv):
        self.mdv = odmlib_mdv
        self.templates = []

    def extract(self):
        for lf in self.mdv.leaf:
            metadata = {}
            metadata["id"] = lf.ID
            metadata["title"] = lf.title._content
            metadata["href"] = lf.href
            self.templates.append(metadata)

    def get_template(self):
        return self.templates