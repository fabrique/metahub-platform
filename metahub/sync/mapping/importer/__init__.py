from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Publication(BaseModel):
    Text: str
    Pages: str
    Illustrations: str
    CatalogueNumber: str
    Notes: str

    def specifications(self):
        return ", ".join(
            [
                i
                for i in [
                    self.Pages,
                    self.Illustrations,
                    self.CatalogueNumber,
                    self.Notes,
                ]
                if i
            ]
        )


class Image(BaseModel):
    Id: int
    CreateUser: str
    CreateDate: datetime
    ChangeUser: str
    ChangeDate: datetime
    License: str
    KeyFileName: str
    OriginalFileName: str


class Creator(BaseModel):
    Id: int
    ChangeUser: str
    ChangeDate: datetime
    ArtistId: int
    Order: int
    Role: str
    Attribution: str
    Description: str


class TypeTextNotes(BaseModel):
    Type: str = ""
    Text: str = ""
    Notes: str = ""


class Dating(TypeTextNotes):
    YearFrom: str
    YearTo: str

    def year_from_date(self):
        if self.YearFrom:
            return datetime(int(self.YearFrom), 1, 1).date()

    def year_to_date(self):
        if self.YearTo:
            return datetime(int(self.YearTo), 1, 1).date()


class OtherObject(BaseModel):
    Id: Optional[int]
    Type: Optional[str]
    Text: Optional[str]
    Notes: Optional[str]
