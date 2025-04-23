import datetime
from pydantic import BaseModel, AnyUrl
from typing import Optional, List, Literal


class Column(BaseModel):
    """ Dataset column, or variable, metadata attributes"""
    itemOID: str
    name: str
    label: str
    dataType: Literal["string", "integer", "decimal", "float", "double", "decimal", "datetime", "boolean", "date", "time", "URI"]
    targetDataType: Optional[Literal["decimal", "integer"]] = None
    length: Optional[int] = None
    displayFormat: Optional[str] = None
    keySequence: Optional[int] = None


class SourceSystem(BaseModel):
    name: str
    version: str


class RowData(BaseModel):
    """ Dataset-JSON records to append to an existing dataset """
    rows: List = []


class DatasetMetadata(BaseModel):
    """ Dataset-JSON ndjson metadata model """
    datasetJSONCreationDateTime: Optional[datetime.datetime] = datetime.datetime.utcnow()
    datasetJSONVersion: Literal["1.0.0", "1.1.0"]
    fileOID: Optional[str] = None
    dbLastModifiedDateTime: Optional[datetime.datetime] = None
    originator: Optional[str] = None
    sourceSystem: Optional[SourceSystem] = None
    studyOID: str
    metaDataVersionOID: Optional[str] = None
    metaDataRef: Optional[str] = None
    itemGroupOID: str
    records: int
    name: str
    label: str
    columns: List[Column]