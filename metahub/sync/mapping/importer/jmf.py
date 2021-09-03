from datetime import datetime
from typing import List

from pydantic import BaseModel

from metahub.sync.mapping.importer import Dating, Creator, TypeTextNotes, OtherObject, Publication, Image


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
    GeographicReferences: List[TypeTextNotes] = []
    Dimensions: List[TypeTextNotes] = []
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
            geographic_reference=", ".join([i.Text for i in self.GeographicReferences]),
            geographic_location=self.get_keyword_text("Geogr. Bezug"),
            convolute=self.Convolute,
            series_id=self.get_series_id(),
            material=", ".join([i.Text for i in self.Material_Technique]),
            dimensions=", ".join([i.Text for i in self.Dimensions]),
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

    def get_title(self):
        return self.Title
