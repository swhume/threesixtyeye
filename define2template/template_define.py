import json

class TemplateFile:
    def __init__(self, templates, template_filename, template_names):
        self.template_file = template_filename
        self.templates = templates
        self.template_names = template_names

    def create(self):
        metadata = {}
        for idx, template in enumerate(self.templates):
            metadata[self.template_names[idx]] = template
        with open(self.template_file, 'w') as f:
            json.dump(metadata, f, indent=4)
