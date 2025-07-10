class Study:
    def __init__(self, odmlib_study, odmlib_mdv, language="en", acrf="LF.acrf"):
        self.study = odmlib_study
        self.mdv = odmlib_mdv
        self.acrf = acrf
        self.language = language
        self.template = {}

    def extract(self):
        print(f"Study OID: {self.study.GlobalVariables.StudyName._content}")
        self.template["studyName"] = self.study.GlobalVariables.StudyName._content
        self.template["studyDescription"] = self.study.GlobalVariables.StudyDescription._content
        self.template["protocolName"] = self.study.GlobalVariables.ProtocolName._content
        self.template["language"] = self.language
        self.template["annotatedCRF"] = self.acrf

    def get_template(self):
        return self.template
