import odmlib.odm_1_3_2.model as ODM
import odmlib.odm_element as OE
import odmlib.typed as T
import odmlib.ns_registry as NS


NS.NamespaceRegistry(prefix="osb", uri="http://www.cdisc.org/ns/osb-xml/v1.0")


class TranslatedText(ODM.TranslatedText):
    lang = ODM.TranslatedText.lang
    version = T.String(namespace="osb")
    _content = ODM.TranslatedText._content


class Alias(ODM.Alias):
    Context = ODM.Alias.Context
    Name = ODM.Alias.Name


class StudyDescription(ODM.StudyDescription):
    _content = ODM.StudyDescription._content


class ProtocolName(ODM.ProtocolName):
    _content = ODM.ProtocolName._content


class StudyName(ODM.StudyName):
    _content = ODM.StudyName._content


class GlobalVariables(ODM.GlobalVariables):
    StudyName = ODM.GlobalVariables.StudyName
    StudyDescription = ODM.GlobalVariables.StudyDescription
    ProtocolName = ODM.GlobalVariables.ProtocolName


class Symbol(ODM.Symbol):
    TranslatedText = ODM.Symbol.TranslatedText


class MeasurementUnit(ODM.MeasurementUnit):
    OID = ODM.MeasurementUnit.OID
    Name = ODM.MeasurementUnit.Name
    version = T.String(name="osb")
    Symbol = ODM.MeasurementUnit.Symbol
    Alias = ODM.MeasurementUnit.Alias


class BasicDefinitions(ODM.BasicDefinitions):
    MeasurementUnit = ODM.BasicDefinitions.MeasurementUnit


class Include(ODM.Include):
    StudyOID = ODM.Include.StudyOID
    MetaDataVersionOID = ODM.Include.MetaDataVersionOID


class Description(ODM.Description):
    TranslatedText = ODM.Description.TranslatedText

class StudyEventRef(ODM.StudyEventRef):
    StudyEventOID = ODM.StudyEventRef.StudyEventOID
    OrderNumber = ODM.StudyEventRef.OrderNumber
    Mandatory = ODM.StudyEventRef.Mandatory
    CollectionExceptionConditionOID = ODM.StudyEventRef.CollectionExceptionConditionOID


class Protocol(ODM.Protocol):
    Description = ODM.Protocol.Description
    StudyEventRef = ODM.Protocol.StudyEventRef
    Alias = ODM.Protocol.Alias


class FormRef(ODM.FormRef):
    FormOID = ODM.FormRef.FormOID
    OrderNumber = ODM.FormRef.OrderNumber
    Mandatory = ODM.FormRef.Mandatory
    CollectionExceptionConditionOID = ODM.FormRef.CollectionExceptionConditionOID


class StudyEventDef(ODM.StudyEventDef):
    OID = ODM.StudyEventDef.OID
    Name = ODM.StudyEventDef.Name
    Repeating = ODM.StudyEventDef.Repeating
    Type = ODM.StudyEventDef.Type
    Category = ODM.StudyEventDef.Category
    FormRef = ODM.StudyEventDef.FormRef
    def __len__(self):
        """ returns the number of FormRefs in an StudyEventDef object as the length """
        return len(self.FormRef)

    def __getitem__(self, position):
        """ creates an iterator from an StudyEventDef object that returns the FormRef in position """
        return self.FormRef[position]

    def __iter__(self):
        return iter(self.FormRef)


class ItemGroupRef(ODM.ItemGroupRef):
    ItemGroupOID = ODM.ItemGroupRef.ItemGroupOID
    OrderNumber = ODM.ItemGroupRef.OrderNumber
    Mandatory = ODM.ItemGroupRef.Mandatory
    CollectionExceptionConditionOID = ODM.ItemGroupRef.CollectionExceptionConditionOID


class ArchiveLayout(ODM.ArchiveLayout):
    OID = ODM.ArchiveLayout.OID
    PdfFileName = ODM.ArchiveLayout.PdfFileName
    PresentationOID = ODM.ArchiveLayout.PresentationOID


class FormDef(ODM.FormDef):
    OID = ODM.FormDef.OID
    Name = ODM.FormDef.Name
    Repeating = ODM.FormDef.Repeating
    version = T.String(name="osb")
    instruction = T.String(name="osb")
    Description = ODM.FormDef.Description
    ItemGroupRef = ODM.FormDef.ItemGroupRef
    ArchiveLayout = ODM.FormDef.ArchiveLayout
    Alias = ODM.FormDef.Alias

    def __len__(self):
        return len(self.ItemGroupRef)

    def __getitem__(self, position):
        return self.ItemGroupRef[position]

    def __iter__(self):
        return iter(self.ItemGroupRef)


class ItemRef(ODM.ItemRef):
    ItemOID = ODM.ItemRef.ItemOID
    OrderNumber = ODM.ItemRef.OrderNumber
    Mandatory = ODM.ItemRef.Mandatory
    KeySequence = ODM.ItemRef.KeySequence
    MethodOID = ODM.ItemRef.MethodOID
    Role = ODM.ItemRef.Role
    RoleCodeListOID = ODM.ItemRef.RoleCodeListOID


class DomainColor(OE.ODMElement):
    namespace = "osb"
    _content = T.String()


class ItemGroupDef(ODM.ItemGroupDef):
    OID = ODM.ItemGroupDef.OID
    Name = ODM.ItemGroupDef.Name
    Repeating = ODM.ItemGroupDef.Repeating
    IsReferenceData = ODM.ItemGroupDef.IsReferenceData
    SASDatasetName = T.String(name="osb")
    Domain = ODM.ItemGroupDef.Domain
    Origin = ODM.ItemGroupDef.Origin
    Purpose = ODM.ItemGroupDef.Purpose
    Comment = ODM.ItemGroupDef.Comment
    version = T.String(name="osb")
    instruction = T.String(name="osb")
    Description = ODM.ItemGroupDef.Description
    ItemRef = ODM.ItemGroupDef.ItemRef
    Alias = ODM.ItemGroupDef.Alias
    DomainColor = T.ODMObject(element_class=DomainColor, namespace="osb")


    def __len__(self):
        return len(self.ItemRef)

    def __getitem__(self, position):
        return self.ItemRef[position]

    def __iter__(self):
        return iter(self.ItemRef)


class Question(ODM.Question):
    TranslatedText = ODM.Question.TranslatedText


class ExternalQuestion(ODM.ExternalQuestion):
    Dictionary = ODM.ExternalQuestion.Dictionary
    Version = ODM.ExternalQuestion.Version
    Code = ODM.ExternalQuestion.Code


class MeasurementUnitRef(ODM.MeasurementUnitRef):
    MeasurementUnitOID = ODM.MeasurementUnitRef.MeasurementUnitOID


class CheckValue(ODM.CheckValue):
    _content = T.String(required=False)


class FormalExpression(ODM.FormalExpression):
    Context = ODM.FormalExpression.Context
    _content = ODM.FormalExpression._content


class ErrorMessage(ODM.ErrorMessage):
    TranslatedText = ODM.ErrorMessage.TranslatedText


class RangeCheck(ODM.RangeCheck):
    Comparator = ODM.RangeCheck.Comparator
    SoftHard = ODM.RangeCheck.SoftHard
    CheckValue = ODM.RangeCheck.CheckValue
    FormalExpression = ODM.RangeCheck.FormalExpression
    MeasurementUnitRef = ODM.RangeCheck.MeasurementUnitRef
    ErrorMessage = ODM.RangeCheck.ErrorMessage


class CodeListRef(ODM.CodeListRef):
    CodeListOID = ODM.CodeListRef.CodeListOID


class Question(ODM.Question):
    Question = ODM.Question


class ItemDef(ODM.ItemDef):
    OID = ODM.ItemDef.OID
    Name = ODM.ItemDef.Name
    DataType = ODM.ItemDef.DataType
    Length = ODM.ItemDef.Length
    SignificantDigits = ODM.ItemDef.SignificantDigits
    SASFieldName = ODM.ItemDef.SASFieldName
    SDSVarName = ODM.ItemDef.SDSVarName
    Origin = ODM.ItemDef.Origin
    Comment = ODM.ItemDef.Comment
    version = T.String(name="osb")
    instruction = T.String(name="osb")
    Description = ODM.ItemDef.Description
    Question = ODM.ItemDef.Question
    ExternalQuestion = ODM.ItemDef.ExternalQuestion
    MeasurementUnitRef = ODM.ItemDef.MeasurementUnitRef
    RangeCheck = ODM.ItemDef.RangeCheck
    CodeListRef = ODM.ItemDef.CodeListRef
    Alias = ODM.ItemDef.Alias


class Decode(ODM.Decode):
    TranslatedText = ODM.Decode.TranslatedText


class CodeListItem(ODM.CodeListItem):
    CodedValue = ODM.CodeListItem.CodedValue
    Rank = ODM.CodeListItem.Rank
    OrderNumber = ODM.CodeListItem.OrderNumber
    name = T.String(namespace="osb")
    OID = T.String(namespace="osb")
    mandatory = T.String(namespace="osb")
    version = T.String(namespace="osb")
    Description = ODM.CodeList.Description
    Decode = ODM.CodeListItem.Decode
    Alias = ODM.CodeListItem.Alias


class EnumeratedItem(ODM.EnumeratedItem):
    CodedValue = ODM.EnumeratedItem.CodedValue
    Rank = ODM.EnumeratedItem.Rank
    OrderNumber = ODM.EnumeratedItem.OrderNumber
    Description = ODM.CodeList.Description
    Alias = ODM.EnumeratedItem.Alias


class ExternalCodeList(ODM.ExternalCodeList):
    Dictionary = ODM.ExternalCodeList.Dictionary
    Version = ODM.ExternalCodeList.Version
    ref = ODM.ExternalCodeList.ref
    href = ODM.ExternalCodeList.href


class CodeList(ODM.CodeList):
    OID = ODM.CodeList.OID
    Name = ODM.CodeList.Name
    DataType = ODM.CodeList.DataType
    SASFormatName = ODM.CodeList.SASFormatName
    version = T.String(namespace="osb")
    Description = ODM.CodeList.Description
    CodeListItem = ODM.CodeList.CodeListItem
    EnumeratedItem = ODM.CodeList.EnumeratedItem
    ExternalCodeList = ODM.CodeList.ExternalCodeList
    Alias = ODM.CodeList.Alias


class Presentation(ODM.Presentation):
    OID = ODM.Presentation.OID
    lang = ODM.Presentation.lang
    _content = ODM.Presentation._content


class ConditionDef(ODM.ConditionDef):
    OID = ODM.ConditionDef.OID
    Name = ODM.ConditionDef.Name
    Description = ODM.ConditionDef.Description
    FormalExpression = ODM.ConditionDef.FormalExpression
    Alias = ODM.ConditionDef.Alias


class MethodDef(ODM.MethodDef):
    OID = ODM.MethodDef.OID
    Name = ODM.MethodDef.Name
    Type = ODM.MethodDef.Type
    Description = ODM.MethodDef.Description
    FormalExpression = ODM.MethodDef.FormalExpression
    Alias = ODM.MethodDef.Alias


class MetaDataVersion(ODM.MetaDataVersion):
    OID = ODM.MetaDataVersion.OID
    Name = ODM.MetaDataVersion.Name
    Description = ODM.MetaDataVersion.Description
    Include = ODM.MetaDataVersion.Include
    Protocol = ODM.MetaDataVersion.Protocol
    StudyEventDef = ODM.MetaDataVersion.StudyEventDef
    FormDef = ODM.MetaDataVersion.FormDef
    ItemGroupDef = ODM.MetaDataVersion.ItemGroupDef
    ItemDef = ODM.MetaDataVersion.ItemDef
    CodeList = ODM.MetaDataVersion.CodeList
    Presentation = ODM.MetaDataVersion.Presentation
    ConditionDef = ODM.MetaDataVersion.ConditionDef
    MethodDef = ODM.MetaDataVersion.MethodDef


class LoginName(ODM.LoginName):
    _content = ODM.LoginName._content


class DisplayName(ODM.DisplayName):
    _content = ODM.DisplayName._content


class FullName(ODM.FullName):
    _content = ODM.FullName._content


class FirstName(ODM.FirstName):
    _content = ODM.FirstName._content


class LastName(ODM.LastName):
    _content = ODM.LastName._content


class Organization(ODM.Organization):
    _content = ODM.Organization._content


class StreetName(ODM.StreetName):
    _content = ODM.StreetName._content


class City(ODM.City):
    _content = ODM.City._content


class StateProv(ODM.StateProv):
    _content = ODM.StateProv._content


class Country(ODM.Country):
    _content = ODM.Country._content


class PostalCode(ODM.PostalCode):
    _content = ODM.PostalCode._content


class OtherText(ODM.OtherText):
    _content = ODM.OtherText._content


class Address(ODM.Address):
    StreetName = ODM.Address.StreetName
    City = ODM.Address.City
    StateProv = ODM.Address.StateProv
    Country = ODM.Address.Country
    PostalCode = ODM.Address.PostalCode
    OtherText = ODM.Address.OtherText


class Email(ODM.Email):
    _content = ODM.Email._content


class Picture(ODM.Picture):
    PictureFileName = ODM.Picture.PictureFileName
    ImageType = ODM.Picture.ImageType


class Pager(ODM.Pager):
    _content = ODM.Pager._content


class Fax(ODM.Fax):
    _content = ODM.Fax._content


class Phone(ODM.Phone):
    _content = ODM.Phone._content

class LocationRef(ODM.LocationRef):
    LocationOID = ODM.LocationRef.LocationOID


class Certificate(ODM.Certificate):
    _content = ODM.Certificate._content


class User(ODM.User):
    OID = ODM.User.OID
    UserType = ODM.User.UserType
    LoginName = ODM.User.LoginName
    DisplayName = ODM.User.DisplayName
    FullName = ODM.User.FullName
    FirstName = ODM.User.FirstName
    LastName = ODM.User.LastName
    Organization = ODM.User.Organization
    Address = ODM.User.Address
    Email = ODM.User.Email
    Pager = ODM.User.Pager
    Fax = ODM.User.Fax
    Phone = ODM.User.Phone
    LocationRef = ODM.User.LocationRef
    Certificate = ODM.User.Certificate


class MetaDataVersionRef(ODM.MetaDataVersionRef):
    StudyOID = ODM.MetaDataVersionRef.StudyOID
    MetaDataVersionOID = ODM.MetaDataVersionRef.MetaDataVersionOID
    EffectiveDate = ODM.MetaDataVersionRef.EffectiveDate


class Location(ODM.Location):
    OID = ODM.Location.OID
    Name = ODM.Location.Name
    LocationType = ODM.Location.LocationType
    MetaDataVersionRef = ODM.Location.MetaDataVersionRef


class Meaning(ODM.Meaning):
    _content = ODM.Meaning._content


class LegalReason(ODM.LegalReason):
    _content = ODM.LegalReason._content


class SignatureDef(ODM.SignatureDef):
    OID = ODM.SignatureDef.OID
    Methodology = ODM.SignatureDef.Methodology
    Meaning = ODM.SignatureDef.Meaning
    LegalReason = ODM.SignatureDef.LegalReason


class AdminData(ODM.AdminData):
    StudyOID = ODM.AdminData.StudyOID
    User = ODM.AdminData.User
    Location = ODM.AdminData.Location
    SignatureDef = ODM.AdminData.SignatureDef


class Study(ODM.Study):
    OID = ODM.Study.OID
    GlobalVariables = ODM.Study.GlobalVariables
    BasicDefinitions = ODM.Study.BasicDefinitions
    MetaDataVersion = ODM.Study.MetaDataVersion


class ODM(ODM.ODM):
    Description = ODM.ODM.Description
    FileType = ODM.ODM.FileType
    Granularity = ODM.ODM.Granularity
    Archival = ODM.ODM.Archival
    FileOID = ODM.ODM.FileOID
    CreationDateTime = ODM.ODM.CreationDateTime
    PriorFileOID = ODM.ODM.PriorFileOID
    AsOfDateTime = ODM.ODM.AsOfDateTime
    ODMVersion = ODM.ODM.ODMVersion
    Originator = ODM.ODM.Originator
    SourceSystem = ODM.ODM.SourceSystem
    SourceSystemVersion = ODM.ODM.SourceSystemVersion
    schemaLocation = ODM.ODM.schemaLocation
    ID = ODM.ODM.ID
    Study = ODM.ODM.Study
    AdminData = ODM.ODM.AdminData
