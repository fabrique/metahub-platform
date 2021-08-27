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
    Type: str
    Text: str
    Notes: str


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



class Object(BaseModel):
    Id: int
    # CreateUser: str
    # CreateDate: datetime
    ChangeUser: str
    ChangeDate: datetime
    InventoryNumber: str = ""
    Title: str = ""
    ObjectName: str = ""
    Datings: List[Dating] = []
    ContainerName: str = ""
    ContainerId: int = 0
    Creditline: str = ""
    Notes: str = ""
    AcquisitionDate: str = ""
    CurrentLocation: str = ""
    Convolute: str = ""
    NumberOfParts: str = ""
    Creators: List[Creator] = []
    Provenance: List[TypeTextNotes] = []
    GeographicReference: str = ""
    GeographicReferences: List[TypeTextNotes] = []
    # Dimensions: List[TypeTextNotes] = []
    Material_Technique: List[TypeTextNotes] = []
    Signatures: List[TypeTextNotes] = []
    # Inscriptions: List[TypeTextNotes]
    Keywords: List[TypeTextNotes] = []
    OtherObjects: List[OtherObject] = []
    Publications: List[Publication] = []
    IsHighlight: bool = False
    Exhibitions: List[TypeTextNotes] = []
    ImageLicense: str = ""
    Images: List[Image] = []

    def to_bc_dict(self):
        return dict(
            bc_id=self.Id,
            bc_inventory_number=self.InventoryNumber,
            bc_change_date=self.ChangeDate,
            bc_change_user=self.ChangeUser,
            bc_object_name=self.ObjectName,
            bc_credits=self.Creditline,
            bc_notes=self.Notes,
            bc_tags="|".join(self.get_tags()),
            bc_images=", ".join([i.KeyFileName for i in self.Images]),
            bc_image_license=", ".join([i.License for i in self.Images]),
            date_acquired=self.AcquisitionDate,
            datings=self.Datings[0].Text or "Unbekannt"
            if self.Datings
            else "Unbekannt",
            dating_from_df=self.Datings[0].year_from_date() if self.Datings else None,
            dating_to_df=self.Datings[0].year_to_date() if self.Datings else None,
            provenance=", ".join(
                [f"{p.Notes}: {p.Text}" for p in self.Provenance if p.Text]
            ),
            signatures=", ".join(
                [f"{s.Text} {s.Type}" for s in self.Signatures if s.Text and s.Type]
            ),
            publications=", ".join(
                [
                    f"{p.Text.strip()}- {p.specifications()}"
                    for p in self.Publications
                    if p.Text
                ]
            ),
            is_highlight=self.IsHighlight,
            current_location=self.CurrentLocation,
            container_name=self.ContainerName,
            container_id=self.ContainerId,
            geographic_reference=self.GeographicReference,
            geographic_location=self.get_keyword_text("Geogr. Bezug"),
            convolute=self.Convolute,
            series_id=self.get_series_id(),
            material=", ".join([i.Text for i in self.Material_Technique]),
            # dimensions=self.get_dimensions(self.get('Dimensions')),
            title=self.Title,
            # artist=self.get_artist_for_object(self),
            object_type=self.get_keyword_text("Objektbezeichnung"),
        )

    def get_tags(self):
        for tag in self.Keywords:
            if tag.Type == "Inhalt/Kontext" and "(" in tag.Text:
                yield tag.Text.split("(")[0].strip()

    def get_keyword_text(self, type):
        keywords = [k for k in self.Keywords if k.Type == type]
        if keywords and "(" in keywords[0]:
            return keywords[0].Text.split("(")[0].strip()
        return "Unbekannt"

    def get_series_id(self):
        if self.OtherObjects:
            parts = self.InventoryNumber.split("-")
            if parts:
                if len(parts) >= 3:
                    return parts[0] + parts[1]
